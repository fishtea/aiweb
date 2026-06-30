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

---

## 6. 2025年 RAG 技术演进全景

### 6.1 从朴素 RAG 到高级 RAG

2025年，RAG 技术已经从简单的"向量搜索+LLM生成"演变为多层级、自适应的智能系统。

| 阶段 | 特点 | 关键技术 |
|------|------|----------|
| **Naive RAG** | 线性流程，一次检索+一次生成 | 固定分块、余弦相似度搜索 |
| **Advanced RAG** | 各阶段独立优化 | 语义分块、查询重写、混合搜索、重排序 |
| **Modular RAG** | 模块可替换组合 | 独立的查询处理、多源检索、过滤排序、上下文增强 |
| **Agentic RAG** | LLM 主导检索过程 | 查询分解、多步规划、自我修正、多智能体协作 |
| **GraphRAG** | 图结构知识表示 | 知识图谱构建、图遍历检索、多跳推理 |

**来源：** [检索增强生成（RAG）当前技术路线与前沿进展](https://yonglun.me/rag101)

### 6.2 三大核心优化方向

#### 检索前增强

- **语义分块（Semantic Chunking）**：按自然语义边界（句子、段落、主题）分割，替代固定 token 分块
- **层级分块（Hierarchical Chunking）**：嵌套层级（章节→段落→句子），支持不同粒度查询
- **元数据增强**：为分块附加时间戳、来源类型、实体标签，支持按条件过滤和优先级排序
- **GraphRAG**：将知识库构建为图结构，通过图遍历发现分散相关片段，支持复杂多跳推理

#### 检索过程优化

- **混合检索（Hybrid Search）**：结合 BM25（关键词精确匹配）和稠密向量检索（语义相似度），通过动态 Alpha 调优（DAT）自动分配权重
- **查询扩展（LLM-QE）**：利用 LLM 生成"文档式"扩展内容，通过基于排序和答案的奖励进行 DPO 微调，显著减少幻觉
- **查询重写/分解（LevelRAG）**：高层搜索器将复杂查询拆分为多个原子子查询，分别分配给不同的低层搜索器处理
- **缓存增强生成（CAG）**：对固定且规模适中的知识库，预先加载所有资源到 LLM 长上下文中并缓存 KV 键值对，推理时绕过实时检索，消除检索延迟

#### 检索后精炼

- **高级重排序（Reranking）**：使用交叉编码器（Cross-Encoder）精细化打分，替代简单的向量相似度排序
- **METEORA（理由驱动选择）**：偏好微调 LLM 生成选择理由，通过拐点检测自适应确定 Top-K，并使用验证器检查证据一致性
- **上下文压缩（MacRAG/PISCO）**：通过硬压缩（摘要）、软压缩（记忆嵌入向量）减少噪音，PISCO 最高实现 16 倍压缩且准确率损失仅 0-3%

**来源：**  
- [检索增强生成（RAG）当前技术路线与前沿进展](https://yonglun.me/rag101)  
- [RAG 2025 最新综述深度解读：架构](https://zhuanlan.zhihu.com/p/1981157339932402521)

### 6.3 自我修正与反思式 RAG

- **CRAG**：轻量级评估器评估检索置信度 → 高置信度直接使用，低置信度触发网络搜索补充，不确定则额外修正
- **AlignRAG**：引入批判语言模型（CLM），通过对比学习识别推理与证据之间的不对齐并生成结构化批判，可即插即用
- **Self-RAG**：训练 LLM 在生成时按需检索，使用反思令牌评估检索必要性、相关性和证据支持度，通过树状解码选择最佳生成路径

### 6.4 多智能体 RAG（MA-RAG）

多智能体系统将 RAG 流程分解为多个专业角色协作：

| 角色 | 职责 |
|------|------|
| **规划器（Planner）** | 分析用户意图，将复杂查询拆解为子任务 |
| **步骤定义器** | 为每个子任务选择合适的检索策略和参数 |
| **提取器（Extractor）** | 从检索结果中提取关键证据 |
| **QA 智能体** | 综合所有证据生成最终答案 |

这种架构大幅提高了对模糊、复杂查询的鲁棒性和可解释性。

---

## 7. 2025年 GitHub 十大 RAG 框架

根据社区活跃度和企业应用情况，2025年最值得关注的 RAG 框架排名如下：

| 框架 | ⭐ Star | 定位 | 核心优势 |
|------|---------|------|----------|
| **RAGFlow** | 53.9k | 低代码开源 RAG 引擎 | 可视化拖拽、行业模板、Docker 部署资源降低 30% |
| **STORM** (Stanford) | 24.3k | 学术前沿知识策展 | 分层检索、语义漂移校正、检索路径可视化 |
| **Haystack** (deepset) | 20.8k | 企业级端到端 AI 编排 | 模块化架构、TB 级分布式、ES+FAISS 混合 |
| **LLM-App** (Pathway) | 24.3k | 生产级云原生 RAG 模板 | Kafka 流实时更新、Docker 一键部署 |
| **txtai** | 11k | 语义搜索+RAG 融合平台 | 嵌入式向量数据库、多语言支持、毫秒响应 |
| **R2R** (SciPhi-AI) | 6.9k | 检索优化增强框架 | 迭代式检索、性能分析工具（P/R 曲线） |
| **Cognita** (truefoundry) | 4.1k | MLOps 导向模块化平台 | 版本管理/监控、RBAC 合规、多框架兼容 |
| **FlashRAG** (RUC-NLPIR) | 2.3k | 高性能效率标杆 | ANNS 算法+量化压缩、检索速度提升 5-8 倍 |
| **Neurite** | 1.7k | 轻量级敏捷开发 | 极简 API、自然语言配置、自动缓存 |
| **Canopy** (Pinecone) | 1k | 向量数据库深度整合 | Pinecone 原生集成、亿级向量秒级查询 |

**框架选型建议：**
- **简单场景** → RAGFlow、Neurite（低代码）
- **复杂场景**（多模态/实时/大规模）→ Haystack、LLM-App（企业级）
- **垂直领域定制** → txtai、Cognita（自定义 embedding/pipeline）
- **学术研究** → STORM、R2R（前沿算法）
- **极致性能** → FlashRAG（高吞吐量）

**来源：** [2025年GitHub上十大RAG框架深度解析 - 53AI](https://www.53ai.com/news/RAG/2025053068710.html)

---

## 8. 评估体系

### 8.1 关键评估指标

| 层级 | 测量指标 | 说明 |
|------|----------|------|
| 检索 | recall@k, precision@k, MRR/NDCG | 判断是否获取正确证据 |
| 重排序 | 相对 baseline 的 precision@k 增量 | 验证重排序 ROI |
| 生成 | 忠实度/依地性、引用准确性 | 减少幻觉 |
| 系统 | 延迟 p50/p95、每次查询成本、缓存命中率 | 保持生产可用性 |

### 8.2 RAGAS 框架

RAGAS 是 2025 年主流的无参考评估框架，核心指标包括：
- **忠实度（Faithfulness）**：生成答案是否严格基于检索上下文
- **答案相关性（Answer Relevance）**：答案是否直接回答了用户问题
- **上下文相关性（Context Relevance）**：检索到的文档是否与查询相关

**来源：** [检索增强生成（RAG）当前技术路线与前沿进展](https://yonglun.me/rag101)

---

## 🔗 参考资料

- [RAG Tutorial: Architecture, Implementation, and Production Guide - Glukhov](https://www.glukhov.org/rag)
- [RAG Architecture Explained: 2026 Guide - ORQ.AI](https://orq.ai/blog/retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks)
- [RAG and Generative AI - Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [检索增强生成（RAG）当前技术路线与前沿进展 - yonglun.me](https://yonglun.me/rag101)
- [2025年GitHub上十大RAG框架深度解析 - 53AI](https://www.53ai.com/news/RAG/2025053068710.html)
- [RAG 2025 最新综述深度解读 - 知乎专栏](https://zhuanlan.zhihu.com/p/1981157339932402521)
- [什么是 RAG 检索增强生成 - Elastic](https://www.elastic.co/cn/what-is/retrieval-augmented-generation)
