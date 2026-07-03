# 👥 多 Agent 协作

设计多智能体协作系统，让多个专业 AI Agent 分工合作，完成复杂任务。

---

## 📖 概述

单个 Agent 能力有限。当任务涉及多个专业领域时，多 Agent 系统的优势就显现出来了。通过将不同角色分配给不同 Agent，每个 Agent 专注于特定的任务，最终通过协作产出更高质量的结果。

> 来源：[Multi-Agent Orchestration Guide — Digital Applied](https://www.digitalapplied.com/blog/ai-agent-orchestration-workflows-guide)

### 为什么需要多 Agent？

| 问题 | 单 Agent | 多 Agent |
|------|---------|---------|
| 角色混淆 | 一个 Agent 承担所有角色 | 每个 Agent 专精一个角色 |
| 上下文超长 | 对话越长 token 越多 | 各自维护独立上下文 |
| 错误蔓延 | 一个判断失误影响全局 | 多 Agent 相互校验 |
| 可扩展性 | 加功能需要改代码 | 加一个 Agent 即可 |

---

## 🏗️ 主流框架对比

目前三大主流多 Agent 框架：

| 框架 | 开发商 | 设计哲学 | 适用场景 | 学习曲线 |
|------|--------|---------|---------|---------|
| **CrewAI** | CrewAI Inc. | 角色分工制（Crew） | 内容生产、研究分析 | 低 |
| **AutoGen** | Microsoft | 对话式多 Agent | 编程、数据分析 | 中 |
| **LangGraph** | LangChain | 有状态图流程 | 生产级复杂工作流 | 高 |

> 来源：[AutoGen vs CrewAI vs LangGraph — 2025 全面对比](https://www.youtube.com/watch?v=8HqeY5v0ohM)

---

## 👥 CrewAI 实战：博客创作团队

CrewAI 的设计模式最直观：定义 Agent → 分配任务 → 组建 Crew → 运行。

### 定义 Agent 角色

```python
from crewai import Agent

planner = Agent(
    role="内容策划师",
    goal="规划博客文章结构和关键主题",
    backstory="你是经验丰富的内容策略专家，擅长将复杂话题拆解成清晰的叙述结构",
    llm="gpt-4o",
    verbose=True
)

writer = Agent(
    role="技术作者",
    goal="根据大纲撰写技术博客的正文内容",
    backstory="你是资深的技术写作专家，能将技术概念转化为通俗易懂的文章",
    llm="gpt-4o",
    verbose=True
)

editor = Agent(
    role="编辑",
    goal="审核并优化文章，确保逻辑连贯、语法正确、风格一致",
    backstory="你是苛刻的编辑，追求完美，擅长润色和纠错",
    llm="gpt-4o",
    verbose=True
)
```

### 定义任务

```python
from crewai import Task

plan_task = Task(
    description="为 'RAG Agent 构建指南' 写一个详细的大纲",
    expected_output="包含引言、5个主要章节和结论的大纲",
    agent=planner
)

write_task = Task(
    description="根据大纲撰写博客正文，包含代码示例",
    expected_output="完整的博客草稿",
    agent=writer
)

edit_task = Task(
    description="审核草稿，修改不通顺、不准确的部分",
    expected_output="最终润色后的博客",
    agent=editor
)
```

### 组建 Crew 并运行

```python
from crewai import Crew

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan_task, write_task, edit_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

### 运行流程

```
规划（策划师）→ 撰写（作者）→ 审核（编辑）
                              ↓
                     产出最终文章
```

> 来源：[CrewAI 多 Agent 教程 — MLWorks](https://www.youtube.com/watch?v=viH5CDG4vWM)

---

## 🔄 LangGraph：更灵活的有状态编排

LangGraph 适合需要复杂循环和状态管理的场景，提供更精细的控制。

### 核心概念

- **Node** — 每一个 Agent 或处理步骤
- **Edge** — 节点之间的连接
- **State** — 在节点间传递的共享状态
- **Conditional Edge** — 基于状态的条件跳转

### 示例：多步研究 Agent

```python
from langgraph.graph import StateGraph

# 定义状态
class ResearchState(TypedDict):
    question: str
    search_results: list
    analysis: str
    report: str

# 定义步骤
def search_web(state):    # → 搜索
def analyze_results(state):  # → 分析
def write_report(state):   # → 报告撰写
def review_report(state):  # → 审查返回修改或结束

# 构建图
graph = StateGraph(ResearchState)
graph.add_node("search", search_web)
graph.add_node("analyze", analyze_results)
graph.add_node("write", write_report)
graph.add_node("review", review_report)

graph.add_conditional_edges(
    "review",
    should_continue,  # 如果质量不够，回到 search
    { "continue": "write", "end": "__end__" }
)
```

---

## 💡 最佳实践

### 1. 角色设计原则

- **职责不重叠** — 每个 Agent 负责明确的范围
- **输出标准化** — 让 Agent 输出结构化格式（JSON/Markdown）
- **设定边界** — Agent 超出能力范围时应明确表示

### 2. 成本控制

- 选择不同档次的模型：复杂分析用 GPT-4o，简单任务用 GPT-4o-mini
- 设置最大迭代次数，防止无限循环
- 缓存 Agent 中间结果

### 3. 错误处理

- 为每个 Agent 设置超时和重试机制
- 实现"人类确认"节点，对关键决策进行人工干预
- 记录完整运行日志，方便排查问题

### 4. 框架选择建议

| 你的需求 | 推荐框架 |
|---------|---------|
| 快速原型、内容生成 | CrewAI |
| 数据分析、编程辅助 | AutoGen |
| 生产级复杂编排 | LangGraph |
| 想自己控制一切 | 自定义 Agent 框架 |

### 多 Agent 协作的核心模式

抛开具体框架，多 Agent 系统的协作关系可归纳为几种经典模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **流水线（Pipeline）** | Agent 依次处理，上一个的输出是下一个的输入 | 写作→编辑→校对 |
| **路由分发（Router）** | 一个调度 Agent 把任务分给最合适的专家 Agent | 客服按意图分流 |
| **辩论/投票（Debate）** | 多个 Agent 各自作答再投票，取共识 | 高准确率要求的事实问答 |
| **主管-工人（Supervisor-Worker）** | 主管拆解任务派发，工人执行后汇报 | 复杂研究、报告生成 |
| **层级（Hierarchical）** | 多层管理，上层规划下层执行 | 大型自动化运营 |

> 关键权衡：多 Agent 能提升质量和分工，但每多一个 Agent 就多一轮 LLM 调用，成本和延迟成倍上升。生产中要警惕"为了多 Agent 而 Agent"——很多时候单 Agent + 好的提示词就够了。

---

## 📚 参考来源

- [AI Agent Orchestration Guide — Digital Applied](https://www.digitalapplied.com/blog/ai-agent-orchestration-workflows-guide)
- [CrewAI Multi-Agent Tutorial — MLWorks (YouTube)](https://www.youtube.com/watch?v=viH5CDG4vWM)
- [AutoGen vs CrewAI vs LangGraph 2025 Comparison (YouTube)](https://www.youtube.com/watch?v=8HqeY5v0ohM)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

## 🆕 2026 最新进展

### 2026：多 Agent 从研究概念走向生产实践

2025-2026 年是多 Agent 系统的分水岭。根据 [多智能体协作入门：概念、模式与上手路径](https://wcowin.work/develop/AI/multi-agent) 的总结，多 Agent 已从学术概念进入实际工程讨论——**但是否值得采用，关键看任务复杂度和协调成本**。核心原则：小任务优先用单 Agent，复杂任务再上多智能体。

### 三大新趋势

#### 1. 扁平路由模型（OpenClaw）
传统的层级管理模型（一个 Supervisor Agent 调度多个 Worker）不再是唯一选择。OpenClaw 采用的**扁平路由模型**让 Gateway 根据消息来源直接路由到对应 Agent，没有"管理者 Agent"：

```
消息源（Discord/Telegram/Slack）→ Gateway → 按 channel 路由 → 对应 Agent
```

每个 Agent 通过 `channel routing` 配置绑定到不同频道，各司其职——编程问题由编程 Agent 处理，生活问题由生活 Agent 处理。

> 来源：[GitHub: OpenClaw 多Agent协作指南](https://github.com/KimYx0207/AI-Coding-Guide-Zh/blob/main/docs/openclaw/08-%E5%A4%9AAgent%E5%8D%8F%E4%BD%9C%E6%8C%87%E5%8D%97.md)

#### 2. Google ADK 多 Agent 系统
Google 的 **Agent Development Kit (ADK)** 提供了三种 Agent 类型：

| Agent 类型 | 说明 | 适用场景 |
|-----------|------|---------|
| LLM Agent | 纯 LLM 驱动的 Agent，支持工具调用 | 通用对话、问答 |
| Workflow Agent | 预定义工作流，确定性执行 | 数据管道、审批流程 |
| Custom Agent | 完全自定义逻辑 | 有特殊业务规则的场景 |

ADK 支持层级结构（Hierarchical），上层 Agent 可委派子任务给下层 Agent，通过结构化的通信机制传递上下文和结果。

> 来源：[Google Cloud: Building Collaborative AI — Multi-Agent Systems with ADK](https://cloud.google.com/blog/topics/developers-practitioners/building-collaborative-ai-a-developers-guide-to-multi-agent-systems-with-adk)

#### 3. 协作架构四模式标准化

2026 年，多 Agent 协作的架构模式已收敛为四种核心形态：

| 模式 | 工作方式 | 典型框架 | 适用场景 |
|------|---------|---------|---------|
| **流水线（Pipeline）** | Agent 依次处理，前一个输出是后一个输入 | CrewAI Sequential | 写作→编辑→审核 |
| **路由分发（Router）** | 调度 Agent 按意图分发到专家 Agent | Dify 工作流 | 客服系统 |
| **辩论/投票（Debate）** | 多 Agent 独立作答，投票取共识 | AutoGen GroupChat | 高准确率问答 |
| **层级管理（Hierarchical）** | 主管拆解任务、工人执行、主管汇总 | Google ADK, LangGraph | 复杂研究、报告生成 |

### 2026 框架全景对比

| 框架 | 最新定位 | 核心优势 | 2026 年重点 |
|------|---------|---------|------------|
| **LangGraph** | 生产级编排引擎 | 图结构、条件分支、状态持久化 | 复杂工作流的可靠性 |
| **CrewAI** | 角色分工型 | 低代码、快速原型、高层 API | 业务编排、内容生产 |
| **AutoGen** | 对话式协作 | 多 Agent 对话、灵活模式 | 微软生态集成 |
| **Dify** | 可视化工作流 | 拖拽式编排，零代码入门 | 多 Agent 工作流 + RAG + MCP |
| **MetaGPT** | 虚拟软件公司 | Code=SOP(Team)，从需求到代码 | 软件开发自动化 |
| **ChatDev** | 研究导向 | 清华开源，模拟完整软件团队 | 教学研究 |
| **OpenClaw** | 扁平路由 | 无中心调度，消息源路由 | 多平台 Agent 矩阵 |

### 生产实践：成本与可靠性

多 Agent 系统的最大挑战不是技术而是**成本**——每多一个 Agent 就多一轮 LLM 调用，延迟和 token 消耗成倍上升。2026 年的最佳实践：

1. **混合模型策略**：复杂推理用强模型（GPT-4o/Claude），简单任务用轻模型（GPT-4o-mini/Haiku）
2. **上下文压缩**：多 Agent 传递时对历史对话做摘要，避免上下文膨胀
3. **步数上限**：每个 Agent 和整个编排流程都设硬上限，防止死循环
4. **人工确认节点**：关键决策（如发邮件、修改数据库）前插人工审批

> 来源：[DEV Community: 多Agent协作架构模式实战](https://dev.to/marufhassan/multi-agent-collaboration-architecture-patterns-a-practical-guide-from-hierarchical-planning-to-dynamic-orchestration-55gg)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-04 00:07:49*
