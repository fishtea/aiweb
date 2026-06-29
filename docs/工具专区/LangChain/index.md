# LangChain

> LangChain 是一个用于构建大语言模型（LLM）应用的开发框架，提供了一套标准化的工具链来创建从简单对话到复杂 AI Agent 的各种应用。

---

## 为什么需要 LangChain？

直接使用 LLM API 构建应用时，你会遇到这些挑战：

- 如何管理多轮对话的上下文？
- 如何让模型使用外部工具（搜索引擎、数据库）？
- 如何从文档中检索相关信息（RAG）？
- 如何构建多步骤的复杂工作流？

LangChain 提供了这些问题的标准化解决方案。

---

## 核心组件

### 1. Models（模型）

统一的模型接口：

```python
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# 统一接口，切换模型只需改类名
llm = ChatOpenAI(model="gpt-4o", temperature=0)
# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
```

### 2. Prompts（提示管理）

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 {role} 专家。"),
    ("human", "{question}")
])

chain = prompt | llm
result = chain.invoke({"role": "Python", "question": "什么是装饰器？"})
```

### 3. Chains（链）

将多个组件串联为管道：

```python
from langchain_core.output_parsers import StrOutputParser

# 链：提示 → 模型 → 输出解析
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"role": "Python", "question": "解释生成器"})
```

### 4. Retrieval（检索增强生成 RAG）

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 加载文档
loader = TextLoader("document.txt")
docs = loader.load()

# 分块
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 向量化存储
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# RAG 链
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)
```

### 5. Agents（代理）

赋予模型工具使用能力：

```python
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor

@tool
def search(query: str) -> str:
    """搜索网络信息"""
    return f"搜索结果: {query}"

tools = [search]
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke({"input": "搜索今天的 AI 新闻"})
```

### 6. Memory（记忆）

管理对话历史：

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

conversation.predict(input="我叫小明")
conversation.predict(input="我叫什么名字？")  # 记住了小明
```

---

## LangGraph：更灵活的工作流

LangGraph 扩展了 LangChain 的能力，支持定义**有状态的多参与者循环图**：

```python
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

# 定义图
graph = StateGraph(MessagesState)

# 添加节点
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))

# 添加边
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

# 编译运行
app = graph.compile()
```

---

## LangSmith：全链路监控

LangSmith 提供 LLM 应用的：
- **追踪（Tracing）**：查看每次调用的完整链路
- **评估（Evaluation）**：自动化测试和评估
- **监控（Monitoring）**：生产环境的性能监控
- **数据集管理**：构建测试数据集

---

## 优势

- **生态丰富**：支持数百种模型、向量数据库、工具集成
- **标准化**：统一的接口抽象，降低切换成本
- **RAG 支持成熟**：文档加载、分块、检索等开箱即用
- **Agent 框架灵活**：ReAct、Plan-and-Execute 等多种模式
- **可观测性**：LangSmith 提供强大的调试和监控能力

## 局限

- **学习曲线**：概念较多（Chain、Agent、Tool、Memory 等）
- **抽象层较厚**：debug 时追踪多层抽象较困难
- **版本变更频繁**：API 仍在快速演进中
- **性能开销**：相比原生调用有一定性能损失

---

## 应用场景

- **智能客服**：RAG + 多轮对话
- **文档分析**：PDF 问答、合同审查
- **代码助手**：代码生成 + 工具调用
- **数据分析**：自然语言→SQL 查询
- **自动化工作流**：多步骤任务编排

---

## 下一步

- 安装 LangChain：`pip install langchain langchain-openai`
- 阅读 LangChain 官方文档
- 构建第一个 RAG 应用
- 学习 LangGraph 构建复杂工作流
- 体验 LangSmith 的追踪功能
