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

## 9. 2026年RAG技术前沿：20种进阶类型与实战蓝图

2026 年，RAG 技术已从简单的“向量搜索 + LLM 生成”演进为面向生产系统的知识访问层。更重要的变化不是术语变多，而是工程目标变清楚：让系统在有限延迟、有限上下文、权限约束和可审计要求下，稳定取回正确证据。

### 9.1 本轮学习整理：生产 RAG 的核心矛盾

基于 Microsoft Azure AI Search 的 RAG 文档和近期生产 RAG 评估论文，本轮更新将重点从“追逐更多 RAG 类型”调整为“如何让 RAG 在真实系统中可靠运行”。

| 生产矛盾 | 具体表现 | 应对方式 |
|----------|----------|----------|
| 查询很口语，资料很正式 | 用户问“远程员工休假怎么算”，制度写的是“telecommute / paid time off” | 查询改写、混合搜索、语义排序 |
| 资料来源分散 | SharePoint、数据库、网页、对象存储各自有权限和格式 | 统一知识源接口，按权限检索 |
| 上下文窗口有限 | 找到 50 段材料，但只能给模型少量片段 | 分块、重排序、阈值过滤、摘要压缩 |
| 响应必须够快 | 多轮搜索、重排和生成会拉高延迟 | 并行子查询、缓存、固定超时、降级路径 |
| 权限和审计不可省 | Agent 不能越权读取财务、人事或客户数据 | 文档级权限裁剪、查询日志、引用追踪 |

### 9.2 Agentic Retrieval：不是“更聪明的搜索”，而是查询规划

Microsoft 将现代 RAG 分成两条路线：

| 路线 | 适合场景 | 特点 |
|------|----------|------|
| Classic RAG | 查询简单、追求速度、已有检索编排代码 | 单次查询，应用侧负责把结果交给 LLM |
| Agentic Retrieval | 面向聊天/Agent、问题复杂、需要更高相关性和引用 | LLM 先分析问题，生成多个子查询，并行检索，返回结构化 grounding 数据 |

Agentic Retrieval 的价值在于把“用户问题”变成“可执行检索计划”。它会利用对话历史理解上下文，把复杂问题拆成更聚焦的子查询，并返回带引用、执行信息和结构化证据的数据。它适合企业知识助手、客服知识库、合规问答和需要跨来源查询的 Agent。

### 9.3 重新看待 Multi-Query 与 RAG-Fusion

多查询和 RAG-Fusion 常被当成提升召回率的默认方案，但生产环境不能只看 recall。2026 年一篇面向企业知识库的 RAG-Fusion 部署研究指出：多查询确实可能提升原始召回，但在固定重排序预算、固定 top-k 和上下文窗口限制下，收益可能被重排序和截断抵消，甚至带来额外延迟。

因此，实践上应把 Multi-Query 当成可测试策略，而不是默认开关：

| 是否启用 | 判断依据 |
|----------|----------|
| 启用 | 用户问题经常模糊、同义词多、原始召回明显不足 |
| 谨慎启用 | 已经有强重排序器、上下文预算很紧、延迟要求严格 |
| 不启用 | 单查询 + 混合检索已经能稳定命中正确证据 |

### 9.4 新的生产实施顺序

不要一开始就上最复杂的 Agentic RAG。推荐顺序：

1. **建立黄金问题集**：先收集 50-200 个真实问题，标注正确证据和期望答案。
2. **先做 Classic RAG baseline**：混合搜索 + 分块 + top-k + 引用输出。
3. **加入重排序**：比较 precision@k、答案忠实度、延迟和成本。
4. **再评估查询规划**：只有当复杂问题、多跳问题明显失败时，才引入 Agentic Retrieval 或 Multi-Query。
5. **补权限与审计**：所有检索都要记录 query、命中文档、分数、引用和用户权限。
6. **上线后回流失败样本**：把“没找到、答错、引用错、越权风险”变成下一轮评估集。

### 9.5 RAG 系统的拒答能力

RAG 不是“检索到了就必须回答”。高质量系统需要判断证据是否充分：

| 证据状态 | 应答策略 |
|----------|----------|
| 多个高相关证据一致 | 正常回答，并给出引用 |
| 证据相关但不完整 | 回答已确认部分，并说明缺口 |
| 证据互相冲突 | 列出冲突点，不强行给单一结论 |
| 低相关或无证据 | 明确拒答或请求补充信息 |

这比“让模型根据感觉回答”更重要。很多 RAG 幻觉不是模型不知道，而是系统没有要求它在证据不足时停止。

### 9.6 本节参考来源

- Microsoft Learn：Retrieval-augmented generation in Azure AI Search，更新于 2026-06-08。
- arXiv 2026：Scaling Retrieval Augmented Generation with RAG Fusion，讨论生产约束下 Multi-Query / RRF 的收益边界。
- DeepLearning.AI RAG 课程说明：强调从检索器、向量数据库、提示、评估和监控一起设计生产 RAG。

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-04 13:05:43*
