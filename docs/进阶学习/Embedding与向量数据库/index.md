# Embedding 与向量数据库

Embedding 是把文本、图片、代码等对象映射为向量表示的技术，向量数据库负责存储、检索和过滤这些表示。它们是 RAG、语义搜索、推荐、去重、聚类和记忆系统的基础设施。

## 适合读者

- 已经理解大语言模型基础，希望构建知识库问答、语义搜索或相似内容召回。
- 需要在 Milvus、Qdrant、Weaviate、pgvector、Chroma、Faiss 等方案之间做工程选型。
- 希望知道为什么“向量检索效果不好”通常不是单一模型问题。

## 核心概念

| 概念 | 说明 |
|------|------|
| Embedding 模型 | 将输入编码为稠密向量，语义相近的内容在向量空间中距离更近 |
| 向量维度 | 向量长度，维度越高不一定越好，还要看模型质量、索引和成本 |
| 相似度度量 | 常见有 cosine、dot product、L2 distance，需要与模型训练方式匹配 |
| ANN 索引 | 近似最近邻检索，用速度换取可控的召回误差 |
| 元数据过滤 | 通过时间、权限、类型、租户等结构化字段缩小候选范围 |
| 混合检索 | 将关键词检索、向量检索、稀疏向量和重排序组合，提高稳定性 |

## 典型流程

1. 清洗文档，去掉目录噪声、页眉页脚、重复段落和无意义字符。
2. 按语义边界切分 Chunk，保留标题、层级、来源、时间、权限等元数据。
3. 使用 Embedding 模型生成向量，写入向量库或支持向量索引的关系数据库。
4. 查询时先做问题改写或意图识别，再执行向量检索、关键词检索或混合检索。
5. 对召回结果进行重排序、去重、压缩和上下文拼接。
6. 将最终上下文交给 LLM，并在答案中返回引用来源。

## 选型建议

| 场景 | 推荐方向 |
|------|----------|
| 小型原型 | Chroma、Faiss、本地文件索引，优先验证数据清洗和切分策略 |
| 已有 PostgreSQL | pgvector，适合中小规模、强事务和业务数据同库管理 |
| 高并发服务 | Milvus、Qdrant、Weaviate 等独立向量数据库 |
| 权限复杂 | 选择元数据过滤、租户隔离和删除更新能力成熟的方案 |
| 检索质量优先 | 混合检索 + reranker，单纯换更大的 Embedding 模型通常不够 |

## 常见误区

- 只调 Chunk 大小，不检查原始文档质量。
- 只看 top-k，不分析召回结果是否覆盖答案证据。
- 把向量数据库当成长期记忆，却没有过期、更新和删除策略。
- 忽略权限过滤，导致 RAG 系统泄露用户无权访问的内容。
- 不记录检索日志，后续无法定位是召回、重排还是生成阶段出错。

## 实践检查清单

- 每个 Chunk 是否保留了可追溯来源。
- 查询和文档是否使用同一个或兼容的 Embedding 模型。
- 相似度阈值、top-k、重排序数量是否有评估集支撑。
- 是否同时评估“召回准确率”和“最终回答质量”。
- 是否设计了增量更新、删除、重建索引和版本回滚流程。

## 延伸学习

### 2026年最新进展

2026年，Embedding模型和向量数据库领域发生了重大变化：**多模态Embedding**成为主流、**跨语言检索**能力大幅提升、向量数据库的选型格局趋于稳定。

> **核心趋势：** 单语言英文检索已不再够用——生产级RAG系统需要同时支持跨模态、跨语言、长文档精准检索和维度压缩。

#### 2026年Embedding模型测评：10款模型对比

**来源：** [Milvus Blog - Best Embedding Model for RAG 2026](https://milvus.io/blog/choose-embedding-model-rag-2026.md)

Milvus团队在2026年发布了**CCKM基准测试**，从四个生产维度评估Embedding模型，弥补了MTEB排行榜的不足：

| 测评维度 | 测试内容 | 为什么重要 |
|---------|---------|-----------|
| **跨模态检索** | 文本描述匹配图片（含强干扰项） | 多模态RAG需要统一的文本/图像向量空间 |
| **跨语言检索** | 中文查询→英文文档（反之亦然） | 企业知识库通常是多语言的 |
| **关键信息检索** | 在4K-32K字符文档中定位特定事实 | RAG系统处理合同、论文等长文档 |
| **维度压缩** | 截断至256维后的质量损失 | 节省向量数据库存储成本 |

**TOP模型测评结果：**

**跨模态检索（文本→图片）TOP3：**
1. **Qwen3-VL-2B**（阿里开源，2B参数）— R@1=0.945，**击败所有闭源API**
2. Gemini Embedding 2（Google）— R@1=0.928
3. Voyage Multimodal 3.5（MongoDB）— R@1=0.900

> 开源Qwen3-VL-2B胜出的关键在于**模态间隙（modality gap）极小**（0.25 vs Gemini的0.73）。

**跨语言检索（中英）TOP3：**
1. **Gemini Embedding 2** — 综合R@1=0.997，困难成语组（如"画蛇添足→gilding the lily"）R@1=**1.000**
2. Qwen3-VL-2B — R@1=0.988
3. Jina Embeddings v4 — R@1=0.985
> 轻量级英文专用模型（nomic-embed-text等）在跨语言任务上几乎无效（R@1≈0.12）。

**关键信息检索（Needle-in-a-Haystack）TOP：**
- **Gemini Embedding 2** — 32K字符文档中**无退化**，R@1=1.000
- OpenAI 3-large / Jina v4 / Cohere v4 — 在16K内无退化，超出后未测试

**综合推荐：**
| 需求 | 推荐模型 | 说明 |
|------|---------|------|
| 全能型 | **Gemini Embedding 2** | 跨模态+跨语言+长文档均第一 |
| 开源跨模态 | **Qwen3-VL-2B** | 2B参数击败闭源，模态间隙最优 |
| 维度压缩 | **Voyage Multimodal 3.5 / Jina v4** | 截断到256维损失最小 |
| 入门快速 | **OpenAI text-embedding-3-small** | 便宜、易用、英文检索足够 |
| 大规模自托管 | **BGE-M3**（开源，568M参数） | 支持100+语言，混合检索（稠密+稀疏） |

#### 2026年向量数据库选型指南

**来源：** [Top 15 Vector Databases in 2026 - Medium](https://medium.com/@pratik-rupareliya/top-15-vector-databases-in-2026-a-production-decision-guide-from-100-enterprise-deployments-dd58a04f51a5)

经过100+企业部署实践验证，2026年向量数据库选型趋于结构化：

| 场景 | 推荐方案 | 核心理由 |
|------|---------|---------|
| 快速原型/PoC | **Chroma** | 基于SQLite，零配置，本地文件即数据库 |
| 已有PostgreSQL | **pgvector** | 同库管理，无需引入新数据库 |
| 中小规模生产（<10M向量） | **Weaviate / Qdrant** | 混合搜索、元数据过滤、Rust性能 |
| 大规模高吞吐（亿级+） | **Milvus / Pinecone** | 分布式、高可用、企业级SLA |
| MongoDB生态 | **MongoDB Atlas Vector Search** | 文档+向量统一查询 |
| 全文搜索需求 | **Elasticsearch** | 已有的搜索基础设施，新增向量能力 |

**关键建议：**
- 不要用向量数据库替代关系数据库——两者承载不同职责
- **混合检索（稠密向量 + BM25稀疏检索 + 重排序）**是2026年的生产标配
- 选型核心指标：p99延迟、并发QPS、元数据过滤能力、增量更新效率

#### RAG系统中的常见Embedding误区（2026版）

1. **只看MTEB不看CCKM** — MTEB仅测试单语言文本检索，忽略跨模态和跨语言
2. **模型截断维度后不重测** — 同一模型在不同维度下的排序可能完全反转
3. **不评估重排序的ROI** — 在top-50中已有正确答案但top-5中没有时，**重排序的收益通常大于换Embedding模型**
4. **忽略查询-文档不对称** — 短查询 vs 长文档，不同模型对此差异敏感
5. **自托管 vs API的选择不是性能问题** — 取决于查询量稳定性、运维能力和隐私要求

---

## 2026 向量数据库选型与实践

2026年，向量数据库的选型格局趋于稳定：**Serverless 架构**成为主流部署模式、**混合检索**（向量+关键词+重排序）成为生产标配、Pinecone 和 Redis 分别以独立托管和集成方案占据了不同生态位。

> 核心趋势：向量数据库的价值不再只是"存向量"，而是如何把存储、检索、过滤、缓存、记忆整合到一个统一的数据层中。

### 向量数据库 vs 向量索引（FAISS 等）

| 维度 | 独立向量索引（FAISS） | 向量数据库 |
|------|---------------------|-----------|
| 增删改 | 需全量重建 | CRUD 原生支持 |
| 元数据过滤 | 无 | 预/后过滤均支持 |
| 高可用 | 手动实现（K8s 等） | 内置分片+复制 |
| 实时更新 | 需全量重建索引 | 支持增量更新 |
| 数据安全 | 无 | ACL、命名空间隔离 |

### 2026 年 Serverless 向量数据库架构

新一代 Serverless 向量数据库（如 Pinecone Serverless）解决了三个关键问题：

1. **存算分离**：索引存储与计算解耦，不查询时不消耗计算资源
2. **几何分区**：将向量空间划分为几何子区域，查询只路由到相关分区，大幅降低计算量
3. **新鲜层（Freshness Layer）**：新增向量先写入临时"缓存"区即可查询，后台建索引器异步构建正式分区索引

> 来源参考：[What is a Vector Database - Pinecone](https://www.pinecone.io/learn/vector-database/)（2026年更新版）

### 混合检索实践建议

1. **不要只依赖向量搜索**：关键词检索（BM25）可捕捉精确匹配场景，与向量检索互为补充
2. **重排序的 ROI 高于换模型**：在 top-50 中已有正确答案但 top-5 中没有时，加一个 cross-encoder reranker 通常比换大 Embedding 模型收益更大
3. **语义缓存降低推理成本**：Redis LangCache 等方案对重复查询可降低最高 73% 的 API 成本，延迟从 ~1.67s 降至 ~0.052s

> 来源参考：[LLM Router Architecture: Best Practices for 2026 - Redis Blog](https://redis.io/en/blog/llm-router-architecture-best-practices/)（2026年7月1日发布）

## Embedding 模型选型与部署实践指南

> 来源：[Zilliz - 如何为RAG应用选择最佳Embedding模型](https://zilliz.com.cn/blog/How-to-choose-the-best-embedding-model-for-RAG)（2026 年更新），[Jina AI - jina-embeddings-v4](https://jina.ai/models/jina-embeddings-v4/)（2026），[A Complete Developer Guide to Vector Embeddings - Neptune.ai](https://www.neptune.ai/blog/vector-embeddings)

### 从 MTEB 到 CCKM：评估维度的演变

传统上，Embedding 模型的选型主要依赖 **MTEB 排行榜**，但 2026 年的共识是：MTEB 仅测试单语言文本检索，不足以反映生产环境的真实需求。

| 评估框架 | 覆盖维度 | 适用场景 |
|---------|---------|---------|
| **MTEB** | 单语言文本检索、分类、聚类 | 通用基准对比 |
| **CCKM**（Milvus） | 跨模态、跨语言、长文档、维度压缩 | 生产级 RAG 选型 |
| **自定义评估集** | 业务数据上的精准召回率 | 业务验证 |

**核心建议**：MTEB 帮助初筛，CCKM 帮助跨模态/跨语言决策，但最终选型必须在自己业务数据上验证。

### Embedding 模型选型的五项关键参数

| 参数 | 说明 | 选型建议 |
|------|------|---------|
| **模型规模（参数量）** | 影响检索性能和延迟 | 先从小模型（如 BGE-small）快速搭建原型，再切换到更大模型 |
| **向量维度** | 影响存储成本和检索精度 | 256-768 维通常足够；高维（>1024）不一定更好，需评估维度压缩后的质量 |
| **最大 Token 数** | 单次可处理的文本长度 | 常规 RAG 分块 512 tokens 足够；长文档场景需 8192+ |
| **延迟（P99）** | 在线服务的核心指标 | API 模型延迟波动大，自托管模型延迟可预测但需要 GPU 资源 |
| **成本（Token/文档）** | 规模化部署的关键 | OpenAI text-embedding-3-small 成本最低；自托管 BGE-M3 免 API 费用但需 GPU |

### 自托管 vs API：选型决策树

```
需要 Embedding 服务
├─ 查询量 < 10万/天 → API 模型（OpenAI / Gemini / Cohere）
├─ 查询量 10万-100万/天
│  ├─ 有 GPU 资源 → 自托管 BGE-M3 / Jina v4
│  └─ 无 GPU 资源 → API 模型 + 语义缓存
└─ 查询量 > 100万/天 → 自托管 + 本地索引（FAISS / Milvus）
```

**关键实践**：
- API 模型适合快速验证，但跨语言场景优先选 Gemini Embedding 2（中英 R@1=0.997）
- 自托管模型适合高频查询和隐私敏感场景，推荐 BGE-M3（100+语言，568M 参数，开源）
- 语义缓存（Redis LangCache）可将重复查询的 API 成本降低最高 73%

### 使用 PyMilvus 快速集成 Embedding 模型

Milvus 2.4+ 提供了与主流 Embedding 模型的原生集成，不需要手动拼接 API 调用：

```python
from pymilvus import model

# 创建 Embedding 函数（自动管理 API Key）
openai_ef = model.dense.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small",
    api_key="sk-xxx"
)

# 生成文档向量
docs = ["文档1内容...", "文档2内容..."]
docs_embeddings = openai_ef(docs)

# 写入 Milvus 集合
collection.insert([docs_embeddings, doc_ids, metadata])
```

> 参考：[PyMilvus Integration with Embedding Models - Milvus Blog](https://milvus.io/blog/introducing-pymilvus-integrations-with-embedding-models.md)（2026 年更新）

### Embedding 模型在 RAG 中的典型误区

1. **只看 MTEB 不看 CCKM** — MTEB 不测试跨模态和跨语言，选择 Embedding 模型时需要根据业务场景选择对应的基准
2. **模型截断维度后不重测** — 同一模型在不同维度下的排序可能完全反转，降低维度后必须重新评估
3. **不评估重排序的 ROI** — 在 top-50 中已有正确答案但 top-5 中没有时，**加 cross-encoder reranker 通常比换 Embedding 模型收益更大**
4. **忽略查询-文档不对称** — 短查询 vs 长文档，不同 Embedding 模型对此差异敏感
5. **自托管不是免费的** — GPU 硬件成本、运维成本和模型更新成本需要纳入预算

### 参考来源

- [如何为RAG应用选择最佳Embedding模型 - Zilliz 向量数据库](https://zilliz.com.cn/blog/How-to-choose-the-best-embedding-model-for-RAG)
- [jina-embeddings-v4 - Jina AI](https://jina.ai/models/jina-embeddings-v4/)
- [PyMilvus Integration with Embedding Models](https://milvus.io/blog/introducing-pymilvus-integrations-with-embedding-models.md)
- [A Complete Developer Guide to Vector Embeddings - Neptune.ai](https://www.neptune.ai/blog/vector-embeddings)
- [Vector Embedding Tutorial - Medium](https://medium.com/@pratik-rupareliya/vector-embeddings-tutorial)

---

## 2026 生产级向量数据库实战全景

> 来源：[Vector Databases in 2026: The Complete Production Guide](https://devstarsj.github.io/2026/02/24/vector-databases-ai-applications-production-guide/)（2026年2月）；[The Ultimate Guide to Vector Databases in 2026](https://codeboxr.com/the-ultimate-guide-to-vector-databases-in-2026/)（2026年4月）；[Embeddings & Vector Databases: A Practitioner's Guide](https://www.aitraining2u.com/embeddings-vector-databases-2026.html)（2026）

### HNSW 为什么是 2026 年的王者算法？

ANN（近似最近邻）算法是向量数据库的核心引擎。2026 年，**HNSW（Hierarchical Navigable Small World）** 已成为绝对主流——pgvector、Pinecone、Qdrant、Weaviate、Milvus 全部默认或主要使用 HNSW。

| 算法 | 速度 | 精度 | 内存占用 | 2026 年地位 |
|------|------|------|---------|------------|
| **HNSW** | 极快 | 极高 | 高 | 🏆 绝对主流 |
| IVF（倒排索引） | 快 | 高 | 中 | 大基数场景替代方案 |
| ScaNN（分区+重排） | 快 | 高 | 中 | Google 系使用 |
| DiskANN | 中 | 高 | 低 | 磁盘优化场景 |

HNSW 构建多层图结构，每层都是一个小世界网络，搜索时从顶层快速跳跃到底层精确匹配，实现**对数级别**的搜索复杂度。核心权衡：**构建索引慢、内存占用高，但查询速度极快且精度损失极小。**

### 向量数据库 2026 年全景对比

| 数据库 | 类型 | 最适合场景 | 托管选项 |
|--------|------|-----------|---------|
| **pgvector** | PostgreSQL 扩展 | 简单 RAG，已有 Postgres 基础设施 | AWS RDS, Supabase, Neon |
| **Pinecone** | 托管云原生 | 企业级，全托管，零运维 | 仅托管 |
| **Qdrant** | 独立，Rust 原生 | 高性能，自托管 | Qdrant Cloud |
| **Weaviate** | 独立 + 多模态 | 多模态搜索，GraphQL API | Weaviate Cloud |
| **Milvus** | 独立，云原生 | 十亿级规模，复杂过滤 | Zilliz Cloud |
| **Chroma** | 嵌入式/本地 | 开发原型，本地测试 | 无 |
| **Redis（向量）** | Redis 模块 | 低延迟，已有 Redis 基础设施 | Redis Cloud |

### 选型决策三步法

**第一步：明确规模**

```
你的向量数量级？
├─ < 10万 → Chroma / pgvector（够用，零额外成本）
├─ 10万 - 1000万 → Qdrant / Weaviate / pgvector（需关注查询延迟）
└─ > 1000万 → Milvus / Pinecone（需要分布式和 HA）
```

**第二步：看基础设施**

- **已有 PostgreSQL？** → 优先 pgvector，同库管理，减少运维复杂度
- **已有 Redis？** → Redis Stack 向量搜索够用且延迟最低
- **MongoDB 生态？** → Atlas Vector Search 统一文档+向量查询
- **全新项目？** → Qdrant（自托管高性能）或 Pinecone（全托管省心）

**第三步：评估非功能性需求**

- **元数据过滤能力**：是否需要复杂条件组合？（Milvus > Qdrant > pgvector）
- **多模态支持**：是否需要文本+图片统一检索？（Weaviate 原生支持）
- **增量更新效率**：是否需要频繁写入？（Qdrant 写入最快）
- **运维能力**：是否有人维护分布式系统？（没有 → Pinecone 托管）

### 2026 年不可忽视的三个实践

1. **混合检索不是可选项而是标配**：稠密向量 + BM25 + 重排序（reranker）的三层架构是 2026 年的基线。单纯向量检索的召回率天花板约为 85%，加上 BM25 可提升至 92%，再加 reranker 可达 97%+。
2. **语义缓存让成本砍半**：FAQ 和文档查询场景下，60-85% 的查询可被语义缓存命中，API 成本降低最高 73%，延迟从 1.67s 降至 0.052s。
3. **不要把向量数据库当成"万能存储器"**：它擅长相似性检索，但不适合事务、聚合查询、复杂关系建模——这些仍由关系数据库承担。

> 来源：[Vector Databases in 2026: The Complete Production Guide](https://devstarsj.github.io/2026/02/24/vector-databases-ai-applications-production-guide/) | [The Ultimate Guide to Vector Databases in 2026](https://codeboxr.com/the-ultimate-guide-to-vector-databases-in-2026/) | [Embeddings & Vector Databases: A Practitioner's Guide (2026)](https://www.aitraining2u.com/embeddings-vector-databases-2026.html)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-22 00:08:01*
