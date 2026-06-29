# 模型训练与优化

> 训练大规模语言模型是一项系统工程，涉及分布式计算、内存管理、数值精度和硬件调度等多方面的优化。本章深入讲解将模型训练扩展到极致的关键技术。

## 🏗️ 分布式训练

当单卡显存不足以承载模型时，分布式训练成为必然选择。

### 数据并行（Data Parallelism, DP）

每张卡持有完整的模型副本，但处理不同的数据批次：

```
批次 → 分片 → [GPU0] → 梯度 → 汇总 → 更新
          → [GPU1] → 梯度 →     ↑
          → [GPU2] → 梯度 ──────┘
```

**局限**：每张卡都必须能装下完整模型，不适合超大模型。

### 分布式数据并行（Distributed Data Parallel, DDP）

PyTorch 的标准方案，比 DP 更高效：

- 每个进程独立前向和反向传播
- 使用 All-Reduce 算法同步梯度
- 通信效率高于 DP（避免 GIL 问题）

```python
from torch.nn.parallel import DistributedDataParallel
model = DistributedDataParallel(model)
```

### 全分片数据并行（FSDP）

ZeRO Stage 3 的 PyTorch 实现，将模型参数、梯度、优化器状态分片到各 GPU：

```
[GPU0]           [GPU1]           [GPU2]
参数分片 0       参数分片 1       参数分片 2
梯度分片 0       梯度分片 1       梯度分片 2
优化器状态分片 0  优化器状态分片 1  优化器状态分片 2
```

- 训练时按需 All-Gather 各层参数
- 反向传播后 Reduce-Scatter 梯度
- 显存节省可达 3-4 倍

## 🔢 混合精度训练

### 精度格式对比

| 格式 | 位数 | 指数位 | 尾数位 | 数值范围 | 精度 |
|------|------|--------|--------|---------|------|
| FP32 | 32 | 8 | 23 | 3.4×10³⁸ | 高 |
| FP16 | 16 | 5 | 10 | 6.6×10⁴ | 中 |
| BF16 | 16 | 8 | 7 | 3.4×10³⁸ | 中（大范围） |
| FP8 (E4M3) | 8 | 4 | 3 | 448 | 低 |
| FP8 (E5M2) | 8 | 5 | 2 | 57344 | 更低但范围大 |

### BF16 为何优于 FP16

BF16 与 FP32 共享相同的指数位范围（8 位），只是尾数更短。这意味着：

- BF16 不会溢出（FP16 常见问题）
- BF16 不会下溢到零
- 训练 Large Models 时 BF16 是默认选择

### 混合精度训练流程

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    with autocast(dtype=torch.bfloat16):
        outputs = model(batch)
        loss = loss_fn(outputs, targets)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

**关键要点**：
- 前向和反向在低精度下计算
- 权重在主精度（FP32）下更新
- Loss Scaling 防止梯度下溢

## 💾 显存优化技术

训练大模型时，显存是核心瓶颈。以下技术可大幅减少显存占用：

### 梯度检查点（Gradient Checkpointing）

**原理**：在前向传播时不保存中间激活值，反向传播时重新计算。

**收益**：节省约 50-70% 激活显存
**代价**：增加约 20-30% 计算时间

```python
model.gradient_checkpointing_enable()
```

### 梯度累积（Gradient Accumulation）

**原理**：多次前向/反向计算梯度后，累积到一定步数再更新参数。

**用途**：在 Batch Size 受显存限制时，模拟大 Batch Size 训练。

```python
accumulation_steps = 8
for i, batch in enumerate(dataloader):
    loss = model(batch)
    loss = loss / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### 内存优化技术汇总

| 技术 | 显存节省 | 速度影响 | 实现复杂度 |
|------|---------|---------|-----------|
| 梯度检查点 | 50-70% | 慢 20-30% | 低 |
| 梯度累积 | 按需 | 无（总计算量不变） | 低 |
| FSDP | 60-80% | 慢 5-15% | 中 |
| Activation Offloading | 40-60% | 慢 10-20% | 高 |
| CPU Offloading | 80%+ | 极慢 | 中 |
| QLoRA (4-bit) | 75% | 慢 10% | 低 |

## 📈 缩放定律（Scaling Laws）

### 核心发现

Kaplan 等人（2020）和 Chinchilla（2022）的研究揭示：

1. **模型大小与数据量应等比缩放**：增加模型参数的同时，训练数据量也要等比例增加
2. **计算最优分配**：对于给定的算力预算，存在最优的模型大小和数据量配比
3. **平滑缩放**：Loss 随模型大小、数据量、算力呈幂律下降

### Chinchilla 最优假设

对于 D 个 token 和 N 个参数的最优关系：
```
N_opt = k × (C / 6)^0.5
D_opt = (C / 6)^0.5 × (1/k)
```

其中 C 是总计算量（FLOPs），k 是常数。

**实际意义**：很多模型（如 GPT-3）实际上是在数据不足的情况下训练的。Chinchilla 表明，用更多的数据训练较小的模型可以达到更好的效果。

## 🔄 大规模训练策略

### 3D 并行（3D Parallelism）

将三种并行策略组合使用：

```
数据并行 × 张量并行 × 流水线并行

数据并行：数据分片到不同 GPU 组
张量并行：单个层的参数分片到多个 GPU
流水线并行：不同层分配到不同 GPU
```

这是训练超大规模模型（千卡以上）的标准方案。

### 训练基础设施

| 组件 | 考虑因素 |
|------|---------|
| **GPU 互联** | NVLink > InfiniBand > Ethernet |
| **存储** | 分布式文件系统（Lustre、GPFS） |
| **网络拓扑** | 减少跨节点通信延迟 |
| **容错** | 定期 checkpoint，断点续训 |
| **监控** | GPU 利用率、温度、通信带宽 |

## ⚡ 训练效率优化

### 通信优化

- **梯度压缩**：量化梯度后通信
- **通信重叠**：计算和通信重叠进行
- **拓扑感知分配**：按网络拓扑分配 GPU

### 数据加载优化

- 使用 **WebDataset** 或 **Mosaic Streaming** 高效加载
- 启用 `num_workers` 和 `prefetch_factor`
- 数据预处理离线完成

## 💡 实践建议

1. **从小开始**：先用小模型验证训练配置，确认无误后扩展
2. **监控一切**：loss、学习率、梯度范数、通信时间都要监控
3. **基准测试**：训练前先跑通信基准（如 NCCL 测试）
4. **定期保存**：每个 epoch 或每 N 步保存 checkpoint
5. **渐进式扩展**：从单卡到多卡，从 FP32 到混合精度

> **下一步**：训练了强大的模型之后，如何确保它安全可靠？学习 [AI 安全与对齐](../AI安全与对齐/index.md)。
