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

## 📚 参考来源

1. [Machine Learning Specialization — Coursera](https://www.coursera.org/specializations/machine-learning-introduction)
2. [Machine Learning Specialization — DeepLearning.AI](https://www.deeplearning.ai/specializations/machine-learning/)
3. [Andrew Ng — Courses 页面](https://www.andrewng.org/courses/)
4. [Coursera AI Learning Roadmap](https://www.coursera.org/resources/ai-learning-roadmap)
5. [AI For Everyone — 入门推荐](https://www.coursera.org/learn/ai-for-everyone)

---

*本页面内容基于真实在线资源编写。所有课程信息、评分和描述均源自各课程官方网站（截至 2026 年 6 月）。*

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-04 13:05:43*
