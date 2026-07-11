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

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-12 00:07:00*
