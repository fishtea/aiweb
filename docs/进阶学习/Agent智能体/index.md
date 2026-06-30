# Agent 智能体

> AI Agent（智能体）是能够**自主推理**并**执行行动**的 AI 系统。它通过"推理→行动→观察"的循环，与环境交互并完成复杂任务。

---

## 1. 什么是 AI Agent？

**来源：** [LangChain AI Agents: Complete Implementation Guide 2025](https://www.digitalapplied.com/blog/langchain-ai-agents-guide-2025)

AI Agent 是以大语言模型为推理引擎，通过工具调用与环境交互的系统。与传统 Chatbot 不同，Agent 能够：

- **自主规划**：分解复杂任务为子步骤
- **工具调用**：搜索、计算、操作 API
- **自我纠正**：根据观察结果调整策略
- **多步推理**：通过多轮推理-行动循环完成任务

> *"Agents built with the ReAct pattern demonstrate significantly better performance on complex queries compared to simple chain-based approaches."*

---

## 2. ReAct 模式

**来源：** [Getting Started with ReAct AI Agents using LangChain](https://www.youtube.com/watch?v=W7TZwB-KErw), [IBM LangChain Tutorial](https://www.ibm.com/think/tutorials/using-langchain-tools-to-build-an-ai-agent)

ReAct（Reasoning + Acting）是 AI Agent 最核心的设计模式。每个循环包含三个阶段：

```
1. Reasoning（推理/思考）→ 分析请求，决定下一步行动
2. Action（行动/工具调用）→ 调用具体工具，传入参数
3. Observation（观察/结果处理）→ 处理工具输出，决定下一步或给出最终答案
```

**示例循环：**
```
用户：2024 年诺贝尔物理学奖得主是谁？
Agent 思考：我需要搜索最新信息 → 使用搜索工具
Agent 行动：search("2024 Nobel Prize in Physics")
观察：[搜索结果] John J. Hopfield 和 Geoffrey E. Hinton
Agent 思考：我已获得答案 → 直接回复
Agent 回复：2024 年诺贝尔物理学奖授予了 John J. Hopfield 和 Geoffrey E. Hinton...
```

---

## 3. LangChain Agent 框架

### 3.1 LangChain vs LangGraph

**来源：** [LangChain AI Agents Guide 2025](https://www.digitalapplied.com/blog/langchain-ai-agents-guide-2025)

| 特性 | LangChain | LangGraph |
|------|-----------|-----------|
| 架构 | 线性 DAG | 基于图，支持循环 |
| 状态管理 | 链式传递 | 一等公民，持久化 |
| 人机协作 | 有限 | 内置中断与审批 |
| 调试 | 标准日志 | 时间旅行调试 |
| 适用场景 | 简单工作流、原型 | 复杂多 Agent 系统、生产环境 |

> 推荐：**原型用 LangChain，生产用 LangGraph**

### 3.2 工具定义最佳实践

```python
from langchain_core.tools import tool
from typing import Optional

@tool
def search_company_info(company_name: str, info_type: Optional[str] = "overview") -> str:
    """Search for company information from various sources.
    
    Args:
        company_name: The name of the company to search for
        info_type: Type of information to retrieve (overview, financials, news)
    
    Returns:
        Relevant company information based on the query
    """
    # implementation...
    pass
```

**工具设计要点：**
1. **清晰、描述性的名称** — 动词+名词模式（`search_database`, `calculate_price`）
2. **全面的文档字符串** — 包含目的、何时使用、参数、返回格式
3. **类型提示** — 用于生成 Schema 和验证
4. **错误处理** — 返回信息性错误消息，便于 Agent 重试或切换

### 3.3 内存与检查点

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "conversation-1"}}
```

- **MemorySaver**：仅用于开发（内存存储）
- **SqliteSaver / PostgresSaver**：生产环境持久化存储

---

## 4. Agent 类型

**来源：** [IBM AI Agents Explainer](https://www.ibm.com/think/tutorials/using-langchain-tools-to-build-an-ai-agent)

| Agent 类型 | 描述 | 适用场景 |
|-----------|------|----------|
| **ReAct Agent** | 推理-行动循环，最经典模式 | 通用任务、信息检索 |
| **Plan-and-Execute** | 先规划再执行 | 复杂多步骤任务 |
| **Multi-Agent** | 多个 Agent 协作 | 大型系统、分工协作 |
| **Reflexion Agent** | 带自我反思的 Agent | 需要持续改进的任务 |
| **Tool-Use Agent** | 专注于工具调用 | 与外部系统集成 |

---

## 5. 生产部署模式

**来源：** [LangChain Agents Guide 2025](https://www.digitalapplied.com/blog/langchain-ai-agents-guide-2025)

生产级 Agent 架构需要：

1. **流式输出** — 实时显示思考过程
2. **错误处理** — 优雅降级与重试机制
3. **可观测性** — LangSmith 等追踪工具
4. **有状态工作流** — 检查点与恢复
5. **安全边界** — 工具调用权限控制
6. **人机协作** — 关键步骤人工审批

---

## 🔗 参考资料

- [LangChain AI Agents: Complete Implementation Guide 2025](https://www.digitalapplied.com/blog/langchain-ai-agents-guide-2025)
- [Getting Started with ReAct AI Agents using LangChain - YouTube](https://www.youtube.com/watch?v=W7TZwB-KErw)
- [Introducing LangChain Agents: 2024 Tutorial - Bright Inventions](https://brightinventions.pl/blog/introducing-langchain-agents-tutorial-with-example)
- [Using LangChain Tools to Build an AI Agent - IBM](https://www.ibm.com/think/tutorials/using-langchain-tools-to-build-an-ai-agent)
- [Learn to Build AI Agents with LangChain - Reddit](https://www.reddit.com/r/LangChain/comments/1f6jknc/learn_how_to_build_ai_agents_react_agent_from/)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 10:42:21*
*资源区块更新时间：2026-06-30 10:25:06*
