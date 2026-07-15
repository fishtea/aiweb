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

### Google ADK 层级架构深入分析

Google 的 **Agent Development Kit (ADK)** 在 2025 年 11 月发布后，至 2026 年已成为多 Agent 系统的重要选择。其核心架构基于清晰的层级结构（Hierarchy）：

#### 三种 Agent 类型

| Agent 类型 | 角色 | 适用场景 |
|-----------|------|---------|
| **LLM Agent** | "大脑"——用 Gemini 理解自然语言、推理并决策 | 通用对话、问答、工具调用 |
| **Workflow Agent** | "经理"——编排任务执行流程，不执行实际工作 | 数据管道、审批流程、多步自动化 |
| **Custom Agent** | "专家"——继承 BaseAgent 实现自定义逻辑 | 特殊业务规则、遗留系统集成 |

#### 层级管理规则

ADK 的 Agent 层级模拟企业组织架构：

```
根 Agent (CEO)
  ├── 子 Agent-1 (VP of Research)
  │   ├── 子 Agent-1a (Director)
  │   └── 子 Agent-1b (Director)
  └── 子 Agent-2 (VP of Engineering)
      └── 子 Agent-2a (Manager)
```

**两条核心规则**：
1. **父 Agent 管理子 Agent**：父级可委派任务给子级
2. **单亲规则**：每个 Agent 只能有一个父级，确保职责清晰

#### 三种预编排器

| 编排器 | 工作方式 | 适用场景 |
|--------|---------|---------|
| **SequentialAgent** | 子 Agent 按序运行，前一个输出为后一个输入 | 多步管道：提取数据→分析→生成报告 |
| **其他编排器** | 可扩展自定义 | 复杂条件分支、人工审批节点 |

> 来源：Google Cloud Blog — Building Collaborative AI: A Developer's Guide to Multi-Agent Systems with ADK（Annie Wang, 2025.11）

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

## 2026年多Agent框架实战对比：CrewAI vs LangGraph vs AutoGen

### 2026年的多Agent格局

2026年，单一模型的AI应用已经像在记事本里写代码——能用，但90%的潜力未被释放。真正的转变是由专业化Agent网络协作完成复杂任务：一个Agent做研究、一个做写作、一个做审查、一个做执行——每个Agent专精一个环节，最终产出的质量是单Agent无法企及的。

基础设施在2026年已经成熟：GPT-4o、Claude 3.7、Gemini 2.0 Flash的推理成本自2023年以来下降超80%，运行5-Agent管线的成本已低于$0.10/次；LangGraph等框架确立了有状态Agent的生产标准。

> 来源：[DEV Community — Multi-Agent AI in 2026: Build Production Systems with CrewAI, LangGraph & AutoGen](https://dev.to/ottoaria/multi-agent-ai-in-2026-build-production-systems-with-crewai-langgraph-autogen-5e40)

### 三大框架最新定位

| 框架 | 开发商 | 2026年定位 | 最适合 | 学习曲线 |
|------|--------|----------|--------|---------|
| **CrewAI** | CrewAI Inc. | 业务自动化首选 | 内容生产、研究分析、营销自动化 | 低 |
| **LangGraph** | LangChain | 复杂状态机 | 需要分支逻辑、人机协作、条件流的应用 | 中-高 |
| **AutoGen v0.4** | Microsoft | 对话式多Agent | Agent间需要来回对话协作的任务 | 中 |

### CrewAI：业务自动化首选

CrewAI 是三者中最易上手的。只需定义Agent和Task，框架自动处理编排。2026年典型用法：

```python
# 定义角色
researcher = Agent(role="研究员", goal="分析最新AI进展",
                   tools=[SerperDevTool()], llm="gpt-4o-mini")
writer = Agent(role="内容策略师", goal="创作引人入胜的内容",
               llm="gpt-4o")

# 定义任务链
research_task = Task(description="分析最新AI趋势，找出关键突破",
                     agent=researcher)
write_task = Task(description="基于研究撰写博客文章，易懂不术语",
                  agent=writer)

# 启动协作
crew = Crew(agents=[researcher, writer],
            tasks=[research_task, write_task])
crew.kickoff()
```

**成本参考**：研究用 gpt-4o-mini、写作用 gpt-4o，一次完整运行约 $0.03-0.05。

### LangGraph：复杂状态机

LangGraph 更冗长但给予开发者对状态和路由的完全控制，适合需要分支逻辑、人工审批或条件流的应用。

**2026年典型应用场景**：
- 代码审查机器人：安全Agent → 性能Agent → 报告Agent
- 客服分流：自动分类 → 知识库检索 → 回复 → 升级判断 → 人工接管
- 研究管线：带回退逻辑的多步研究 + 人工审核节点

### AutoGen v0.4：对话式协作

AutoGen v0.4 是微软的框架，核心特点是**Agent间可以像人类一样对话**。一个Agent生成代码，另一个Agent执行它，发现bug后回传给第一个Agent修复——完全自主。

**典型模式**：
```
User → CoderAgent(写代码) → ExecutorAgent(执行+报错)
  → CoderAgent(修复bug) → ExecutorAgent(验证通过)
  → User(收到正确的代码)
```

### 五大经过生产验证的多Agent蓝图

以下模式来自真实生产部署：

| # | 蓝图 | Agent链 | 产出 |
|---|------|---------|------|
| 1 | **内容工厂** | 趋势侦察→内容策略→写手→SEO编辑→社交媒体经理 | 完整文章+SEO数据+5条推文+1篇LinkedIn |
| 2 | **销售情报** | 网站爬虫→新闻聚合→技术栈检测→痛点识别→报告生成 | 销售通话前的个性化简报 |
| 3 | **代码审查流水线** | 安全审查→性能审查→报告撰写 | 带评分的人前结构化审查 |
| 4 | **客服自动化** | 分类器→文档检索→回复→升级检查→发送 | 80-90%的一线工单自动处理 |
| 5 | **投资研究** | 新闻分析→技术分析→基本面Agent→组合经理 | 每日邮件：组合健康评分+风险标记 |

### 生产基础设施清单

```
1. 混合模型策略：非关键步骤用便宜模型
   研究→gpt-4o-mini | 写作→gpt-4o | 审查→Claude

2. 错误处理：每个Agent调用包裹try-catch
   失败重试3次，指数退避

3. 监控日志：Langfuse / Weave 追踪每一次LLM调用
   成本、延迟、成功率实时看板

4. 人工审批：关键操作前插入确认节点
   发邮件、修改数据库 → 人工确认

5. 步数上限：每个Agent和整个编排流设硬上限
   防止死循环烧钱
```

### 商业机会：多Agent = 新产品

| 想法 | 描述 | 定价 |
|------|------|------|
| 自动化内容工厂 | 每周自动发布5篇文章，AdSense+联盟营销 | $500-2000/月被动收入 |
| AI销售研究 | 通话前自动研究潜在客户 | €49/次搜索 |
| 代码审查SaaS | GitHub集成，自动多维度审查 | €29/月/seat |
| AI投资顾问 | 个性化加密/股票研究 | €9/月 |
| AI客服白标 | 80%一线工单自动处理 | 按工单定价 |

**行动路线**：先构建蓝图1（内容工厂）→ 部署蓝图2或3供自己使用 → 挑表现最好的Agent加cron定时+Slack通知+FastAPI包装 → 找到外部需求最强的用例 → 5个beta用户免费测试 → 定价$29-99/月 → 目标10个付费用户。

> 来源：[DEV Community — Multi-Agent AI in 2026: Build Production Systems with CrewAI, LangGraph & AutoGen](https://dev.to/ottoaria/multi-agent-ai-in-2026-build-production-systems-with-crewai-langgraph-autogen-5e40)

---

## 🏭 2026 多 Agent 框架新格局

### 六强争霸：2026 框架全景

2026 年，多 Agent 框架生态已从"三足鼎立"进入"六强争霸"。构建多 Agent 系统不再是从 LangGraph/CrewAI/AutoGen 三选一——OpenAI、Google 和 Anthropic 都已加入战场：

| 框架 | 开发商 | 发布/成熟时间 | 核心抽象 | 最适合 |
|------|--------|------------|---------|--------|
| **OpenAI Agents SDK** | OpenAI | 2025.03 | Handoff（交接） | 基于 GPT 的 Agent 编排 |
| **LangGraph** | LangChain | 2024+ 持续迭代 | 有状态图（StateGraph） | 需要复杂条件分支的生产系统 |
| **CrewAI** | CrewAI Inc. | 2024+ 持续迭代 | 角色分工（Role+Task） | 内容生产、研究分析自动化 |
| **AutoGen/AG2** | Microsoft | v0.4 (2025) | 对话式协作 | Agent 间需要来回对话的场景 |
| **Google ADK** | Google | 2025.04 | 层级结构（Hierarchical） | Gemini 生态、企业级部署 |
| **Claude Agent SDK** | Anthropic | 2026 (随 Claude 4.6) | 原生工具调用 | Claude 生态、安全优先场景 |

> 来源：[GuruSup — Best Multi-Agent Frameworks 2026](https://gurusup.com/blog/best-multi-agent-frameworks-2026)、[RankSquire — Open Source AI Agent Frameworks 2026](https://ranksquire.com/2026/05/03/open-source-ai-agent-frameworks-2026/)

### 新入局者详解

#### OpenAI Agents SDK：Handoff 模式的工业化

2025 年 3 月，OpenAI 发布了 Agents SDK，取代了实验性的 Swarm 框架。其核心设计哲学是 **Handoff（交接）**——Agent 之间显式地转移控制权，同时传递对话上下文。

核心三原语：
- **Handoffs**：Agent→Agent 任务转移（类似队列分配模式）
- **Guardrails**：输入/输出验证护栏
- **Tracing**：端到端可观测性

典型模式是"分流→专项"：一个分流 Agent 接收用户输入 → 判断意图 → 交接给专项 Agent（账单、技术支持、账户管理）→ 专项 Agent 可返回控制权或继续交接。

#### Google ADK：层级结构的企业级方案

Google 的 Agent Development Kit (ADK) 采用企业管理式的**层级结构**：

```
根 Agent (CEO)
  ├── 研究 Agent (VP)
  │   ├── 文献检索 Agent
  │   └── 数据分析 Agent
  └── 工程 Agent (VP)
      ├── 代码生成 Agent
      └── 测试 Agent
```

核心规则：
- **父管子**：父 Agent 委派任务给子 Agent
- **单亲制**：每个 Agent 只有一个父级，职责清晰
- **SequentialAgent 编排器**：子 Agent 按序运行，前一个输出为后一个输入

#### Claude Agent SDK：安全优先

Anthropic 随 Claude 4.6 发布了 Agent SDK，强调**安全约束下的工具调用**——原生支持的宪法 AI（Constitutional AI）护栏和引用溯源，特别适合金融、医疗等监管严格的领域。

### 生产验证：什么真正活了下来

根据 [Multi-Agent in Production in 2026: What Actually Survived](https://medium.com/@Micheal-Lanham/multi-agent-in-production-in-2026-what-actually-survived-f86de8bb1cd1) 的生产数据分析：

| 发现 | 影响 |
|------|------|
| ✅ **集中式协调**在可并行化任务上提升 80.9% | 任务可拆解 → 多 Agent 真有价值 |
| ❌ **顺序规划任务**上每个多 Agent 变体都**退化 39-70%** | 串行任务 → 单 Agent 更好 |
| ⚠️ 大多数多 Agent 部署是"过度工程" | 降级到单 Agent 后效果反而更好 |
| ✅ Graph-based 编排（LangGraph）在故障恢复和合规上表现最佳 | 生产环境优先考虑可靠性 |

**核心教训**：多 Agent 不是免费的午餐。在决定使用多 Agent 之前，先问自己：任务是否可并行拆解？是否真的需要不同专业的 Agent？单 Agent + 好的提示词能否解决？

### 框架选型决策矩阵（2026）

| 判断条件 | 推荐 | 理由 |
|---------|------|------|
| 任务可并行拆解 | CrewAI / OpenAI SDK | 流水线和 Handoff 开销最低 |
| 需要复杂分支逻辑 | LangGraph | 图结构 + 条件边 + 状态持久化 |
| Agent 间需要来回对话 | AutoGen / AG2 | 对话式协作原语 |
| Gemini 生态 | Google ADK | 原生集成，层级管理 |
| 监管严格（安全/合规） | Claude SDK / LangGraph | 护栏 + 可审计的决策链 |
| 快速原型 | CrewAI | 最低学习曲线 |
| 不确定是否需要多 Agent | **单 Agent 先上线** | 大多数情况不需要多 Agent |

### 多 Agent 生产成本速算

```
5-Agent 管线成本参考（2026）：
- 研究 Agent：gpt-4o-mini → ~$0.005
- 写作 Agent：gpt-4o → ~$0.02
- 审查 Agent：claude-3.5-haiku → ~$0.005
- SEO Agent：gpt-4o-mini → ~$0.005
- 发布 Agent：gpt-4o-mini → ~$0.005
总计：~$0.04/次

每月 1000 次运行 ≈ $40
推理成本自 2023 年下降 >80%
```

> 来源：[DEV Community — Multi-Agent AI in 2026](https://dev.to/ottoaria/multi-agent-ai-in-2026-build-production-systems-with-crewai-langgraph-autogen-5e40)、[Medium — Multi-Agent in Production in 2026](https://medium.com/@Micheal-Lanham/multi-agent-in-production-in-2026-what-actually-survived-f86de8bb1cd1)

### 五大经过生产验证的多 Agent 蓝图

以下蓝图来源于 2026 年真实生产部署，每个都包含 Agent 链、产出物和成本参考数据：

| # | 蓝图名称 | Agent 链 | 产出物 | 每次成本 | 耗时 |
|---|---------|---------|--------|---------|------|
| 1 | **AI 内容工厂** | 趋势侦察 → 内容策略 → 写手 → SEO 编辑 → 社交媒体经理 | 完整文章 + SEO 数据 + 5 条推文 + LinkedIn 帖子 | ~$0.05 | ~3 分钟 |
| 2 | **自动化销售情报** | 网站爬虫 → 新闻聚合 → 技术栈检测 → 痛点识别 → 报告生成 | 销售通话前的个性化客户简报 | ~$0.08 | ~5 分钟 |
| 3 | **代码审查流水线** | 安全审查 → 性能审查 → 报告撰写 | 结构化审查报告+各维度评分（PR 自动触发） | ~$0.15 | ~2 分钟 |
| 4 | **客服自动化** | 分类器 → 文档检索 → 回复 → 升级检查 → 发送 | 80-90% 一线工单自动处理 | ~$0.03 | ~30 秒 |
| 5 | **每日投资研究简报** | 新闻分析 → 技术分析 → 基本面分析 → 组合经理汇总 | 每日邮件：组合健康评分+风险标记 | ~$0.12/天 | ~1 分钟 |

#### 蓝图 1 实战：AI 内容工厂（最适合入门）

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# 角色定义（混合模型策略降低成本）
researcher = Agent(
    role="趋势侦察员",
    goal="发现 AI 领域的最新发展和趋势",
    tools=[SerperDevTool()],
    llm="gpt-4o-mini"  # 研究用轻量模型
)
writer = Agent(
    role="技术写手",
    goal="基于研究成果撰写引人入胜的博客",
    llm="gpt-4o"       # 写作用强模型
)
editor = Agent(
    role="SEO 编辑",
    goal="审核并优化文章 SEO",
    llm="gpt-4o-mini"
)

# 任务链
tasks = [
    Task(description="搜索 AI 最新趋势，找出 5 个关键突破",
         expected_output="包含来源和分析的研究报告", agent=researcher),
    Task(description="根据研究撰写 4 段博客文章",
         expected_output="完整的博客文章", agent=writer),
    Task(description="添加 SEO 元数据并审核",
         expected_output="最终 SEO 优化版本", agent=editor)
]

crew = Crew(agents=[researcher, writer, editor],
            tasks=tasks, process=Process.sequential)
result = crew.kickoff()
```

**关键优化**：研究用 `gpt-4o-mini`（$0.15/百万 token）节省 90% 成本，写作和编辑用更强的模型保证质量。

#### 生产部署检查清单

```yaml
# 2026 年多 Agent 系统生产基础设施
1. 混合模型策略:
   研究/分类 → gpt-4o-mini | 写作/推理 → gpt-4o | 审查 → Claude

2. 错误处理:
   每个 Agent 调用包裹 try-catch
   失败重试 3 次，指数退避（4s → 8s → 16s）

3. 可观测性:
   Langfuse / LangSmith 追踪每一次 LLM 调用
   成本、延迟、成功率实时看板

4. 人工审批:
   写操作（发邮件、改数据库）前插入 human-in-the-loop 节点

5. 步数上限:
   每个 Agent max_iter=5，整体编排设最大轮次
   防止死循环烧钱
```

> 来源：[DEV Community — Multi-Agent AI in 2026: Build Production Systems](https://dev.to/ottoaria/multi-agent-ai-in-2026-build-production-systems-with-crewai-langgraph-autogen-5e40)

---

## 🔄 CrewAI Flows：事件驱动的多 Agent 编排（v1.15.2 新架构）

CrewAI 在 v1.15 版本引入了 **Flows** 架构，这是对传统 Agent/Task/Crew 模型的重大升级。Flows 提供了**声明式、事件驱动的工作流编排**，用 `@start()` 和 `@listen()` 装饰器定义任务依赖关系，让多 Agent 协作从"顺序排列"升级为"响应式编排"。

> 来源：[CrewAI Flows 官方文档](https://docs.crewai.com/concepts/flows)

### Flows vs 传统 Crew 对比

| 维度 | 传统 Crew (旧 API) | Flows (新架构) |
|------|-------------------|---------------|
| 编排模型 | 顺序/层级 Process | 事件驱动 `@listen()` |
| 状态管理 | 手动传递 | Pydantic BaseModel 自动持久化 |
| 并行支持 | 有限（层级模式） | 原生支持多 `@start()` 并行 |
| 条件分支 | 需自定义 Manager Agent | `@start(condition=...)` + `or_` / `and_` 路由 |
| 可观测性 | 外部工具 | 内建 `flow.plot()` 生成流程图 |
| Human-in-the-Loop | 黑盒 | Flow 级别显式控制 |

### 核心概念：@start() 和 @listen()

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ResearchState(BaseModel):
    topic: str = ""
    search_results: list = []
    draft: str = ""
    final_report: str = ""

class ResearchFlow(Flow[ResearchState]):
    @start()                          # ← 入口点（支持多个并行启动）
    def search(self):
        # 搜索阶段
        self.state.search_results = [...]
        return self.state.search_results

    @listen(search)                   # ← 监听 search 完成，自动触发
    def write_draft(self, results):
        # 根据搜索结果写初稿
        self.state.draft = "..."
        return self.state.draft

    @listen(write_draft)              # ← 链式监听
    def review_and_polish(self, draft):
        self.state.final_report = f"润色后: {draft}"
        return self.state.final_report

flow = ResearchFlow()
flow.plot("research_pipeline")        # 自动生成 HTML 流程图
result = flow.kickoff()               # 返回最后一个方法的输出
```

### Flows + Crews 组合模式

Flows 的最大威力在于**与 Crews 的组合**：用 Flow 管理整体流程和状态，在需要多 Agent 协作的环节嵌入 Crew：

```python
from crewai import Crew, Agent, Task
from crewai.flow.flow import Flow, listen, start

class ContentPipeline(Flow):
    @start()
    def research_phase(self):
        # Flow 管理状态
        self.state["brief"] = "AI Agent 趋势报告"
        return self.state["brief"]

    @listen(research_phase)
    def crew_phase(self, brief):
        # 在 Flow 中嵌入 Crew 处理复杂子任务
        researcher = Agent(role="研究员", goal="深度调研", llm="gpt-4o")
        writer = Agent(role="作者", goal="撰写报告", llm="gpt-4o")

        crew = Crew(
            agents=[researcher, writer],
            tasks=[
                Task(description=f"调研: {brief}", agent=researcher),
                Task(description="基于调研写报告", agent=writer)
            ]
        )
        return crew.kickoff()

    @listen(crew_phase)
    def publish_phase(self, report):
        # Flow 控制后续流程
        self.state["published"] = True
        return f"✅ 已发布: {report[:100]}..."
```

### 高级路由：条件分支与并行

```python
@start()
@start()                        # 两个 @start 并行执行
def fetch_news(self): ...

@start()
def fetch_papers(self): ...

@listen(fetch_news)
@listen(fetch_papers)           # 等待两者都完成后触发
def merge_sources(self, news, papers):
    return {"news": news, "papers": papers}

@listen(merge_sources)
def route_by_quality(self, merged):
    if len(merged["papers"]) > 5:
        return self.deep_analysis()   # 路由到深度分析
    return self.quick_summary()       # 路由到快速摘要
```

### 生产 Flows 的最佳实践

| 实践 | 说明 |
|------|------|
| **Pydantic State** | 用 Pydantic BaseModel 定义状态，获得类型检查和自动验证 |
| **状态持久化** | Flow 状态自动携带 UUID，支持跨步骤追踪 |
| **异常处理** | 每个 `@listen` 方法内包裹 try-except，失败时状态可回滚 |
| **混合模型** | 搜索/分类用轻量模型，Crew 内部用强模型 |
| **流程图可视化** | `flow.plot()` 输出 HTML 供团队审查流程设计 |

> 来源：[CrewAI Documentation v1.15.2 — Flows](https://docs.crewai.com/concepts/flows)

---

## 🏛️ Google ADK：多Agent系统的企业级架构（2026）

> 来源：Google Cloud Blog — [Building Collaborative AI: A Developer's Guide to Multi-Agent Systems with ADK](https://cloud.google.com/blog/topics/developers-practitioners/building-collaborative-ai-a-developers-guide-to-multi-agent-systems-with-adk)（2025-11）

Google 的 **Agent Development Kit (ADK)** 从底层就为多Agent系统而设计，提供了结构化的层次架构，而非将不同组件拼凑在一起。

### 多Agent系统的三个核心理念

| 理念 | 说明 | 类比 |
|------|------|------|
| **去中心化控制** | 没有"老板"Agent 统一指挥，每个Agent基于自身规则和局部信息独立决策 | 鸟群——没有领导者，却形成协调的飞行模式 |
| **局部视图** | 每个Agent只感知和响应其直接环境，而非整个系统状态 | 球场观众——只看得到周围的人，看不到全场 |
| **涌现行为** | 简单的局部交互产生复杂、智能的全局行为 | 蚁群——简单个体规则涌现出复杂社会行为 |

### ADK 的三种 Agent 类型

| 类型 | 角色 | 说明 |
|------|------|------|
| **LLM Agent** | 大脑 🧠 | 利用 Gemini 等大模型理解自然语言、推理问题、决定行动方案 |
| **Workflow Agent** | 管理者 📋 | 不执行具体任务，而是编排其他Agent的执行流程 |
| **Custom Agent** | 专家 🔧 | 继承 `BaseAgent`，用 Python 编写特定逻辑和完全自定义行为 |

### Agent 层级结构（Agent Hierarchy）

ADK 将Agent组织成树形层级，类似公司组织架构：

```
Root Agent (CEO)
  ├── VP Agent (研发)
  │   ├── Director (前端)
  │   └── Director (后端)
  └── VP Agent (市场)
      └── Director (内容)
```

核心规则：
- **父Agent可管理多个子Agent**，委托任务给它们
- **每个Agent只能有一个父Agent**，确保清晰的指令和数据流线

### 三种工作流编排器（Workflow Agents）

| 编排器 | 模式 | 适用场景 |
|--------|------|---------|
| **SequentialAgent** | 流水线——子Agent按预定顺序逐个执行，前一个的输出作为后一个的输入 | `fetch data → clean data → analyze → summarize` |
| **ParallelAgent** | 并行——所有子Agent同时执行 | 同时调用3个不同API收集信息 |
| **LoopAgent** | 循环——反复执行子Agent直到条件满足或达到最大迭代次数 | 轮询API状态、重试直到成功 |

### Agent 间通信机制

ADK 提供三种通信方式：

| 机制 | 原理 | 类比 |
|------|------|------|
| **Shared Session State** | Agent将结果写入共享状态对象，其他Agent可读取 | 共享数字白板 |
| **LLM-Driven Delegation** | 父Agent（LLM Agent）分析请求，推理出最适合的子Agent并动态路由 | 协调者按需分派 |
| **AgentTool（显式调用）** | 一个Agent将另一个Agent包装为\"工具\"，通过函数调用方式直接调用 | 外部顾问——需要时调用，不属于核心团队 |

### Sub-Agent vs AgentTool 的区别

| 维度 | Sub-Agent | AgentTool |
|------|-----------|-----------|
| 关系 | 层级中的固定成员 | 外部"顾问" |
| 生命周期 | 始终在编 | 按需调用 |
| 使用方式 | 父Agent管理、委托 | 作为工具被调用 |

### ADK 快速上手

```bash
pip install google-adk
```

```python
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search

# 定义子Agent
researcher = LlmAgent(
    name="researcher",
    model="gemini-2.5-pro",
    instruction="Research the given topic and provide key findings",
    tools=[google_search]
)

writer = LlmAgent(
    name="writer",
    model="gemini-2.5-pro",
    instruction="Write a comprehensive summary based on research findings",
)

# 用 SequentialAgent 编排流水线
pipeline = SequentialAgent(
    name="research_pipeline",
    sub_agents=[researcher, writer]
)

result = pipeline.run("Latest advances in AI agents 2026")
```

> **选型建议**：如果你的技术栈在 GCP 生态中，ADK 是原生选择；如果追求框架无关性和社区生态，LangGraph 更通用。ADK 的层级结构设计使其在超大规模多Agent系统中优势明显。

### 参考来源
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Samples on GitHub](https://github.com/google/adk-samples)
- [ADK Codelab](https://codelabs.developers.google.com/onramp/instructions#0)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-16 00:08:55*
