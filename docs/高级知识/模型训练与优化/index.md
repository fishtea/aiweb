# 模型训练与优化

> 大模型训练需要高效的分布式策略和内存优化技术。本页面总结了 PyTorch DDP、FSDP、混合精度训练、DeepSpeed ZeRO 等关键技术。

---

## 1. 分布式训练概述

**来源：** [Everything about Distributed Training and Efficient Finetuning - Sumanth R Hegde](https://sumanthrh.com/post/distributed-and-efficient-finetuning)

训练 10B+ 参数的大型语言模型时，单 GPU 无法容纳整个模型。主要并行策略包括：

| 策略 | 描述 | 特点 |
|------|------|------|
| **数据并行 (DP)** | 每 GPU 有完整模型副本，梯度 all-reduce | 高内存冗余 |
| **张量并行 (TP)** | 每 GPU 持有张量切片 | 需要模型改造 |
| **流水线并行 (PP)** | 层拆分到不同 GPU，微批次流水线 | 利用率取决于微批次数 |
| **ZeRO/FSDP** | 分片参数/梯度/优化器状态 | 无需模型改造 |

**通信开销（baseline DDP）：** 每步 2Ψ（Ψ = 参数量）

---

## 2. PyTorch Distributed Data Parallel (DDP)

**来源：** [How Distributed Training Works in PyTorch - AI Summer](https://theaisummer.com/distributed-training-pytorch)

DDP 是多进程模式，每 GPU 一个独立进程。关键特点：

- 参数永不广播——仅通信梯度
- 反向传播时通过 **all-reduce** 梯度平均
- 每 worker 独立更新参数

### DDP 优势

| 设置 | 每 epoch 时间 |
|------|--------------|
| 单 GPU (baseline) | 13.2 秒 |
| DataParallel 4 GPU | 19.1 秒（更慢！） |
| **DDP 2 GPU** | **9.8 秒** |
| **DDP 4 GPU** | **6.1 秒** |
| DDP 4 GPU + Mixed Precision | 6.5 秒 |

> *"It is recommended to use nn.DistributedDataParallel, instead of DataParallel, to do multi-GPU training, even if there is only a single node."* — PyTorch Docs

### 核心步骤

```python
# 初始化分布式进程
dist.init_process_group(backend='nccl', rank=rank, world_size=world_size)

# 包装模型
model = nn.parallel.DistributedDataParallel(model, device_ids=[rank])

# 使用 DistributedSampler
sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
dataloader = DataLoader(dataset, batch_size=batch_size, sampler=sampler)
```

---

## 3. 混合精度训练

**来源：** [AI Summer - Mixed Precision Training](https://theaisummer.com/distributed-training-pytorch)

混合精度训练结合 **FP16**（计算）和 **FP32**（权重存储），减少内存并加速训练。

```python
scaler = torch.cuda.amp.GradScaler()

for data, labels in dataloader:
    optimizer.zero_grad()
    with torch.cuda.amp.autocast():  # FP16 前向
        outputs = model(data)
        loss = criterion(outputs, labels)
    scaler.scale(loss).backward()    # 缩放反向传播
    scaler.step(optimizer)           # 反缩放并更新
    scaler.update()
```

**机制：**
- 前向/反向用 FP16 计算
- Loss 在 FP32 下计算（避免下溢/上溢）
- Loss 放大后反向传播，梯度缩小后更新权重
- 维护 FP32 权重副本

---

## 4. FSDP (Fully Sharded Data Parallel)

**来源：** [PyTorch FSDP Advanced Tutorial](https://docs.pytorch.org/tutorials/intermediate/FSDP_advanced_tutorial.html), [Sumanth - Distributed Training](https://sumanthrh.com/post/distributed-and-efficient-finetuning)

FSDP 类似于 DeepSpeed ZeRO-3，将模型参数、梯度和优化器状态分片到所有 GPU 上。

### FSDP 工作原理

```
构造函数：参数分片，每 GPU 仅保留自己的一份
前向传播：all_gather → 恢复完整参数 → 计算 → 丢弃非所属参数
反向传播：all_gather → 计算梯度 → 丢弃非所属参数 → reduce_scatter 同步梯度
```

### 关键特性

| 特性 | 说明 |
|------|------|
| **自动包装策略** | 注册 Transformer 层类（如 `T5Block`）以提高通信效率 |
| **混合精度** | `MixedPrecision` 支持 fp16/bf16，可粒度控制参数、梯度、缓冲区精度 |
| **设备初始化** | `device_id` 指定 FSDP 单元所在设备，避免 OOM |
| **分片策略** | `FULL_SHARD` (ZeRO-3) 或 `SHARD_GRAD_OP` (ZeRO-2) |
| **反向预取** | `BACKWARD_PRE` 提前请求下一单元参数，获得 2-10% 提速 |
| **流式检查点** | 仅 rank 0 保存完整状态，offload 到 CPU |

**BF16 混合精度效果：** 最高 **4 倍加速** 和 **约 30% 内存减少**。

```python
from torch.distributed.fsdp import MixedPrecision

mp_fp16 = MixedPrecision(
    param_dtype=torch.float16,
    reduce_dtype=torch.float16,
    buffer_dtype=torch.float16
)
```

---

## 5. DeepSpeed ZeRO

**来源：** [Sumanth - Distributed Training and Efficient Finetuning](https://sumanthrh.com/post/distributed-and-efficient-finetuning)

| 阶段 | 分片内容 | 通信量 | 内存减少 |
|------|----------|--------|----------|
| **ZeRO-1** | 优化器状态 | 2Ψ | ~4× |
| **ZeRO-2** | 优化器 + 梯度 | 2Ψ | ~8× |
| **ZeRO-3** | 参数 + 梯度 + 优化器 | 3Ψ | ~64× |
| **ZeRO-Offload** | 卸载到 CPU | - | 更大 |
| **ZeRO-Infinity** | 卸载到 CPU + NVMe | - | 200B+ 模型 |
| **ZeRO++** | 量化 + 层级分片 | 减少 4× | 更大 |

**ZeRO vs FSDP：** 功能相似，DeepSpeed 更成熟但 FSDP 原生集成在 PyTorch 中。

---

## 6. 高效微调技术

| 技术 | 描述 | 权衡 |
|------|------|------|
| **混合精度 (bf16/fp16)** | 半精度权重/激活，fp32 主权重 | bf16 无需 loss scaling |
| **PEFT (LoRA/IA³)** | 冻结大部分权重，训练小适配器 | 轻微性能损失 |
| **Flash Attention** | IO-aware 精确注意力，最高 220+ TFLOPS | 需要 Ampere+ GPU |
| **梯度检查点** | 用计算换内存，仅保留部分激活 | 约 20% 训练时间增加 |

### 6. 训练范式演进：预训练后训练与强化学习

2024-2025 年，大模型训练从"预训练 + SFT + RLHF"三段式，演进为更精细的多阶段后训练：

| 阶段 | 目标 | 方法 |
|------|------|------|
| 预训练 | 学习语言和世界知识 | 自回归下一 token 预测 |
| SFT | 学会遵循指令 | 指令-响应监督微调 |
| 偏好优化 | 对齐人类偏好 | DPO / KTO / SimPO（替代复杂 PPO） |
| 推理强化学习 | 学会"思考" | GRPO / RLVR（可验证奖励强化学习） |

- **DPO 取代 PPO 趋势**：DPO 无需奖励模型和在线采样，稳定性更高，已成为多数开源模型偏好优化首选。
- **RLVR 与推理能力**：DeepSeek-R1 用"可验证奖励"（数学题有标准答案）做强化学习，让模型自发涌现长思维链，证明推理能力可通过 RL 涌现而非纯靠 SFT。
- **蒸馏推理能力**：将大推理模型的思维链蒸馏到小模型，让 7B 模型也能做复杂推理。

> 启示：R1 的成功让社区重新审视"纯 RL 能否产生推理"，推动了 2025 年推理模型的爆发。训练范式正向"预训练 → SFT → 推理 RL → 蒸馏"演进。

---

## 🔗 参考资料

- [How Distributed Training Works in PyTorch - AI Summer](https://theaisummer.com/distributed-training-pytorch)
- [PyTorch FSDP Advanced Tutorial](https://docs.pytorch.org/tutorials/intermediate/FSDP_advanced_tutorial.html)
- [Everything about Distributed Training and Efficient Finetuning](https://sumanthrh.com/post/distributed-and-efficient-finetuning)
- [FSDP Mixed Precision Training - YouTube](https://www.youtube.com/watch?v=-caN92JtKqA)
- [Amazon SageMaker Mixed Precision Training](https://docs.aws.amazon.com/sagemaker/latest/dg/model-parallel-core-features-v2-mixed-precision.html)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-02 12:09:15*
