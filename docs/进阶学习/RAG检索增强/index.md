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

## 🔗 参考资料

- [RAG Tutorial: Architecture, Implementation, and Production Guide - Glukhov](https://www.glukhov.org/rag)
- [RAG Architecture Explained: 2026 Guide - ORQ.AI](https://orq.ai/blog/retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks)
- [RAG and Generative AI - Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Retrieval Augmented Generation: A Complete Guide - WEKA](https://www.weka.io/learn/guide/ai-ml/retrieval-augmented-generation)
- [What is RAG? A Practical Guide - K2View](https://www.k2view.com/what-is-retrieval-augmented-generation)
