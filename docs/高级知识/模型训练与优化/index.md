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

## 7. 2026 训练效率新突破

### 7.1 NeMo AutoModel：MoE 微调 3.7 倍加速

**来源：** [Accelerating Transformers Fine-Tuning with NVIDIA NeMo AutoModel — HuggingFace Blog (2026-06-24)](https://huggingface.co/blog/nvidia/accelerating-fine-tuning-nvidia-nemo-automodel)

2026 年 6 月，NVIDIA 发布了 **NeMo AutoModel**，这是一个直接构建在 HuggingFace Transformers v5 之上的开源训练加速库，专为 MoE（混合专家）模型的大规模微调设计。

**核心性能数据（对比原生 Transformers v5）：**

| 指标 | 提升幅度 |
|------|---------|
| 训练吞吐量 | **3.4-3.7×** |
| GPU 显存占用 | **减少 29-32%** |

**技术栈：**

- **Expert Parallelism**：将不同专家分布到不同 GPU 上，减少通信开销
- **DeepEP**：融合的 all-to-all 派发（dispatch）内核，优化 MoE 路由的专家间通信
- **TransformerEngine 内核**：针对 NVIDIA GPU 优化的高性能算子
- **动态权重加载**：继承 Transformers v5 的能力，按需加载专家权重

**关键亮点——零代码迁移：**

```python
# 只需替换一行 import，其余代码不变
from nemo_automodel import AutoModelForCausalLM  # 替代 transformers.AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-30B-A3B")
# 训练代码完全不变
```

> **启示：** 2026 年的训练加速已经从"需要深入理解分布式框架"走向"一行 import 即用"。Transformers v5 + NeMo AutoModel 的组合让 MoE 微调的门槛大幅降低，中小团队也能高效微调百亿级 MoE 模型。

### 7.2 HuggingFace Kernels 2.0：自定义算子的标准化生态

**来源：** [🤗 Kernels: Major Updates — HuggingFace Blog (2026-07-06)](https://huggingface.co/blog/revamped-kernels)

2026 年 7 月，HuggingFace 对其 Kernels 项目进行了重大升级，旨在标准化自定义 CUDA/Metal 等算子的打包、分发和消费方式。

**主要更新：**

| 更新 | 说明 |
|------|------|
| **新仓库类型 "kernel"** | Kernels 成为 Hub 上的一等公民，可查看支持的加速器、操作系统和后端版本 |
| **可复现构建** | 使用 Nix 进行封闭构建（hermetic build），确保二进制与源代码匹配 |
| **可信发布者** | 引入信任机制，区分社区和官方维护的 kernel |
| **代码签名** | 嵌入源码 Git SHA1，防止篡改 |
| **改进的 CLI** | 统一的命令行工具，简化 kernel 安装和管理 |

**对训练优化的意义：**

- FlashAttention-3 等关键算子可通过统一的 Kernels 生态安装和验证
- 安全机制降低第三方 kernel 的供应链风险
- 为后续"Agent 化 kernel 开发"（AI 辅助编写和优化 kernel）打下基础

> 2026 年的训练栈正在形成新的分层：**Transformers v5（模型层）→ NeMo AutoModel（分布层）→ Kernels 2.0（算子层）**，每一层都有标准化的接口和一流的生态支持。

---

### 7.3 ZeRO 三阶段深入解析：从原理到选型

**来源：** [HuggingFace Transformers — Perf Train GPU Many](https://huggingface.co/docs/transformers/en/perf_train_gpu_many)

ZeRO（Zero Redundancy Optimizer）是 2026 年大模型训练的标配技术，它通过将参数、梯度和优化器状态分片（shard）到数据并行进程中，大幅降低每 GPU 的内存占用。理解三个阶段的差异对训练配置至关重要：

| 阶段 | 分片内容 | 通信开销 | 内存节省（相对 DDP） | 适用场景 |
|------|----------|---------|---------------------|---------|
| **ZeRO-1** | 优化器状态 | 2Ψ | ~4× | 模型刚好能放进单 GPU，想扩大 batch size |
| **ZeRO-2** | 优化器 + 梯度 | 2Ψ | ~8× | 模型能放进单 GPU，但需要更大的有效 batch |
| **ZeRO-3** | 参数 + 梯度 + 优化器 | 3Ψ | ~64× | 模型单 GPU 放不下，必须分片 |

> Ψ = 参数量（例如 7B 模型，Ψ = 7B 个 float16 ≈ 14GB）

**关键选择依据：**
- **ZeRO-1 对通信模式无影响**，因为它只分片优化器状态，前向/反向时参数和梯度仍是完整的
- **ZeRO-2 在前向时也不影响**，但在反向阶段需要 reduce-scatter 梯度
- **ZeRO-3 在前向和反向都需要 all-gather 恢复完整参数**，通信量最大，但内存节省最显著
- 实践中，**如果模型能放进单 GPU，优先 ZeRO-2；如果放不下，才用 ZeRO-3**

### 7.4 模型并行：流水线并行与张量并行

除 ZeRO 数据并行外，当模型极大（100B+）时还需要模型并行（Model Parallelism）。HuggingFace 文档区分了两种主要方式：

**流水线并行（Pipeline Parallelism, PP）**：
- 将模型的不同层分配到不同 GPU 上
- 前向时：GPU 1 处理一个 batch → 传给 GPU 2 → 以此类推
- 反向时：从最后一个 GPU 向前传播梯度
- **优点**：适合层数极深的模型
- **缺点**：GPU 利用率可能不均衡，需要微批次调度（micro-batch scheduling）来减少"气泡"

**张量并行（Tensor Parallelism, PP）**：
- 将单层内的矩阵运算拆分到多个 GPU
- 每个 GPU 持有张量的一部分（如按列分割权重矩阵）
- **优点**：单层超大（如 embedding 层、FFN 层）时的必需策略
- **缺点**：对模型架构有侵入性，需修改模型定义

**3D 并行（3D Parallelism）**：ZeRO 数据并行 + 流水线并行 + 张量并行三者组合，是训练 100B+ 模型的工业级标准方案，在 DeepSpeed 和 Megatron-LM 中得到广泛实践。

> **2026 趋势**：随着模型规模持续增长（DeepSeek V3/R1 参数达 671B），3D 并行已成为大模型训练的默认架构。但中小团队（<30B 参数）通常只需 ZeRO-2 或 ZeRO-3 即可满足需求，无需引入额外的并行复杂度。

---

## 8. 2026 MoE 模型微调实战：NVIDIA NeMo AutoModel 深度解析

> 本节基于 NVIDIA 官方博客 [Accelerating Transformers Fine-Tuning with NVIDIA NeMo AutoModel](https://huggingface.co/blog/nvidia/accelerating-fine-tuning-nvidia-nemo-automodel)（2026-06-24）和 HuggingFace Transformers v5 发布说明。

### 8.1 MoE 模型微调面临的三大挑战

MoE（混合专家）模型已成为前沿模型的默认架构（DeepSeek V3/R1、Qwen3、Nemotron 等），但其微调面临独特的工程挑战：

| 挑战 | 描述 | 影响 |
|------|------|------|
| **专家分片困难** | 100+ 专家需要在 GPU 间均匀分配 | 负载不均衡导致 straggler |
| **通信开销大** | 路由 token 到专家需要 all-to-all 通信 | 通信可能占训练时间的 40%+ |
| **FSDP 兼容性** | ModuleList 方式的专家实现可能导致死锁 | v4 下 Qwen3 直接死锁 |

**案例：Qwen3-30B-A3B 在 Transformers v4 上的死锁问题**

Transformers v4 将 Qwen3 的 MoE 专家存储为 ModuleList（128 个独立 MLP 模块），每个模块单独被 FSDP 包装。前向传播时，不同 rank 上的数据分配到的专家不同——某些 rank 跳过了部分专家，导致 FSDP 的 AllGather/ReduceScatter 集合操作不匹配，产生无限期挂起（deadlock）。

**Transformers v5 的修复方案**：将专家存储为融合的 3D 参数张量（不再有逐专家模块和逐专家 FSDP 集合操作），彻底消除了这一死锁问题。

### 8.2 NeMo AutoModel：一行代码迁移的 MoE 训练加速库

2026 年 6 月，NVIDIA 发布了 NeMo AutoModel，建立在 HuggingFace Transformers v5 之上，为 MoE 模型的大规模微调提供开箱即用的加速方案。

**核心特性：**

| 特性 | 说明 |
|------|------|
| **API 兼容** | 继承 AutoModelForCausalLM，只需替换 import 行 |
| **专家并行（Expert Parallelism, EP）** | 将不同专家分布到不同 GPU，减少每 GPU 内存 |
| **DeepEP** | 融合的 all-to-all 派发内核，通信与计算重叠 |
| **TransformerEngine 内核** | 针对 NVIDIA GPU 优化的融合注意力、MLP 层 |
| **Liger Kernel 回退** | 非 MoE 层自动应用 Liger Kernel 优化 |
| **HF 检查点兼容** | save_pretrained() 输出标准 HF 格式，vLLM/SGLang 可直接加载 |

**一行代码迁移示例：**

```python
# 只需替换 import
from nemo_automodel import NeMoAutoModelForCausalLM  # 替代 transformers.AutoModelForCausalLM

model = NeMoAutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-30B-A3B",
    dtype=torch.bfloat16,
)
# 后续训练代码完全不变——相同的前向、loss、backward 调用
```

### 8.3 性能基准实测

**Qwen3-30B-A3B（单节点 8×H100 80GB）：**

| 指标 | v4 | v5 (FA2+grouped_mm) | NeMo AutoModel (EP=8) | v5 → AutoModel |
|------|----|--------------------|-----------------------|---------------|
| TPS/GPU | 死锁 | 3,075 | **11,340** | **3.69×** |
| 峰值显存 | — | 68.2 GiB | **48.1 GiB** | **-29%** |
| 前向+Loss | — | 582 ms | **194 ms** | 3.00× |
| 反向传播 | — | 758 ms | **178 ms** | 4.26× |

**Nemotron 3 Nano 30B A3B（单节点 8×H100 80GB）：**

| 指标 | v4 (hub代码) | v5 (FA2+grouped_mm+Mamba CUDA) | NeMo AutoModel (EP=8) | v5 → AutoModel |
|------|-------------|-------------------------------|-----------------------|---------------|
| TPS/GPU | 1,807 | 4,583 | **15,421** | **3.36×** |
| 峰值显存 | 61.9 GiB | 62.1 GiB | **42.5 GiB** | **-32%** |
| 前向+Loss | 1,024 ms | 283 ms | **109 ms** | 2.60× |
| 反向传播 | 1,246 ms | 611 ms | **157 ms** | 3.89× |

**Nemotron 3 Ultra 550B A55B（多节点 16×H100 节点，128 GPU，EP=64）：**

| 指标 | NeMo AutoModel |
|------|---------------|
| TPS/GPU | 815 |
| TFLOP/s/GPU | ~293 |
| 峰值显存 | 58.2 GiB |
| Transformers v5 | 无法运行（OOM） |

> **关键洞察**：550B 模型的对比没有 v5 列——因为 Transformers v5 在 EP=64 的规模下直接 OOM 了。NeMo AutoModel 的专家并行将专家权重分散到 64 路 GPU 上，使全参数微调在 128 GPU 上成为可能。

### 8.4 加速来源分析

3.4-3.7× 的加速来自三个独立的技术贡献：

1. **专家并行降低内存压力 (≈1.5×)**：EP=8 将专家权重分布到 8 块 GPU，单 GPU MoE 占用降低 8×，以 Qwen3 为例峰值显存从 68.2 GiB 降至 48.1 GiB（-29%），释放的空间可用于更大 batch 或更长序列。

2. **DeepEP 融合通信与计算 (≈1.3×)**：传统的专家路由需要独立的 AllGather/ReduceScatter 集合通信步骤，DeepEP 将 token 派发和组合融合为优化的 GPU 内核，使通信与专家计算重叠执行——相当于"免费"的通信时间。

3. **TransformerEngine 内核加速核心运算 (≈1.5×)**：TE 的融合注意力、线性层和 RMSNorm 实现在所有层类型上（不仅仅是 MoE 层）都提供了比原生 PyTorch/FlashAttention 更一致的加速。

### 8.5 2026 训练栈分层架构

NeMo AutoModel 的出现标志着 2026 年的训练栈形成了清晰的分层结构：

```
┌─────────────────────────────────────────┐
│  Transformers v5（模型层）               │
│  ─ 模型定义、检查点加载、专家接口          │
├─────────────────────────────────────────┤
│  NeMo AutoModel（分布式层）              │
│  ─ 专家并行、DeepEP、FSDP2 编排          │
├─────────────────────────────────────────┤
│  Kernels 2.0（算子层）                   │
│  ─ FlashAttention-3、TE 内核、自定义 CUDA │
├─────────────────────────────────────────┤
│  HuggingFace Hub（分发层）               │
│  ─ 标准化 kernel 打包、可复现构建、签名    │
└─────────────────────────────────────────┘
```

每一层都有标准化的接口和活跃的生态支持，中小团队无需深入理解分布式框架细节，即可高效微调百亿级 MoE 模型。

> **实际建议**：如果你要微调 MoE 模型（Qwen3、DeepSeek、Nemotron 系列），优先尝试 NeMo AutoModel。只需 `pip install nemo-automodel` + 修改 import 行，即可获得 3×+ 的吞吐提升和 30% 的内存节省。对于非 MoE 模型，升级到 Transformers v5 并启用 grouped_mm 后端的专家实现同样能获得显著加速。

**来源：**
- [Accelerating Transformers Fine-Tuning with NVIDIA NeMo AutoModel — HuggingFace Blog (2026-06-24)](https://huggingface.co/blog/nvidia/accelerating-fine-tuning-nvidia-nemo-automodel)
- [🤗 Kernels: Major Updates — HuggingFace Blog (2026-07-06)](https://huggingface.co/blog/revamped-kernels)

---

## 10. 2026 知识蒸馏实战：前沿模型如何使用蒸馏

### 概述

2026 年 7 月，HuggingFace 社区发布了一份系统的"Distillation in 2026"总结报告，揭示了前沿模型在后训练中使用知识蒸馏的三种主要模式。知识蒸馏已从传统的"大模型教小模型"演进为多种复杂形态——包括多专家蒸馏、自我蒸馏等，成为 2026 年后训练流程的关键组成部分。

### 模式 1：大教师→小学生（Off-Policy 蒸馏）

这是最经典的蒸馏形态，用一个大型、昂贵的教师模型训练更小的学生模型。

| 应用实例 | 说明 |
|---------|------|
| **Gemma 3** | 后训练"依赖从大型 IT 教师（instruction-tuned）改进版本的知识蒸馏" |
| **Qwen3** | 同样采用类似的蒸馏后训练配方 |
| **DeepSeek-R1 Distill** | 将 R1 的推理轨迹通过 SFT 蒸馏到紧凑的 Qwen 和 LLaMA 学生模型中 |

两种分支：
- **软标签（Soft Labels, 白盒）**：学生匹配教师的 next-token 概率分布
- **硬标签（Hard Labels, 黑盒）**：直接在教师生成的文本上训练（R1-Distill 采用此方式）

### 模式 2：多专家蒸馏（On-Policy 蒸馏）——2026 年最主流的方式

2026 年，前沿实验室普遍采用这一新范式：为每个领域训练**独立的 RL 专家**（数学专家、代码专家、Agent 任务专家），然后**将所有专家蒸馏到一个学生模型中**。

**为什么这么做？** 通过 RL 让单个模型在所有领域都优秀极其复杂——一个训练阶段获得的技能会在下一个阶段退化和遗忘。

**运作机制：**
- **On-Policy**：学生在自己生成的 rollouts 上学习，教师逐 token 打分
- **教师通常是同等大小的专家**：不是更大的模型，而是在特定领域通过 RL 推向极致的相同基础模型分叉
- **逐 token 密集信号** vs RL 的"整个输出一次奖励"：蒸馏收敛快得多

| 应用实例 | 实现方式 |
|---------|---------|
| **MiMo-V2-Flash** | 每个领域训练独立专家（SFT → GRPO），然后用 On-Policy Distillation 统一模型 |
| **GLM-5** | 跨训练阶段应用：每轮 RL 后回退到更早的 checkpoint 做蒸馏，恢复退化的能力 |
| **Nemotron 3 Ultra** | 大规模多教师蒸馏：10+ 领域专家给学生逐 token 指导 |
| **MiniMax M2** | 经典方向：大教师 + 小学生，成本约为 RL 的 1/10 GPU 小时，效果更好 |

### 模式 3：自我蒸馏（Self-Distillation）

完全去掉独立教师，让模型**从自身更好的版本中学习**：

| 应用实例 | 方法 |
|---------|------|
| **Cursor Composer 2.5** | 在 context 中注入 hint 描述期望行为，用 hint-conditioned 的输出作为教师的 per-token KL 目标 |
| **Thinking Machines** | 在领域数据微调后，从微调前的 checkpoint 蒸馏——恢复被微调抹去的旧行为，保持新知识 |

> 教师不需要更大，只需要在 context 中更好。有时教师就是模型自己。

### 关键启示

- **三个模式本质相同**：都是 off-policy、on-policy 和 self-distillation 三类变化
- **蒸馏的优势**：教师能在每个 token 上打分，而 RL 对整个输出只给一个奖励——所以蒸馏收敛更快，计算成本更低
- **2026 年的蒸馏不再只是"压缩"工具**，更是"能力集成"和"技能保持"的核心手段

### 参考来源

- [Distillation in 2026 (so far): which frontier models use it and how — Sergio Paniego (2026-07-08)](https://huggingface.co/blog/sergiopaniego/distillation-2026)
- [KV Caching Explained: Optimizing Transformer Inference Efficiency — Not Lain (HuggingFace)](https://huggingface.co/blog/not-lain/kv-caching)

---

## 11. KV Cache 原理与 Transformer 推理优化

### 概述

KV Cache（键值缓存）是 Transformer 推理加速的核心技术。每次模型生成新 token 时，注意力层都需要计算当前 token 与之前所有 token 的注意力权重——KV Cache 通过**记住先前计算的 Key 和 Value 矩阵**，避免重复计算，显著加速推理。

### 工作原理

| 步骤 | 标准推理 | KV Cache |
|------|---------|----------|
| 第一步 | 计算第一个 token 的 K、V、Q | 计算 K1、V1 并存入缓存 |
| 第二步 | 重新计算之前所有 token 的 K、V | 从缓存读取 K1、V1，只计算新 token 的 K2、V2 |
| 第 n 步 | 每次重新计算 O(n×d) | 只需计算 O(d)，缓存增长为 [K1..Kn, V1..Vn] |

### 标准推理 vs KV Cache 对比

| 维度 | 标准推理 | KV Cache |
|------|---------|----------|
| 计算方式 | 每步从头计算所有 token | 缓存历史 K/V，仅计算新 token |
| 每步内存 | 少（不存储历史） | 多（存储历史 K/V） |
| 长文本表现 | 随序列增长变慢 | 保持稳定 |
| 计算成本 | 高（重复工作） | 低（复用缓存） |
| 推荐场景 | 短文本生成 | 长文本、实时应用 |

### 实践实现

在 HuggingFace Transformers 中，KV Cache 默认启用（`use_cache=True`）。随着模型上下文窗口的增长（128K → 1M+），KV Cache 的内存管理成为关键挑战——这推动了 KV 缓存量化（FP8/INT4）、Multi-Query Attention（MQA）、Grouped-Query Attention（GQA）、以及 MLA（多头潜在注意力）等优化技术的广泛应用。

> **2026 趋势**：KV Cache 优化已成为推理引擎（vLLM、TGI、TensorRT-LLM）的核心竞争力。新型架构如 Mamba（无 KV Cache）和混合架构（Mamba + Attention）正在从根本改变长上下文推理的效率格局。

### 参考来源

- [KV Caching Explained — Not Lain (HuggingFace Blog)](https://huggingface.co/blog/not-lain/kv-caching)
- [Distillation in 2026 — Sergio Paniego (2026-07-08)](https://huggingface.co/blog/sergiopaniego/distillation-2026)

---

## 🔗 参考资料

- [How Distributed Training Works in PyTorch - AI Summer](https://theaisummer.com/distributed-training-pytorch)
- [PyTorch FSDP Advanced Tutorial](https://docs.pytorch.org/tutorials/intermediate/FSDP_advanced_tutorial.html)
- [Everything about Distributed Training and Efficient Finetuning](https://sumanthrh.com/post/distributed-and-efficient-finetuning)
- [FSDP Mixed Precision Training - YouTube](https://www.youtube.com/watch?v=-caN92JtKqA)
- [Amazon SageMaker Mixed Precision Training](https://docs.aws.amazon.com/sagemaker/latest/dg/model-parallel-core-features-v2-mixed-precision.html)
- [HuggingFace Transformers — Scalability Guide](https://huggingface.co/docs/transformers/en/perf_train_gpu_many)
- [Accelerating Transformers Fine-Tuning with NVIDIA NeMo AutoModel (2026-06-24)](https://huggingface.co/blog/nvidia/accelerating-fine-tuning-nvidia-nemo-automodel)
- [🤗 Kernels: Major Updates (2026-07-06)](https://huggingface.co/blog/revamped-kernels)

---

## 9. Harness 工程与递归自我改进

**来源：** [Harness Engineering for Self-Improvement — Lilian Weng (2026-07-04)](https://lilianweng.github.io/posts/2026-07-04-harness/)

递归自我改进（Recursive Self-Improvement, RSI）最早由 I.J. Good (1965) 提出——一个能设计出更优机器的超智能系统。在 2026 年的 AI 语境下，RSI 不仅意味着模型直接改写自身权重，更广泛地指向模型改进训练管线、部署系统，从而提升后继模型性能的完整循环。前沿实验室（Anthropic、OpenAI）已经验证了这一反馈循环的加速效应。

### 9.1 什么是 Harness？

Harness（线束/框架）是围绕基础模型的系统层，负责编排执行、决策模型如何思考与规划、调用工具与行动、感知与管理上下文、存储产物与评估结果。与早期 "Agent = LLM + Memory + Tools + Planning + Action" 的简单公式不同，现代 Harness 工程更接近运行时与软件系统设计。

**核心设计原则**：刻意保持简单性和通用性，参考既有软件工程实践（如操作系统抽象），让 Harness 封装复杂逻辑的同时保持接口简洁。

### 9.2 三大设计模式

**模式 1：工作流自动化（Workflow Automation）**
定义一个"规划→执行→观察/测试→改进→再执行"的目标导向循环。Karpathy 的 [autoresearch](https://github.com/karpathy/autoresearch) 和 Codex agent loop 是典型范例。

**模式 2：文件系统作为持久记忆（File System as Persistent Memory）**
长周期 Agent 任务中，产物（实验日志、代码 diff、论文摘要、错误轨迹）远超出上下文窗口容量。通过文件的读写和编辑管理持久状态，天然受益于 LLM 基础能力的提升。

**模式 3：子 Agent 与后台任务（Sub-agent and Backend Jobs）**
Harness 可派生多个子 Agent 并行执行，搜索多条假设、运行并发实验或委派隔离子任务。父 Agent 作为轻量进程管理器：启动任务、检查日志、取消失败运行、合并结果。

### 9.3 Harness 优化进阶

**上下文工程（Context Engineering）**：
- **ACE (Zhang et al. 2025)**：将上下文视为"动态演化的剧本"，通过生成器、反思器、策展人三个组件维护条目化的上下文日志
- **Meta Context Engineering (Ye et al. 2026)**：分离"如何管理上下文"的机制与"上下文内容"，在元优化层进化技能，在基础层优化上下文

**工作流搜索**：
- **ADAS (Hu et al. 2025)**：将 Agent 设计本身形式化为优化问题，元 Agent 搜索新的 Agent 工作流设计
- **AFlow (Zhang et al. 2025)**：将工作流表示为图（节点=LLM 调用，边=逻辑操作），用 MCTS 搜索最优工作流

**元 Harness (Meta-Harness, Lee et al. 2026)**：优化的对象是"决定什么信息该存储、检索和呈现给模型"的代码本身。整个执行历史通过文件系统访问，Harness 候选者作为字典存储（含源代码、评分、轨迹、状态更新），只有合格的 Harness 被保留。

### 9.4 关键洞察

> *"Harness 工程将向着元方法论的方向演进——优化的是'获得更好答案的机制'，而不仅仅是答案本身。"*

- Harness 本身成为优化目标，从手工启发规则转向通用机制
- STOP (Zelikman et al. 2023) 实验表明：递归自我改进需要足够强的基础模型（GPT-4 有效，GPT-3.5/Mixtral 退化）
- 随着模型智能提升，许多 Harness 改进可能内化到模型行为中（类似 prompt engineering 的演变路径）

### 参考来源
- [Harness Engineering for Self-Improvement — Lilian Weng (Jul 2026)](https://lilianweng.github.io/posts/2026-07-04-harness/)
- [STOP: Self-Taught Optimizer — Zelikman et al. (2023)](https://arxiv.org/abs/2310.02304)
- [ADAS — Hu et al. (2025)](https://arxiv.org/abs/2408.08435)
- [Distillation in 2026 — Sergio Paniego (2026-07-08)](https://huggingface.co/blog/sergiopaniego/distillation-2026)
- [KV Caching Explained — Not Lain (HuggingFace)](https://huggingface.co/blog/not-lain/kv-caching)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-23 00:09:06*
