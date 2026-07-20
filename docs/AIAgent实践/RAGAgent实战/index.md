# 🔍 RAG Agent 实战

构建结合检索增强生成（RAG）的智能 Agent，实现基于私有知识库的精准问答。

---

## 📖 概述

RAG（检索增强生成）是一种将 LLM 与外部知识库结合的架构。当一个 RAG Agent 收到问题时，它不会仅依赖 LLM 的训练数据，而是先从知识库中检索相关信息，再将检索结果作为上下文提供给 LLM，最后生成回答。这种方式有效解决了 LLM 的知识截止问题和幻觉问题。

> 来源：[LangChain v0.3 课程 — James Briggs](https://www.aurelio.ai/course/langchain)

### RAG Agent vs 普通 RAG

| 维度 | 普通 RAG | RAG Agent |
|------|---------|-----------|
| 检索方式 | 每次查询都执行相同流程 | 根据问题类型智能选择检索策略 |
| 多轮优化 | 单次检索 | 可多次检索、追问、细化 |
| 工具集成 | 仅检索 | 可调用搜索、数据库、API 等多工具 |
| 决策能力 | 固定路线 | 自主决定何时检索、何时结束 |

---

## 🏗️ 架构设计

### 核心组件

```
用户提问
    ↓
[Agent 控制器] —— 判断是否需要检索
    ↓                          |
[检索器] ← 向量数据库          |（如不需要，直接回答）
    ↓                          |
[检索结果 + 原问题]            |
    ↓                          |
[LLM 生成回答] ←───────────────┘
    ↓
最终回复
```

### 技术栈选型

| 组件 | 推荐工具 | 说明 |
|------|---------|------|
| LLM | GPT-4o / Claude 3.5 | 支持函数调用的模型 |
| 向量数据库 | Chroma / Pinecone / Qdrant | 存储文档向量 |
| 检索框架 | LangChain / LlamaIndex | 提供 RAG 管道 |
| 嵌入模型 | text-embedding-3-small / bge | 生成文本向量 |
| Agent 框架 | LangChain Agent / LangGraph | 控制 Agent 循环 |

---

## 📝 实现步骤

### 1. 文档加载与分块

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = TextLoader("knowledge_base.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
```

### 2. 构建向量存储

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

### 3. 创建 RAG Agent

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI

# 将检索器封装为工具
retriever_tool = create_retriever_tool(
    retriever,
    "search_knowledge_base",
    "搜索知识库获取相关信息。当用户问到知识库中的内容时使用此工具。"
)

# 初始化 Agent
llm = ChatOpenAI(model="gpt-4o-mini")
tools = [retriever_tool, web_search_tool]  # 可组合多个工具

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)
```

### 4. 执行查询

```python
response = agent_executor.invoke({
    "input": "我们公司的退款政策是什么？"
})
print(response["output"])
```

---

## 🔄 高级模式：多轮检索

在实际应用中，用户的问题往往需要通过多轮检索才能回答完整。

### 追问式 RAG

```
用户: "去年的营收如何？"
Agent: [检索] → "2024年营收为1200万元"
用户: "相比前年增长了多少？"
Agent: [检索2023年数据] → "较2023年的980万元增长22.4%"
用户: "主要增长来自哪个业务线？"
Agent: [检索业务线数据] → "主要来自SaaS业务的同比增长35%"
```

### 多源融合检索

```python
# 多个知识库工具
tools = [
    retriever_tool_tech,      # 技术文档
    retriever_tool_product,   # 产品手册
    retriever_tool_faq,       # 常见问题
    web_search_tool           # 网络搜索
]
```

Agent 自主判断需要查询哪个知识源，必要时组合使用多个工具。

---

## 💡 最佳实践

1. **分块大小要合理** — 512-1024 tokens 是常见选择，太小丢失上下文，太大浪费 token
2. **重叠分块** — 200 tokens 的重叠确保边界信息不丢失
3. **检索结果排序** — 使用重排序（Re-ranking）提升准确率
4. **缓存常见问题** — 对高频问题缓存检索结果，降低延迟
5. **设置检索阈值** — 当检索结果相关性低于阈值时，让 Agent 明确告知用户"未找到相关信息"

### RAG Agent 的质量保障

RAG Agent 引入了"自主检索决策"，也引入了新的失控风险，需要针对性评估：

| 风险 | 现象 | 对策 |
|------|------|------|
| 不该检索却检索 | 简单问题也调用检索，浪费成本 | 在系统提示中明确"知识库范围"，训练模型判断 |
| 该检索却不检索 | 依赖参数知识硬答，产生幻觉 | 强制工具调用策略、设置"不确定时必须检索"规则 |
| 检索到错误信息仍采纳 | 盲信召回内容，传播错误 | 检索结果置信度阈值、与参数知识交叉验证 |
| 引用伪造 | 编造不存在的来源编号 | 引用必须在检索结果中存在，后处理校验 |
| 多轮检索膨胀 | 反复检索堆积上下文，超窗 | 检索次数上限、上下文压缩 |

### 引用可信度的实现

生产级 RAG Agent 应让每个关键陈述可追溯到具体文档片段：

1. 检索时为每个片段保留 `doc_id`、`chunk_id`、`source_url`、`score`。
2. 提示词要求模型"在回答中用 [1][2] 标注引用"。
3. 后处理校验：回答中的引用编号必须能在检索片段中找到对应。
4. 前端展示时把引用渲染为可点击链接，跳转到原文位置。

这样既提升可信度，也让用户能自行核验，是 RAG 系统区别于普通聊天机器人的关键体验。

---

## 📚 参考来源

- [LangChain v0.3 Full Course — James Briggs](https://www.aurelio.ai/course/langchain)
- [LangChain Agents in 2025 (YouTube)](https://www.youtube.com/watch?v=Gi7nqB37WEY)
- [LangChain for Beginners to Advanced — Towards AI](https://pub.towardsai.net/langchain-for-beginners-to-advanced-6a1d272437d0)
- [LangChain Documentation — RAG](https://python.langchain.com/docs/tutorials/rag/)

---

## 🆕 2026 最新进展

### RAG 2026：从朴素检索到智能路由

2026 年的 RAG 已不再是最初的"检索→拼接→生成"三板斧，而是演变为**多路由、多策略的智能检索系统**。根据 [RAG in 2026: A Practical Blueprint](https://dev.to/suraj_khaitan_f893c243958/-rag-in-2026-a-practical-blueprint-for-retrieval-augmented-generation-16pp) 的梳理，当前 RAG 系统需要支持两种核心路由模式：

#### 逻辑路由（Logical Routing）
根据查询类型将请求分发到不同的检索管道：
- **事实查询** → 向量检索 + 精确匹配
- **总结查询** → 全文检索 + 大 chunks
- **对比查询** → 多源检索 + 合并去重
- **实时查询** → 跳过知识库，直接调用 web search

#### 语义路由（Semantic Routing）
用 LLM 理解查询意图，自动选择检索策略：
1. 先用轻量模型分析用户意图
2. 根据意图类别选择对应的检索器组合
3. 复杂意图可触发多路并行检索再融合

### Agentic RAG：检索不再是单次操作

2026 年 RAG Agent 的核心进化是**检索本身成为 Agent 循环的一部分**，而非独立前置步骤：

```
传统 RAG：检索 → 生成（一次完成）
Agentic RAG：检索 → 评估 → (不够则)细化检索词 → 再检索 → 再评估 → 生成
```

这意味着 RAG Agent 可以：
- **自我纠正**：检索结果不相关时自动改写查询重试
- **多步推理检索**：将复杂问题拆解为多个子查询，分别检索后综合
- **来源抉择**：判断该查知识库、搜网页还是直接问模型

### 引用可信度成为标配

2026 年生产级 RAG Agent 的硬性要求是**每个关键陈述必须有可追溯的引用**：

| 层级 | 做法 | 效果 |
|------|------|------|
| 基础 | 要求模型标注引用编号 [1] [2] | 起码能给用户核对入口 |
| 进阶 | 后处理校验：引用的编号必须在检索结果中存在 | 杜绝"幻觉引用" |
| 高级 | 前端渲染为可点击链接，跳转到文档原文位置 | 可核验，可信赖 |

### 新框架选型速查

| 方向 | 推荐 | 理由 |
|------|------|------|
| 快速搭建 RAG Agent | LangChain `create_tool_calling_agent` + `create_retriever_tool` | API 最成熟，教程最多 |
| 生产级复杂 RAG | LangGraph | 支持条件分支、循环、多源融合 |
| 企业文档 QA | LlamaIndex + `QueryEngineTool` | 内置多种检索策略和重排序 |
| 轻量/本地 RAG | Ollama + Chroma + 自写循环 | 零成本，可控性最高 |

> 来源：[DEV Community: From Zero to Hero — Building Your First LangChain Agent with RAG](https://dev.to/vaib/from-zero-to-hero-building-your-first-langchain-agent-with-rag-1c8h)、[DEV Community: RAG in 2026 — A Practical Blueprint](https://dev.to/suraj_khaitan_f893c243958/-rag-in-2026-a-practical-blueprint-for-retrieval-augmented-generation-16pp)

### 查询策略：检索质量的核心杠杆

2026 年 RAG Agent 的一个关键认知是：**大多数弱 RAG 回答不是生成问题，而是检索问题**。一个模糊的用户查询往往需要多个检索策略来覆盖。以下是被生产实践证明有效的三种核心查询策略：

| 策略 | 做法 | 为什么有效 | 适用场景 |
|------|------|-----------|---------|
| **查询扩展（Query Expansion）** | 将用户问题改写为多个同义变体，分别检索后合并 | 不同措辞命中不同词汇，提高召回 | 用户用词不精确的 FAQ |
| **子问题分解（Sub-Query）** | 先问更高层次的问题确定领域，再向下检索 | 减少词汇不匹配，锚定检索方向 | 技术文档、法律条文检索 |
| **假设文档嵌入（HyDE）** | 先生成一个假设回答，用该回答的 Embedding 检索 | 假设回答包含领域术语，提升精度 | 知识库稀疏的长尾问题 |

**查询扩展的 Python 实现**：

```python
from langchain_core.prompts import ChatPromptTemplate

query_expansion_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个查询扩展助手。请将用户的原始问题改写成3个不同的同义问法。"),
    ("human", "原始问题：{question}\\n请输出互不相同的3个变体，每行一个。")
])

def expand_query(question: str, llm) -> list[str]:
    response = llm.invoke(query_expansion_prompt.format(question=question))
    variants = [v.strip() for v in response.content.split("\\n") if v.strip()]
    return [question] + variants[:3]

# 所有变体分别检索，结果去重合并
all_results = []
for q in expanded:
    docs = retriever.get_relevant_documents(q)
    all_results.extend(docs)
# 按相关性去重排序
unique_results = deduplicate_by_score(all_results)
```

> 来源：[DEV Community — RAG in 2026: A Practical Blueprint](https://dev.to/suraj_khaitan_f893c243958/-rag-in-2026-a-practical-blueprint-for-retrieval-augmented-generation-16pp)

### 多源检索路由

生产级 RAG Agent 很少只有一种数据源。当同时拥有向量数据库、关系型数据库和图数据库时，核心设计决策变成了：**如何将用户问题路由到正确的检索器？**

```
用户问题
    ↓
[路由决策层]
    ├── 涉及数值 → 路由到 Text-to-SQL 检索器（查关系型数据库）
    ├── 涉及概念 → 路由到向量检索器（查文档知识库）
    ├── 涉及关系 → 路由到图检索器（查图数据库）
    ├── 涉及实时性 → 路由到 Web Search
    └── 通用问题 → 路由到综合检索器（多源融合）
```

两种主流路由模式：

1. **规则路由**：用轻量级分类器或关键词规则判断意图
   - "如果问题包含 '收入'、'利润' → 查询 SQL"
   - "如果问题包含 '政策'、'规定' → 查询手册索引"

2. **语义路由**：用 Embedding 或小模型判断问题与哪种检索器最匹配
   - 预计算每个检索器的"代表性问题"的 Embedding
   - 新问题与各检索器的 Embedding 做相似度匹配
   - 选择相似度最高的检索器

### 混合检索策略

单一检索方式（纯向量搜索）在 2026 年已不满足生产需求。推荐**混合检索**架构——同时使用多种检索方式并融合结果：

```python
class HybridRetriever:
    def __init__(self):
        self.vector_retriever = VectorRetriever()   # 语义搜索
        self.keyword_retriever = BM25Retriever()     # 关键词搜索
        self.reranker = CohereRerank()               # 重排序

    def retrieve(self, query: str, top_k: int = 10):
        # 1. 并行检索：向量搜索 + 关键词搜索
        vector_results = self.vector_retriever(query, k=20)
        keyword_results = self.keyword_retriever(query, k=20)

        # 2. 合并去重
        all_results = merge_and_dedupe(
            vector_results, keyword_results
        )

        # 3. 重排序：用更精确的模型重新排序
        reranked = self.reranker.rerank(
            query=query, documents=all_results[:30]
        )

        return reranked[:top_k]
```

**重排序（Reranking）** 是提升 RAG 质量性价比最高的"单一改动"——无需改索引、无需改分块策略，加一个 reranker 通常能提升 15-25% 的检索准确率。

### 2026 RAG Agent 生产级检查清单

| 层级 | 检查项 | 说明 |
|------|--------|------|
| **索引层** | 分块策略合理 | 512-1024 tokens + 200 tokens overlap |
| **索引层** | 元数据完整 | doc_id, chunk_id, source_url, 层级路径 |
| **检索层** | 混合检索 | 向量 + 关键词双重保障 |
| **检索层** | 重排序 | 用 Cross-encoder 或 Cohere Rerank |
| **检索层** | 查询扩展 | 单问题 → 多变体，提高召回 |
| **路由层** | 多源路由 | 按查询类型分发到不同检索器 |
| **生成层** | 引用标注 | 每个关键句必须有 [来源编号] 标记 |
| **生成层** | 引用校验 | 后处理检查引用编号是否在检索结果中存在 |
| **安全层** | 检索阈值 | 低相关性结果直接丢弃，不喂给 LLM |
| **监控层** | 归因追踪 | 每个回答可追溯到具体文档片段 |

---

## 🏭 2026 RAG 生产实践全景

### 残酷现实：朴素 RAG 的 40% 失败率

2026 年，RAG 已成为用外部知识接地 LLM 的主流架构——但**朴素 RAG 管线在检索阶段大约有 40% 的失败率**。LLM 生成自信、结构工整的回答，却建立在错误的文档之上。2026 年的共识是：**检索步骤才是真正的瓶颈，而非生成**。

这一现实推动了 RAG 超越基本向量搜索，进入混合检索、Agentic RAG 和图增强架构的时代。

> 来源：[Lushbinary — RAG in 2026: The Complete Production Guide](https://lushbinary.com/blog/rag-retrieval-augmented-generation-production-guide/)、[Iterathon — RAG Systems Production Guide 2026](https://iterathon.tech/blog/rag-systems-production-guide-2025)

### GraphRAG：知识图谱 + RAG

2026 年，**GraphRAG（图增强检索）** 已成为处理多跳推理和实体关系型问题的关键技术。与仅依赖向量相似度的传统 RAG 不同，GraphRAG 将知识图谱的显式关系结构注入检索过程：

- **实体提取**：从文档中提取实体（人物、组织、概念）及其关系
- **图构建**：构建实体-关系知识图谱
- **图遍历检索**：查询时沿图谱关系路径检索相关子图
- **图上下文注入**：将图谱上下文与文本块一起提供给 LLM

GraphRAG 在以下场景中显著优于纯向量 RAG：
- **多跳问题**："张三所在部门的副总裁是谁？"
- **对比问题**："产品 A 和产品 B 的技术架构有何不同？"
- **聚合问题**："哪些客户同时购买了服务 X 和 Y？"

> 来源：[EmergentMind — Graph-Based Agentic RAG](https://www.emergentmind.com/topics/graph-based-agentic-rag)、[myengineeringpath.dev — GraphRAG 2026](https://myengineeringpath.dev/genai-engineer/graph-rag/)

### 混合检索已成为基线

纯粹向量搜索在 2026 年已不满足生产需求。**混合检索**（Hybrid Search）成为新基线——同时使用向量检索 + BM25 关键词检索 + 重排序：

```python
class HybridRetriever:
    def __init__(self, vector_store, bm25_index):
        self.vector_store = vector_store
        self.bm25_index = bm25_index

    def retrieve(self, query, k=10, alpha=0.5):
        # 向量语义搜索
        vector_results = self.vector_store.similarity_search(query, k=k*2)
        # BM25 关键词搜索
        bm25_results = self.bm25_index.search(query, k=k*2)
        # 倒数排名融合（Reciprocal Rank Fusion）
        merged = self.rrf_merge(vector_results, bm25_results, alpha)
        # 重排序
        reranked = self.reranker.rerank(query, merged)
        return reranked[:k]
```

**重排序（Reranking）** 被广泛认为是提升 RAG 质量性价比最高的"单一改动"——无需改索引、无需改分块策略，一个 reranker 通常能提升 **15-25%** 的检索准确率。

### RAG 评估：RAGAS 成为标配

2026 年，**RAGAS（RAG Assessment）** 已成为 RAG 系统评估的事实标准。它从三个维度衡量检索质量：

| 指标 | 衡量内容 | 目标 |
|------|---------|------|
| **Context Precision** | 检索到的上下文中相关文档的比例 | > 0.7 |
| **Context Recall** | 相关文档被检索到的比例 | > 0.7 |
| **Faithfulness** | 生成内容是否完全基于检索上下文（无幻觉） | > 0.8 |
| **Answer Relevancy** | 回答与问题的相关程度 | > 0.7 |

持续低分意味着索引、检索或生成管道有结构性问题，而非个别 case。

### 分块策略速查（2026）

| 策略 | 适用场景 | 注意事项 |
|------|---------|---------|
| **固定大小（512-1024 tokens）** | 通用文档 | 最简单，但不是最优 |
| **语义分块（按段落/章节）** | 结构化文档 | 保留语义完整性 |
| **递归分块（按分隔符层级）** | 混合内容（代码+文本） | 优先在段落边界切割 |
| **10-20% Overlap** | 所有策略 | 防止边界信息丢失 |
| **元数据保留** | 生产必备 | `source`、`timestamp`、层级路径 |

### 2026 RAG 架构选型矩阵

| 场景 | 架构 | 理由 |
|------|------|------|
| 文档 QA | 混合检索 + Reranking | 覆盖面 + 准确率的最佳平衡 |
| 多跳推理 | GraphRAG + 向量检索 | 显式关系推理必须图支持 |
| 动态/实时数据 | Agentic RAG + Web Search | 不确定何时需要检索 |
| 企业知识库 | 混合检索 + 多源路由 | 多数据源需要路由层 |
| 客服 FAQ | 查询扩展 + 混合检索 | 用户表达方式多样 |

> 来源：[Lushbinary — RAG Production Guide 2026](https://lushbinary.com/blog/rag-retrieval-augmented-generation-production-guide/)、[Iterathon — RAG Systems Production Guide 2026](https://iterathon.tech/blog/rag-systems-production-guide-2025)

---

## 🪞 Self-Reflective RAG：自我反思的检索增强

2026 年 RAG 的一个重要进化方向是 **Self-Reflective RAG（自我反思 RAG）**——让 RAG 系统不仅检索和生成，还能对自己的检索结果进行评估和修正，而非盲目信任第一次召回的内容。

### 核心机制

与传统 RAG 的单向流水线不同，Self-Reflective RAG 引入了一个**评估-反馈循环**：

```
用户问题 → 检索 → 生成 → 评估置信度
                           ↓
               置信度 > 0.8 → 直接输出
               置信度 < 0.8 → 改写查询 → 重新检索 → 重新生成
                           ↓
               仍不足 → 触发 Web Search 作为补充
```

这种设计**可将幻觉率降低 52% 以上**，因为系统在生成最终回答前先验证了检索内容是否真正支撑了回答。

### 实现示例

```python
class SelfReflectiveRAG:
    def __init__(self, retriever, generator, evaluator):
        self.retriever = retriever
        self.generator = generator
        self.evaluator = evaluator

    async def generate_with_reflection(
        self, query: str, max_iterations: int = 2
    ):
        for iteration in range(max_iterations):
            context = self.retriever.retrieve(query)
            answer = self.generator.generate(query, context)

            # 评估答案的置信度和检索支撑度
            evaluation = self.evaluator.evaluate(
                query=query,
                context=context,
                answer=answer
            )

            if evaluation["confidence"] > 0.8:
                return answer, evaluation

            # 置信度不足：根据评估反馈改写查询
            if evaluation["needs_more_context"]:
                query = self._refine_query(query, evaluation)
            # 继续下一轮检索-生成循环
        return answer, evaluation  # 已达最大迭代次数
```

### CRAG：纠正性 RAG（Corrective RAG）

**Corrective RAG（CRAG）** 是 Self-Reflective RAG 的一个变体，专注于**检测检索结果的质量并采取纠正动作**。当检索内容质量不佳时，CRAG 不是简单重试，而是智能切换策略：

| 检测到的状态 | 采取的纠正动作 |
|------------|--------------|
| 检索结果高度相关（置信度 > 0.8） | 直接使用检索结果生成回答 |
| 检索结果部分相关（0.5 < 置信度 < 0.8） | 仅保留高相关片段，丢弃噪声内容 |
| 检索结果不相关（置信度 < 0.5） | 触发 Web Search 替换知识库检索 |
| 检索结果过时 | 自动触发知识库更新或实时数据查询 |

CRAG 的关键洞察是：**"错误"不等于"无信息"**——有时检索到的内容部分正确、部分过时，CRAG 能精细地只保留有用的部分，而非全盘接受或全盘否定。

### 在 bRAG-langchain 中体验

如果你希望从可运行的代码中学习 Self-Reflective RAG 和 CRAG，推荐参考开源项目 **[bRAG-langchain](https://github.com/bRAGAI/bRAG-langchain/)**。该项目以 Jupyter Notebook 形式，从基础 RAG 逐步演进到多查询、路由、高级索引、重排序和自反思检索，是 2026 年学习 RAG 进阶技术的优秀实战材料。

> 来源：[Iterathon — RAG Systems Production Guide 2026](https://iterathon.tech/blog/rag-systems-production-guide-2025)、[DEV — RAG in 2026: A Practical Blueprint](https://dev.to/suraj_khaitan_f893c243958/-rag-in-2026-a-practical-blueprint-for-retrieval-augmented-generation-16pp)

---

## 🏛️ 2026 前沿：从 RAG Pipeline 到 Agentic RAG

Anthropic 的《Building Effective Agents》（2024.12）提出了"**Augmented LLM**"（增强型 LLM）作为 Agent 系统的基础构建块——这与 RAG 的概念一脉相承，但把它提升到了一个更高的抽象层次。

### Augmented LLM：RAG 进化的方向

传统 RAG 关注"检索 + 生成"两个步骤的串联。Augmented LLM 则将检索、工具和记忆作为 LLM 的三个**可组合增强能力**：

```
         ┌──────────────┐
         │   LLM 核心    │
         │  (推理/生成)  │
         └──┬───┬───┬───┘
    ┌───────┘   │   └───────┐
    ▼           ▼           ▼
┌──────┐  ┌──────┐    ┌──────┐
│ 检索  │  │ 工具  │    │ 记忆  │
│(RAG) │  │(API) │    │(状态) │
└──────┘  └──────┘    └──────┘
```

在这个框架下，RAG 不再是独立的"管道"，而是 Agent 可以**自主决定何时启用、如何组合**的一项能力。例如：Agent 可以先尝试从记忆中找到相关信息，如果没有，再触发检索；检索结果不满意时，自动切换到 Web 搜索——这已经超越了传统 RAG 的固定路线。

### Agentic RAG 的编排模式

在 Agentic RAG 中，最常用的两种工作流模式：

#### Orchestrator-Workers for Multi-Source RAG

中央 LLM 动态判断：这个查询需要哪些数据源？（知识库 / 实时 API / Web Search / 数据库）→ 分派给对应 Worker 检索 → 汇总结果。这对跨系统知识检索（如同时查内部文档 + 客户 CRM + 实时价格）尤其有效。

#### Evaluator-Optimizer for Retrieval Quality

检索结果 → LLM 评估相关性 → 不满足则重新检索（换查询词 / 换数据源 / 调整 chunk 大小）→ 再次评估 → 直到满足阈值。这本质上是 CRAG（Corrective RAG）的通用化版本。

### 何时升级到 Agentic RAG？

Anthropic 的建议是：**先追求简单**。如果以下条件不满足，标准 RAG Pipeline 就足够了：

- ✅ 单个检索源的 top-k 结果经常不满足需求
- ✅ 查询需要跨多个不同系统组装信息
- ✅ 检索质量需要用反馈循环来保证（如法律/医疗场景）
- ✅ 任务的步骤数不可预测（如多跳推理 QA）

升级前先衡量：增加的延迟和成本是否值得更好的任务表现？

> 来源：[Anthropic — Building Effective Agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-21 00:08:07*
