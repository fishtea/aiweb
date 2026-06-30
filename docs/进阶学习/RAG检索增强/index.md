# RAG 检索增强生成

> 检索增强生成（Retrieval-Augmented Generation, RAG）是一种系统设计模式，将**检索**（搜索/查找相关文档）与**生成**（LLM 基于检索上下文生成答案）相结合。

---

## 1. RAG 是什么？

**来源：** [RAG Tutorial: Architecture, Implementation, and Production Guide - Glukhov](https://www.glukhov.org/rag)

RAG 是一种**无需重新训练模型**即可为 LLM 注入外部知识的方法。与微调不同，RAG：

- **不需要重新训练模型**
- **通过更新文档索引即可刷新知识**
- **提供引用来源，保证可审计性**
- **减少幻觉，提高事实准确性**

> *"If you only improve one thing in a working RAG system: add reranking and an evaluation harness."*

---

## 2. RAG 架构

### 2.1 基础 RAG 流程

```
用户查询 → 嵌入查询 → 向量搜索 → 检索文档 → 构建提示词 → LLM 生成 → 输出
```

### 2.2 生产级 RAG 蓝图

**来源：** [RAG and Generative AI - Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

**数据摄入管道（离线/持续）：**
1. 加载文档
2. 文本分块（Chunking）
3. 生成向量嵌入
4. 存入向量数据库 + 元数据索引

**查询管道（在线）：**
1. 查询嵌入
2. 向量搜索（或混合搜索）
3. 重排序（Reranking）
4. 构建提示词（含检索上下文）
5. LLM 生成响应
6. 评估（忠实度、引用准确性）

### 2.3 现代 RAG 架构演进

| 阶段 | 描述 |
|------|------|
| **Naive RAG** | 简单向量搜索 + LLM 生成 |
| **Advanced RAG** | 查询重写、混合搜索、重排序、缓存 |
| **Modular RAG** | 可替换的检索/生成模块组合 |
| **Agentic RAG** | LLM 辅助查询规划、多源访问、结构化响应 |
| **GraphRAG** | 图遍历 + 向量相似度搜索结合 |

---

## 3. 核心组件详解

### 3.1 文本分块（Chunking）

检索质量很大程度上取决于分块策略。

**来源：** [RAG Tutorial - Chunking Strategies](https://www.glukhov.org/rag/retrieval/chunking-strategies-in-rag/)

| 策略 | 方法 | 适用场景 |
|------|------|----------|
| 固定大小分块 | 按固定 token 数切分 | 简单、快速、通用 |
| 语义分块 | 按句子/段落边界切分 | 需要语义完整性 |
| 层级分块 | 文档 → 章节 → 块 | 需要多粒度检索 |

> *"Poor chunking is one of the most common causes of underperforming RAG systems."*

### 3.2 向量搜索

- **基础：** 余弦相似度 / 点积相似度
- **高级：** 混合搜索（BM25 + 向量）、层级检索、查询重写

### 3.3 重排序（Reranking）

> 重排序是 RAG 实现中**最大**的质量改进因素。

重排序提升 `precision@k`，减少噪声，提升端到端答案质量。在生产环境中，重排序往往比切换更大的模型更有效。

### 3.4 评估框架

| 层级 | 测量指标 | 重要性 |
|------|----------|--------|
| 数据摄入 | 分块覆盖率、去重率、嵌入版本 | 防止静默漂移 |
| 检索 | recall@k、precision@k、MRR/NDCG | 判断是否获取正确证据 |
| 重排序 | 相对 baseline 的 precision@k 增量 | 验证重排序 ROI |
| 生成 | 忠实度/依地性、引用准确性 | 减少幻觉 |
| 系统 | 延迟 p50/p95、每次查询成本、缓存命中率 | 保持生产可用性 |

> **最小评估套件：** 50-200 个查询足以检测主要回归问题。

---

## 4. RAG vs 微调

| 维度 | RAG | 微调 |
|------|-----|------|
| 知识更新 | 刷新文档索引即可 | 需要重新训练 |
| 可审计性 | 可提供引用来源 | 黑盒输出 |
| 幻觉控制 | 依赖检索质量 | 依赖训练数据质量 |
| 计算成本 | 低（仅推理） | 高（需要训练） |
| 长尾知识 | 强（可检索任何文档） | 弱（可能遗忘） |
| 延迟 | 较高（含检索步骤） | 较低（直接生成） |

---

## 5. 主流工具与框架

| 工具 | 用途 |
|------|------|
| **LangChain** | RAG 流程编排 |
| **LlamaIndex** | 数据索引与检索 |
| **Chroma / Weaviate / Pinecone** | 向量数据库 |
| **FAISS** | 高效向量相似度搜索 |
| **Cohere Rerank / BGE Reranker** | 重排序模型 |
| **RAGAS** | RAG 评估框架 |

---

## 6. 进阶 RAG 模式详解

基础 RAG（检索一次 → 拼接 → 生成）在面对复杂问题、多跳推理和噪声文档时容易失效。以下模式通过增加"判断"和"纠错"环节提升鲁棒性。

### 6.1 查询改写与扩展

| 技术 | 思路 | 适用场景 |
|------|------|----------|
| 查询分解（Query Decomposition） | 把复杂问题拆成多个子问题分别检索 | 多跳问答、对比类问题 |
| HyDE（假设性文档嵌入） | 先让 LLM 生成"假设答案"，用答案去检索 | 查询与文档表述差异大 |
| 查询重写（Query Rewriting） | 把口语化问题改写为检索友好的关键词 | 用户输入模糊 |
| 多查询生成（Multi-Query） | 生成多个变体查询并行检索后合并 | 提升召回率 |

### 6.2 检索后增强

- **上下文压缩（Contextual Compression）**：召回长文档后用小模型或 LLM 抽取相关片段，丢弃噪声，降低 token 成本。
- **重排序（Reranking）**：召回 top-50 后用交叉编码器精排到 top-5，通常比换更大的 Embedding 收益更高。
- **去重与多样性**：按来源、语义簇去重，避免上下文重复占满窗口。

### 6.3 自适应与自纠错 RAG

| 模式 | 机制 |
|------|------|
| **Self-RAG** | 模型在每步生成"反思 token"，自主决定是否检索、检索结果是否相关、回答是否有支撑 |
| **Corrective RAG (CRAG)** | 用轻量评估器给检索文档打分；低质量时触发网络搜索兜底，高质量时精炼后使用 |
| **Adaptive RAG** | 按问题难度路由：简单问题直接回答，中等问题单次检索，复杂问题多步检索 |

> 这些模式把"无脑检索"变成"带判断的检索"，代价是更多 LLM 调用和更高延迟，适合对准确率敏感的场景。

### 6.4 GraphRAG

传统向量检索难以回答"全局性"问题（如"这份文档的主要主题有哪些"）。GraphRAG 在索引阶段构建实体-关系知识图谱，查询时通过图遍历聚合跨文档信息，再结合向量检索补充细节。适合法律、科研、企业知识库等需要跨文档推理的场景，代价是索引构建成本高。

### 6.5 生产优化清单

- 缓存高频查询的嵌入和检索结果，FAQ 类场景命中率可达 60%+。
- 父子分块（Parent-Child Chunking）：用小块检索，返回所属大块保证上下文完整。
- 记录每次检索的召回片段、重排分数和最终引用，便于回归评估。
- 设置相关性阈值，低于阈值时明确回答"未找到相关资料"，而非硬编答案。

---

## 🔗 参考资料

- [RAG Tutorial: Architecture, Implementation, and Production Guide - Glukhov](https://www.glukhov.org/rag)
- [RAG Architecture Explained: 2026 Guide - ORQ.AI](https://orq.ai/blog/retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks)
- [RAG and Generative AI - Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Retrieval Augmented Generation: A Complete Guide - WEKA](https://www.weka.io/learn/guide/ai-ml/retrieval-augmented-generation)
- [What is RAG? A Practical Guide - K2View](https://www.k2view.com/what-is-retrieval-augmented-generation)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:37:40*
