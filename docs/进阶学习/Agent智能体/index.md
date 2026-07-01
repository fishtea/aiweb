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

## 6. Agent 的失败模式与对策

让 Agent 真正可用，关键在于知道它会在哪里出错并提前设防。

| 失败模式 | 典型表现 | 对策 |
|---------|---------|------|
| 无限循环 | 反复调用同一工具不收敛 | 设最大步数、检测重复动作、强制终止 |
| 工具误用 | 选错工具或参数错误 | 优化工具描述、参数 schema 校验、失败重试 |
| 上下文爆炸 | 历史累积过多导致超窗 | 摘要压缩、滚动窗口、只保留关键观察 |
| 错误级联 | 早期判断错误影响后续 | 中间校验点、分阶段确认、可回退状态 |
| 幻觉行动 | 编造不存在的工具或结果 | 工具白名单、结果校验、引用来源 |
| 越权操作 | 执行了不该执行的动作 | 最小权限、敏感操作人工确认 |

### 生产级 Agent 的必备护栏

1. **步数与成本上限**：硬性限制最大迭代轮数和 token 预算，超过即终止。
2. **状态检查点**：每步持久化状态，失败可从断点恢复而非从头重来。
3. **人工兜底**：高风险动作（删除、支付、外发）触发暂停等待确认。
4. **轨迹可观测**：完整记录思考、工具调用、参数、结果和耗时，便于复盘。
5. **降级路径**：Agent 失败时回退到规则流程或人工处理，而不是直接报错。

### 何时不该用 Agent

Agent 的自主性是把双刃剑。以下场景更适合确定性工作流而非开放式 Agent：

- 任务步骤固定、可预见 → 用编排式工作流（DAG）。
- 对延迟和成本极敏感 → 直接调用或简单链。
- 错误代价极高且不可逆 → 人工或半自动流程。
- 工具数量少且调用模式单一 → 单次函数调用即可。

> 经验：能用工作流解决的就不要用 Agent。Agent 的价值在于"任务路径不可预先确定"的场景，代价是更高的不确定性。

---

## 🔗 参考资料

- [Getting Started with ReAct AI Agents using LangChain - YouTube](https://www.youtube.com/watch?v=W7TZwB-KErw)
- [Introducing LangChain Agents: 2024 Tutorial - Bright Inventions](https://brightinventions.pl/blog/introducing-langchain-agents-tutorial-with-example)
- [Using LangChain Tools to Build an AI Agent - IBM](https://www.ibm.com/think/tutorials/using-langchain-tools-to-build-an-ai-agent)
- [Learn to Build AI Agents with LangChain - Reddit](https://www.reddit.com/r/LangChain/comments/1f6jknc/learn_how_to_build_ai_agents_react_agent_from/)

---


## 8. 2025年分领域 Agent 实战推荐

### 8.1 企业级通用：实在 Agent（实在智能）

从 RPA 进化而来的"全能数字员工"：

- **深度规划引擎**：目标驱动，自动拆解。一句话即可生成带图表的 PPT（8 分钟完成原本 2 小时的工作）
- **ISSUT 技术**：像人一样"看"屏幕操作，兼容无 API 的老旧系统
- **安全合规**：数据存储国内服务器，符合等保三级标准
- **客户案例**：中国联通、北方华创、空中客车已实战验证

### 8.2 低代码开发：扣子（字节跳动）

非技术人员的"Agent 搭建神器"：

- **可视化拖拽**：零编程 15 分钟上手
- **生态整合**：调用抖音热点、今日头条数据、与飞书/剪映联动
- **实战效果**：运营人员 40 分钟搭建营销工具，文案互动率比人工高 12%

### 8.3 开发者专属：MetaGPT（开源）

模拟完整软件开发团队的协作：

- **模拟角色**：产品经理、项目经理、工程师、测试员
- **实战效果**：3 小时完成双人对战贪吃蛇游戏（传统至少 1 天）
- **成本**：完全开源，API 集成仅 ~2 美元
- **GitHub**：80k+ Star

### 8.4 客服场景：智齿 Agent（智齿科技）

"人机协同"的标杆：

- AI 处理简单查询（物流信息），复杂情绪化问题自动转人工
- 情绪识别：检测愤怒等负面情绪，自动触发优先转接
- **实战效果**：咨询量下降 60%，满意度从 82 分提升至 91 分

### 8.5 知识管理：司马诸葛

知识密集型企业的精准大脑：

- 自研 Doc Mind 模型：将文档结构化后处理，解决"幻觉"问题
- **实测**：回答准确度满分，能引用具体条款和页码
- **效果**：查阅资料周期从 3 个月缩短至分钟级

**来源：** [2025年最好的Agent智能体有哪些？权威测评+实战推荐 - 百度千帆社区](https://qianfan.cloud.baidu.com/qianfandev/topic/686932)

---

## 9. 避坑指南与未来趋势

### 避坑四原则

1. **别信"全场景覆盖"**：全能往往平庸，聚焦核心痛点选垂直工具
2. **免费版够用别升级**：大部分免费版已满足基础需求
3. **避开"需改造IT系统"的产品**：选开箱即用，避免高额费用和漫长周期
4. **人机协同是王道**：AI 是助手，不是替代者

### 未来趋势

- **自主性更强**：Agent 从"被动响应"变为"主动发现问题"
- **生态化更明显**：Agent 市场兴起，像装 App 一样选择行业插件
- **人才需求爆发**：提示工程和 Agent 设计能力成为核心竞争力

**来源：**  \n- [2025年中国AI Agent年度最佳实践应用榜单 - 头豹研究院](https://www.fxbaogao.com/detail/5038572)  \n- [2025年最好的Agent智能体推荐 - 百度千帆社区](https://qianfan.cloud.baidu.com/qianfandev/topic/686932)

---

## 10. 2026年AI Agent框架全景对比

2026年被称为"智能体应用爆发之年"，Agent框架生态呈现多元化的繁荣景象。以下综合JetBrains PyCharm Blog和LangChain官方的权威评测，梳理主流框架的技术定位与选型建议。

### 10.1 什么是AI Agent？（2026定义）

**来源：** [Top Agentic Frameworks for Building Applications 2026 - JetBrains PyCharm Blog](https://blog.jetbrains.com/pycharm/2026/06/top-agentic-frameworks-for-building-applications-2026/)

AI Agent遵循 **PRAR循环**：
- **Perceive（感知）** — 观察环境、用户输入、系统状态、工具、记忆
- **Reason（推理）** — 使用LLM或混合逻辑规划并决策行动
- **Act（行动）** — 执行行动（调用工具、更新记忆、触发工作流）
- **Reflect（反思）** — 评估结果并调整未来行为

> *"与传统的LLM和聊天机器人不同，Agent不需要持续的用户输入……它们是主动的，基于设定的规则和参数自主工作以实现目标。"*

### 10.2 三种核心编排范式（2026）

| 范式 | 描述 | 优势 | 局限 |
|------|------|------|------|
| **图式编排（Graph-Based）** | Agent和工具作为有向图节点，流程预定义 | 确定性强、易调试、生产级可靠 | 前期设计多、创造性空间小 |
| **角色式编排（Role-Based）** | Agent被分配特定角色（如"规划者""研究员"），通过消息协作 | 直觉化、原型快、模仿人类团队 | 执行路径难强制、可复现性差 |
| **链式编排（Chain-Based/Adaptive）** | Agent在动态链/循环中自主决定下一步 | 灵活、适合创造性任务 | 可预测性低、治理难 |

### 10.3 十大Agent框架深度对比（2026）

**来源：**  \n- [Top Agentic Frameworks for Building Applications 2026 - JetBrains](https://blog.jetbrains.com/pycharm/2026/06/top-agentic-frameworks-for-building-applications-2026/)  \n- [The best AI agent frameworks in 2026 - LangChain](https://www.langchain.com/resources/ai-agent-frameworks)

| 框架 | 编排方式 | 多Agent | 记忆 | 人机协作 | 开源 | 最佳场景 |
|------|---------|---------|------|---------|------|---------|
| **LangChain** | 链式 | 部分 | 中 | 有限-中等 | MIT | 快速LLM应用原型 |
| **LangGraph** | 图式 | 强 | 强 | 强 | MIT | 生产级Agent工作流 |
| **LlamaIndex Workflows** | 事件驱动 | 有限 | 强 | 中 | MIT | 知识密集型Agent |
| **Haystack** | 流水线式 | 中 | 强 | 中 | 开源 | 生产RAG与上下文AI |
| **CrewAI** | 角色式 | 强 | 轻量 | 有限 | MIT | 任务导向Agent团队 |
| **AutoGen** | 角色式 | 强 | 中 | 有限 | MIT | 对话式多Agent |
| **Semantic Kernel** | 规划式 | 中 | 中 | 强 | MIT | 企业AI(微软栈) |
| **Microsoft Agent Framework** | 图式 | 强 | 强 | 强 | MIT | 微软统一框架 |
| **OpenAI Agents SDK** | 图式(托管) | 是 | 托管 | 强 | MIT | 托管Agent应用 |
| **Google ADK** | 图式(托管) | 是 | 强 | 强 | Apache 2.0 | GCP原生团队 |

### 10.4 各框架深度解析

#### LangChain（⭐ ~134k）
- **定位**：基于链的LLM应用框架，可快速原型Agent功能
- **核心优势**：1,000+集成（模型、向量数据库、文档加载器、API），一行代码切换模型提供商
- **生产准备度**：抽象层需要谨慎管理，建议搭配LangSmith使用
- **最佳场景**：工具增强聊天机器人、LLM后端服务、快速原型

#### LangGraph
- **定位**：有状态多参与者系统的图式编排，构建于LangChain之上
- **核心优势**：确定性工作流、原生状态管理、通过中断机制实现优秀的人机协作
- **最佳场景**：自主客户支持、AI驱动的DevOps、多步决策引擎

#### CrewAI（⭐ ~49k）
- **定位**：基于角色的多Agent编排，每个Agent有特定人设、目标和背景故事
- **生态**：支持网络抓取、PostgreSQL、MongoDB、Qdrant、Weaviate、MCP
- **注意事项**：社区报告显示执行追踪不够准确、异步执行和流式输出的痛点。免费版限制50次执行/月
- **最佳场景**：多角色协作任务的快速原型

#### Microsoft Agent Framework（⭐ ~9.6k）
- **定位**：AutoGen + Semantic Kernel的统一继任者（2025年10月宣布），Python和.NET已GA（2026年4月3日）
- **核心特性**：带类型安全路由、检查点、人机协作的图式工作流；原生MCP支持；A2A协议适配器（beta）
- **最佳场景**：微软技术栈团队的企业应用

#### LlamaIndex Workflows
- **定位**：以检索为中心、数据优先，从数据出发构建Agent行为
- **核心优势**：高级文档索引、强长期记忆
- **局限**：不适合复杂动作编排；多Agent能力有限
- **最佳场景**：研究助手、知识库Agent、企业文档智能

### 10.5 框架选型决策树

```
你要构建什么？
├── 简单工具调用聊天机器人 → LangChain
├── 生产级复杂Agent工作流 → LangGraph
├── 多Agent角色协作 → CrewAI / AutoGen
├── 知识密集/文档处理 → LlamaIndex Workflows / Haystack
├── 企业微软技术栈 → Microsoft Agent Framework
├── GCP原生项目 → Google ADK
├── 托管/快速部署 → OpenAI Agents SDK
└── TypeScript项目 → Mastra
```

### 10.6 2026年Agent开发趋势

1. **MCP（Model Context Protocol）成为行业标准**：主流框架均原生支持MCP，实现工具发现的标准化
2. **可观测性成为标配**：LangSmith、LangFuse等追踪工具与框架深度集成
3. **人机协作（HITL）成为生产级必备**：关键步骤的人工审批与中断恢复
4. **多Agent编排成熟化**：从实验阶段进入生产级可靠性的关键一年
5. **框架趋同但仍有分化**：LangChain/LangGraph生态最完整，微软统一框架对微软栈用户最有吸引力

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：自动更新*
