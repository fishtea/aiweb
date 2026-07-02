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

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-02 12:09:15*
