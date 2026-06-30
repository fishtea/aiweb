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

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:37:40*
