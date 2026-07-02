# LangChain — LLM 应用开发框架

> LangChain 是一个开源的 LLM 应用开发框架，提供了构建 AI Agent、RAG（检索增强生成）和 LLM 工作流所需的完整工具链。2025 年 10 月，LangChain 1.0 和 LangGraph 1.0 同时发布稳定版本。

---

## 工具概述

| 属性 | 详情 |
|------|------|
| **开发者** | LangChain Inc. |
| **首次发布** | 2022 年 |
| **最新版本** | LangChain 1.0 (2025.10) |
| **许可** | MIT |
| **主要语言** | Python, TypeScript |
| **GitHub** | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) |

---

## 生态架构

根据 [LangChain 官方文档](https://docs.langchain.com/oss/python/langgraph/overview) 和 [LangGraph 1.0 指南](https://ai.plainenglish.io/the-complete-guide-to-langchain-langgraph-2025-updates-and-production-ready-ai-frameworks-58bdb49a34b6)：

### 核心组件

| 组件 | 功能 | 状态 |
|------|------|------|
| **LangChain** | LLM 应用框架（链、代理、RAG） | 1.0 稳定版 |
| **LangGraph** | Agent 编排运行时 | 1.0 稳定版 |
| **LangSmith** | 可观测性和评估平台 | 商业产品 |
| **LangServe** | AI 应用部署 | 集成在 LangGraph 中 |

### LangChain 1.0 关键变化

- 简化核心 API，移除冗余抽象
- 新的 `create_agent` 方法替代 `create_react_agent`
- 标准化的工具调用接口
- 更好的流式支持

### LangGraph 1.0 核心特性

根据 [LangGraph 官方概览](https://docs.langchain.com/oss/python/langgraph/overview)：

- **持久化执行:** 支持状态持久化、中断和恢复
- **流式处理:** 实时输出流，适合对话式应用
- **Human-in-the-Loop:** 支持人工审核和干预
- **时间旅行:** 回溯到任何历史状态分支重试
- **错误容忍:** 内置容错机制

### Agent 架构演进：从 ReAct 到 LangGraph

LangChain 生态的 Agent 设计经历了明显代际更替：

| 代际 | 代表 | 特点 |
|------|------|------|
| 早期 AgentExecutor | `create_react_agent` + AgentExecutor | 基于 ReAct 提示词，循环固定 |
| Tool Calling Agent | `create_tool_calling_agent` | 依赖模型原生函数调用，更稳定 |
| LangGraph Agent | `create_agent` / 自定义图 | 显式状态图，可控循环、检查点、人机协作 |

> 建议：新项目直接从 LangGraph 开始，AgentExecutor 已逐步被标记为遗留。LangGraph 的图结构让 Agent 的循环、分支、中断、恢复都变得显式可调试。

---

## LangGraph — Agent 编排

LangGraph 是 LangChain 生态的 Agent 编排引擎，将 Agent 工作流建模为**有向图（Graph）**：

- **节点（Nodes）:** LLM 调用、工具执行、条件判断
- **边（Edges）:** 控制流和数据流
- **状态（State）:** 全局状态管理与持久化

### 快速示例

```python
from langgraph.graph import StateGraph, MessagesState
from langchain_openai import ChatOpenAI

# 定义图
graph = StateGraph(MessagesState)

# 添加节点
def call_model(state):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph.add_node("agent", call_model)

# 编译并运行
app = graph.compile()
result = app.invoke({
    "messages": [("user", "你好！")]
})
```

---

## 企业级应用

根据 [LangChain 官方用户案例](https://www.langchain.com/langgraph)，LangChain 被以下企业用于生产环境：

- **Uber:** 客户支持自动化
- **LinkedIn:** AI 驱动的推荐
- **Klarna:** 智能客服机器人
- **JP Morgan:** 金融文档分析

---

## 如何开始

### 安装

```bash
pip install langchain langgraph
# 或特定 LLM 的绑定
pip install langchain-openai langchain-anthropic
```

### 基础使用

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke([HumanMessage(content="用中文解释什么是 RAG？")])
print(response.content)
```

---

## 优势与局限

**优势:**
- 最成熟的 LLM 应用框架之一
- LangGraph 提供生产级 Agent 编排
- 丰富的模型和工具集成（30+ 模型提供商）
- 企业级可观测性（LangSmith）
- 活跃的社区和文档

**局限:**
- 学习曲线中高（抽象层次多）
- 1.0 版本仍有 API 不兼容变更
- 简单任务可能过度复杂（过度抽象）
- 调试较困难

---

**参考资料：**
- [LangGraph Overview (LangChain Docs)](https://docs.langchain.com/oss/python/langgraph/overview)
- [The Complete Guide to LangChain & LangGraph 2025 (PlainEnglish)](https://ai.plainenglish.io/the-complete-guide-to-langchain-langgraph-2025-updates-and-production-ready-ai-frameworks-58bdb49a34b6)
- [LangChain Official Site](https://www.langchain.com/langgraph)
- [LangGraph Tutorial for Beginners (DataCamp)](https://www.youtube.com/watch?v=UklCxmEvz2w)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

- **[LangChain 教程：构建您的第一个 LLM 应用程序（2026）|我的工程之路](https://myengineeringpath.dev/tools/langchain-tutorial)**
  - 来源：`myengineeringpath.dev` · 质量分：10 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # LangChain 教程：构建您的第一个 LLM 应用程序（2026）。 **LangChain 是用 Python 构建 LLM 支持的应用程序的最流行的框架 - 本教程可让您在 20 分钟内从零开始构建一个可运行的应用程序。** 您将构建三样东西：一个简单的链、一个 RAG 管道和一个工具调用代理。最后，您将了解 LangChain 的核心抽象以及何时使用每个抽象。您需要构建一个由法学硕士支持的功能。原始 OpenAI SDK ...

- **[LangChain Python 教程：2026 年完整指南 - JetBrains 博客](https://blog.jetbrains.com/pycharm/2026/02/langchain-tutorial-2026)**
  - 来源：`blog.jetbrains.com` · 质量分：10 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - 如果您阅读过博客文章*如何使用 LangChain 构建聊天机器人*，您可能想了解更多有关 LangChain 的信息。这篇博文将深入探讨 LangChain 提供的功能，并指导您完成一些更多的实际用例。即使您还没有阅读第一篇文章，您仍然可能会发现本文中的信息有助于构建您的下一个人工智能代理。 Let’s have a look at what LangChain is. LangChain 提供了一个标准框架，用于构建由法学硕士支持的...

- **[使用LangChain构建RAG代理](https://docs.langchain.com/oss/python/langchain/rag)**
  - 来源：`docs.langchain.com` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - 2. **RAG 代理**：一种通用实现，用于搜索索引内容并将相关上下文传递给 LLM。 3. **Embed**：Embeddings模型将每个块转换为捕获其含义的数字向量，从而实现对内容的相似性搜索。 VectorStore 会保留文档块及其嵌入，从而在用户提出问题时启用相似性搜索来检索相关部分。 2. **生成**：模型 使用包含问题和检索到的数据的提示生成答案。 ！图片4：检索图这个本教程介绍了该流程的两种实现：一个在需要时调用...

- **[使用 LangGraph 构建自定义 RAG 代理 - LangChain 提供的文档](https://docs.langchain.com/oss/python/langgraph/agentic-rag)**
  - 来源：`docs.langchain.com` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # 使用 LangGraph 构建自定义 RAG 代理。在本教程中，我们将使用 LangGraph 构建一个检索代理。当您希望法学硕士决定是从矢量存储中检索上下文还是直接响应用户时，检索代理非常有用。在本教程结束时，我们将完成以下操作： 2. 为这些文档建立索引以进行语义搜索，并为代理创建检索器工具。 3. 构建一个代理 RAG 系统，可以决定何时使用检索器工具。它将调用 LLM 根据当前图形状态（消息列表）生成响应。给定输入消息，它将...

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-02 11:56:59*
