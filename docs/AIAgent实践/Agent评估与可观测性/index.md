# Agent 评估与可观测性

Agent 系统的失败往往不是一句“模型不聪明”能解释的。它可能出在任务理解、计划拆解、工具选择、参数生成、权限控制、外部 API、记忆污染或停止条件上。评估与可观测性用于把这些问题拆开定位。

## 为什么 Agent 更难评估

- 输出不是单次文本，而是一串计划、工具调用、观察结果和最终回答。
- 同一任务可能存在多条可接受路径，不能只用字符串匹配判断。
- 工具调用可能产生真实副作用，测试需要隔离环境。
- 长任务容易累积错误，早期小偏差会影响后续步骤。
- 成本、延迟和成功率之间经常互相拉扯。

## 评估维度

| 维度 | 关注点 |
|------|--------|
| 任务成功率 | 是否完成用户目标，最终结果是否可用 |
| 计划质量 | 步骤是否必要、顺序是否合理、是否遗漏关键约束 |
| 工具选择 | 是否调用正确工具，是否避免无意义或危险调用 |
| 参数正确性 | schema 是否符合要求，关键字段是否准确 |
| 过程效率 | 调用次数、token 消耗、耗时和重试次数 |
| 安全合规 | 是否越权、泄露信息、执行高风险动作或绕过确认 |
| 可解释性 | 是否能复盘为什么这样执行，失败原因是否清晰 |

## 日志设计

每一次 Agent 运行建议记录结构化轨迹：

```json
{
  "run_id": "agent-run-001",
  "user_goal": "查询订单并生成回复",
  "steps": [
    {
      "type": "tool_call",
      "tool": "search_order",
      "arguments": { "order_id": "masked" },
      "status": "success",
      "latency_ms": 320
    }
  ],
  "final_status": "success"
}
```

实际生产环境应对用户输入、工具参数和返回内容做脱敏，只保留排障所需字段。

## 测试集构建

| 样例类型 | 示例 |
|----------|------|
| 正常任务 | 查询信息、整理资料、调用工具完成标准流程 |
| 边界任务 | 缺少参数、上下文冲突、结果为空、工具超时 |
| 安全任务 | 越权请求、敏感信息、需要人工确认的动作 |
| 长链任务 | 多步骤规划、跨工具依赖、需要中间状态校验 |
| 对抗任务 | Prompt injection、恶意文档、诱导泄露系统提示词 |

## 改进方法

- 对工具 schema 增加清晰描述、枚举值、必填字段和参数示例。
- 将高风险动作拆成“准备”和“确认执行”两个阶段。
- 为 Agent 设置最大步数、最大成本、超时和停止条件。
- 对常见任务使用工作流约束，而不是完全开放式自主规划。
- 把失败轨迹回放到离线评估集中，防止同类问题反复出现。

### 可观测性工具链

生产 Agent 的可观测性已形成成熟工具生态：

| 工具 | 定位 | 特点 |
|------|------|------|
| **LangSmith** | LangChain 官方追踪 | 与 LangGraph 深度集成，trace 可视化 |
| **Langfuse** | 开源可观测平台 | 自托管、多框架支持、评估+追踪一体 |
| **Arize Phoenix** | 开源 + OpenInference 标准 | 标准化追踪格式，跨框架统一 |
| **Datadog / CloudWatch** | 传统 APM 扩展 | Agent 与基础设施统一监控 |

一个完整的 Agent 可观测性方案应覆盖：**追踪（Trace）→ 指标（Metrics）→ 评估（Eval）→ 告警（Alert）→ 回放（Replay）**。追踪记录"发生了什么"，指标量化"做得怎样"，评估判断"好不好"，告警发现"出问题了"，回放用于"事后归因和回归测试"。

### 评估指标速查

| 维度 | 关键指标 |
|------|---------|
| 任务效果 | 任务成功率、最终答案准确率、人工接管率 |
| 过程效率 | 平均步数、平均工具调用数、token 消耗 |
| 性能 | 首 token 延迟、端到端延迟 p50/p95 |
| 成本 | 每次任务平均成本、token 单价 |
| 安全 | 越权次数、敏感动作拦截率、提示注入防御率 |
| 稳定性 | 超时率、重试率、降级触发率 |

## 与现有实践衔接

- 先完成 [函数调用 Agent](/AIAgent实践/函数调用Agent/) 的最小闭环。
- 对知识库型 Agent，结合 [RAG Agent 实战](/AIAgent实践/RAGAgent实战/) 检查召回和引用。
- 多角色系统需要额外关注 [多 Agent 协作](/AIAgent实践/多Agent协作/) 中的任务分工和冲突解决。

---

## 🆕 2026 最新进展

### AgentOps：Agent 可观测性的标准化

2026 年，**AgentOps**（Agent Operations）已成为 Agent 评估与可观测性的标准化方法论。根据 arXiv 论文 [AgentOps: Enabling Observability of LLM Agents](https://arxiv.org/abs/2411.05285) 的全面梳理，AgentOps 的核心思想是：在整个 Agent 生命周期中系统化追踪**制品（Artifacts）** 和**关联数据**，以实现有效可观测性。论文通过对现有 AgentOps 工具的系统映射研究，提出了一套完整分类法：

> 从 DevOps 视角看，Agent 的可观测性是确保 AI 安全的必要条件——利益相关者需深入理解 Agent 的内部运作，主动了解 Agent 行为、检测异常、预防潜在故障。

**AgentOps 生命周期分类法：**

| 阶段 | 追踪的制品 | 关键数据 |
|------|-----------|---------|
| **设计阶段** | 系统提示词、工具定义、知识库配置 | 版本历史、变更记录 |
| **构建阶段** | Agent 代码、依赖库、模型选择 | 构建产物哈希、依赖树 |
| **部署阶段** | 运行环境、模型权重、配置文件 | 部署时间戳、环境变量 |
| **运行阶段** | 输入输出、工具调用、中间推理 | 延迟、Token消耗、调用链 |
| **监控阶段** | 成功率、异常率、成本指标 | 告警阈值、SLA 达标情况 |

> 来源：[arXiv 2411.05285 — AgentOps: Enabling Observability of LLM Agents](https://arxiv.org/abs/2411.05285)

### 2026 年主流可观测性工具全景

2026 年 Agent 可观测性工具已高度成熟，形成多层级工具生态：

| 工具 | 核心定位 | 特色 | 适用规模 |
|------|---------|------|---------|
| **Langfuse** | 开源 LLM 可观测平台 | 自托管、多框架、评估+追踪一体化 | 中小规模、需要私有部署 |
| **LangSmith** | LangChain 官方追踪 | 与 LangGraph 深度集成，Trace 可视化 | 使用 LangChain/LangGraph 的项目 |
| **Arize Phoenix** | 开源 + OpenInference 标准 | 标准化追踪格式，跨框架统一 | 多框架混用的团队 |
| **Confident AI / DeepEval** | Agent 评估框架 | 内置 14+ 评估指标，CI 集成 | 需要自动化回归测试的团队 |
| **Datadog / CloudWatch** | 传统 APM 扩展 | Agent 与基础设施统一监控 | 已有监控基础设施的企业 |

> 来源：[Arize AI — LLM Observability for AI Agents and Applications](https://arize.com/blog/llm-observability-for-ai-agents-and-applications/)

### Agent 可观测性与普通应用监控的区别

Agent 的可观测性与传统应用监控有根本性不同，主要体现在：

| 维度 | 传统应用监控 | Agent 可观测性 |
|------|------------|---------------|
| **调用模式** | 请求→响应，可预测 | 多步 Agent 循环，路径不确定 |
| **状态管理** | 无状态或简单会话 | 有状态推理链+工具调用+记忆 |
| **输出验证** | 结构化返回码 | 非结构化文本+工具调用 JSON |
| **失败模式** | 超时/错误码/异常 | 幻觉/错误工具/计划损坏/循环 |
| **调试难度** | 可复现，日志即可 | 非确定性，需完整 Trace 回放 |

> 来源：[Reddit 讨论 — Agent Observability Is Way Different From Regular](https://reddit.com/r/ChatGPTCoding/comments/1qc0fhl/agent_observability_is_way_different_from_regular/)

**核心区别归纳**：Agent 可观测性需要追踪的是**"一条思考轨迹"**而非"一次请求"——包括 LLM 的每一步推理、工具调用的参数和结果、状态变化，以及最终的决策路径。

### Agent 评估框架的工程化

2026 年，使用专门的评估框架已成为最佳实践。以 **DeepEval**（Confident AI 开源）为代表的评估框架提供了系统性方法：

```python
# 使用 DeepEval 评估 Agent 的工具调用
from deepeval import evaluate
from deepeval.metrics import ToolCallingMetric, TaskCompletionMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="查询本月销售额并生成邮件回复",
    expected_tools=["query_sales_db", "generate_email"],
    actual_output="...Agent 实际输出...",
    tools_called=["query_sales_db", "generate_email"]
)

# 评估工具调用准确率
tool_metric = ToolCallingMetric()
tool_metric.measure(test_case)
print(f"工具调用准确率: {tool_metric.score}")
print(f"理由: {tool_metric.reason}")
```

**评估框架的核心能力：**

1. **工具调用评估**：检查 Agent 是否调用了正确的工具、参数是否正确、调用顺序是否合理
2. **任务完成度评估**：判断 Agent 是否完整完成了用户目标
3. **推理质量评估**：LLM 评估 Agent 的推理链是否逻辑连贯
4. **基于 Trace 的评估**：从完整追踪链中提取评估信号

> 来源：[Confident AI — LLM Agent Evaluation Metrics in 2026](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide)

### 2026 年 Agent 评估体系速查表

| 评估维度 | 关键指标 | 推荐工具/方法 |
|---------|---------|-------------|
| **任务完成** | 成功率、人工接管率、最终答案准确率 | DeepEval TaskCompletionMetric |
| **工具调用** | 工具选择准确率、参数正确率、调用顺序合规 | DeepEval ToolCallingMetric |
| **推理质量** | 推理链连贯性、计划合理性、逻辑一致性 | LLM-as-Judge 评估 |
| **过程效率** | 平均步数、Token 消耗、端到端延迟 | Langfuse / LangSmith Trace |
| **安全合规** | 越权次数、敏感动作拦截率、提示注入防御率 | 红队测试 + 人工审核 |
| **稳定性** | 超时率、重试率、降级触发率、P50/P95 延迟 | Datadog / CloudWatch |

### 生产级 Agent 可观测性架构

一个完整的 Agent 可观测性方案应覆盖 **5 层**：

```
追踪（Trace）→ 指标（Metrics）→ 评估（Eval）→ 告警（Alert）→ 回放（Replay）
```

- **追踪**：记录"发生了什么"——每一步工具调用、LLM 输出、状态变化
- **指标**：量化"做得怎样"——延迟分布、成功率、Token 消耗趋势
- **评估**：判断"好不好"——自动化回归测试、质量分数
- **告警**：发现"出问题了"——异常检测阈值、降级自动触发
- **回放**：事后"怎么修的"——失败 Trace 回放到评估集，防止同类问题再出现

### 评估的持续集成实践

2026 年的先进团队已将 Agent 评估纳入 CI/CD 管线：

```yaml
# 在 CI 中自动运行 Agent 评估
steps:
  - name: Run Agent Eval Suite
    run: |
      deepeval test run --tests test_agent_suite.py \
        --model-provider openai \
        --model gpt-4o-mini
  - name: Fail if quality below threshold
    run: |
      deepeval check --threshold 0.85
```

**关键实践**：
- 每个新工具添加后，自动生成工具调用测试用例
- 每次系统提示词变更，跑全量回归测试
- 失败轨迹自动入库，作为下一轮评估的测试集
- 设置质量门槛（如工具调用准确率 < 85% 则 CI 失败）

---

## 2026年Agent可观测性完整指南：从追踪到持续改进

### 为什么Agent需要可观测性

考虑一个场景：你的客服Agent Garry收到一条消息 "发票#4471被双重收费，能退款吗？" Garry按流程查政策、看账户、判定符合条件并发起退款。回复温暖自信，语法完美。**只有一个问题**——Garry退款给了发票#4477，一个因幻觉转置产生的错误ID，属于完全不同的客户。

问题在哪？Garry返回了HTTP 200，延迟曲线平稳，每条日志都显示"成功"。这个静默失败发生在三层调用深处的一个工具调用参数中——你拥有的所有仪表盘都看不到它。

这就是Agent可观测性所要解决的问题。

> 来源：[Confident AI — AI Agent Observability: Everything You Need to Know in 2026](https://www.confident-ai.com/blog/ai-agent-observability)

### 核心概念分层

| 层级 | 概念 | 说明 |
|------|------|------|
| **Span** | 一个工作单元 | 一次LLM调用、一次检索或一次工具调用 |
| **Trace** | 一次请求的完整span树 | Agent处理单条用户消息的全部过程 |
| **Thread** | 一个会话的所有trace | 多轮对话中每轮用户消息的trace集合 |
| **Session** | 用户一段时间内的thread | 跨时间维度的用户行为汇总 |
| **Run** | Agent的一次执行 | 单次运行的完整记录 |

**调试路径**：从Thread找问题对话 → 进入Trace → 放大到具体出错的Span。

### 四种Span类型

每种Span携带不同数据，回答不同问题：

| Span类型 | 记录内容 | 评估维度 |
|---------|---------|---------|
| **LLM** | prompt、completion、模型名、token数、延迟 | 推理质量、成本 |
| **Retriever** | 查询、返回chunk、embedder、top-k、chunk size | 检索上下文相关性 |
| **Tool** | 模型选择的参数、工具返回结果 | **参数幻觉在这里暴露** |
| **Agent** | 包含所有上述span的高层步骤 | 端到端效果 |

Garry的错误退款会在Tool span中直接暴露——一个转置的ID参数，清晰可见。

### 三大支柱：追踪、评估、监控

**追踪 (Tracing)** = 记录"发生了什么"。一次运行的完整span，回答"这次执行到底干了什么？"

**评估 (Evaluation)** = 判断"做得怎么样"。分为两层：

| 评估层级 | 测量对象 | 作用 |
|---------|---------|------|
| **端到端 (End-to-End)** | Agent最终回答 vs 用户需求 | 发现有问题 |
| **组件级 (Component-Level)** | 单个Span（工具正确性、检索相关性、参数正确性） | 定位哪里出问题 |

**监控 (Monitoring)** = 聚合视图。将追踪和评估转化为业务可用的聚合指标：成本、延迟、吞吐量——跨数千次运行。

三者关系：不附带评估的可观测性只是昂贵的日志记录。评估告诉你是对是错；监控告诉你成本的代价；追踪让三者关联在一起。

### 在线评估 vs 离线评估

| | 离线评估 (Offline) | 在线评估 (Online) |
|---|-------------------|-------------------|
| **时机** | 部署前（CI/CD） | 部署后持续运行 |
| **目的** | 防止回归 | 发现漂移和生产故障 |
| **参考数据** | 通常有预期输出 | 无参考，用reference-free指标 |
| **能发现** | 已知模式 | 未知的未知 |

**闭环**：在线评估发现了 #4471 发票问题 → 这个case加入离线数据集 → 下一版本必须通过它才能发布。在线评估发现你不能预见的问题；离线评估保证同样的问题不会出现第二次。

### Guardrails（护栏）：实时拦截

评估和信号都是在**事后**生效——这对学习有用，但对阻止伤害无用。Guardrails在请求路径中运行，能在响应到达用户前或工具执行前拦截：

- **输入护栏**：在Agent执行前拦截提示注入（OWASP LLM Top 10 #1风险）和越界请求
- **输出护栏**：在返回用户前捕获PII泄露、毒性内容、幻觉
- **工具护栏**：在执行前验证敏感操作（退款、删除、发邮件）是否被允许

**工具护栏正是阻止Garry错误退款的安全网**——在执行任何资金操作前确认发票归属客户。

### AI Agent可观测性框架（2026）

框架生态已标准化到OpenTelemetry（OTel）上：

| 方案 | 特点 |
|------|------|
| **OpenTelemetry GenAI语义约定** | 厂商中立，社区标准，覆盖模型调用、agent span、工具调用 |
| **自动插桩** | LangGraph、CrewAI、LlamaIndex、OpenAI Agents SDK等自带检测，无需装饰器 |
| **LLM-native SDK** | 更少的样板代码，更丰富的结构，可在插桩时附加评估 |

**推荐做法**：OTel作为传输层 + LLM-native SDK提供语义丰富度。

### 生产监控的核心指标

| 指标 | 关注点 |
|------|--------|
| 每次trace/thread/用户的成本 | 找到悄悄变贵的对话和客户 |
| 模型消耗分布 | 知道哪里换成更便宜的模型真的能省钱 |
| 延迟P50/P95/P99 | 评估和工具调用的时间分布 |
| 吞吐量 | 并发运行的agent数量 |
| 成功率趋势 | 按Agent类型、工具、模型分组的成功率 |

**法规要求**：NIST AI风险管理框架要求AI"在运行中定期测试"；EU AI Act对高风险系统要求自动事件记录。

### 何时不需要完整的可观测性

并非所有场景都需要完整追踪栈。以下情况可以跳过：
- **无工具、无检索、单步推理**的简单应用（一次性总结/分类器）——基本日志+小离线评估集即可
- **原型阶段**——print语句和少量测试用例比仪表化更快
- **低流量**——还能逐条手工审查每次交互

**临界点**：Agent在一次turn中链式调用 ≥2个工具、日请求量超过几十条、或者调试者不是编写者本人。可观测性从"可选的"变成"必需的"那天，就是你无法再逐条手工审阅每条trace的那一天。

> 来源：[Confident AI — AI Agent Observability: Everything You Need to Know in 2026](https://www.confident-ai.com/blog/ai-agent-observability)

### 闭环反馈循环：从生产故障到持续改进

2026 年 Agent 可观测性的最高境界不是"能看见问题"，而是**生产中发现的问题自动成为测试集的一部分，防止同类问题再次发生**。根据 Confident AI 的完整指南，这个闭环由以下环节构成：

#### 反馈循环的四个步骤

| 步骤 | 做什么 | 产出 |
|------|--------|------|
| **1. 发现问题** | 在线评估 + 用户反馈 + 信号分析自动发现失败轨迹 | 标记失败的 Trace |
| **2. 人工标注** | 人工审核失败案例，调整评估指标使其与人类判断对齐 | 修正后的标注数据 |
| **3. 入库回归** | 确认的失败案例自动加入离线评估数据集 | 新增回归测试用例 |
| **4. 持续验证** | 每次部署前跑全量回归测试，确保历史问题不复发 | CI 质量门禁 |

#### 信号（Signals）与评估（Evals）的区别

2026 年的先进 Agent 可观测性平台引入了**信号（Signals）** 概念，与传统的评估（Evals）互补：

| 维度 | Evals（评估） | Signals（信号） |
|------|-------------|----------------|
| **测量对象** | 你已定义好的指标 | 你未曾预见的新模式 |
| **触发方式** | 针对已知失败模式的明确指标 | 从生产流量中自动提取的异常模式 |
| **典型输出** | 工具调用准确率 85%、回复相关性 0.7 | "本周 '退款' 相关投诉量上升 40%" |
| **用途** | 确保已知问题不复发 | 发现你不知道自己有的问题 |

**最佳实践**：先用 Signals 探测生产中的新模式 → 确认是问题是 → 将其转化为一个正式的 Eval 指标 → 加入 CI 管线防止复发。

#### 自动化工作流

成熟的 Agent 可观测性管线应该尽可能自动化：

```yaml
# 理想的闭环流程
1. 在线评估自动标记失败 Trace
2. 失败 Trace 自动汇总到审查队列
3. 审查队列通知相关人员（Slack/邮件）
4. 人员标注完成后，案例自动加入离线数据集
5. 定时评估（每日/每周）自动检测偏移
6. 确认的失败案例自动提升为回归测试
```

**关键原则**：自动化的是"流程编排"而非"判断"。人工判断仍然需要——但应该只用在需要的地方，而不是手动复制粘贴数据。

> 来源：[Confident AI — AI Agent Observability: Everything You Need to Know in 2026](https://www.confident-ai.com/blog/ai-agent-observability)

---

## 🔍 2026 Agent 可观测性工具生态全景

2026 年的 Agent 可观测性已经从单一工具演变为**分层工具生态**，开发者需要根据自身阶段选择合适的工具组合。以下是按成熟度分层的工具选型指南。

### 工具分层选型

| 层级 | 适用阶段 | 代表工具 | 核心能力 |
|------|---------|---------|---------|
| **开发调试** | 本地开发、原型验证 | LangSmith, Langfuse (local) | 单次 Trace 可视化、Prompt Playground |
| **CI 评估** | 代码合并前 | DeepEval, Ragas, Braintrust | 离线评估、回归测试、质量门禁 |
| **生产监控** | 上线后持续运行 | Datadog, Langfuse (cloud), Arize Phoenix | 实时 Trace、异常告警、成本追踪 |
| **反馈闭环** | 持续优化 | Confident AI, Patronus AI | Signals → Evals 转换、自动回归 |

### CrewAI 的可观测性集成矩阵

CrewAI v1.15 官方支持 **13+ 可观测性平台**的原生集成，覆盖从开源到企业级的全场景。根据 [CrewAI Tracing 文档](https://docs.crewai.com/concepts/observability)：

| 集成平台 | 类型 | 核心能力 | 适用场景 |
|---------|------|---------|---------|
| **Langfuse** | 开源 | 追踪 + 评估 + Prompt 管理 | 中小团队全栈可观测 |
| **Arize Phoenix** | 开源 | OpenInference 标准追踪 | 跨框架统一观测 |
| **Braintrust** | 商业 | 评估驱动开发 | 高质量 AI 产品团队 |
| **Datadog** | 企业 APM | Agent + 基础设施统一监控 | 已有 Datadog 的团队 |
| **MLflow** | 开源 | 实验追踪 + 模型注册 | ML 实验管理 |
| **Weights & Biases (Weave)** | 商业 | 实验追踪 + 协作 | 研究型团队 |
| **OpenLIT** | 开源 | OpenTelemetry 原生 | CNCF 生态用户 |
| **Patronus AI** | 商业 | LLM 评估 + 安全检查 | 合规要求高的团队 |
| **Portkey** | 商业 | AI 网关 + 可观测 | 多模型提供商管理 |
| **Galileo** | 商业 | GenAI 评估 + 监控 | 企业级 AI 产品 |
| **Opik** | 开源 | Comet 出品追踪平台 | 替代 LangSmith 的开源方案 |
| **Maxim** | 商业 | AI 质量 + 安全评估 | 重视安全和质量的团队 |
| **TrueFoundry** | 商业 | MLOps 平台 | 端到端 AI 部署 |

### 选型决策树

```
你的团队情况 → 推荐方案

只有 1-2 人，快速验证
  → Langfuse (self-hosted) + DeepEval (离线评估)

3-10 人，已用 LangChain
  → LangSmith（开发）+ Langfuse（生产）

已用 Datadog 监控基础设施
  → Datadog LLM Observability + CrewAI 原生集成

开源优先，避免 vendor lock-in
  → Arize Phoenix（追踪）+ Opik（评估）+ OpenLIT（指标）

企业合规要求高
  → Patronus AI（安全评估）+ Datadog（审计日志）
```

### 2026 新兴趋势：Agent-Native 评估

传统的 LLM 评估（准确率、相关性、毒性检测）对 Agent 来说不够。2026 年出现了**Agent 原生评估维度**：

| 评估维度 | 检测什么 | 示例指标 |
|---------|---------|---------|
| **计划可行性** | Agent 制定的步骤计划是否合理 | 计划步骤数、跳过必要步骤率 |
| **工具选择准确率** | 是否正确选择工具 | 选错工具率、遗漏必要工具率 |
| **错误恢复能力** | 遇到工具失败后能否自动恢复 | 重试成功率、降级策略生效率 |
| **任务完成效率** | 完成任务消耗的资源 | 平均步数、token 消耗、端到端延迟 |
| **目标一致性** | 最终输出是否偏离用户意图 | 目标偏移距离、无关步骤比例 |

> 来源：[CrewAI Documentation — Observability](https://docs.crewai.com/concepts/observability)、[Confident AI — AI Agent Observability](https://www.confident-ai.com/blog/ai-agent-observability)

---

## 🧪 2026 前沿：UniClawBench — 能力驱动型 Agent 评估基准

2026 年出现的 **UniClawBench** 代表了 Agent 评估方法的重大转变：从"场景驱动"到"**能力驱动**"。

### 为什么需要能力驱动评估？

传统 Agent 基准的致命缺陷：**把任务按场景分类（客服 / 编程 / 数据分析），但每个场景内的任务同时混杂了对多种能力的要求**。Agent 失败时，你只知道"它做不好客服任务"，却不知道是工具选择出了问题、探索能力不足、还是长上下文理解崩溃了。

UniClawBench 改为按五种基础能力分类任务：

| 能力维度 | 检测什么 | 典型任务示例 |
|---------|---------|------------|
| **Skill Usage（技能使用）** | 是否正确选择并调用工具 | 调用正确的 API 完成数据查询 |
| **Exploration（探索能力）** | 能否主动浏览、发现信息 | 在未知网页中定位目标数据 |
| **Long-Context Reasoning（长上下文推理）** | 处理长文档、多轮对话推理 | 从多页合同中提取关键条款逻辑 |
| **Multimodal Understanding（多模态理解）** | 理解图文混合输入 | 解析截图中的表格数据 |
| **Cross-Platform Coordination（跨平台协调）** | 跨不同应用/系统协同操作 | 从邮件提取数据、录入 CRM、发通知 |

### 关键创新

1. **真实环境评估**：在 **Docker 容器**中运行 Agent，不依赖预录答案——Agent 真的需要操作浏览器、调用 API、执行代码
2. **细粒度检查点**：不是"结果对不对"的二元判断，而是 **step-by-step 完成点**——知道 Agent 在哪一步卡住
3. **闭环评估架构**：包含三个角色——
   - **Executor Agent**：被测试的 Agent
   - **Hidden Supervisor Agent**：暗中监督，不透露评分标准
   - **User Agent**：模拟真实用户的多轮反馈
4. **框架解耦**：在多个 Agent 框架下评估同一模型，区分"基模型能力"和"框架设计"各自的贡献

### 对实践者的启示

UniClawBench 的结果表明：**Agent 框架的设计选择和基模型能力同等重要**。即使使用同一底层模型，不同框架在跨平台协调任务上的得分可能相差 2 倍以上。这意味着：

- 选框架时不要只看模型 benchmark 分数，要针对你的任务类型做 AB 测试
- 评估 Agent 时要分开度量"模型能做什么"和"框架让它做了什么"
- 长上下文推理和跨平台协调是当前所有模型的共同短板

> 来源：[UniClawBench — A Universal Benchmark for Proactive Agents on Real-World Tasks](https://github.com/HKU-MMLab/UniClawBench) (arXiv, 2026)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-12 05:04:02*
