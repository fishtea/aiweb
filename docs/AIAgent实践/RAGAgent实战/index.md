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

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-09 00:14:29*
