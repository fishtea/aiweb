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

## 📚 参考来源

1. [Machine Learning Specialization — Coursera](https://www.coursera.org/specializations/machine-learning-introduction)
2. [Machine Learning Specialization — DeepLearning.AI](https://www.deeplearning.ai/specializations/machine-learning/)
3. [Andrew Ng — Courses 页面](https://www.andrewng.org/courses/)
4. [Coursera AI Learning Roadmap](https://www.coursera.org/resources/ai-learning-roadmap)
5. [AI For Everyone — 入门推荐](https://www.coursera.org/learn/ai-for-everyone)

---

*本页面内容基于真实在线资源编写。所有课程信息、评分和描述均源自各课程官方网站（截至 2026 年 6 月）。*
