# 模型训练与优化：GPU 显存就是你的硬通货

> 你有一张 24GB 显存的 4090，想微调一个 70B 模型。听起来像天方夜谭？看完这篇你会发现——它只是技术挑战，不是不可能。

---

## 决策树：先看你的显存

```
你的 GPU 显存是多少？
│
├─ < 8GB（消费级老卡/笔记本）
│   → 只能跑推理。训练？用 API。别折磨自己。
│
├─ 8-16GB（3060/4060）
│   → 可训练 1-3B 模型（全量）或 7B 模型（QLoRA）
│   → 推荐：QLoRA + gradient_checkpointing
│
├─ 16-24GB（4090/A4500）
│   → 最佳性价比区间
│   → 可训练 7B（全量）或 70B（QLoRA）
│   → 推荐：LoRA/QLoRA + 混合精度
│
├─ 24-48GB（A6000/L40S）
│   → 可训练 13B（全量）或 70B（LoRA）
│   → 推荐：全量微调小模型 或 LoRA 大模型
│
├─ 48-80GB（A100-80G/H100）
│   → 专业训练卡
│   → 可单卡训练 7-13B（全量）
│   → 推荐：全量微调 + FSDP
│
└─ 80GB+（多卡集群）
    → 可训练 70B+ 模型
    → 推荐：FSDP + Pipeline Parallelism + Activation Checkpointing
```

---

## 技术一：混合精度训练（FP16 / BF16 / FP8）

### 为什么需要混合精度？

模型训练的核心矛盾：
- FP32：精度够，但显存占用翻倍，速度慢
- FP16：速度快、省显存，但容易数值溢出（gradient underflow/overflow）
- BF16：FP16 的升级版——同样的内存节省，但数值稳定性更好

| 精度 | 位宽 | 显存节省 | 数值范围 | 稳定性 | 适用硬件 |
|-----|:---:|:-------:|:--------:|:-----:|---------|
| FP32 | 32 | 基准 | ±3.4×10³⁸ | 最高 | 所有 GPU |
| FP16 | 16 | -50% | ±6.5×10⁴ | 差（易下溢） | Volta+ |
| BF16 | 16 | -50% | ±3.4×10³⁸ | 好 | Ampere+ |
| FP8 | 8 | -75% | ±448 | 挑战性 | H100+ |
| NF4 | 4 | -87.5% | ~[-8, 8] | 用于 QLoRA | 需量化 |

### 实战配置

```python
# FP16（老卡 T4/V100）
training_args = TrainingArguments(
    fp16=True,
    fp16_opt_level="O2",       # O2 = 保持部分层为 FP32
)

# BF16（A100/H100 推荐）
training_args = TrainingArguments(
    bf16=True,                  # BF16 比 FP16 稳定，推荐
    bf16_full_eval=True,       # 评估时也用 BF16
)

# FP8（H100 专用）
training_args = TrainingArguments(
    fp8=True,                   # 最新 H100 才支持
)

# 混合精度策略（不推荐手动管理）
# 让 PyTorch AMP 自动决定每层的精度
with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    output = model(input_ids)
```

**黄金法则**：只要你的卡支持 BF16（Ampere 架构及以上），永远优先选 BF16 而不是 FP16。BF16 的数值稳定性带来的收敛质量提升，远大于你手动调 FP16 loss scaling 的收益。

---

## 技术二：梯度累积（Gradient Accumulation）

### 什么时候用？

你的 batch size 设 32，但显存只装得下 batch size 4。

**梯度累积 = 假装 batch size 很大，但每次只训练一个小 batch，攒够梯度再更新参数。**

```python
training_args = TrainingArguments(
    per_device_train_batch_size=4,       # 显存只能装 4 个样本
    gradient_accumulation_steps=8,        # 累积 8 次梯度
    # 等效 batch size = 4 × 8 = 32
)
```

### 效果对比

| 显式 batch size | gradient_accumulation_steps | 等效 batch size | 训练速度（相对） | 梯度质量 |
|:--------------:|:--------------------------:|:--------------:|:--------------:|:-------:|
| 32 | 1 | 32 | 4x | 基准 |
| 16 | 2 | 32 | 2x | 几乎等同 |
| 8 | 4 | 32 | 1.5x | 略差 |
| 4 | 8 | 32 | 1x | 可接受 |
| 2 | 16 | 32 | 0.7x | 噪声较大 |
| 1 | 32 | 32 | 0.5x | 不推荐 |

**注意**：梯度累积不能无限增大等效 batch size。当真实 batch size 太小（<4）时，梯度信噪比会显著下降，影响收敛。

---

## 技术三：分布式策略（DDP vs FSDP vs Pipeline）

### 三种策略的对比

```
DDP（Distributed Data Parallel）：
  每个 GPU 一份完整的模型副本
  数据切片：各 GPU 处理不同数据
  通信：每步同步梯度
  场景：模型能放进单卡显存

FSDP（Fully Sharded Data Parallel）：
  模型参数分片在各 GPU
  数据切片 + 模型切片
  通信：计算前 gather 参数，计算后 reduce 梯度
  场景：模型超单卡显存

Pipeline Parallelism：
  模型按层拆分，各 GPU 处理不同层
  数据流水线式流过各 GPU
  场景：超深层模型（100B+）
```

### 选型建议

```python
# DDP：简单场景（单机多卡，模型能放进单卡）
# 启动方式
# torchrun --nproc_per_node=4 train.py
training_args = TrainingArguments(
    per_device_train_batch_size=8,
    ddp_find_unused_parameters=False,
)

# FSDP：模型太大，单卡放不下
# 启动方式
# torchrun --nproc_per_node=8 train.py
from transformers import HfArgumentParser
training_args = TrainingArguments(
    fsdp="full_shard auto_wrap",
    fsdp_config={
        "fsdp_offload_params": False,    # 如果显存还是不够，设为 True
        "fsdp_transformer_layer_cls_to_wrap": ["LlamaDecoderLayer"],
    },
)

# Pipeline：超大模型（百亿+）
# 需要手动切分层到不同 GPU
# 建议用 DeepSpeed 或 Megatron-LM 框架
```

### 性能对比（8×A100，7B 模型）

| 策略 | 吞吐量（tokens/s） | 显存/卡 | 实现复杂度 |
|------|:-----------------:|:-------:|:---------:|
| DDP | 15,000 | ~56GB | 低 |
| FSDP（full shard） | 21,000 | ~28GB | 中 |
| FSDP（hybrid shard） | 18,000 | ~14GB | 中 |
| DeepSpeed ZeRO-3 | 23,000 | ~20GB | 中 |
| Pipeline + FSDP | 19,000 | ~12GB | 高 |

---

## 技术四：显存优化术

### Activation Checkpointing（梯度检查点）

最有效的显存节省手段——不存中间激活值，反向传播时**重新计算**。

```python
# 启用梯度检查点
model.gradient_checkpointing_enable()

# 60% 显存节省，30% 速度损耗
# 性价比极高，默认开启
```

权衡：节省 ~60% 显存，代价是 ~30% 的额外计算时间（因为需要重新计算前向传播）。

### CPU Offloading

把优化器状态、梯度等放到 CPU 内存，只在 GPU 上保留模型参数。

```python
training_args = TrainingArguments(
    fsdp_config={
        "fsdp_offload_params": True,     # 优化器状态放到 CPU
    },
)
# 或者 DeepSpeed ZeRO-3 Offload
```

代价：CPU ↔ GPU 传输速度 ~50GB/s（NVLink 下是 900GB/s），所以 offload 会让训练慢 **3-10x**。只有在显存实在不够时才用。

### 实用显存计算公式

```
训练 7B 模型的显存需求 ≈ 模型参数(GB) × (精度系数):

FP32:  7B × 4字节 = 28GB  (参数) 
       + 28GB (梯度) + 56GB (优化器状态) = 112GB
BF16:  7B × 2字节 = 14GB (参数)
       + 14GB (梯度) + 28GB (优化器状态, FP32) = 56GB
QLoRA: 7B × 0.5字节 = 3.5GB (4-bit 量化参数)
       + 0.01GB (LoRA 适配器) = ~6GB
```

---

## 全套优化模板

```python
# 终极省钱配置（适用于 4090 + 7B 模型）
training_args = TrainingArguments(
    # 精度
    bf16=True,                          # BF16 训练
    # 批大小  
    per_device_train_batch_size=1,      # 最小 batch
    gradient_accumulation_steps=16,     # 累积到等效 16
    # 显存优化
    gradient_checkpointing=True,        # 必须开启
    optim="adamw_8bit",                 # 8-bit 优化器
    # 分布式（如果有多个 GPU）
    ddp_find_unused_parameters=False,
    # 日志
    logging_steps=1,
    report_to="none",
    # 保存
    save_strategy="epoch",
    save_total_limit=2,
)
```

## 常见问题速查

```
Q: 训练时 OOM（显存溢出）怎么办？
A: 按优先级试：
   1. 开启 gradient_checkpointing
   2. 降低 batch size 到 1
   3. 使用 8-bit 优化器（bitsandbytes）
   4. 切换到 QLoRA
   5. CPU offload（最后手段）

Q: 训练速度太慢怎么办？
A: 按优先级试：
   1. 确认使用了 BF16 而不是 FP32
   2. 增加 batch size（如果显存允许）
   3. 检查 DataLoader num_workers
   4. 使用 Flash Attention 2
   5. 检查 CPU/GPU 数据传输是否成为瓶颈（在 nvidia-smi 中看 PCIe 利用率）
```
