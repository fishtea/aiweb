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

## 10. 2026 年开源 RAG 引擎全景：四大框架横向对比

2026 年的开源 RAG 生态已从"一个框架跑通"进入"按场景选型"的阶段。以下四个项目代表了不同的设计哲学，它们的 GitHub 活跃度和覆盖场景可以帮助开发者快速定位适合的引擎。

### 10.1 四大开源 RAG 引擎概览

| 引擎 | Stars | 语言 | 核心定位 | License | 适合场景 |
|------|-------|------|---------|---------|----------|
| [RAGFlow](https://github.com/infiniflow/ragflow) | 84,292 ⭐ | Go | 生产级 RAG 引擎，深度融合 Agent 能力 | Apache-2.0 | 企业知识库、需要文档解析+Agent 编排 |
| [LightRAG](https://github.com/HKUDS/LightRAG) | 37,322 ⭐ | Python | 轻量级图增强 RAG（EMNLP 2025 论文） | MIT | 研究实验、小团队快速验证 |
| [GraphRAG](https://github.com/microsoft/graphrag) | 34,183 ⭐ | Python | 微软出品的基于知识图谱的模块化 RAG | MIT | 需要跨文档全局理解的企业场景 |
| [RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) | 28,340 ⭐ | Jupyter Notebook | 进阶 RAG 技术教程库 | — | 学习与实验，研究各种 RAG 变体 |

### 10.2 选型决策树

```
你的场景是什么？
├── 需要企业级文档解析 + Agent 编排？
│   └── → RAGFlow（Go 实现，高性能文档处理）
├── 研究实验，想快速尝试不同 RAG 变体？
│   ├── 需要内置知识图谱？→ LightRAG（轻量，论文级实现）
│   └── 需要全局文档理解？→ GraphRAG（微软出品，图增强）
└── 想系统学习 RAG 进阶技术？
    └── → RAG_Techniques（32+ 技术的教程+代码）
```

### 10.3 RAGFlow 深度解读（84,292 ⭐）

RAGFlow 是当前增长最快的开源 RAG 引擎。其核心优势在于**将 RAG 与 Agent 能力深度整合**：

- **自研文档解析引擎**：结构化解析 PDF、Office、图像等格式，保留表格、段落层级信息
- **Agentic Retrieval**：不是简单的"搜索→拼入 prompt"，而是让 LLM 先分析用户意图，生成检索计划，再执行多源搜索
- **上下文引擎**：管理检索结果的排序、压缩和引用追踪
- **企业级权限与审计**：文档级权限裁剪、查询日志、引用追溯

### 10.4 LightRAG vs GraphRAG：两种图增强路线

两个项目都引入了**图结构**来增强传统向量检索，但设计哲学截然不同：

| 维度 | LightRAG（HKU） | GraphRAG（Microsoft） |
|------|----------------|----------------------|
| 图构建方式 | 从文档增量构建实体-关系图 | 先分块，再提取实体关系构建全局图谱 |
| 查询模式 | 支持局部/全局/混合查询 | 强调全局查询和主题发现 |
| 论文发表 | EMNLP 2025 | 预印本 |
| 部署复杂度 | 低（pip install 即可运行） | 中（需要 API key） |
| 适合场景 | 小数据集、快速实验 | 大规模文档库、需要全局理解 |

### 10.5 RAG_Techniques：进阶 RAG 技术百科全书

NirDiamant 维护的教程仓库，覆盖 **32 种以上** RAG 技术变体，包括：

- 基础 RAG → 高级 RAG → Agentic RAG → 多模态 RAG
- 每种技术附有 Jupyter Notebook 教程和对比分析
- 适合已理解基础 RAG 原理的开发者和研究人员系统学习

### 10.6 本节结论

2026 年选择 RAG 引擎的关键不是"哪个最强"，而是**找对场景**：

1. **企业生产环境** → RAGFlow（文档解析 + Agent 编排 + 权限管理）
2. **研究实验** → LightRAG（轻量、论文级、快速迭代）
3. **全局文档理解** → GraphRAG（微软生态，跨文档图分析）
4. **技术学习** → RAG_Techniques（32+ 技术变体教程）

### 10.7 参考来源

- [RAGFlow GitHub](https://github.com/infiniflow/ragflow) — Stars 数据采集于 2026-07-05
- [LightRAG GitHub](https://github.com/HKUDS/LightRAG) — EMNLP 2025 论文
- [Microsoft GraphRAG GitHub](https://github.com/microsoft/graphrag)
- [RAG_Techniques GitHub](https://github.com/NirDiamant/RAG_Techniques)

---

## 11. RAG 核心设计原理与实践经验

> 来源：[What is Retrieval-Augmented Generation? - IBM Research](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)（Aug 2023）

### 11.1 "开卷考试" vs "闭卷考试"

RAG 的核心思想可以用一个简单的类比理解：

> **闭卷考试（纯 LLM）**：模型只能依赖训练时记住的知识，像学生凭记忆答题。遇到训练数据之外的信息或新变化的内容，就容易"编造"答案。
>
> **开卷考试（RAG）**：模型像学生翻阅参考书一样，在回答前先检索外部知识库，确保答案有据可查。

RAG 的**两大核心优势**：
1. **确保最新、可靠的事实**：知识库可以随时更新，无需重新训练模型
2. **提供可追溯的来源**：用户可以检查模型据以回答的原始内容，验证真实性

> *"You want to cross-reference a model's answers with the original content so you can see what it is basing its answer on"* — Luis Lastras, IBM Research

### 11.2 RAG 的额外收益

- **减少幻觉**：通过将 LLM 约束在可验证的事实集合上，模型减少了从参数中"编造"信息的机会
- **降低数据泄露风险**：模型不需要记住敏感数据，只需在需要时检索
- **降低计算成本**：无需频繁重新训练模型，更新知识库即可保持内容新鲜
- **更快响应变化**：企业政策更新后，只需更新文档索引，无需等待模型重新训练

### 11.3 从对话流程看 RAG vs 传统方案

| 维度 | 传统对话机器人 | 纯 LLM 聊天 | RAG 增强 LLM |
|------|--------------|------------|-------------|
| 回答方式 | 预写脚本匹配 | 凭记忆生成 | 检索后生成 |
| 个性化 | 有限，依赖人工编写 | 中等 | 强（结合用户上下文） |
| 更新成本 | 重写脚本 | 重新训练/微调 | 更新文档库 |
| 可审计性 | 高（已预写） | 低（来源不可追溯） | 高（引用原始文档） |
| "我不知道" 能力 | 需人工写 | 需大量微调训练 | 可通过检索结果判断 |

**真实案例**：IBM 内部客服机器人使用 RAG 处理员工请假查询。例如员工 Alice 询问儿子学校提前放学能否请假，RAG 系统：① 从 HR 档案检索 Alice 的年假余额 ② 从公司政策文档核实请假流程 ③ 综合生成个性化回复。

### 11.4 教模型识别"不知道"

LLM 天然倾向于"硬答所有问题"——就像一个过于热情的初级员工，在没核实事实的情况下就脱口而出。在更复杂的场景中，这种倾向更危险：

> 真实案例：当员工问"我有多少天产假"时，不使用 RAG 的聊天机器人愉快地（且错误地）回答："随你休多久。"

RAG 的解决思路：
- 如果检索结果不充分或不存在，模型应回答"我不知道"
- 让模型学会在不确定时主动追问更多上下文
- 高质量的 RAG 系统需要同时优化检索端（找到最相关信息）和生成端（结构化组织信息）

### 11.5 检索与生成的平衡艺术

RAG 不是简单的"搜到就拼进去"，需要精心设计：

**检索端优化要点**：
- **覆盖率 vs 精准度**：检索过多无关信息会污染 prompt；检索过少可能遗漏关键事实
- **多源融合**：结构化数据（数据库）+ 非结构化文本（文档）+ 实时信息（API）
- **混合搜索**：向量相似度 + 关键词 BM25 相结合，覆盖语义和字面匹配

**生成端优化要点**：
- **上下文窗口管理**：检索结果可能超出 LLM 上下文限制，需要排序、压缩、剪枝
- **引用机制**：每条生成内容都应能追溯到原始文档片段
- **忠实度验证**：LLM 是否真的基于检索内容作答，还是忽略检索结果自行发挥

### 11.6 RAG 在企业落地的关键考量

| 考量 | 建议 |
|------|------|
| **权限控制** | 文档级别权限裁剪，确保模型只访问用户有权查看的内容 |
| **多语言支持** | 选择跨语言嵌入模型（如 multilingual-e5），确保多语言文档的检索质量 |
| **更新频率** | 建立文档变更→重新索引的自动化管道，避免知识滞后 |
| **回退策略** | 当检索质量低于阈值时，主动告知用户"信息不足"而非编造答案 |
| **成本控制** | 嵌入计算（离线）和 LLM 推理（在线）的权衡——缓存高频查询结果 |

### 11.7 参考来源

- [What is Retrieval-Augmented Generation? - IBM Research](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)
- [RAG: Retrieval-Augmented Generation for LLMs - IBM Think](https://www.ibm.com/think/topics/retrieval-augmented-generation)
- [Building Enterprise RAG Systems - NVIDIA Technical Blog](https://developer.nvidia.com/blog/building-enterprise-retrieval-augmented-generation-systems/)

---

## 12. 2026年RAG新前沿：多模态RAG与缓存增强生成

### 12.1 多模态RAG（Multimodal RAG）

随着多模态大模型（GPT-4o、Gemini、Claude 3.5 等）的普及，RAG 正在从"纯文本检索"向"跨模态检索"演进。多模态 RAG 的核心挑战在于：**用户的问题可能是文本，但相关证据可能存在于图片、表格、图表、视频甚至音频中**。

**核心架构变化：**

```
传统 RAG：文本查询 → 文本嵌入 → 文本向量搜索 → 文本片段 → LLM 生成
多模态 RAG：
  文本查询 → 多模态嵌入（CLIP/ColPali/Unified Embedding）
           → 跨模态搜索
           → 图片 + 表格 + 文本片段
           → 多模态 LLM 生成
```

**主流技术路线：**

| 路线 | 技术方案 | 代表工作 | 适用场景 |
|------|---------|---------|----------|
| **嵌入对齐** | 用 CLIP / SigLIP 将文本和图片映射到统一向量空间 | CLIP-based 方案 | 图文匹配检索 |
| **视觉语言模型直接检索** | 用 VLM（如 ColPali）直接对 PDF 页面截图生成嵌入 | ColPali, ColQwen | PDF 文档理解 |
| **文档解析 + 多模态分块** | 先用文档解析引擎提取表格、图片、文本，分别嵌入再融合 | LlamaParse, RAGFlow | 混合文档（报告、手册） |
| **后期融合** | 文本检索 + 图片检索并行，结果合并后统一排序 | 混合搜索扩展 | 已有文本 RAG 的升级 |

**关键工程考量：**

- **嵌入模型选择**：多语言场景选 `multilingual-e5`，图文场景选 `CLIP-ViT` 或 `ColPali`
- **存储成本**：图像嵌入向量维度通常比文本嵌入更大（768-1024 vs 384-768），需要更多存储
- **检索速度**：跨模态检索在大型文档库中可能比纯文本慢 2-5 倍，建议对图片数量多的文档预先分层
- **上下文窗口管理**：多模态 LLM 的上下文窗口通常更紧张（图片 token 消耗大），需要更激进的压缩和重排序

### 12.2 缓存增强生成（CAG: Cache-Augmented Generation）

**来源：** [Cache-Augmented Generation - arXiv 2024/12](https://arxiv.org/abs/2412.15605)

CAG 是 2025-2026 年 RAG 领域的一个新范式，核心思想是：**当知识库足够小（能塞进上下文窗口），直接用 KV Cache 替代检索**。

**CAG 的工作原理：**

```
传统 RAG：查询 → 检索(耗时) → 拼接 → 生成
CAG：预加载全部文档 → 预计算 KV Cache → 查询 → 直接基于 Cache 生成（无检索延迟）
```

**三阶段流水线：**

| 阶段 | 操作 | 说明 |
|------|------|------|
| **预热（Preloading）** | 将所有文档拼入提示词，预计算 LLM 的 KV Cache | 一次性成本，离线完成 |
| **缓存存储** | 将 KV Cache 持久化到磁盘/内存 | 避免每次查询都重新编码 |
| **推理** | 用户查询直接加载预计算 Cache，无需检索 | 零检索延迟，100% 召回 |

**CAG vs RAG 适用边界：**

| 维度 | CAG | 传统 RAG |
|------|-----|----------|
| **知识库规模** | 小（< 上下文窗口长度） | 不限 |
| **检索延迟** | 零 | 10-500ms |
| **召回率** | 100%（全文在上下文中） | 受检索质量影响 |
| **幻觉控制** | 极好（模型看到全部内容） | 依赖检索和重排序 |
| **知识更新成本** | 需要重新计算全量 KV Cache | 只需增量索引 |
| **Token 成本** | 高（每次推理传递完整上下文） | 低（仅传递少数检索片段） |

**实践建议：**

- **小知识库（< 128K tokens）且高频查询** → CAG 是更好的选择（零延迟 + 完美召回）
- **大型知识库或频繁更新** → 传统 RAG 架构
- **混合方案**：核心文档用 CAG（预热缓存），长尾文档用 RAG（按需检索）
- 注意 CAG 的 KV Cache 在不同推理框架中的序列化兼容性（vLLM、SGLang 对 Cache 序列化支持程度不同）

### 12.3 多模态 RAG 与 CAG 的选型总结

```
你的场景是什么？
├── 文档含大量图片、图表、表格？
│   ├── 知识库 < 128K tokens → 尝试多模态 CAG
│   └── 知识库大 → 多模态 RAG（ColPali + 混合搜索）
├── 纯文本文档？
│   ├── 知识库 < 128K tokens，高频查询 → CAG
│   └── 知识库大或常更新 → 传统 RAG + 重排序
└── 混合场景（部分核心+部分长尾）？
    └── 核心文档 CAG + 长尾文档 RAG 混合架构
```

### 12.4 参考来源

- [ColPali: Efficient Document Retrieval with Vision-Language Models](https://arxiv.org/abs/2407.01449)
- [Cache-Augmented Generation (CAG) - arXiv](https://arxiv.org/abs/2412.15605)
- [Multimodal RAG with LlamaIndex - LlamaIndex Blog](https://www.llamaindex.ai/blog)
|- [ColQwen: Visual Document Retrieval](https://github.com/illuin-tech/colqwen)

---

## 13. RAGAgent：RAG + Agent 的融合模式

2026 年，RAG 和 Agent 两个范式的边界正在模糊。越来越多的生产系统不再区分"我这个系统是 RAG 还是 Agent"——而是将检索作为 Agent 的工具之一，让 LLM 自主决定何时检索、检索什么、怎么组织检索结果。

### 13.1 为什么需要融合？

传统 RAG 的局限在于**检索是固定流程**：用户查询 → 向量搜索 → 拼入上下文 → 生成。它假设"一次检索就能找到所有答案"。但在真实场景中：

| 传统 RAG 的失败场景 | 表现 |
|--------------------|------|
| **多跳问题** | "2024 年诺贝尔物理学奖得主创办的公司叫什么？" → 需要先查诺贝尔奖，再查公司信息 |
| **对比类问题** | "对比 GPT-4o 和 Claude 3.5 在代码生成上的表现" → 需要分别搜索两种模型 |
| **信息不足** | 首次检索返回空结果 → 传统 RAG 只能返回空，Agent 可以改写查询重试 |
| **权限敏感** | 不同用户看到不同文档 → Agent 可以根据用户身份自适应检索范围 |

**RAGAgent 的解决思路：** 将检索抽象为 Agent 的一个工具（或一组工具），Agent 自主规划检索策略，而非在流程图中硬编码。

### 13.2 RAGAgent 的三种架构模式

**来源：** [Agentic RAG with LangGraph - LangChain Blog](https://blog.langchain.dev/agentic-rag-langgraph/), [Building Agentic RAG Systems - LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/agent/agentic_rag/)

| 模式 | 架构描述 | 适用场景 |
|------|---------|----------|
| **Tool-based RAG** | 检索作为 Agent 的一个工具（search_docs），Agent 自主决定何时调用 | 通用问答、需要多步推理 |
| **Query Planning RAG** | Agent 先分析用户问题，拆解为多个子查询并行/串行检索 | 复杂多跳、对比分析问题 |
| **Adaptive RAG** | Agent 按问题难度路由：简单直接回答，中等单次检索，复杂多步检索 | 需要平衡延迟和准确率 |

### 13.3 Tool-based RAG：检索即工具

最简单的融合模式——将检索封装为一个工具函数，Agent 像调用计算器或搜索一样调用它：

```python
@tool
def search_knowledge_base(query: str, top_k: int = 5) -> str:
    """Search the company knowledge base for relevant documents.
    
    Use this tool when you need factual information from internal documentation.
    The knowledge base contains product docs, policies, and technical references.
    
    Args:
        query: The search query, should be concise and specific
        top_k: Number of results to return (1-10)
    
    Returns:
        Relevant document excerpts with their source references
    """
    # 向量搜索 + 重排序
    results = vector_store.similarity_search(query, k=top_k)
    reranked = reranker.rerank(query, results)
    return format_results(reranked)
```

**关键设计要点：**
- **工具描述包含"何时使用"**：帮助 Agent 判断当前场景是否需要检索
- **参数简洁**：减少 Agent 调用时的出错概率
- **返回结构化结果**：包含引用来源，便于 Agent 追溯验证

### 13.4 Query Planning RAG：Agent 作为检索规划器

当问题复杂到需要多步、多源检索时，Agent 充当"检索规划器"的角色：

**工作流程：**

```
用户提问 → Agent 分析问题
  → 生成检索计划（3 个子查询）
  → 并行执行 3 个检索
  → 合并检索结果
  → 评估是否充分
  → 如不足，补充检索（可选）
  → 生成最终回答（含引用）
```

**示例（对比类问题）：**

```
用户："对比 LangGraph 和 CrewAI 在多人协作场景中的优劣"

Agent 检索计划：
1. search("LangGraph multi-agent collaboration features 2026")
2. search("CrewAI multi-agent orchestration 2026")
3. search("LangGraph vs CrewAI comparison agent frameworks")

Agent 评估：三个查询结果覆盖了各自的特性和已知对比 → 充分
Agent 回答：...（综合三个来源生成对比分析）
```

> **实践建议：** Query Planning 需要增加"充分性评估"步骤。Agent 应在生成最终答案前检查：检索结果是否覆盖了问题的所有方面？信息是否有冲突？如果信息不足，应补充检索。

### 13.5 Adaptive RAG：按需路由

Adaptive RAG 根据问题复杂度动态调整检索策略，是延迟和准确率的最佳平衡点：

```
用户问题
  ├── 简单问答（"公司年假政策是什么？"）
  │   └── → 单次向量检索 → 直接回答
  ├── 中等复杂度（"远程员工的出差报销流程？"）
  │   └── → 检索 + 重排序 → 回答
  └── 复杂问题（"对比去年和今年 Q2 的销售策略变化？"）
      └── → Query Planning RAG → 多步检索 → 综合回答
```

**分类方法：**
| 分类方式 | 实现 | 效果 |
|---------|------|------|
| 关键词启发式 | 按问题长度、疑问词类型判断 | 简单高效，但不够精准 |
| LLM 路由 | 用一个小模型（如 GPT-4o-mini）分类问题 | 准确，增加一次 LLM 调用 |
| 嵌入相似度 | 将问题与预定义的复杂度模板匹配 | 零额外延迟，需预定义分类 |

### 13.6 RAGAgent 的实践经验

**1. 最少检索原则**：不要让 Agent 过度检索。每多一次检索就多一次延迟和 Token 消耗。能用一次检索解决的问题，不要用两次。

**2. 检索结果缓存**：相同或相似的查询在短时间内复用缓存结果，缓存命中率可达 50-70%。

**3. 检索引用的自动验证**：Agent 在引用检索结果时，应附带原文片段链接，方便人工验证。这是从"可信"到"可证"的关键一步。

**4. 降级路径**：当所有检索都返回空时，Agent 应明确告知而非编造。建议提供三种降级策略：
| 降级策略 | 行为 |
|---------|------|
| 拒绝回答 | "未找到相关信息，请补充文档或联系专家" |
| 网络搜索候选 | 启用公共网络搜索作为后端（需授权） |
| 转人工 | 记录查询并转给人工客服 |

### 13.7 参考来源

- [Agentic RAG with LangGraph - LangChain Blog](https://blog.langchain.dev/agentic-rag-langgraph/)
- [Building Agentic RAG Systems - LlamaIndex Docs](https://docs.llamaindex.ai/en/stable/examples/agent/agentic_rag/)
- [Adaptive RAG: Retrieval-Augmented Generation with Dynamic Routing - arXiv](https://arxiv.org/abs/2403.14403)
- [Self-RAG: Learning to Retrieve, Generate, and Critique - arXiv](https://arxiv.org/abs/2310.11511)
- [CRAG: Corrective RAG - arXiv](https://arxiv.org/abs/2401.15884)

---

## 14. Pinecone RAG 进阶实战：重排序与两阶段检索

### 14.1 RAG 检索的两阶段范式

**来源：** [Pinecone RAG Series - Rerankers and Two-Stage Retrieval](https://www.pinecone.io/learn/series/rag/)（2026年持续更新）

Pinecone 在其 RAG 系列教程中将生产级检索提炼为一个清晰的**两阶段模式**：

```
第一阶段（粗排）：快速检索（向量/BMS25） → 召回 Top-100 候选
第二阶段（精排）：重排序模型 → 精选 Top-5 → 送入 LLM 生成
```

这种架构的核心洞察是：**召回和精排应该使用不同的模型**——召回阶段追求速度和覆盖率（用轻量嵌入模型），精排阶段追求准确率（用计算量更大的交叉编码器或 LLM）。

### 14.2 重排序器的三种类型

| 类型 | 代表工具 | 速度 | 精度 | 适用场景 |
|------|---------|------|------|---------|
| **交叉编码器** | Cohere Rerank、BGE Reranker、MixedBread | 慢 | 最高 | 对准确率要求最高的生产场景 |
| **双编码器** | ColBERT、Sentence-BERT | 中 | 中 | 平衡速度与质量 |
| **LLM 直接评分** | GPT-4 打分、Claude 排序 | 最慢 | 最高（但成本高昂） | 小批量、高价值场景 |

> Pinecone 建议：**交叉编码器重排序是 RAG 系统性价比最高的单项优化**——比换更大的嵌入模型或更大的 LLM 收益更高。

### 14.3 嵌入模型选型（2026 年推荐）

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 英文通用 | `voyage-3`、`text-embedding-3-large` | 性价比最高 |
| 多语言 | `multilingual-e5-large` | 跨语言检索首选 |
| 代码检索 | `voyage-code-2` | 代码语义理解 |
| 高精度 | `Cohere embed-v4` | 最高质量 |
| 本地部署 | `BGE-M3`（开源） | 无需 API 调用 |

### 14.4 指标驱动的 Agent 开发

Pinecone 强调，RAG Agent 的开发应从**定义评估指标**开始，而非从选择工具开始：

1. **先定指标**：`precision@5`、`recall@20`、答案忠实度、端到端延迟
2. **建基线**：最简单的 Naive RAG 跑一遍指标
3. **逐步叠加**：每次只加一个优化（先加重排序，再加查询改写，再加混合搜索），对比指标变化
4. **只在有数据支撑时才保留优化**：如果某个优化没有显著改善指标，果断移除

> 来源参考：[Pinecone RAG Series](https://www.pinecone.io/learn/series/rag/)

---

## 15. 2026年7月RAG研究前沿

### 15.1 FAIR GraphRAG：将 FAIR 数据原则引入图检索增强

**来源：** [FAIR GraphRAG: A Retrieval-Augmented Generation Approach for Semantic Data Analysis - arXiv:2607.11464 (2026-07-13), IEEE ICKG 2025](https://arxiv.org/abs/2607.11464v1)

GraphRAG 通过知识图谱捕获语义关系来增强检索，但在生物医学等复杂领域，现有方法缺乏对底层知识资源的**结构化 FAIR 化处理**。FAIR GraphRAG 是首个将 FAIR 原则（可发现 Findability、可访问 Accessibility、可互操作 Interoperability、可复用 Reusability）与图检索增强生成深度整合的框架。

**核心架构创新：FAIR 数字对象（FDO）作为图节点**

```
传统 GraphRAG:  实体节点 → 属性边 → 向量嵌入
FAIR GraphRAG:  FDO节点（核心数据 + 元数据 + 持久标识符 + 语义链接） → 向量嵌入
```

每个图节点不再只是简单的实体，而是包含以下四层信息的 FAIR 数字对象：

| 层级 | 内容 | 在检索中的作用 |
|------|------|-------------|
| **核心数据** | RNA 测序表达值、基因注释 | 向量相似度匹配的基础 |
| **元数据** | 样本来源、实验条件、质量控制指标 | 支持按条件过滤检索结果 |
| **持久标识符（PID）** | DOI、数据集 accession 号 | 确保可追溯性和可引用性 |
| **语义链接** | 本体论关系（如 Gene Ontology）、跨数据集引用 | 支持跨数据源推理 |

**LLM 辅助的自动化构建管道：**

论文设计了由医生和计算机科学家共同参与的协作设计流程，LLM 在以下环节发挥关键作用：
1. **Schema 构建**：从数据源自动推断本体论结构
2. **内容与元数据提取**：从非结构化文本中抽取结构化信息
3. **语义链接生成**：自动建立跨数据集的关联关系

**在胃肠病学 RNA 测序数据上的验证结果：**

FAIR GraphRAG 在处理涉及**元数据和本体论链接的复杂查询**时，在答案准确性、覆盖率和可解释性方面均显著优于传统 GraphRAG baseline。特别是在需要跨数据集推理的场景下，FAIR 化的知识表示使模型能够追溯到原始数据源，显著减少幻觉。

> **拓展潜力**：论文指出该框架不仅适用于生物医学，还可扩展到教育、商业等需要 FAIR 数据治理的专业领域。

---

### 15.2 RAG 中的意识形态偏差传递：温度参数的关键作用

**来源：** [How Temperature Shapes Ideological Discourse in Retrieval-Augmented Generation? - arXiv:2607.11783 (2026-07-13)](https://arxiv.org/abs/2607.11783v1)

这是一项开创性的研究，首次系统考察了 RAG 框架在**传递、放大或抑制检索材料中的意识形态话语**方面的行为。研究团队构建了一个包含 1,117 篇 COVID-19 治疗文献的语料库，通过词汇多维分析（Lexical Multidimensional Analysis, LMDA）识别出三种意识形态话语，再将其作为 RAG 系统的外部知识源。

**核心实验设计：**

1. 对 1,117 篇文章进行 LMDA 分析，识别三种意识形态话语维度
2. 将这些文章作为 RAG 系统的检索知识库
3. 让多个 LLM 在不同采样温度（temperature）下回答意识形态相关问题
4. 从语义和词汇两个维度评估生成文本与意识形态参考文本的相似度

**关键发现：温度参数的 U 型效应**

| 温度设置 | 话语传递强度 | 解释 |
|---------|------------|------|
| **低温度（接近 0）** | **最低** | 过度确定性采样抑制了从检索材料中吸收话语特征 |
| **中等温度** | **最高** | 在随机性与检索基础之间达到最佳平衡，最忠实地传递了检索材料的意识形态特征 |
| **高温度** | 中等 | 随机性增加导致话语传递的一致性下降 |

> **核心洞察**：RAG 并不是意识形态中立的——检索材料中的立场和观点会系统性地影响 LLM 输出。温度参数不是简单的"创造性调节旋钮"，而是**控制模型对检索材料"忠实度"的关键杠杆**。过度降低温度（如设置为 0）虽然减少了随机性，却可能意外地**抑制了 RAG 从检索材料中获取上下文信息的能力**。

**实践启示：**
- 如果希望 RAG 系统忠实反映检索材料的立场，应使用中等温度（如 0.5-0.7）
- 如果希望模型保持更"中立"的立场，低温度反而可能适得其反——需要额外的提示词约束
- 对于敏感领域（如政治、医疗政策），建议在 RAG 管道中增加**话语审计层**来检测和报告潜在的意识形态偏差

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-21 00:08:07*
