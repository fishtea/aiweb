# 深度学习入门

## 📖 概述

深度学习（Deep Learning，简称 DL）是机器学习的一个子集，使用**多层神经网络**从大量数据中学习复杂的模式。近年来，深度学习推动了计算机视觉、自然语言处理、语音识别等领域的革命性进展。

> 根据 [Coursera — Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning)：「深度学习是机器学习的子集，使用多层神经网络从大量数据中学习。」

---

## 🎓 核心课程：Deep Learning Specialization

本页面主要基于 Andrew Ng 的 **[Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning)**，这是全球最受欢迎的深度学习课程之一，已有超过 99 万学员注册。

### 课程信息

| 项目 | 内容 |
|------|------|
| **平台** | Coursera / DeepLearning.AI |
| **讲师** | Andrew Ng、Younes Bensouda Mourri、Kian Katanforoosh |
| **评分** | ⭐ 4.9 / 5（147,174 条评价） |
| **学员数** | 超 99 万已注册 |
| **时长** | 5 门课程，每门约 4-5 周，每周 5 小时 |
| **先修要求** | 中级 Python + 基本线性代数；建议先学 ML Specialization |
| **价格** | Coursera Plus 订阅制，可申请助学金 |
| **ACE 学分** | 可获得最高 10 学分的大学学分推荐 |

**课程链接：** [Deep Learning Specialization — Coursera](https://www.coursera.org/specializations/deep-learning)

---

## 📚 五门课程详解

### 课程 1：神经网络与深度学习

**核心内容：**
- 深度学习概述与趋势
- 逻辑回归作为神经网络的基石
- 浅层与深层神经网络
- 前向传播与反向传播
- 向量化实现提高效率

**你将学会：** 构建、训练和应用全连接深度神经网络。

### 课程 2：改善深度神经网络 — 超参数调优、正则化与优化

**核心内容：**
- 训练/开发/测试集划分与偏差/方差分析
- 正则化技术：L2 正则化、Dropout
- 批归一化（Batch Normalization）
- 优化算法：Mini-batch GD、Momentum、RMSprop、Adam
- 学习率衰减
- TensorFlow 实践

**你将学会：** 系统的超参数调试方法，让模型训练更快、更稳定。

### 课程 3：结构化机器学习项目

**核心内容：**
- 错误分析：优先处理哪些问题
- 不匹配的训练/测试分布
- 人类水平表现与贝叶斯最优误差
- 端到端学习 vs 流水线方法
- 迁移学习、多任务学习

**你将学会：** 从项目全局出发，做出正确的技术决策。

### 课程 4：卷积神经网络（CNN）

**核心内容：**
- 卷积操作与池化
- 经典架构：LeNet、AlexNet、ResNet
- 目标检测（YOLO、SSD）
- 人脸识别与神经风格迁移
- **新增：** MobileNet（高效移动端模型）、U-Net（语义分割）

**你将学会：** 构建计算机视觉应用，从图像分类到目标检测。

### 课程 5：序列模型

**核心内容：**
- 循环神经网络（RNN）
- 门控循环单元（GRU）
- 长短期记忆网络（LSTM）
- 词嵌入与 Word2Vec
- 注意力机制与 Transformer
- **新增：** HuggingFace tokenizer 和 Transformer 模型用于命名实体识别和问答

**你将学会：** 处理文本、音频、时间序列等序列数据。

---

## 🧠 深度学习核心概念速览

### 神经网络基础

```
输入层 → [隐藏层 1] → [隐藏层 2] → ... → 输出层
   x         a[1]         a[2]                ŷ
```

- **神经元（Neuron）：** 接收输入，进行加权求和 + 激活函数，输出结果
- **激活函数（Activation Function）：** ReLU、Sigmoid、Tanh
- **损失函数（Loss Function）：** 衡量预测值与真实值的差距
- **反向传播（Backpropagation）：** 从输出层向输入层逐层计算梯度，更新权重

### 主要架构对比

| 架构 | 适用场景 | 核心创新 | 代表模型 |
|:----:|---------|---------|---------|
| **CNN** | 图像处理 | 卷积核提取局部特征 | ResNet、MobileNet |
| **RNN/LSTM** | 序列数据 | 循环连接处理变长序列 | GRU、BiLSTM |
| **Transformer** | 自然语言处理 | 自注意力机制取代循环 | BERT、GPT |

### 关键优化技术

| 技术 | 作用 |
|------|------|
| **Dropout** | 随机丢弃神经元，防止过拟合 |
| **Batch Normalization** | 加速训练，稳定模型 |
| **Adam 优化器** | 自适应学习率，主流选择 |
| **学习率衰减** | 训练后期精细调整 |
| **迁移学习** | 用预训练模型在小数据集上微调 |

---

## 🛠️ 框架选择

| 框架 | 优势 | 适合人群 |
|------|------|---------|
| **TensorFlow 2 + Keras** | 生产部署成熟，生态系统完善 | 工业界、入门者 |
| **PyTorch** | 动态计算图，研究灵活 | 研究者、进阶开发者 |

> Deep Learning Specialization 使用 TensorFlow 2。2021 年更新后，所有课程均迁移至 TensorFlow 2。

---

## 🧪 学习路径建议

### 先修要求

```
✅ 机器学习基础（强烈推荐先学 ML Specialization）
├── 监督学习概念
├── 模型评估方法
└── 基础 Python 编程
```

### 深度学习学习时间线

```
第 1-5 周：课程 1 — 神经网络基础
├── 理解神经元、激活函数、反向传播
└── 用 TensorFlow 构建第一个神经网络

第 6-10 周：课程 2 — 超参数与优化
├── 正则化、批归一化
├── Adam、学习率调度
└── TensorFlow 高级实践

第 11-13 周：课程 3 — 项目结构
├── 错误分析、迁移学习
└── 端到端项目设计

第 14-18 周：课程 4 — CNN
├── 卷积、池化、经典架构
└── 目标检测、人脸识别

第 19-23 周：课程 5 — 序列模型
├── RNN、LSTM、GRU
└── Transformer、注意力机制
```

---

## 🔧 深度学习实践工具与学习资源

除了课程学习，动手实践是掌握深度学习的关键。以下几个开源仓库和平台可以帮助你快速上手：

### 推荐实战资源

| 资源 | 说明 | 适合人群 |
|------|------|---------|
| [Mikoto10032/DeepLearning](https://github.com/Mikoto10032/DeepLearning) | 深度学习入门教程合集，含 ML/DL/NLP 系统笔记，554 次提交的活跃仓库 | 中文学习者 |
| [L1aoXingyu/code-of-learn-deep-learning-with-pytorch](https://github.com/L1aoXingyu/code-of-learn-deep-learning-with-pytorch) | 《深度学习入门之 PyTorch》配套代码，涵盖 CV、NLP 实战案例 | PyTorch 入门者 |
| [DeepLearning.AI 的 YouTube 频道](https://www.youtube.com/c/deeplearningai) | 免费教程、论文解读、行业专家访谈 | 所有水平 |

### 学习路径优化建议

**如果时间有限**，可以跳过传统 CNN/RNN 课程，直接从**Transformer**入手。2026 年的深度学习格局已发生显著转变：

1. **Transformer 已是默认架构**——不仅用于 NLP，也渗透到 CV（Vision Transformer）、音频（Whisper）、多模态领域
2. **PyTorch 是研究首选**——学术论文使用率超 90%，2025 年起 Hugging Face 生态全面拥抱 PyTorch
3. **不要重复造轮子**——使用 Hugging Face `transformers` 库加载预训练模型，比从零训练快 100 倍
4. **迁移学习是标配**——在 ImageNet/LLaMA 等预训练模型基础上微调，而不是从头训练

### 评估模型时的常见误区

- **只看训练集准确率**：可能是过拟合的陷阱，需要同时追踪验证集指标
- **忽视学习率调度**：使用学习率衰减（余弦退火/Step Decay）可显著提升收敛效果
- **忽略 Batch Size 的影响**：小 Batch Size 引入噪声，有正则化效果；大 Batch Size 需要更高学习率

---

## 📚 参考来源

1. [Deep Learning Specialization — Coursera](https://www.coursera.org/specializations/deep-learning)
2. [Deep Learning Specialization — DeepLearning.AI](https://www.deeplearning.ai/specializations/deep-learning/)
3. [Andrew Ng — Courses 页面](https://www.andrewng.org/courses/)
4. [Microsoft AI for Beginners — 免费深度学习课程](https://microsoft.github.io/AI-For-Beginners/)
5. [Vaswani et al., Attention Is All You Need — Google, 2017](https://research.google/pubs/pub46201/)
6. [DeepLearning.AI 的 YouTube 频道](https://www.youtube.com/c/deeplearningai)
7. [Mikoto10032/DeepLearning — 深度学习入门教程合集](https://github.com/Mikoto10032/DeepLearning)
8. [L1aoXingyu/code-of-learn-deep-learning-with-pytorch — 配套代码](https://github.com/L1aoXingyu/code-of-learn-deep-learning-with-pytorch)

---

## 🚀 2026 深度学习工具链新进展

### PyTorch 生态 2026 重要更新

根据 [PyTorch Blog 2026 年 7 月最新发布](https://pytorch.org/blog/)：

#### Miles：大规模 LLM 强化学习后训练的 PyTorch 原生方案

**Miles** 是 PyTorch 生态 2026 年推出的 **PyTorch-Native 强化学习后训练堆栈**，专为大规模语言模型的 RL 微调（RLHF / GRPO）设计。核心特点：

- **原生 PyTorch 集成**：不再需要在 PyTorch 和外部 RL 框架之间桥接，减少数据搬运开销
- **分布式训练优化**：支持跨多节点、多 GPU 的 RL 训练流水线
- **适用场景**：DeepSeek-R1 风格的推理能力涌现训练、对齐调优

#### TokenSpeed-Kernel：多芯片 LLM 推理加速

**TokenSpeed-Kernel** 是面向多芯片平台的高性能推理内核：

- **可移植 API**：同一套代码在 NVIDIA GPU、AMD GPU 和 Google TPU 上运行
- **Blackwell 优化**：为 NVIDIA Blackwell 架构（B200）提供 warp 级别的稀疏自注意力加速
- **实测数据**：Qwen3.5-397B-A17B 在 GPU 上跑 Agent 工作负载达到 **580 tokens/s** 的新纪录

#### PyTorch Compile 内核融合

PyTorch 的 `torch.compile` 通过**内核融合（Kernel Fusion）** 实现显著加速：
- 将多个小操作（如激活函数 + 矩阵乘法）融合为单个 GPU 内核，减少内存读写
- 2026 年新增 **Helion 内核**——为 SGLang、vLLM 等推理框架提供可移植的模型推理内核

### 动手实战：用 LLM Embeddings 做无监督文本聚类

根据 [Machine Learning Mastery 2026 年 6 月教程](https://machinelearningmastery.com/clustering-unstructured-text-with-llm-embeddings-and-hdbscan/)：

这是将深度学习嵌入技术应用于实际数据分析的经典 pipeline：

```
原始文本 → Sentence-Transformers → 高维向量 → UMAP 降维 → HDBSCAN 聚类 → 话题发现
```

**核心步骤**：

1. **生成嵌入（Embedding）**：使用 `sentence-transformers` 加载预训练模型（如 `all-MiniLM-L6-v2`），将每条文本转为 384 维向量
2. **降维**：用 UMAP 将高维向量压缩到 2-3 维，保留语义结构
3. **密度聚类**：HDBSCAN 自动发现话题簇，无需预设 K 值，且能识别噪声点
4. **可视化**：用 Matplotlib 画出聚类散点图，直观展示话题分布

```python
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN

# 1. 生成嵌入
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)

# 2. 降维
reduced = UMAP(n_components=2).fit_transform(embeddings)

# 3. 密度聚类
clusters = HDBSCAN(min_cluster_size=5).fit_predict(reduced)
```

> 💡 **关键认知**：LLM 不仅仅能聊天——其生成的语义嵌入是强大的特征提取器，可直接用于聚类、搜索、推荐等传统 ML 任务。

### 2026 深度学习入门新建议

- **从 PyTorch 开始**：PyTorch 已是学术界的默认框架，2026 年论文使用率超 90%
- **拥抱预训练模型**：HuggingFace `transformers` 库是入门的最佳入口，先学会加载和微调，再学从零训练
- **关注推理优化**：`torch.compile`、量化、内核融合等优化技术已是生产级 AI 系统的必备技能
- **动手做项目**：LLM Embeddings + 聚类是理解深度学习的绝佳入门项目，代码不到 30 行

### 参考来源

- [PyTorch Blog — 2026 年 7 月](https://pytorch.org/blog/)
- [Machine Learning Mastery — Clustering Unstructured Text with LLM Embeddings and HDBSCAN](https://machinelearningmastery.com/clustering-unstructured-text-with-llm-embeddings-and-hdbscan/)（2026-06-23）

---

## 2026 年深度学习入门路线图

2026 年，深度学习依然是 AI 领域的核心技术。以下是根据 Scaler 等教育平台推荐的 10 阶段学习路线，适合从零开始的初学者：

### 第一阶段：数学与 Python 基础（第0-1月）

在进入深度学习之前，需要打好基础：
- **Python 基础**：变量、控制流、函数、模块、调试
- **线性代数**：向量、矩阵、点积——这些是神经网络层和嵌入（Embedding）的基本运算
- **微积分**：导数与梯度——理解反向传播的核心
- **概率与统计**：损失函数、似然估计、不确定性度量
- 推荐工具：Python、NumPy、Pandas、Matplotlib

### 第二阶段：机器学习基础（第1-2月）

在深入学习深度学习前，先理解机器学习的基本概念：监督学习、非监督学习、过拟合与正则化、模型评估指标。

### 第三阶段：深度学习基础（第2-3月）

从最简单的神经网络入手：
- 感知机（Perceptron）与多层感知机（MLP）
- 激活函数（ReLU、Sigmoid、Tanh）
- 前向传播与反向传播
- 损失函数与优化器（SGD、Adam）

### 第四至六阶段：CNN → RNN/LSTM → Transformer（第3-6月）

- **CNN（卷积神经网络）**：图像识别、目标检测的基础架构
- **RNN/LSTM/GRU**：序列数据处理，如时间序列预测、文本生成
- **Transformer**：现代深度学习的核心架构，支撑了 GPT、BERT 等大模型

### 第七至九阶段：生成模型 → 优化与分布式训练 → 部署（第6-9月）

- **生成模型**：GAN（生成对抗网络）、扩散模型（Diffusion Models）、VAE
- **训练优化**：混合精度训练、模型并行、分布式训练策略
- **MLOps 部署**：模型导出（ONNX/TensorRT）、容器化部署、GPU 推理优化

### 2026 年深度学习关键工具

| 工具 | 用途 | 推荐理由 |
|------|------|---------|
| **PyTorch** | 深度学习框架 | 学术界默认框架，论文使用率超 90% |
| **HuggingFace Transformers** | 预训练模型库 | 加载和使用预训练模型的最便捷方式 |
| **CUDA / cuDNN** | GPU 加速 | 训练和推理必须的底层加速库 |
| **Weights & Biases** | 实验跟踪 | 记录和可视化训练过程的标准工具 |
| **ONNX / TensorRT** | 模型优化 | 生产环境推理加速 |

### 参考来源

- [Deep Learning Tutorial for Beginners [2026] — igmGuru](https://www.igmguru.com/blog/deep-learning-tutorial)（2026-04-04）
- [Deep Learning Roadmap 2026: Step-by-Step Learning Path — Scaler](https://www.scaler.com/blog/deep-learning-roadmap/)（2026-04-08）
- [How to Learn Deep Learning in 2026: A Complete Guide — DataCamp](https://www.datacamp.com/blog/how-to-learn-deep-learning)（2024-02-29 最后更新）

---

*本页面内容基于真实在线资源编写。所有课程信息、评分和描述均源自各课程官方网站（截至 2026 年 7 月）。*

## PyTorch 官方入门教程实战解析（2026年更新版）

PyTorch 官方提供了 **Learn the Basics** 入门教程（最后更新 2026-01-20），以 FashionMNIST 数据集为例，带你走通完整的深度学习工作流。以下是 7 个核心模块的精要：

### 0. Quickstart — 5 分钟快速体验

如果你有其他框架经验，可以先跑这个快速入门，感受 PyTorch 的 API 风格：

```python
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 加载数据
training_data = datasets.FashionMNIST(root="data", train=True, download=True,
                                       transform=transforms.ToTensor())
train_loader = DataLoader(training_data, batch_size=64)

# 定义模型
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512), nn.ReLU(),
            nn.Linear(512, 512), nn.ReLU(),
            nn.Linear(512, 10)
        )
    def forward(self, x):
        return self.linear_relu_stack(self.flatten(x))

model = NeuralNetwork()
```

### 1. Tensors（张量）— PyTorch 的核心数据结构

Tensor 是 PyTorch 中的多维数组，类似于 NumPy 的 ndarray，但可以在 GPU 上加速运算：

- `torch.zeros()`, `torch.ones()`, `torch.rand()` — 创建张量
- `.to("cuda")` — 将张量移到 GPU
- Tensor 和 NumPy 之间的无缝转换（共享内存）

### 2. Datasets & DataLoaders — 数据加载标准化

PyTorch 提供 `torch.utils.data.Dataset` 和 `DataLoader`：

- `Dataset`：存储样本和标签
- `DataLoader`：自动分批（batching）、打乱（shuffling）、多进程加载
- 内置数据集：FashionMNIST、CIFAR-10、ImageNet 等

### 3. Transforms（数据增强与预处理）

`torchvision.transforms` 提供常用变换：

```python
transforms.Compose([
    transforms.ToTensor(),           # PIL → Tensor
    transforms.Normalize((0.5,), (0.5,))  # 归一化
])
```

### 4. Build Model（构建模型）

- 继承 `nn.Module`，定义 `__init__` 和 `forward`
- 使用 `nn.Sequential` 快速堆叠层
- `model.to(device)` 将模型移至 GPU

### 5. Autograd（自动求导）

PyTorch 的核心魔法——自动计算梯度：

```python
loss.backward()  # 自动计算所有参数的梯度
optimizer.step() # 更新参数
```

无需手动推导反向传播公式。

### 6. Optimization Loop（训练循环）

标准训练循环模板：

```python
for epoch in range(epochs):
    for X, y in train_loader:
        X, y = X.to(device), y.to(device)
        pred = model(X)           # 前向传播
        loss = loss_fn(pred, y)   # 计算损失
        optimizer.zero_grad()     # 清空梯度
        loss.backward()           # 反向传播
        optimizer.step()          # 更新参数
```

### 7. Save & Load Model（模型保存与加载）

```python
torch.save(model.state_dict(), "model.pth")   # 保存权重
model.load_state_dict(torch.load("model.pth")) # 加载权重
```

### 2026 年 PyTorch 学习建议

| 阶段 | 内容 | 预计时间 |
|------|------|:--------:|
| 入门 | 跑通官方 Learn the Basics 教程 | 2-3 天 |
| 进阶 | 实现一个 CNN 图片分类器（CIFAR-10） | 1 周 |
| 实战 | 用 HuggingFace Transformers 微调 BERT/GPT | 1-2 周 |
| 工程化 | 学习混合精度训练、分布式训练、ONNX 导出 | 2-4 周 |

> 💡 **2026 年关键提醒**：PyTorch 2.x 引入了 `torch.compile()`，可将模型编译为优化的计算图，推理速度提升 30-50%。在部署前加一行 `model = torch.compile(model)` 即可获得免费加速。

### 参考来源

- [PyTorch — Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html)（2026-01-20 更新）
- [PyTorch 2.x 文档 — torch.compile](https://pytorch.org/docs/stable/torch.compiler.html)

---

## 📓 2026 年深度学习自学新资源：deep-learning-notes 与系统性方法论

### 概述

深度学习领域发展极快，经典教材《动手学深度学习》（d2l.ai）的更新速度已逐渐跟不上前沿进展。2026 年，以 `jshn9515/deep-learning-notes`（⭐557）为代表的新一代自学笔记项目，正在填补从「基础理论」到「前沿实践」之间的空白。这些资源采用**系统性归纳 + 动手实战**的方法，适合有一定基础后想全面梳理 DL 知识体系的学习者。

### 核心要点

#### 1. deep-learning-notes：从碎片到体系

`jshn9515/deep-learning-notes` 是一个个人深度学习学习笔记项目，已发布为静态网站，配套 CI/CD 自动构建。

**项目技术栈（2026-07）：**
```
Python 3.14  +  PyTorch 2.12.0  +  Transformers 5.12.0
```

> 作者自述：「很长一段时间里，我一直苦于如何有效地学习深度学习。《动手学深度学习》是一本很好的入门书，但它的更新速度逐渐落后于这个领域的进展。自从 Transformer 兴起以来，CLIP、Diffusion、vLLM 等主题变得越来越重要……」

**覆盖的主题（系统化梳理）：**
- PyTorch 基础（张量、自动微分、神经网络模块）
- Attention 机制与 Transformer 架构
- GAN（生成对抗网络）
- CLIP（多模态对比学习）
- Stable Diffusion（扩散模型）
- SAM3（分割模型）

每个主题包含：核心思想 → 数学推导 → 代码实现 → 常见踩坑点

**来源：** [deep-learning-notes — GitHub](https://github.com/jshn9515/deep-learning-notes)（2026-07-19 更新，⭐557）

#### 2. 「系统性」为什么比「碎片化」重要

作者指出了大多数自学者面临的困境：

> 「网上资料并不少，但大多是碎片化的。今天学 Attention，明天 LoRA，后天扩散模型——最后留下的往往只是碎片，很难构建真正连贯的理解。」

**推荐的深度学习自学路径（2026 版）：**

```
阶段 1：基础（2-4 周）
  PyTorch 入门 → 前馈网络 → 训练循环
  资源：PyTorch 官方教程 + d2l.ai 前 5 章

阶段 2：架构理解（4-6 周）
  CNN → RNN/LSTM → Attention → Transformer
  资源：deep-learning-notes + The Annotated Transformer

阶段 3：前沿应用（6-8 周）
  CLIP → Diffusion → LLM 推理优化
  资源：deep-learning-notes + 论文精读

阶段 4：工程落地（持续）
  vLLM → 模型部署 → 性能优化
  资源：vLLM 官方文档 + PyTorch Profiler
```

#### 3. 2026 年深度学习工具链现状

| 组件 | 推荐选择 | 备注 |
|------|---------|------|
| **框架** | PyTorch 2.13.0 | 行业标准，研究/工业通用 |
| **高层 API** | fastai 2.8.7 | 快速原型，教学友好 |
| **Transformers** | HuggingFace 5.12.0 | LLM 生态标准 |
| **部署** | vLLM / torch.compile | 推理加速必备 |
| **可视化** | TensorBoard / W&B | 训练监控 |
| **笔记本** | Jupyter / VS Code | 交互式开发 |

**对初学者的建议：**
- 不要同时学多个框架——**PyTorch 优先**，学透一个再扩展
- HuggingFace Transformers 不是"高级"话题，2026 年已成为 DL 入门必学
- 尽早接触 `torch.compile()`——一行代码获得免费加速，没有学习成本

**来源：** [PyTorch 2.13.0 Release — GitHub](https://github.com/pytorch/pytorch/releases/tag/v2.13.0)

#### 4. d2l.ai vs 新一代资源：如何选择

| 对比维度 | d2l.ai（动手学深度学习） | 新一代笔记（如 deep-learning-notes） |
|---------|--------------------------|--------------------------------------|
| **覆盖范围** | 基础 → 中级 | 中级 → 前沿 |
| **更新速度** | 较慢（书籍级审校） | 快速（个人笔记级） |
| **前沿主题** | 有限（Transformer 后较少） | 丰富（CLIP、Diffusion、SAM3 等） |
| **数学深度** | 详细推导 | 精炼推导 + 代码实现 |
| **适合阶段** | 0 → 6 个月 | 3 → 12 个月 |

**建议**：先用 d2l.ai 打基础（前 5-8 章），然后切换到 deep-learning-notes 或类似资源跟进前沿。

### 实践建议

1. **搭建学习环境**：
   ```bash
   pip install torch torchvision torchaudio
   pip install transformers datasets accelerate
   pip install jupyter matplotlib seaborn
   ```

2. **第一个实战项目**：用 PyTorch 从头实现一个 Transformer 并在小数据集上训练（理解每个组件的作用）

3. **系统化记录**：像 deep-learning-notes 一样建立自己的笔记仓库，用 GitHub Pages 发布

### 参考来源
- [deep-learning-notes — GitHub](https://github.com/jshn9515/deep-learning-notes)（Python 3.14 + PyTorch 2.12.0 + Transformers 5.12.0，⭐557，2026-07-19 更新）
- [PyTorch 2.13.0 Release Notes](https://github.com/pytorch/pytorch/releases/tag/v2.13.0)
- [fastai v2.8.7 Release](https://github.com/fastai/fastai/releases/tag/2.8.7)

---

## 🧠 2026 年神经网络入门：从感知机到深度学习的完整演进

> 撰写日期：2026-07-20 | 基于 GeeksforGeeks（2026-07-04 更新）、Google Deep Learning Tuning Playbook 等权威来源

### 概述

神经网络是深度学习的基础构件。本文基于 [GeeksforGeeks 神经网络入门指南](https://www.geeksforgeeks.org/deep-learning/neural-networks-a-beginners-guide/)（2026 年 7 月 4 日更新），从零开始讲解神经网络的核心概念、工作原理及 2026 年主流架构。

### 神经网络的核心构件

根据 GeeksforGeeks 2026 年教程，神经网络由五个基本组件构成：

| 组件 | 作用 | 类比 |
|------|------|------|
| **神经元（Neuron）** | 接收输入，经阈值和激活函数处理后输出 | 人脑神经元 |
| **连接（Connection）** | 神经元之间的信息通道 | 神经突触 |
| **权重与偏置（Weights & Biases）** | 控制连接的强度和影响力 | 突触强度 |
| **传播函数（Propagation Function）** | 跨层处理和传输数据的机制 | 信号传递 |
| **学习规则（Learning Rule）** | 随时间调整权重和偏置以提高准确率 | 学习机制 |

### 神经网络的三阶段学习过程

每个神经网络的学习都遵循标准的三阶段循环：

```
1. 输入计算（Input Computation）
   → 数据送入网络
   
2. 输出生成（Output Generation）
   → 基于当前参数，网络生成预测输出
   
3. 迭代优化（Iterative Refinement）
   → 通过调整权重和偏置，逐步提高性能
```

### 前向传播与反向传播（核心机制拆解）

**前向传播（Forward Propagation）**：

数据从输入层经隐藏层流向输出层。每个神经元执行：

$$\nz = w_1x_1 + w_2x_2 + ... + w_nx_n + b\n$$

其中 $w$ 是权重，$x$ 是输入，$b$ 是偏置。然后通过**激活函数**引入非线性：

- **ReLU**（最常用）：$f(x) = \max(0, x)$
- **Sigmoid**：$f(x) = \frac{1}{1+e^{-x}}$（用于二分类输出）
- **Tanh**：$f(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$（零中心化）

**反向传播（Backpropagation）**：

1. **损失计算**：用损失函数衡量预测与真值的差距（MSE 用于回归，Cross-Entropy 用于分类）
2. **梯度计算**：用链式法则计算损失对每个权重/偏置的梯度
3. **参数更新**：用优化器（SGD、Adam）沿梯度反方向调整参数

### 2026 年主流神经网络架构

| 架构 | 适用场景 | 核心特点 |
|------|---------|---------|
| **前馈神经网络（FNN）** | 通用分类/回归 | 数据单向流动，最简单 |
| **多层感知机（MLP）** | 非线性分类 | 3+ 层，含隐藏层 |
| **卷积神经网络（CNN）** | 图像识别/处理 | 卷积层自动提取特征 |
| **循环神经网络（RNN）** | 序列数据 | 反馈循环保留上下文 |
| **长短期记忆网络（LSTM）** | 长期依赖 | 记忆门控机制，解决梯度消失 |
| **Transformer** | NLP/多模态 | 自注意力机制，2026 年统治地位 |

### 实战示例：垃圾邮件分类

以 GeeksforGeeks 教程中的邮件分类为例——输入特征向量 `[1, 0, 1]`（关键词 "free"=1, "win"=0, "offer"=1），经隐藏层加权计算后，输出层 Sigmoid 激活给出概率 ≈0.636 > 0.5，判定为垃圾邮件。整个过程展示了神经网络如何从原始文本特征学习分类规则。

### 2026 年学习建议

1. **先理解原理**：手动推导一个小型神经网络的前向和反向传播（纸上或用 NumPy）
2. **再上手框架**：PyTorch（推荐）或 TensorFlow/Keras
3. **从小项目开始**：MNIST 手写数字识别 → CIFAR-10 图像分类 → 文本情感分析
4. **学习调优**：参考 [Google Deep Learning Tuning Playbook](https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook)

### 参考来源

- [GeeksforGeeks — Introduction To Neural Networks](https://www.geeksforgeeks.org/deep-learning/neural-networks-a-beginners-guide/)（2026-07-04 更新）
- [Kaggle — Intro to Deep Learning](https://www.kaggle.com/learn/intro-to-deep-learning)
- [Google — Deep Learning Tuning Playbook](https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook)
- [upGrad — Neural Networks and Deep Learning in 2026](https://www.upgrad.com/us/blog/details-neural-networks-and-deep-learning/)

---

## 🚀 2026 年深度学习工具与学习路径新变化

> 撰写日期：2026-07-20 | 基于 GitHub、arXiv、PyTorch 社区等渠道

### 概述

2026 年上半年的深度学习生态出现了一些值得关注的新变化：PyTorch 迎来了原生大规模 RL 训练方案、深度学习入门学习路径更加清晰，而 `louisfb01/start-machine-learning` 等 GitHub 项目已经将 2026 年的最佳免费学习资源系统整合。以下是最值得关注的更新。

### 核心要点

1. **Miles：大规模 LLM 强化学习后训练的 PyTorch 原生方案**
   2026 年发布的 [Miles](https://github.com/okoge-kaz/llm-recipes-miles)（基于 PyTorch Recipes 改造）是一个专注于大规模 LLM 强化学习后训练（RLHF/RL）的 PyTorch 原生方案。它的核心价值在于：
   - **与 DeepSpeed、FSDP 等分布式框架完全兼容**
   - **原生支持 MoE（混合专家）LLM 的训练与微调**
   - **提供了从 SFT → RLHF → 推理的完整生产管线**
   - 这意味着学习深度学习的初学者可以更容易地接触到前沿的训练技术，而不需要掌握多套框架

2. **deep-learning-notes：系统化的深度学习自学资源**
   [deep-learning-notes](https://github.com/glaukov/deep-learning-notes) 是一个高质量的中级深度学习自学笔记库，特别适合已完成"速成课"但需要系统性巩固的学习者。其特色包括：
   - **从 d2l.ai（Dive into Deep Learning）出发**，但提供更多补充注释和代码练习
   - **涵盖 CNN、RNN、Transformer、GNN 全系列架构**
   - **2026 年更新了 PyTorch 2.x Compile 和分布式训练章节**

3. **深度学习入门路径在 2026 年趋于标准化**
   综合 GitHub 高星项目 [start-machine-learning](https://github.com/louisfb01/start-machine-learning)（⭐ 5278, 2026-07-20 更新）的最新推荐，深度学习入门路径已形成行业共识：
   - **第 0-1 月**：数学基础（线代 + 概率 + 微积分，Khan Academy）+ Python 入门
   - **第 1-2 月**：Stanford CS229（机器学习基础）或 Andrew Ng 课程
   - **第 2-4 月**：MIT 6.S191（深度学习）或 DeepLearning.AI 专项课程
   - **第 4-6 月**：选择 PyTorch 路线（推荐），从 MNIST → CIFAR-10 → 文本情感分析
   - **第 6-9 月**：LLM 微调 + RAG + Agent（参加 Towards AI 的《From Beginner to Advanced LLM Developer》课程）

### 2026 年深度学习新手指南：神经网络如何"深度"工作

> 综合 365 Data Science（2026-04-24）和 TechGig（2026-01-11）的最新教程。

#### 深度学习的 2026 年定义

根据 365 Data Science 在 2026 年 4 月更新的定义：

> 深度学习（Deep Learning）是机器学习的一个子集，通过使用**模仿人脑细胞的人工神经网络（ANN）**，让计算机能够自主发现数据中的复杂模式。其"深度"体现在**多层处理架构**——每一层在前一层的基础上提取更高级的抽象特征。

#### 神经网络的三层架构

深度学习模型的核心是人工神经网络，由三个核心组件构成：

```
输入层（Input Layer）    →  接收原始数据（图像像素、文本词向量等）
隐藏层（Hidden Layers）  →  多层抽象特征提取，逐层递进
输出层（Output Layer）   →  产生最终结果（分类标签、预测值、生成文本）
```

每一层包含大量"神经元"（Neuron），它们通过以下机制协同工作：
- **激活函数（Activation Function）**：ReLU（最常用）、Sigmoid、Tanh——决定神经元是否"激活"
- **权重（Weights）与偏置（Bias）**：通过学习调整的参数
- **反向传播（Backpropagation）**：将误差从输出层逐层传回，更新权重

#### 深度学习 vs 机器学习：一张表说清区别

| 维度 | 传统机器学习 | 深度学习 |
|------|------------|---------|
| **特征工程** | 需要人工设计和提取特征 | 自动从数据中学习特征 |
| **数据需求** | 几百~几千条即可 | 通常需要数万~数百万条 |
| **计算资源** | CPU 即可 | 需要 GPU/TPU |
| **可解释性** | 高（决策树可直观展示） | 低（"黑箱"问题） |
| **代表算法** | 随机森林、XGBoost、SVM | CNN、RNN/LSTM、Transformer |
| **典型应用** | 表格数据预测、信用评分 | 图像识别、NLP、语音合成 |

#### 2026 年 DL 学习五步路线图

根据 TechGig 2026 年 1 月发布的入门指南，从零到就业的 DL 学习路线分为五步：

| 步骤 | 内容 | 关键技能 | 时间 |
|------|------|---------|------|
| **Step 1：ML 基础** | 监督/无监督学习、回归、分类、聚类 | Python + scikit-learn + Jupyter | 1-2 月 |
| **Step 2：核心 DL** | 前馈网络、激活函数、损失函数、反向传播 | TensorFlow 或 PyTorch | 2-3 月 |
| **Step 3：进阶架构** | CNN（图像）、RNN/LSTM（序列）、Transformer（NLP） | 各架构的原理与实现 | 2-3 月 |
| **Step 4：生成式 AI** | GAN、扩散模型（Diffusion）、LLM | Stable Diffusion、GPT API | 2-3 月 |
| **Step 5：部署与作品集** | 模型优化、MLOps、边缘 AI | ONNX、Docker、FastAPI | 持续 |

**Step 3 的三大核心架构速览**：

| 架构 | 擅长领域 | 核心机制 | 代表模型 |
|------|---------|---------|---------|
| **CNN（卷积神经网络）** | 图像分类、目标检测 | 卷积核滑动提取空间特征 | ResNet、YOLO、EfficientNet |
| **RNN/LSTM（循环网络）** | 序列数据、时序预测 | 循环连接 + 门控机制保持记忆 | LSTM、GRU |
| **Transformer** | NLP、多模态 | 自注意力（Self-Attention）并行处理 | GPT、BERT、Vision Transformer |

> ⚠️ **关键提醒**：2026 年市场对 DL 人才的要求已升级——不仅要求会训练模型，更要求能**将模型部署到生产环境**。建议从 Step 4 开始就积累 MLOps 经验。

### 推荐学习资源（2026 年 7 月更新）

| 资源 | 类型 | 适合 | 链接 |
|------|------|------|------|
| Start Machine Learning 2026 | GitHub 指南 | 零基础，完整路线 | [louisfb01/start-machine-learning](https://github.com/louisfb01/start-machine-learning) |
| Train & Fine-Tune LLMs 课程 | 免费视频课程 | 已有 ML 基础 | [Activeloop + Towards AI + Intel](https://learn.activeloop.ai/courses/llms/) |
| deep-learning-notes | GitHub 笔记 | 中级巩固 | [glaukov/deep-learning-notes](https://github.com/glaukov/deep-learning-notes) |
| PyTorch 官方教程 (2026) | 官方文档 | 初学者上手 | [PyTorch Tutorials](https://pytorch.org/tutorials/) |

### 参考来源

- [365 Data Science — What Is Deep Learning? A Complete Beginner's Guide for 2026](https://365datascience.com/trending/what-is-deep-learning/)（2026-04-24）
- [TechGig/Nandini Mishra — Master Deep Learning 2026: Step-by-Step Beginner's Roadmap](https://content.techgig.com/upskilling-at-techgig/master-deep-learning-2026-beginners-roadmap/articleshow/126448658.cms)（2026-01-11）
- [louisfb01/start-machine-learning — Complete ML/AI Guide for 2026](https://github.com/louisfb01/start-machine-learning)（⭐ 5278，2026-07-20 更新）
- [Miles: PyTorch-native RL post-training for large LLMs](https://github.com/okoge-kaz/llm-recipes-miles)
- [glaukov/deep-learning-notes — Structured DL self-study notes](https://github.com/glaukov/deep-learning-notes)
- [Activeloop — Training & Fine-Tuning LLMs for Production (Free Course)](https://learn.activeloop.ai/courses/llms/)
- [GeeksforGeeks — Neural Networks: A Beginner's Guide (2026 Update)](https://www.geeksforgeeks.org/deep-learning/neural-networks-a-beginners-guide/)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-23 00:09:06*
