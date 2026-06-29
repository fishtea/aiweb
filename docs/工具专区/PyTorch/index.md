# PyTorch

> PyTorch 是当今 AI 研究和开发中最流行的深度学习框架，以其动态计算图和 Python 友好的设计理念赢得了全球开发者的青睐。

---

## 为什么是 PyTorch？

在众多深度学习框架中，PyTorch 脱颖而出：

| 特性 | PyTorch | TensorFlow (Keras) | JAX |
|-----|---------|-------------------|-----|
| **计算图** | 动态（Define-by-Run） | 静态/动态 | 函数式 (JIT) |
| **学习曲线** | 平缓、Pythonic | 中等 | 较陡 |
| **调试** | 原生 Python 调试器 | 需 TF 调试工具 | 较复杂 |
| **研究社区** | 主流（大部分论文用 PyTorch） | 企业为主 | 小但快速增长 |
| **生产部署** | TorchScript + TorchServe | TF Serving | — |
| **分布式** | DDP/FSDP 原生支持 | 支持 | 原生优秀 |

---

## 核心概念

### 1. Tensor（张量）

PyTorch 的基本数据结构，类似 NumPy 但支持 GPU：

```python
import torch

# 创建张量
x = torch.tensor([[1, 2], [3, 4]])
y = torch.randn(3, 4)      # 正态分布随机
z = torch.zeros(2, 3)      # 全零
device = torch.zeros(2, 3, device="cuda")  # GPU 张量

# 运算（与 NumPy 类似）
x + y, x @ y.T, x.mean(), x.sum()

# NumPy 互转
np_array = x.numpy()
tensor = torch.from_numpy(np_array)
```

### 2. Autograd（自动求导）

PyTorch 的核心特性——自动计算梯度：

```python
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2 + 2 * x + 1
loss = y.sum()
loss.backward()  # 自动计算梯度

print(x.grad)  # 梯度: dy/dx = 2x + 2
# 输出: tensor([4., 6., 8.])
```

### 3. nn.Module（神经网络模块）

```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):  # 自动定义计算图
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.log_softmax(x, dim=1)

model = SimpleNet()
print(model)
```

---

## 训练循环

### 完整的训练流程

```python
import torch.optim as optim

# 数据加载
from torch.utils.data import DataLoader, TensorDataset

dataset = TensorDataset(inputs, labels)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 模型、损失函数、优化器
model = SimpleNet().to("cuda")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练循环
for epoch in range(10):
    running_loss = 0.0
    for batch_x, batch_y in dataloader:
        batch_x, batch_y = batch_x.to("cuda"), batch_y.to("cuda")

        # 前向传播
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {running_loss/len(dataloader):.4f}")
```

---

## 分布式训练

### 数据并行（DDP）

```bash
# 启动多 GPU 训练
torchrun --nproc_per_node=4 train.py
```

```python
# train.py
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group(backend="nccl")
model = SimpleNet().to(local_rank)
model = DDP(model, device_ids=[local_rank])

# 后续训练代码与单卡完全相同
```

### FSDP（完全分片数据并行）

适用于大模型训练：

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

model = FSDP(
    model,
    sharding_strategy="FULL_SHARD",
    mixed_precision=True
)
```

---

## 生态系统

| 领域 | 库/工具 | 用途 |
|-----|---------|------|
| **视觉** | torchvision | 图像模型、数据集、转换 |
| **文本** | torchtext | 文本处理、词向量 |
| **音频** | torchaudio | 音频处理、模型 |
| **推理优化** | torch.compile | JIT 编译加速 |
| **模型部署** | TorchScript / TorchServe | 生产环境推理 |
| **分布式** | PyTorch DDP / FSDP | 多卡训练 |
| **量化** | torch.quantization | 模型压缩 |

---

## 优势

- **Pythonic 设计**：与 Python 原生风格一致，学习成本低
- **动态计算图**：运行时定义图结构，调试方便
- **研究首选**：AI 论文最常用的框架
- **社区活跃**：丰富的教程、预训练模型、扩展库
- **GPU 原生支持**：CUDA 集成自然高效
- **生产就绪**：TorchServe、TorchScript 支持部署

## 局限

- **生产部署**：不如 TensorFlow 的 TF Serving 成熟
- **移动端支持**：相比 CoreML/TFLite 较弱
- **自动优化**：需要手动编写优化逻辑
- **内存管理**：大模型训练需精细管理显存

---

## 学习路径

1. **张量基础**：掌握 Tensor 操作和 NumPy 互转
2. **自动求导**：理解 Autograd 机制
3. **模块构建**：学习 nn.Module 和 forward 方法
4. **训练循环**：实现完整的训练和评估流程
5. **数据处理**：使用 DataLoader 管理数据
6. **进阶技巧**：分布式训练、混合精度、模型量化

---

## 下一步

- 安装 PyTorch：`pip install torch torchvision`
- 运行官方 [PyTorch 60 分钟入门教程](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
- 尝试用 PyTorch 实现一个简单的 CNN
- 学习使用 torch.compile 加速模型
- 探索 HuggingFace Transformers 与 PyTorch 的集成
