# PyTorch — 深度学习框架

> PyTorch 是 Meta（Facebook）开发的**动态计算图**深度学习框架。它是目前 AI 研究和开发中使用最广泛的框架，从学术论文到生成式 AI 产品，PyTorch 无处不在。

---

## 框架概述

| 属性 | 详情 |
|------|------|
| **开发者** | Meta AI (Facebook AI Research) |
| **首次发布** | 2016 年 (PyTorch 0.1) |
| **当前版本** | PyTorch 2.x (2025) |
| **许可** | BSD |
| **核心语言** | Python + C++/CUDA |
| **GitHub** | [pytorch/pytorch](https://github.com/pytorch/pytorch) |

---

## 为什么 PyTorch 成为主流？

根据 [PyTorch 教程 (GeeksForGeeks)](https://www.geeksforgeeks.org/deep-learning/pytorch-tutorial-2) 和 [UvA DL Notebooks](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial2/Introduction_to_PyTorch.html)：

### 动态计算图（Define-by-Run）

与 TensorFlow 1.x 的静态图不同，PyTorch 使用**动态计算图**：
- 图在执行时即时构建
- 可以随意使用 Python 控制流（if/for/while）
- 调试直观（标准的 Python 错误信息）

```python
# 动态图示例 — 条件分支
for epoch in range(n_epochs):
    for x, y in train_loader:
        optimizer.zero_grad()
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()
```

### PyTorch 2.x 关键特性

| 特性 | 说明 |
|------|------|
| **torch.compile** | 即时编译优化，提升 40-50% 性能 |
| **TorchDynamo** | 安全捕获 Python 计算图 |
| **TorchInductor** | 生成 CUDA/CPU 优化内核 |
| **DTensor** | 分布式张量，简化模型并行 |
| **torch.export** | 模型导出到标准格式 |
| **FlexAttention** | 灵活定义注意力变体，兼顾性能与定制 |
| **TorchTitan / FSDP2** | 大模型预训练与分布式训练框架 |

### PyTorch 在 LLM 时代的地位

PyTorch 几乎是 LLM 研究与训练的事实标准：

- **HuggingFace Transformers** 默认后端，几乎所有开源 LLM 都提供 PyTorch 权重。
- **训练框架**：Megatron-LM、Torchtitan、DeepSpeed、FSDP2 都基于 PyTorch 构建分布式训练。
- **微调**：PEFT、TRL、Unsloth、LLaMA Factory 等 LoRA 微调链路均依赖 PyTorch。
- **研究友好**：动态图让论文复现和架构实验（Mamba、MoE、新注意力）极其方便。

> 注：PyTorch 在"推理部署"环节相对薄弱，生产推理更多交给 vLLM、SGLang、TensorRT 等专用引擎。典型分工是 PyTorch 训练 → 导出 → 推理引擎部署。

---

## 核心概念

### 张量（Tensor）

PyTorch 中的基本数据结构，类似 NumPy 但支持 GPU：

```python
import torch

# 创建张量
x = torch.tensor([1, 2, 3])           # 一维
y = torch.rand(2, 3)                   # 随机
z = torch.zeros(4, 4)                  # 全零

# GPU 加速
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x_gpu = x.to(device)

print(f"Using device: {device}")
```

### 自动微分（Autograd）

自动计算梯度，反向传播的核心：

```python
x = torch.randn(3, requires_grad=True)
y = x ** 2 + 2 * x
y.sum().backward()   # 自动计算梯度
print(x.grad)        # 输出梯度
```

### 模块（nn.Module）

所有神经网络的基础类：

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 5)
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.relu(self.linear(x))
```

---

## 训练循环模板

```python
# 数据加载
dataset = MyDataset(file)
train_loader = DataLoader(dataset, batch_size=16, shuffle=True)

# 模型
model = MyModel().to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练循环
for epoch in range(n_epochs):
    model.train()
    for x, y in train_loader:
        optimizer.zero_grad()
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()

# 验证
model.eval()
with torch.no_grad():
    # 验证代码
    pass
```

---

## PyTorch 生态

| 库 | 功能 | 类型 |
|----|------|------|
| **torchvision** | 计算机视觉工具 | 官方 |
| **torchaudio** | 音频处理 | 官方 |
| **torchtext** | 文本处理 | 社区 |
| **HuggingFace Transformers** | Transformer 模型 | 第三方 |
| **PyTorch Lightning** | 训练脚手架 | 第三方 |
| **torchtune** | LLM 微调 | 官方（Meta） |

---

## 如何开始

### 安装

```bash
# CPU 版本
pip install torch torchvision torchaudio

# CUDA 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 从示例开始

推荐学习路径：
1. [PyTorch 官方 60 分钟入门教程](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
2. [PyTorch 官方教程](https://pytorch.org/tutorials/)
3. 动手实现简单模型（MLP、CNN、RNN）

---

## 优势与局限

**优势:**
- **研究首选:** 学术界最广泛使用的框架
- **动态图:** 调试友好，适合实验
- **丰富的生态:** 几乎所有的 LLM 和扩散模型都用 PyTorch 实现
- **torch.compile:** 即时代码优化
- **强大的分布式训练支持**

**局限:**
- **生产部署不如 TensorFlow 成熟**
- **深度学习框架的通病：学习曲线陡峭**
- **移动端支持不如 TensorFlow Lite**
- **C++ API 不如 Python API 完善**

---

**参考资料：**
- [PyTorch Tutorial (GeeksForGeeks)](https://www.geeksforgeeks.org/deep-learning/pytorch-tutorial-2)
- [UvA DL Notebooks — Introduction to PyTorch](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial2/Introduction_to_PyTorch.html)
- [NTU PyTorch Tutorial PDF](https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall-course-data/Pytorch%20Tutorial.pdf)
- [Learn PyTorch in 5 Projects (freeCodeCamp)](https://www.youtube.com/watch?v=E0bwEAWmVEM)
- [Best Resources to Learn PyTorch 2025 (Reddit)](https://www.reddit.com/r/learnmachinelearning/comments/1j5trra/best_resources_to_learn_pytorch_in_2025)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:37:40*
