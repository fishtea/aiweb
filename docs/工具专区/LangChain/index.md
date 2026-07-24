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

## 2026年LangChain/LangGraph生产实战

### LangChain vs LangGraph：何时用哪个

2026 年生产环境中的明确分工已形成：

**LangChain (LCEL) 适合：**
- 线性 RAG 管道（检索 → 组装上下文 → 生成）
- 简单的 1-2 工具调用 Agent
- 快速原型验证——可读的管道语法、内建流式/批处理/异步
- 利用 1000+ 预建集成，无需手写 PDF 加载器、FAISS 包装器等

**LangGraph 适合：**
- **状态化多步 Agent**：条件分支、循环、多轮推理
- **Human-in-the-Loop**：审批、中断、恢复（一行代码实现）
- **持久化会话**：跨会话状态保持和检查点
- **错误恢复**：工具调用失败时的结构化重试和回退

> 来自 Kalvium Labs 2026 年实践数据：12 个 Agent 项目中 8 个以 LangChain 起步，其中 4 个因状态管理成为瓶颈而**重写为 LangGraph**。LangChain 给你循环，LangGraph 给你循环周围的基础设施。

### LangGraph 三大优势

以代码为例说明：

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list, add]   # 追加而非替换
    error_count: int

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "end"
    if state["error_count"] >= 3:    # 错误上限保护
        return "end"
    return "tools"

graph = StateGraph(AgentState)
# ... 添加节点和边 ...
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
```

**1. 类型化的显式状态** — `AgentState` 精确定义追踪内容，可在任意检查点检查。

**2. 一等公民的条件边** — `should_continue` 是可测试的纯函数，可按错误计数、标志位、模式等分支。

**3. Human-in-the-Loop（一行代码）** — 原生中断/恢复 + 持久化状态：
```python
from langgraph.checkpoint.memory import MemorySaver
app = graph.compile(checkpointer=MemorySaver(), interrupt_before=["tools"])
```

### 2026 AI Agent 框架全景

根据 LangChain 官方 2026 年 6 月发布的框架评估：

| 框架 | 类型 | 开源 | 最适合 |
|------|------|------|--------|
| **LangChain + LangGraph** | LLM 应用框架 + Agent 运行时 | MIT | 快速原型 + 精确的多 Agent 编排 |
| **Deep Agents** | Agent 执行器 | MIT | 长时间运行的编程/研究工作流 |
| **CrewAI** | 多 Agent 编排 | MIT | 基于角色的 Agent 快速原型 |
| **Microsoft Agent Framework** | 多 Agent 编排 | MIT | AutoGen + Semantic Kernel 统一继任者 |
| **LlamaIndex Workflows** | Agent 工作流 | MIT | 文档密集、数据驱动的管道 |
| **Google ADK** | Agent 开发框架 | Apache 2.0 | GCP 原生团队 |
| **OpenAI Agents SDK** | 多 Agent SDK | MIT | 轻量级、低抽象的 OpenAI 助手 |
| **Mastra** | TypeScript Agent 框架 | 部分开源 | TypeScript 团队构建生产 Agent |

### LangChain 2026 关键数字

- **~134k GitHub Stars**，1000+ 预建集成
- **LangSmith**：框架无关的可观测性平台，支持追踪、评估、部署和自动化问题优先级排序（LangSmith Engine）
- **MCP/A2A 协议**支持：模型上下文协议和 Agent-to-Agent 通信

### 生产落地警示

LangChain 的抽象层在快速原型时高效，但在生产环境中需要谨慎管理：
- 状态通过可变字典传递时，条件逻辑最终散落在不可测试的 if-else 树中（有团队到 400 行后才承认框架不再有帮助）
- 中段会话中断需要 200+ 行自定义轮询 + 信号机制
- 类型化错误处理缺失——第 7 步工具失败时需手动构建重试、退避和反馈逻辑

> **选型建议**：新项目直接从 LangGraph 起步，LangChain 的 AgentExecutor 已被标记为遗留。搭配 LangSmith 做全链路可观测，Deep Agents 处理长期运行 Agent。框架选择的核心原则：**"抽象只有加速正确决策时才有用——掩盖故障模式的抽象，调试时间远超搭建时间。"**

### 参考来源

- [The Best AI Agent Frameworks in 2026 - LangChain](https://www.langchain.com/resources/ai-agent-frameworks)
- [LangGraph vs LangChain: Which We Deploy in Production (2026)](https://www.kalviumlabs.ai/blog/langgraph-vs-langchain-production)
- [AI Agent Frameworks 2026: Production-Tested Ranking - Alice Labs](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026)

---

## 2026 Q2 最新动态 (v1.2 / v1.3 重大更新)

### LangGraph v1.2.0（2026年5月）

LangGraph v1.2.0 带来了一系列面向生产的关键增强，参考 [官方 Changelog](https://docs.langchain.com/oss/python/releases/changelog)：

| 特性 | 说明 |
|------|------|
| **DeltaChannel（Beta）** | 新型 Channel 仅存储增量变化，大幅压缩长对话的 Checkpoint 体积。每隔 `snapshot_frequency=K` 步写入完整快照以控制读取延迟，非常适合长时间运行的 Agent 会话 |
| **逐节点超时控制** | `add_node(..., timeout=...)` 支持 `run_timeout`（时钟时间）、`idle_timeout`（空闲重置）或组合策略 `TimeoutPolicy`。超时时抛出 `NodeTimeoutError`，清空写入并触发重试（仅限 async 节点） |
| **节点级错误处理** | `add_node(..., error_handler=...)` 在所有重试耗尽后执行，可返回 `Command` 更新状态并路由到其他节点，支持 Saga/补偿模式 |
| **优雅停机** | `RunControl.request_drain()` 在当前 superstep 完成后停止运行并保存可恢复的 Checkpoint，后续可继续执行 |
| **Event Streaming v3（Beta）** | `stream_events` 新版本提供 content-block 为中心的类型化流式 API，支持 `run.values`、`run.messages`、`run.lifecycle`、`run.subgraphs` 等投影，每个 LLM 调用产出 `ChatModelStream`（含 text、reasoning、tool_calls、usage 子投影） |

### DeepAgents v0.6.0（2026年5月）

[DeepAgents](https://docs.langchain.com/oss/python/deepagents) 是 LangChain 的长期运行 Agent 框架，v0.6.0 新增：

- **CodeInterpreterMiddleware（实验性）**：通过 scoped QuickJS 运行时提供代码执行和编程式工具调用
- **Harness Profiles**：按提供商/模型注册配置包，自动应用系统提示、工具覆盖、中间件和子 Agent 默认值，无需修改调用点
- **ContextHubBackend**：基于 LangSmith Hub 的文件系统后端，Agent 文件以 Hub commits 存储，提供版本历史和原生持久化
- **Event Streaming v3** 同步支持

### LangChain v1.3.0（2026年5月）

同步引入 Event Streaming v3 支持。

### 选型建议更新

> 2026 年 Q2 后，LangGraph 已全面成为生产 Agent 的默认选择。LangChain 的 `AgentExecutor` 已被标记为遗留（Legacy），新项目直接从 `create_agent`（LangChain v1.x）或 LangGraph 的 `StateGraph` 起步。搭配 LangSmith 做全链路可观测，DeepAgents 处理长期运行 Agent。

### 参考来源

- [LangChain Changelog — May 2026](https://docs.langchain.com/oss/python/releases/changelog)
- [LangGraph vs LangChain: Production AI Agents 2026 (Spheron)](https://www.spheron.network/blog/langgraph-vs-langchain)
- [LangChain 与 LangGraph 学习笔记（2026最新版） — 知乎](https://zhuanlan.zhihu.com/p/1992203641751360821)

---

## LangChain 1.3.12 补丁版（2026年7月8日）

2026年7月8日，LangChain 发布 **1.3.12** 补丁版，主要修复 Agent 中间件在生产环境中的稳定性问题。

### 修复要点

| 修复 | 说明 |
|------|------|
| **中断传播修复** | `ToolRetryMiddleware` 中的中断（interrupts）现在能正确传播，避免 Agent 在工具重试时吞掉取消信号 |
| **Shell 中间件进程组修复** | 避免共享进程组被意外 kill，防止并行 Agent 任务间互相干扰 |
| **Anthropic 缓存标记清理** | 在回退重试（fallback retries）时清理 Anthropic 缓存标记，防止缓存标记污染后续请求 |

### 版本演进

| 版本 | 日期 | 关键变化 |
|------|------|---------|
| v1.2.0 | 5月 | LangGraph DeltaChannel、逐节点超时、Event Streaming v3 Beta |
| v1.3.0 | 5月 | LangChain 同步引入 Event Streaming v3 |
| v1.3.11 | 6月 | 多个中间件修复和类型增强 |
| **v1.3.12** | **7月8日** | **中断传播、Shell 中间件、Anthropic 缓存修复** |

### 参考来源
- [LangChain v1.3.12 Release Notes](https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.3.12)

---

## LangGraph 7月迭代速览（v1.2.7 → v1.2.9）

LangGraph 在 2026 年 6 月底至 7 月初保持了高频迭代节奏，连续三周发布补丁版本，重点修复分布式状态管理中的边缘情况。

### 版本变化一览

| 版本 | 日期 | 关键修复 |
|------|------|---------|
| **v1.2.9** | **7月10日** | `updateState` 在 delta channel 上的 metadata/counters 修复——确保增量更新时计数器不丢失 |
| v1.2.8 | 7月6日 | delta channel 在全新线程上调用 `updateState` 时强制生成 snapshot 而非空 stub checkpoint，避免状态丢失 |
| v1.2.7 | 6月30日 | `DeltaChannel` 的 `Overwrite` 操作在 JSON 往返后不再丢失语义；snapshot 场景下 superstep 覆盖行为修正 |

### 技术解读：DeltaChannel 的演进

DeltaChannel 是 LangGraph v1.2.0 引入的增量状态通道机制，允许 Agent 在多轮工具调用中仅传递状态变更（delta）而非全量 snapshot，大幅减少序列化开销。

v1.2.7–v1.2.9 这三个补丁集中解决了 DeltaChannel 在生产环境中的三个边缘问题：

1. **Overwrite 的 JSON 保真性**（v1.2.7）：`Overwrite` 是 DeltaChannel 的一种写入语义——"用新值完全替换旧值"。但在某些序列化路径中（如通过 LangGraph API 传输），`Overwrite` 经 JSON 往返后会退化为普通写入，导致并发冲突时旧值残留。v1.2.7 通过保留类型标记解决了这个问题。

2. **全新线程的 updateState**（v1.2.8）：在一个尚未执行任何 superstep 的线程上调用 `updateState` 时，旧代码会生成空的 stub checkpoint，导致后续状态读取为空。修复后强制生成真实 snapshot。

3. **Counters 一致性**（v1.2.9）：DeltaChannel 维护内部计数器以追踪增量顺序。`updateState` 在某些路径下会绕过计数器更新，导致后续增量被错误排序。v1.2.9 修复了 metadata/counters 的同步问题。

> **实际影响**：如果你的 LangGraph 应用使用了 `updateState` API（从外部注入状态更新，如人工审批流程），升级到 v1.2.9 可以避免状态更新在特定时序下丢失。

### 生态节奏

LangChain 生态在 2026 年 Q3 初的迭代节奏约为：
- **LangChain 核心**：~1-2 周发布补丁（1.3.x 系列）
- **LangGraph**：~每周发布补丁（1.2.x 系列）
- **LangSmith**：持续交付，无固定版本号
- **DeepAgents**：~每月发布功能版本（当前 v0.6.0）

### 参考来源
- [LangGraph v1.2.9 Release Notes](https://github.com/langchain-ai/langgraph/releases/tag/1.2.9)
- [LangGraph v1.2.8 Release Notes](https://github.com/langchain-ai/langgraph/releases/tag/1.2.8)
- [LangGraph v1.2.7 Release Notes](https://github.com/langchain-ai/langgraph/releases/tag/1.2.7)
- [LangChain Changelog](https://docs.langchain.com/oss/python/releases/changelog)

---

## LangChain core 1.5.0：`reasoning_effort` 标准参数（2026年7月23日）

2026年7月23日，LangChain 发布 **langchain-core 1.5.0**（从 1.3.x 直接跃升至 1.5.x），核心变化是新增 `reasoning_effort` 作为聊天模型的标准参数，标志着 LangChain 对推理模型的全面正式支持。

### `reasoning_effort` — 推理模型的标准协议

`reasoning_effort` 是一个标准化参数，用于控制推理模型（如 DeepSeek-R1、o3、Gemini 2.5 Pro Thinking 等）的推理深度：

| 取值 | 含义 | 适用场景 |
|------|------|---------|
| `"low"` | 轻量推理 | 简单问题、快速响应 |
| `"medium"` | 中等推理（默认） | 通用场景 |
| `"high"` | 深度推理 | 复杂逻辑、数学、编程 |

```python
from langchain.chat_models import ChatOpenAI

# 使用推理模型时指定 effort
llm = ChatOpenAI(
    model="o3-mini",
    reasoning_effort="high",
)
```

这项参数的标准化消除了各模型提供商之间不同的推理控制方式（OpenAI 的 `reasoning_effort`、Anthropic 的 `thinking`、Google 的 `thinking_config`），LangChain 在底层自动映射到对应提供商的参数格式。

### 配套更新

- **langchain-core 1.5.1**（同日）：修复 langsmith gateway 环境变量支持（`LANGSMITH_GATEWAY_URL`）和工具调用 token 计数缓存
- 配套包同步更新：`langchain-openai==1.4.1`、`langchain-anthropic==1.5.1`、`langchain-fireworks==1.5.1`

### 对 Agent 开发者的意义

1. **推理 Agent 更易构建**：无需为不同模型手写参数映射
2. **成本精细控制**：简单问题用 `"low"` 省 token，复杂问题用 `"high"` 保证质量
3. **跨模型迁移**：从 o3 换到 Gemini 2.5 Pro，推理参数自动适配

### 参考来源
- [LangChain core 1.5.0 Release Notes](https://github.com/langchain-ai/langchain/releases/tag/langchain-core==1.5.0)
- [LangChain core 1.5.1 Release Notes](https://github.com/langchain-ai/langchain/releases/tag/langchain-core==1.5.1)
- [LangChain Changelog](https://docs.langchain.com/oss/python/releases/changelog)

---

## LangChain v1.x `create_agent` 全解析（2026 实战模式）

> 来源：JetBrains Blog — [LangChain Python Tutorial: A Complete Guide for 2026](https://blog.jetbrains.com/pycharm/2026/02/langchain-tutorial-2026)

LangChain v1.0 将 Agent 创建简化为 `create_agent()` 一个函数调用，彻底告别了旧版 `create_react_agent` + `AgentExecutor` 的组合。

### 核心 API

```python
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-5",       # 支持 GPT-4o/5、Claude、Gemini 等
    tools=tools,          # @tool 装饰器定义的工具列表
    system_prompt="...",  # 系统提示词
)
```

### 静态 vs 动态模型

LangChain v1.x 区分两种模型使用模式：

| 模式 | 特点 | 适用场景 |
|------|------|---------|
| **静态模型** | Agent 创建时固定模型，运行期间不变 | 大多数常规场景 |
| **动态模型** | 运行时根据状态/上下文切换模型 | 需要模型回退、成本优化的场景 |

**动态模型示例**——通过 `ModelFallbackMiddleware` 实现主模型失败时自动切换到备用模型：

```python
from langchain.agents.middleware import ModelFallbackMiddleware

agent = create_agent(
    model="gpt-4o",
    tools=[],
    middleware=[
        ModelFallbackMiddleware(
            "gpt-4o-mini",
            "claude-3-5-sonnet-20241022",
        ),
    ],
)
```

### 工具（Tools）——@tool 装饰器

LangChain v1.x 使用 `@tool` 装饰器定义工具，比旧版更简洁：

```python
@tool
def search_db(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query."""
    ...
    return f"Found {limit} results for '{query}'"

@tool("pycharm_docs_search", return_direct=False)
def pycharm_docs_search(q: str) -> str:
    """Search the local FAISS index of documentation."""
    ...
    docs = retriever.get_relevant_documents(q)
    return format_docs(docs)
```

### 中间件（Middleware）一览

中间件是 LangChain v1.x 最强大的扩展机制，可在 Agent 运行时拦截和定制行为：

| 中间件 | 功能 |
|--------|------|
| **Summarization** | Token 接近上限时自动摘要对话历史 |
| **Human-in-the-loop** | 工具调用前暂停等待人工审批 |
| **Context editing** | 修剪或清除工具调用记录，管理上下文长度 |
| **PII detection** | 检测并处理个人身份信息 |
| **ModelFallback** | 主模型失败时自动切换到备用模型 |
| **ToolRetry** | 工具调用失败时自动重试 |

### 文档问答实战（FAISS + LangChain）

JetBrains 教程中的完整文档问答 Agent 模式：

```python
from langchain.agents import create_agent
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. 定义文档搜索工具
@tool("pycharm_docs_search")
def pycharm_docs_search(q: str) -> str:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.load_local(
        "index_dir", embeddings, allow_dangerous_deserialization=True
    )
    retriever = vector_store.as_retriever(
        search_type="mmr", search_kwargs={"k": 4, "fetch_k": 12}
    )
    docs = retriever.invoke(q)
    return format_docs(docs)

# 2. 创建 Agent
agent = create_agent(
    model="gpt-5",
    tools=[pycharm_docs_search],
    system_prompt="You are a helpful assistant. Always consult the docs tool before answering. Cite sources."
)

# 3. 调用
result = agent.invoke({"messages": [{"role": "user", "content": "How to debug in PyCharm?"}]})
```

### 架构最佳实践

> 2026 年 LangChain Agent 架构的推荐分层：
> - **LangChain v1.x `create_agent`**：适合简单到中等复杂度的单 Agent 场景
> - **LangGraph StateGraph**：需要精确控制循环、分支、人工干预的生产级 Agent
> - **DeepAgents**：长时间运行（数小时/天）的复杂编程或研究任务

---

## 2026 最新进展：LangChain 的"安静出走"与生态重塑

### 概述

2025 年 10 月 LangChain 1.0 发布后，社区曾寄予厚望。但进入 2026 年，一股"安静出走"（Quiet Migration）的趋势正在生产环境中蔓延——越来越多的工程团队正悄然将代码从 LangChain 迁移至 OpenAI Agents SDK、Claude Agent SDK 或直接 API 调用。这场迁移没有喧哗，没有告别博文，但正在深刻改变 LLM 框架的格局。

### 核心要点

#### 1. 为什么生产团队在"离开"LangChain？

根据 Ravoid 2026 年 4 月的深度分析 *The LangChain Exit*（Fernando, 2026），迁移的根本原因不是 LangChain 做得不好，而是**结构性问题**：

- **抽象层价值被模型厂商吸收**：OpenAI、Anthropic 等厂商推出的原生 Agent SDK 已经内置了 LangChain 过去提供的核心抽象（工具调用、函数选择、多步推理），开发者不再需要一个中间层框架。
- **1.0 来得太晚**：LangChain 在 v0.x 阶段经历了 3 年的频繁破坏性变更，许多团队在 1.0 发布前就已经转向其他方案。1.0 稳定后反而失去了"早期尝鲜者"的意义。
- **隐藏的复杂度成本**：表面上 LangChain 用几行代码就能搭建 Agent，但在生产环境中，调试、定制、性能调优时需要深入理解框架内部——这种"漏抽象"反而增加了维护负担。

> *"Engineering teams do not write celebratory blog posts about frameworks they removed. They write about frameworks they adopted."* — 这正是 2026 年 LangChain 迁移潮在公开讨论中几乎不可见的原因。

#### 2. LangChain 生态系统在 2026 年仍然是完整的工具链

尽管有迁移趋势，LangChain 生态在 2026 年仍然是最完整的 LLM 应用开发工具链（来源：LangChain 2026 年 1 月 Newsletter）：

| 组件 | 2026 状态 | 说明 |
|------|----------|------|
| **LangChain v1.x** | 稳定维护 | 快速搭建 Agent 的框架，`create_agent()` API |
| **LangGraph** | 生产级编排 | 精确控制循环、分支、人工干预的 StateGraph |
| **LangSmith Agent Builder** | GA (2026.01) | 用自然语言描述需求，自动生成完整 Agent（含 prompt、工具选择、子 Agent 和技能） |
| **DeepAgents** | 新推出 | 面向长时间运行（数小时/天）的复杂编程和研究任务 |
| **LangSmith 可观测性** | 持续增强 | 支持 Side-by-side LLM 实验对比，快速发现回归和改进 |

#### 3. 当前最佳实践：分层选择

2026 年 LangChain 生态的推荐使用策略（综合 Ravoid 分析和官方文档）：

- **快速原型 / 简单 Agent**：`LangChain v1.x create_agent()` — 几行代码即可跑通，适合 PoC 和小型项目
- **生产级 Agent（需精确控制）**：`LangGraph StateGraph` — 适合需要复杂循环、人工审批、条件分支的场景
- **长时间自主任务（研究/编程）**：`DeepAgents` — 可运行数天的复杂任务 Agent
- **团队快速交付**：`LangSmith Agent Builder` — 自然语言描述需求，自动生成可部署的 Agent

### 参考来源

- [The LangChain Exit: Why Production Teams Are Quietly Rewriting to Raw SDKs in 2026 — Ravoid (2026.04)](https://ravoid.com/blog/langchain-exit-raw-sdk-migration-2026)
- [January 2026: LangChain Newsletter — LangChain Blog (2026.01.29)](https://blog.langchain.com/january-2026-langchain-newsletter/)
- [LangChain Changelog — docs.langchain.com](https://docs.langchain.com/oss/python/releases/changelog)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-25 00:09:45*
