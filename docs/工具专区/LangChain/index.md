# LangChain：LLM 应用框架的"React"

> 它是第一个让"用 API 串联 AI"变得有章可循的框架。
> 也是最容易被骂"过度抽象"的框架之一。

---

## 核心定位

LangChain 诞生于一个简单的问题：**"调用 GPT-4 API 只是第一步，真正的应用需要链式调用、记忆、工具——谁来写这些胶水代码？"**

LangChain 的答案是：我来给你一套通用的抽象层，你只需要按规则填空。

---

## 六大抽象

### 1️⃣ Model I/O — 模型交互

最基础的层：把"跟模型说话"这件事标准化。

```python
from langchain_openai import ChatOpenAI

# 所有模型通过同一接口调用
llm = ChatOpenAI(model="gpt-4o")
claude = ChatAnthropic(model="claude-3-sonnet")

# 调用方式完全一样
llm.invoke("你好")
claude.invoke("你好")
```

**好处**：切换模型只需要改一行。**坏处**：每个模型的独特能力（Claude 的 XML 标记、GPT 的 function calling 细节）在抽象层被磨平了。

### 2️⃣ Retrieval — 检索（RAG 核心）

让 LLM 能"读书"的组件链：

```
用户问题
   ↓
文档 → 分词器 → Embedding模型 → 向量数据库 → 检索相关片段
                                                      ↓
用户问题 + 检索片段 → LLM → 基于知识的回答
```

```python
from langchain_chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

retriever = Chroma(
    collection_name="my_docs",
    embedding_function=OpenAIEmbeddings()
).as_retriever(search_kwargs={"k": 5})
```

**核心难点**：不是检索本身，而是片段大小、重排序、多轮问答的上下文管理。

### 3️⃣ Chains — 链

把多个操作串起来：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{language}专家。回答下面问题。"),
    ("human", "{question}")
])

chain = prompt | ChatOpenAI() | output_parser
result = chain.invoke({
    "language": "Python",
    "question": "解释装饰器"
})
```

**LCEL（LangChain Expression Language）**：用 `|` 操作符把组件"管道式"串联起来。这是 LangChain 最优雅的设计。

### 4️⃣ Agents — 智能体

让模型自主选择使用什么工具：

```
用户："帮我订一张明天去北京的机票"
Agent (LLM):
  ├── 思考：需要查询航班
  ├── 调用工具：search_flights("北京", "明天")
  ├── 思考：需要预订
  ├── 调用工具：book_flight("CA1234")
  └── 回复："已订好国航 CA1234 明早 8 点"
```

```python
from langchain.agents import create_openai_functions_agent

agent = create_openai_functions_agent(
    llm=llm,
    tools=[search_flights, book_flight, get_weather],
    prompt=agent_prompt
)
```

### 5️⃣ Memory — 记忆

让模型"记住"过去说了什么：

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
# 还有：SummaryMemory, VectorStoreMemory, ZepMemory...
```

**问题**：记忆管理是 AI 应用中最容易出 bug 的地方。"模型记错了之前的对话"——这类问题 LangChain 解决不了，它只是给了你一个容器。

### 6️⃣ Callbacks — 回调

监控、日志、token 计数：

```python
from langchain.callbacks import FileCallbackHandler

handler = FileCallbackHandler("trace.log")
chain.invoke({"question": "hi"}, config={"callbacks": [handler]})
```

---

## LangGraph：超越线性链条

2024 年 LangChain 发布了 **LangGraph**——一个图状（graph-based）框架。

**之前（Chain）**：
```
A → B → C → D（固定顺序）
```

**之后（Graph）**：
```
     ┌→ B ─┐
A ─→┤      ├→ C → D（条件分支）
     └→ E ─┘
```

```python
from langgraph.graph import StateGraph

graph = StateGraph(MyState)
graph.add_node("classify", classify_input)
graph.add_node("code_agent", code_agent)
graph.add_node("chat_agent", chat_agent)
graph.add_conditional_edges("classify", route_based_on_intent)
```

**什么时候用 LangGraph**：
- 你需要"if-then-else"逻辑（不是简单的链）
- 你的 Agent 需要循环、写入状态、条件跳转
- 你需要构建多 Agent 协作系统

---

## 帮 vs 害：什么时候该用 LangChain？

### ✅ 用 LangChain 的时候

| 场景 | 理由 |
|------|------|
| 快速搭建 RAG 原型 | 开箱即用的检索组件 |
| 需要频繁切换模型 | Model I/O 抽象层有用 |
| 多步骤复杂链 | LCEL 管道设计简洁 |
| 团队多人协作 | 标准化组件，降低沟通成本 |
| 需要 Agent + 工具编排 | Agent 概念模型的实现 |

### ❌ 别用 LangChain 的时候

| 场景 | 理由 |
|------|------|
| 简单的单次 LLM 调用 | 加了一层不必要的抽象 |
| 生产环境高并发 | 调试复杂，性能开销 |
| 你需要深度控制 | 抽象层会挡住你 |
| 团队只有 1 人 | 学 LangChain 的时间 > 自己写 |
| 核心功能就一个 chain | 用直接 API 调用更简单 |

---

## 一个简单的 Agent 实现

```python
from langchain_openai import ChatOpenAI
from langchain.agents import tool

@tool
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city} 今天晴，22°C"

llm = ChatOpenAI(model="gpt-4o")
agent = create_openai_functions_agent(
    llm=llm,
    tools=[get_weather],
    prompt=ChatPromptTemplate.from_messages([...])
)

agent_executor = AgentExecutor(agent=agent, tools=[get_weather])
result = agent_executor.invoke(
    {"input": "北京今天天气怎么样？需要带伞吗？"}
)
# 输出： Agent 自己决定调用 get_weather("北京") → 根据回答判断不需要带伞
```

---

> **一句话总结**：LangChain 是 AI 应用开发的"脚手架"。对快速原型和标准化大有帮助。对精简化生产可能太重。**用它的前提是你知道不用它的时候该怎么做。**
