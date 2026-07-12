# 自然语言处理基础

自然语言处理（NLP）研究如何让计算机理解、处理和生成文本。搜索、翻译、客服、摘要、情感分析和大语言模型都属于 NLP 的应用范围。

## NLP 解决什么问题

| 任务 | 说明 | 示例 |
|------|------|------|
| 文本分类 | 给文本打标签 | 垃圾邮件、情感分析 |
| 信息抽取 | 从文本中抽取结构化信息 | 人名、地点、金额、日期 |
| 文本匹配 | 判断两段文本是否相关 | 搜索召回、相似问题匹配 |
| 机器翻译 | 从一种语言转成另一种语言 | 中英翻译 |
| 文本摘要 | 压缩长文本 | 新闻摘要、会议纪要 |
| 问答系统 | 根据问题给出答案 | 客服、知识库问答 |
| 文本生成 | 生成文章、代码、对话 | ChatGPT、写作助手 |

## 从文本到数字

模型不能直接处理自然语言，需要先转成数字表示。

```text
文本 → 分词/token 化 → 向量化 → 模型处理 → 输出结果
```

传统 NLP 常用词袋模型、TF-IDF；现代 NLP 更多使用 Embedding 和 Transformer。

## 分词与 token

中文文本没有天然空格，所以分词尤其重要。大语言模型通常使用子词 token 化，把词拆成更小的片段。

Token 会影响：

- 上下文窗口能放多少内容。
- API 计费和推理成本。
- 长文档切分策略。
- 生成内容的速度。

## Embedding

Embedding 是把文本映射成向量的方法。语义相近的文本，向量距离通常也更近。

典型用途：

- 相似句检索
- 推荐系统
- 聚类分析
- RAG 文档召回
- 语义去重

## 传统 NLP 与 LLM 的关系

| 阶段 | 方法 | 特点 |
|------|------|------|
| 规则方法 | 关键词、正则、词典 | 可解释但泛化差 |
| 统计学习 | TF-IDF、朴素贝叶斯、SVM | 适合小任务，依赖特征工程 |
| 深度学习 | Word2Vec、RNN、CNN | 能学习语义表示 |
| Transformer | BERT、GPT、T5 | 预训练后可迁移到多任务 |
| LLM | 指令跟随、多轮对话、工具调用 | 通用能力强，但需要评估和约束 |

## 2025-2026 NLP 最新进展

### 大语言模型重塑 NLP 生态

2025-2026 年，LLM 已经深刻改变了 NLP 的工作方式。许多传统 NLP 任务（文本分类、命名实体识别、情感分析）现在通过 Prompt 或 Few-shot 即可完成，不再需要为每个任务单独训练模型。

| 传统方法 | LLM 方法 | 对比 |
|----------|----------|------|
| 微调 BERT 做分类 | 用 GPT/Claude 做 zero-shot 分类 | LLM 更灵活，但成本更高 |
| 独立训练 NER 模型 | 结构化输出抽取 | LLM 可处理开放类型 |
| 单独训练摘要模型 | LLM 直接生成摘要 | 质量更高，但需关注幻觉 |
| 规则+模型做意图识别 | Function Calling 自动识别 | LLM 推理能力强，延迟较高 |

**关键判断标准**：高吞吐、低延迟场景宜用传统小模型；需要理解复杂语义、推理和上下文关联的场景更适合 LLM。

### 多模态 NLP 成为主流

- **文本+图像**：GPT-4o、Gemini、Claude 3.5 等模型同时理解文字和图像
- **音频理解**：Whisper + LLM 实现语音到文本到意图的端到端处理
- **文档理解**：Docling、LayoutLM 等模型将 PDF/扫描件转为结构化数据
- **视频理解**：从视频中提取字幕、检测事件、生成摘要

多模态 NLP 使得企业不再需要单独搭建 OCR、ASR 和 NLU 流水线——一个模型可以串联完成所有步骤。

### 检索增强生成（RAG）与 NLP

RAG 已成为企业 NLP 应用的标准架构：

1. **文档切分**：将知识库文档切成适合检索的段落
2. **向量化**：用 Embedding 模型（text-embedding-3-small、BGE、E5）将段落转为向量
3. **语义检索**：在向量数据库中召回最相关文档
4. **答案生成**：将检索结果拼入 Prompt，让 LLM 生成回答

RAG 的核心优势在于可以结合传统 NLP 的精确检索能力 + LLM 的灵活生成能力。

### Agent 与工具调用

2026 年 NLP 的重要趋势是 Agent 系统：

- **函数调用（Function Calling）**：LLM 自动判断需要调用哪个 API、提取参数、返回结果
- **代码解释（Code Interpreter）**：模型写代码并执行，用于数据分析、可视化
- **多步骤推理**：Chain-of-Thought（思维链）让模型逐步推理，提升复杂任务准确率
- **Multi-Agent 协作**：多个 Agent 分别处理搜索、计算、验证等子任务

### 中文 NLP 的特殊进展

- **中文 Embedding 质量大幅提升**：BGE、Conan-embedding-v1 等模型对中文语义理解已接近英文水平
- **混合语言处理**：Qwen、DeepSeek 等国产模型在中英混合场景表现优秀
- **行业中文 NLP**：医疗、法律、金融等行业已有专项微调模型可用
- **中文 RAG**：中文分句分词优化结合向量检索，准确率持续提升

### NLP 工程最佳实践（2026）

- **不盲目用 LLM**：简单分类任务用传统方法（如 fastText、TF-IDF + LR）成本更低、延迟更小
- **评估分层**：RAG 需要评估检索召回率 + 生成准确率，分开追踪
- **质量控制**：LLM 输出需约束格式（JSON Schema）、验证字段合法性、检测幻觉
- **监控与回退**：置信度低于阈值时回退到规则引擎或人工处理
- **成本控制**：短文本用小模型（如 GPT-4o-mini、Claude Haiku），复杂推理用大模型

## 常见误区

- LLM 很强，但不等于所有 NLP 任务都必须用大模型。
- 文本相似不等于答案正确，RAG 需要检索和生成两层评估。
- 长文本直接塞进上下文不一定好，切分、排序和去噪同样重要。
- 中文任务要关注分词、术语、繁简体、行业缩写和混合语言。

## 入门项目

- 评论情感分类
- FAQ 相似问题匹配
- 简历信息抽取
- 长文章摘要
- 企业文档问答

## 2026 NLP 前沿趋势

NLP 在 2026 年已进入后 Transformer 时代，新思路和新架构正在重塑这一领域。以下是五个值得关注的前沿趋势。

### 1. 高效注意力机制（Efficient Attention）

Transformer 的核心弱点——自注意力（Self-Attention）的计算和内存消耗随序列长度二次增长——正在被多种高效注意力机制解决：

| 方法 | 原理 | 代表研究 |
|------|------|----------|
| 线性注意力（Linear Attention） | 将注意力复杂度从 O(n²) 降到 O(n) | Linformer |
| 稀疏注意力（Sparse Attention） | 只让 tokens 关注局部或特定范围 | HydraRec |
| 硬件感知注意力 | 利用 GPU 显存层级优化计算 | FlashAttention 3, AttentionEngine |

这些方法使模型能处理更长的上下文而不受硬件瓶颈限制，让大规模 NLP 应用更经济、更可持续。

> 来源：KDnuggets, "5 Cutting-Edge Natural Language Processing Trends Shaping 2026", https://www.kdnuggets.com/5-cutting-edge-natural-language-processing-trends-shaping-2026。

### 2. 自主语言 Agent（Autonomous Language Agents）

2025-2026 年，自主语言 Agent 从研究项目走向业务应用。这些系统能**独立规划、执行多步任务**，而不是简单回答单个问题：

例如，一个 Agent 处理"分析上季度销售数据并起草报告"的请求时，会自动完成：
1. 检索销售数据
2. 运行计算分析
3. 生成图表
4. 生成书面摘要报告

| 框架 | 特点 |
|------|------|
| **AutoGen**（Microsoft） | 多 Agent 对话、代码生成 |
| **LangGraph** | 有状态图工作流、条件路由 |
| **CAMEL-AI** | 角色扮演式多 Agent 协作 |

多 Agent 系统——多个专业 Agent 像人类团队一样协作——是这一方向的前沿热点。

> 来源：KDnuggets, "5 Cutting-Edge NLP Trends Shaping 2026", https://www.kdnuggets.com/5-cutting-edge-natural-language-processing-trends-shaping-2026。

### 3. 世界模型（World Models）

世界模型是 2026 年 NLP 领域最令人兴奋的新方向之一。它不只是预测下一个词，而是**在内部构建对环境的模拟**：

- **感知**：理解系统读取到的内容
- **记忆**：记住已经发生的状态变化
- **预测**：推演未来可能的状态

| 研究 | 来源 | 意义 |
|------|------|------|
| DreamerV3 | DeepMind | 强化学习中的世界模型先驱 |
| Genie 2 | DeepMind | 从图片生成可交互世界 |
| SocioVerse | 学术研究 | 社会交互模拟 |

世界模型使 AI 能够维持一致的"心智模型"——理解人物、物品和事件在整个交互过程中的关系，而不仅仅是串接句子。

### 4. 神经符号 NLP 与知识图谱

NLP 系统不再只把文本当作非结构化数据处理，知识图谱（Knowledge Graph）将文本转化为**互联、可查询的知识网络**：

| 工具 | 定位 |
|------|------|
| Neo4j | 最流行的图数据库，支持 Cypher 查询 |
| TigerGraph | 高性能图分析，适合大规模图数据 |
| OpenIE | 从文本自动抽取三元组（主体-关系-客体） |

知识图谱为 NLP 系统提供了三个传统方法缺乏的能力：
- **上下文**：消歧义（"苹果"是水果还是公司）
- **可追溯**：每个事实都有来源，可验证
- **一致性**：违反物理或逻辑规则的结果可以被拦截

> 来源：KDnuggets, "5 Cutting-Edge NLP Trends Shaping 2026", https://www.kdnuggets.com/5-cutting-edge-natural-language-processing-trends-shaping-2026。

### 5. 端侧 NLP（On-Device NLP / TinyML）

越来越多的 NLP 任务从云端迁移到设备端。模型通过量化（Quantization）、剪枝（Pruning）和蒸馏（Distillation）等技术压缩后，直接在手机、手表和 IoT 设备上运行：

| 框架 | 提供商 | 特点 |
|------|--------|------|
| LiteRT | Google | 移动端推理，前身为 TensorFlow Lite |
| Neural Processing SDK | Qualcomm | 骁龙芯片上的 AI 加速 |
| Edge Impulse | 第三方 | 低代码端侧 ML 平台 |

**优势**：更快的响应速度（无需网络传输）、更强的隐私保护、离线可用。

### NLP 在行业中的实际应用（2026）

| 行业 | 应用场景 | 核心技术 |
|------|----------|----------|
| 医疗 | 病历分析、药物相互作用检查 | NER、关系抽取、知识图谱 |
| 金融 | 财报分析、情感分析、合规审查 | 文本分类、摘要、实体识别 |
| 法律 | 合同审查、案例检索、合规检查 | 长文档理解、语义搜索 |
| 客服 | 多语言自动回复、工单分类 | 意图识别、翻译、对话管理 |
| 教育 | 自动评分、个性化辅导 | 文本评估、问答、解释生成 |

> 综合参考：
> - KDnuggets, "5 Cutting-Edge NLP Trends Shaping 2026", https://www.kdnuggets.com/5-cutting-edge-natural-language-processing-trends-shaping-2026
> - GraffersID, "Advancements in NLP in 2026: Tools, Trends, and AI Applications", https://graffersid.com/advancements-in-natural-language-processing-nlp/

## 延伸阅读

- [大语言模型基础](../大语言模型基础/)
- [Embedding 与向量数据库](/进阶学习/Embedding与向量数据库/)
- [RAG 检索增强](/进阶学习/RAG检索增强/)
- [Agent 智能体](/进阶学习/Agent智能体/)
- [提示词工程](/进阶学习/提示词工程/)
- [Python 与数据处理基础](../Python与数据处理基础/)

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-13 00:08:05*
