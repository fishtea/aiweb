# AI 学习路线图

这是一条面向零基础读者的 AI 入门路线。目标不是先背模型名，而是逐步建立“问题、数据、模型、评估、应用”的完整框架。

## 先理解学习目标

不同读者进入 AI 的目标不同，学习顺序也不同：

| 目标 | 优先学习 | 暂时不用深挖 |
|------|----------|--------------|
| 产品、运营、管理者 | AI 能力边界、典型应用、提示词、风险判断 | 反向传播、分布式训练 |
| 应用开发者 | Python、API 调用、提示词、RAG、Agent、评估 | 从零训练大模型 |
| 数据分析/算法入门 | Python、数据处理、机器学习、模型评估 | 复杂系统架构 |
| 研究型读者 | 数学、深度学习、论文阅读、实验复现 | 过早做复杂产品化 |

初学者最常见的误区是直接跳到“哪个模型最强”。更稳妥的路线是先理解 AI 系统如何工作，再学习具体模型和工具。

## 推荐顺序

```text
第 1 步：人工智能入门
理解 AI、机器学习、深度学习、生成式 AI 的关系。

第 2 步：数学与 Python 基础
补齐线性代数、概率统计、Python、数据处理的最低必要知识。

第 3 步：机器学习基础
理解监督学习、无监督学习、训练集、测试集、过拟合和评估指标。

第 4 步：深度学习入门
理解神经网络、损失函数、梯度下降、CNN、RNN、Transformer。

第 5 步：大语言模型基础
理解 token、上下文窗口、预训练、指令微调、幻觉和生成过程。

第 6 步：提示词、RAG 和 Agent
把模型接入真实任务：检索知识、调用工具、执行工作流。

第 7 步：评估、安全和部署
建立质量评估、成本控制、隐私保护和持续迭代意识。
```

## 30 天入门计划

| 时间 | 学习重点 | 产出 |
|------|----------|------|
| 第 1-3 天 | AI 基本概念、发展史、应用场景 | 能解释 AI/ML/DL/LLM 的关系 |
| 第 4-7 天 | Python、NumPy、Pandas 基础 | 能读取 CSV 并做简单统计 |
| 第 8-12 天 | 监督学习、分类、回归 | 训练一个房价预测或分类模型 |
| 第 13-16 天 | 模型评估、过拟合、特征工程 | 能判断模型是否真的有效 |
| 第 17-20 天 | 神经网络和深度学习 | 理解损失函数、梯度下降、激活函数 |
| 第 21-24 天 | LLM、token、提示词 | 能稳定写出结构化提示词 |
| 第 25-27 天 | Embedding、RAG 基础 | 做一个小型文档问答原型 |
| 第 28-30 天 | 安全、伦理、成本、上线检查 | 形成一个可演示的小项目 |

## 第一个项目怎么选

优先选“小、明确、能验证”的项目：

- 文档问答：上传几篇文章，让模型回答并引用来源。
- 评论分类：判断用户评论是正面、负面还是中性。
- 表格预测：用历史数据预测销量、价格或风险等级。
- 自动摘要：把长文、会议记录、客服对话压缩成结构化摘要。
- 简单 Agent：让模型根据用户问题选择调用搜索、计算或数据库查询。

不要把第一个项目做成“全自动公司助手”。范围太大时，问题很难定位，学习效率反而低。

## 学习检查点

学完初级知识后，你应该能回答这些问题：

- AI、机器学习、深度学习、大语言模型分别是什么关系？
- 数据集为什么要分训练集、验证集和测试集？
- 准确率高为什么不一定代表模型好？
- 过拟合是什么，如何发现和缓解？
- LLM 为什么会出现幻觉？
- 提示词、RAG、微调分别适合解决什么问题？
- 什么时候应该用现成模型，什么时候才考虑训练或微调？

## 推荐的免费课程资源

以下课程均经过社区验证，质量可靠，且大部分免费。按学习阶段分类：

### 入门阶段

| 课程 | 平台 | 适合人群 | 说明 |
|------|------|----------|------|
| [AI for Beginners](https://github.com/microsoft/AI-For-Beginners) | Microsoft | 零基础 | 12 周 24 节课，涵盖符号 AI、神经网络、CV、NLP、LLM、AI 伦理 |
| [Making Friends with Machine Learning](https://www.youtube.com/playlist?list=PLRKtJ4IpxJpDxl0NTvNYQWKCYzHNuy2xG) | YouTube | 零基础 | 迷你系列讲座，解释分类 vs 回归、精度 vs 召回等核心概念 |
| [Caltech CS156: Learning from Data](https://www.youtube.com/playlist?list=PLD63A284B7615313A) | YouTube/Caltech | 有编程基础 | 经典入门课程，覆盖学习问题、VC 维、偏差-方差权衡、过拟合 |

### 机器学习进阶

| 课程 | 平台 | 适合人群 | 说明 |
|------|------|----------|------|
| [Stanford CS229: Machine Learning](https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU) | Stanford | 有数学基础 | 线性回归、逻辑回归、SVM、决策树、神经网络入门 |
| [Applied Machine Learning](https://www.youtube.com/playlist?list=PL2UML_KCiC0UlY7iCQDSiGDMovaupqc83) | YouTube | 有 Python 基础 | 优化、过拟合、正则化、蒙特卡洛估计等实用技术 |

### 深度学习

| 课程 | 平台 | 适合人群 | 说明 |
|------|------|----------|------|
| [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) | YouTube (Andrej Karpathy) | 有编程基础 | 从零实现神经网络，深入理解反向传播 |
| [Stanford CS230: Deep Learning](https://www.youtube.com/playlist?list=PLoROMvodv4rOABXSygHTsbvUz4G_YQhOb) | Stanford | 有 ML 基础 | 构建 CNN、RNN、LSTM，涵盖 GAN、可解释性 |
| [Practical Deep Learning for Coders](https://www.youtube.com/playlist?list=PLfYUBJiXbdtSvpQjSnJJ_PmDQB_VyT5iU) | fast.ai | 有 Python 基础 | 使用 PyTorch 和 fastai 快速上手深度学习实践 |

### NLP 与大语言模型

| 课程 | 平台 | 适合人群 | 说明 |
|------|------|----------|------|
| [CS224N: NLP with Deep Learning](https://www.youtube.com/playlist?list=PLoROMvodv4rOSH4v6133s9LFPRHjEmbmJ) | Stanford | 有深度学习基础 | 依存分析、RNN、Transformer、预训练模型、LLM |
| [Hugging Face NLP Course](https://www.youtube.com/playlist?list=PLo2EIpI_JMQvWfQndUesu0nPBAtZ9gP1o) | YouTube/Hugging Face | 有 Python 基础 | 迁移学习、分词、微调、文本嵌入、模型评估 |

### 学习建议

- **不要同时学多门课程**：选一门主线课程（推荐 Microsoft AI for Beginners 或 Stanford CS229），从头到尾学完再看其他的。
- **边学边练**：每学一个概念，立刻用小项目验证。比如学完回归就拿一个公开数据集跑一遍。
- **加入学习社区**：Microsoft AI Discord、Hugging Face 社区、Reddit r/MachineLearning 都是不错的讨论场所。
- **定期回顾**：AI 领域更新很快，但基础概念（偏差-方差、过拟合、梯度下降）不会变。打好基础再看新论文会更轻松。

## 延伸阅读

- [人工智能入门](../人工智能入门/)
- [Python 与数据处理基础](../Python与数据处理基础/)
- [机器学习基础](../机器学习基础/)
- [大语言模型基础](../大语言模型基础/)
- [提示词工程](/进阶学习/提示词工程/)

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-08。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-25 00:09:45*
