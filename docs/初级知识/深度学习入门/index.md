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

## 📚 参考来源

1. [Deep Learning Specialization — Coursera](https://www.coursera.org/specializations/deep-learning)
2. [Deep Learning Specialization — DeepLearning.AI](https://www.deeplearning.ai/specializations/deep-learning/)
3. [Andrew Ng — Courses 页面](https://www.andrewng.org/courses/)
4. [Microsoft AI for Beginners — 免费深度学习课程](https://microsoft.github.io/AI-For-Beginners/)
5. [Vaswani et al., "Attention Is All You Need" — Google, 2017](https://research.google/pubs/pub46201/)
6. [DeepLearning.AI 的 YouTube 频道](https://www.youtube.com/c/deeplearningai)

---

*本页面内容基于真实在线资源编写。所有课程信息、评分和描述均源自各课程官方网站（截至 2026 年 6 月）。*
