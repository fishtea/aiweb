# 机器学习基础

## 📖 概述

机器学习（Machine Learning，简称 ML）是人工智能的核心分支。它不是通过显式编程来告诉计算机做什么，而是让计算机**从数据中自动学习模式**并做出预测或决策。

> 根据 [Coursera AI 学习路线图](https://www.coursera.org/resources/ai-learning-roadmap)：「机器学习使计算机能够从数据中学习，而无需进行显式编程。」

---

## 🎓 核心课程：Machine Learning Specialization

本页面内容主要基于 Andrew Ng 的 **[Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction)**，这是全球最受欢迎的 AI 课程之一（原版课程自 2012 年起已吸引超过 480 万学习者）。

### 课程信息

| 项目 | 内容 |
|------|------|
| **平台** | Coursera / Stanford Online / DeepLearning.AI |
| **讲师** | Andrew Ng（DeepLearning.AI 创始人、Coursera 联合创始人、斯坦福教授） |
| **评分** | ⭐ 4.9 / 5 |
| **学员数** | 超 79 万已注册 |
| **时长** | 约 10 周，每周 5 小时 |
| **先修要求** | 基础 Python 编程（循环、函数、条件判断）+ 高中数学 |
| **价格** | Coursera Plus 订阅制（约 $49/月），可申请助学金 |

**课程链接：** [Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction)  
**DeepLearning.AI 页面：** [Machine Learning Specialization](https://www.deeplearning.ai/specializations/machine-learning/)

---

## 📚 三门课程详解

### 课程 1：监督式机器学习 — 回归与分类

| 周次 | 主题 | 内容 |
|:----:|------|------|
| 第 1 周 | 机器学习入门 | 什么是 ML、监督学习 vs 非监督学习、线性回归模型 |
| 第 2 周 | 多元线性回归 | 梯度下降、特征缩放、学习率、特征工程 |
| 第 3 周 | 分类（逻辑回归） | 逻辑回归、决策边界、过拟合与正则化 |

**实践工具：** NumPy、scikit-learn

### 课程 2：高级学习算法

| 周次 | 主题 | 内容 |
|:----:|------|------|
| 第 1 周 | 神经网络 | 感知机、多层感知机、激活函数 |
| 第 2 周 | 训练神经网络 | TensorFlow 实现、前向传播、反向传播 |
| 第 3 周 | 模型评估与调优 | 偏差/方差诊断、学习曲线、数据增强、迁移学习 |
| 第 4 周 | 决策树 | 决策树、随机森林、XGBoost、树集成方法 |

**实践工具：** TensorFlow

### 课程 3：无监督学习、推荐系统与强化学习

| 周次 | 主题 | 内容 |
|:----:|------|------|
| 第 1 周 | 无监督学习 | K-means 聚类、异常检测、主成分分析（PCA） |
| 第 2 周 | 推荐系统 | 协同过滤、基于内容的深度学习推荐 |
| 第 3 周 | 强化学习 | 深度强化学习、Q-learning、状态/动作/奖励 |

---

## 🔑 核心概念速览

### 机器学习三大类型

```
监督学习
├── 定义：使用有标签的数据训练模型
├── 任务：预测（回归）和分类
├── 算法：线性回归、逻辑回归、决策树、随机森林
└── 应用：房价预测、垃圾邮件检测、医疗诊断

无监督学习
├── 定义：使用无标签的数据，发现隐藏模式
├── 任务：聚类和降维
├── 算法：K-means、PCA、异常检测
└── 应用：客户分群、异常检测、图像压缩

强化学习
├── 定义：智能体通过与环境交互获得奖励/惩罚来学习
├── 任务：序列决策
├── 算法：Q-learning、深度 Q 网络
└── 应用：游戏 AI（AlphaGo）、机器人控制、自动驾驶
```

### 常用评估指标

| 指标 | 定义 | 适用场景 |
|-----|------|---------|
| **准确率（Accuracy）** | 正确预测数 / 总预测数 | 数据集均衡时 |
| **精确率（Precision）** | 真正例 / 预测为正例总数 | 假阳性代价高（如垃圾邮件） |
| **召回率（Recall）** | 真正例 / 实际为正例总数 | 假阴性代价高（如医疗诊断） |
| **F1 分数** | 精确率和召回率的调和平均 | 需要平衡两者时 |

**来源：** [Coursera AI Learning Roadmap](https://www.coursera.org/resources/ai-learning-roadmap)

---

## 🛠️ 实践工具

| 工具/库 | 主要用途 | 学习建议 |
|---------|---------|---------|
| **Python** | 通用编程语言 | AI/ML 的必备语言 |
| **NumPy** | 数值计算、矩阵运算 | 基础中的基础 |
| **scikit-learn** | 传统机器学习算法 | 入门首选 |
| **TensorFlow** | 深度学习框架 | 学完基础后学习 |
| **Pandas** | 数据处理与清洗 | 数据预处理必备 |
| **Matplotlib/Seaborn** | 数据可视化 | 分析数据、展示结果 |

---

## 🧪 学习路径建议

### 时间线（10 周计划）

```
第 1-3 周：课程 1 — 监督学习基础
├── 线性回归、逻辑回归
└── 用 NumPy 和 scikit-learn 实践

第 4-7 周：课程 2 — 高级算法
├── 神经网络、TensorFlow
├── 决策树、随机森林
└── 模型调优技巧

第 8-10 周：课程 3 — 无监督与高级主题
├── 聚类、异常检测
├── 推荐系统
└── 强化学习
```

### 与原始课程的关键区别

Andrew Ng 在 2022 年重新设计了这门课程。与原版相比，新版有这些变化：

| 特性 | 原版课程（2012） | 新版 Specialization |
|------|----------------|-------------------|
| 编程语言 | Octave | **Python**（NumPy、TensorFlow） |
| 课程数 | 1 门 | **3 门**（内容大幅扩展） |
| 教学方法 | 先讲数学 | **直觉先行** → 代码 → 可选数学 |
| 实践 | 直接评分作业 | **先练后考**（含交互式图表的练习） |
| 最佳实践 | 较少 | **更新**了最近十年的实践经验 |

**来源：** [DeepLearning.AI ML Specialization 页面](https://www.deeplearning.ai/specializations/machine-learning/)

---

## 🧠 机器学习全景：IBM 2026 指南

### 机器学习的三大核心类型

根据 [IBM 2026 机器学习指南](https://www.ibm.com/think/machine-learning)，所有 ML 算法可归为三类：

| 类型 | 原理 | 典型算法 | 典型应用 |
|------|------|---------|---------|
| **监督学习** | 用标注数据训练（输入 → 已知输出） | 线性回归、决策树、SVM、随机森林 | 房价预测、垃圾邮件分类 |
| **无监督学习** | 从无标注数据中发现模式 | K-Means 聚类、层次聚类、PCA | 用户分群、异常检测 |
| **强化学习** | 通过试错 + 奖励信号学习策略 | Q-Learning、Deep Q-Network、PPO | 游戏 AI、机器人控制 |

此外，**半监督学习**和**自监督学习**在实践中越来越重要——前者结合少量标注 + 大量无标注数据，后者（如 BERT 的掩码预测）已成为 LLM 预训练的核心范式。

### 特征工程：被低估的关键环节

> 来源：[IBM 特征工程专题](https://www.ibm.com/think/topics/feature-engineering)

特征工程是从原始数据中**选择、转换和创建新特征**的过程，直接影响模型上限：

- **特征选择**：去除冗余/无关特征，降低过拟合风险
- **特征提取**：PCA、LDA 等降维技术，将高维数据映射到低维空间
- **向量嵌入**：将类别变量、文本转化为稠密向量（Word2Vec、BERT Embeddings）
- **数据泄漏防范**：训练数据中混入未来信息是 ML 项目失败的头号原因之一

### ML 开发生命周期（MLOps）

现代 ML 项目已从「训练一个模型」扩展到完整工程流水线：

```
业务理解 → 数据采集 → 数据清洗 → 特征工程 → 模型训练 → 模型评估 → 部署 → 监控 & 迭代
```

其中 **MLOps**（[IBM MLOps 指南](https://www.ibm.com/think/topics/mlops)）关注模型上线后的持续管理：漂移检测、模型治理、自动重训练。

### 2026 年学习路线图要点

根据 [Coursera ML 路线图](https://www.coursera.org/resources/ml-learning-roadmap) 和 [DataCamp AI 入门指南](https://www.datacamp.com/blog/how-to-learn-ai) 的建议：

1. **打好编程基础**：Python + NumPy/Pandas（2-4 周）
2. **理解核心算法**：线性回归 → 决策树 → SVM → 神经网络（4-8 周）
3. **掌握工具链**：Scikit-learn → TensorFlow/PyTorch
4. **动手做项目**：Kaggle 竞赛、个人项目（持续）
5. **进阶方向**：NLP / 计算机视觉 / 生成式 AI / MLOps

---

## 🎯 初学者常见误区与应对策略

根据博客园 EdisonZhou 的文章[《机器学习入门：基础知识与快速开始》](https://cnblogs.com/edisontalk/p/-/quick-start-on-machine-learning)以及 Machine Learning Mastery 的[入门指南](https://machinelearningmastery.com/start-here)总结的学习经验：

### 误区一：追求完美模型，忽视基线

许多初学者一上来就想训练出准确率 95%+ 的模型。正确的做法是先建立一个**简单基线**（如线性回归或决策树），了解数据的基本可预测性，再逐步优化。

### 误区二：跳过 EDA（探索性数据分析）

> "了解数据比选择算法更重要。"

在训练任何模型之前，先用 Pandas + Matplotlib 分析：
- 缺失值分布与处理策略（均值填充/删除/插值）
- 特征之间的相关性热力图
- 目标变量的分布（偏态 → 考虑 log 变换）

### 误区三：混淆训练集与测试集

新手常犯的错误是在训练前对整个数据集做归一化/标准化。正确流程应是：
1. `train_test_split` 先拆分
2. 只在**训练集上**计算均值和标准差
3. 用训练集的参数**转换**训练集和测试集

### 误区四：选择算法前不做数据预处理

> 据 GeeksforGeeks [Machine Learning Tutorial](https://geeksforgeeks.org/machine-learning/machine-learning) 指出，数据预处理是 ML pipeline 中最耗时但最重要的环节。

**标准化（Standardization）**：对正态分布的数据适用，使特征均值为 0、标准差为 1。
**归一化（Normalization）**：将特征缩放到 [0,1] 区间，适合非正态分布。
**编码（Encoding）**：One-Hot 编码处理无序类别变量；Label Encoding 处理有序类别。

### 实操建议：从第一个项目开始

根据博客园文章推荐的实战 5 步法：

1. **定义问题**：是回归还是分类？监督还是无监督？
2. **收集数据与预处理**：可视化 → 清洗 → 特征工程 → 拆分训练/验证/测试集
3. **选择与训练模型**：从最简单的算法开始（线性回归/KNN/决策树）
4. **模型评估**：使用交叉验证 + 评估指标（准确率/F1/MSE）
5. **部署与迭代**：保存模型（pickle/joblib），在新数据上持续测试

> 参考示例：公众号文章阅读量预测——根据点赞数、转发数等特征，用线性回归预估阅读量。这是一个典型的监督学习回归问题，适合作为第一个练手项目。

---

## 🧪 2026 机器学习全景：范式、模型与挑战

### Mitchell 的形式化定义

Tom Mitchell（1997）给出了机器学习最经典的定义：

> "A computer program is said to **learn** from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E."

简单翻译：计算机程序通过**经验（E）** 在**任务（T）** 上的**表现（P）** 得到提升，就是学习。

### 三大学习范式对比

| 范式 | 数据形式 | 核心思想 | 典型应用 | 代表算法 |
|------|---------|---------|---------|---------|
| **监督学习** | 带标签数据 (X → Y) | 从示例中学习映射关系 | 垃圾邮件分类、房价预测、图像识别 | 线性回归、决策树、SVM、神经网络 |
| **无监督学习** | 无标签数据 (X) | 自动发现数据结构 | 客户分群、异常检测、降维可视化 | K-Means、PCA、DBSCAN、自编码器 |
| **强化学习** | 环境交互 (状态→动作→奖励) | 通过试错最大化累积奖励 | 游戏AI、机器人控制、推荐系统 | Q-Learning、PPO、DQN |

此外还有：
- **半监督学习**：少量标签 + 大量无标签数据混合训练
- **自监督学习**：从数据自身构造监督信号（如 LLM 的下一词预测）
- **迁移学习**：将一个任务学到的知识应用到另一个任务
- **联邦学习**：多方协作训练模型，数据不出本地（如 Gboard 键盘预测）

### 关键模型速览（2026）

| 模型类型 | 原理 | 优缺点 |
|---------|------|-------|
| **决策树 / 随机森林** | 基于特征分裂做决策 | ✅ 可解释性强 ❌ 容易过拟合 |
| **支持向量机（SVM）** | 寻找最大间隔超平面 | ✅ 小样本表现好 ❌ 大规模数据慢 |
| **K 近邻（KNN）** | 相似样本投票 | ✅ 无需训练 ❌ 推理慢 |
| **朴素贝叶斯** | 基于贝叶斯定理的条件概率 | ✅ 速度快，Google 内部最常用 |
| **神经网络 / 深度学习** | 多层非线性变换 | ✅ 表达能力强 ❌ 需要大量数据和算力 |
| **XGBoost / LightGBM** | 梯度提升树集成 | ✅ 表格数据王者 ❌ 不可微 |

### 模型崩溃（Model Collapse）——2026 年的新挑战

当 AI 生成的内容充斥互联网，后续模型如果使用这些合成数据进行训练，会逐渐"退化"——

```
第一代模型：用人类数据训练 → 正常
第二代模型：用第一代输出训练 → 开始退化
第三代模型：用前两代输出训练 → 质量崩塌
```

这被称为"模型崩溃"（也称 AI 近亲繁殖 / Habsburg AI / MAD）。2025-2026 年这已成为学术界密切关注的问题——互联网上 AI 生成内容占比越来越高，数据清洗需过滤掉合成内容。

### 机器学习的局限性

- **可解释性（黑箱问题）**：深度神经网络即使设计者也难以解释其决策过程
- **过拟合**：模型在训练数据上表现完美，但新数据上泛化差
- **数据偏见**：训练数据中的偏见会被模型放大（如招聘系统歧视、司法系统偏见）
- **对抗脆弱性**：微小的输入扰动可能导致完全错误的输出
- **幻觉**：LLM 生成看似合理但实际错误的输出

---

## 📚 参考来源

1. [Machine Learning Specialization — Coursera](https://www.coursera.org/specializations/machine-learning-introduction)
2. [Machine Learning Specialization — DeepLearning.AI](https://www.deeplearning.ai/specializations/machine-learning/)
3. [Andrew Ng — Courses 页面](https://www.andrewng.org/courses/)
4. [Coursera AI Learning Roadmap](https://www.coursera.org/resources/ai-learning-roadmap)
5. [AI For Everyone — 入门推荐](https://www.coursera.org/learn/ai-for-everyone)
6. [EdisonZhou — 机器学习入门：基础知识与快速开始](https://cnblogs.com/edisontalk/p/-/quick-start-on-machine-learning)
7. [Machine Learning Mastery — Start Here](https://machinelearningmastery.com/start-here)
8. [GeeksforGeeks — Machine Learning Tutorial](https://geeksforgeeks.org/machine-learning/machine-learning)
9. [Machine Learning — Wikipedia](https://en.wikipedia.org/wiki/Machine_learning)（2026 年 7 月查阅）

---

*本页面内容基于真实在线资源编写。所有课程信息、评分和描述均源自各课程官方网站（截至 2026 年 7 月）。*

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-05 05:14:27*
