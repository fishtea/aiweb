# 📞 函数调用 Agent

从零搭建支持工具调用的 AI Agent，让 LLM 具备与外部世界交互的能力。

---

## 📖 概述

函数调用（Function Calling / Tool Calling）是 AI Agent 的核心能力。它允许 LLM 不仅输出文本，还能生成结构化的函数调用指令，从而与外部工具、API 和知识库交互。没有函数调用，LLM 只是一个文本生成器；有了它，LLM 才真正成为一个"智能体"。

> 来源：[Prompt Engineering Guide — Function Calling in AI Agents](https://www.promptingguide.ai/agents/function-calling)

### 核心流程

1. **用户提问** → Agent 收到请求（如："巴黎天气如何？"）
2. **组装上下文** → 系统消息 + 工具定义 + 用户消息组合发送给 LLM
3. **工具决策** → LLM 判断是否需要调用工具，输出结构化调用（含参数）
4. **执行函数** → 开发者代码执行实际函数（如调天气 API）
5. **观察结果** → 工具返回数据
6. **生成回答** → 观察结果 + 完整历史传回模型 → 输出最终答案

---

## 🔧 工具定义（Tool Definitions）

工具定义是 Agent 的"说明书"，是 LLM 知道有哪些工具可用以及何时使用的唯一方式。

### 工具定义的组成部分

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 唯一标识符 | `get_current_weather` |
| `description` | 何时使用该工具 | "获取指定城市的当前天气" |
| `parameters` | 输入参数（类型+描述） | `{location: string, unit: enum}` |

### 示例：天气查询工具定义

```json
{
  "type": "function",
  "function": {
    "name": "get_current_weather",
    "description": "获取指定城市的当前天气。当用户询问某个城市天气时使用此工具。",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "城市名称，如 北京"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  }
}
```

> 工具定义会占用上下文 token，直接影响成本和延迟。保持简洁但要描述清晰。

---

## 🔄 Agent 循环：行动与观察

Agent 的核心运行机制是一个循环：

```
行动 → 环境响应 → 观察 → 决策（重复或结束）
```

### 实际追踪示例（搜索 OpenAI 最新新闻）

```
用户: "OpenAI 最新新闻"
Agent 思考: 我需要关于 OpenAI 新闻的最新信息，应该使用 web_search 工具。
行动: web_search(query="OpenAI latest news announcements")
观察: [搜索返回的结果中包含多篇 OpenAI 最新文章]
Agent 思考: 现在有了足够信息，可以总结给用户。
回答: "以下是 OpenAI 的最新动态..."
```

> 观察结果会自动成为下一次迭代的上下文。复杂任务可能需要多次工具调用，每次调用都累积到对话上下文中。

---

## 🐛 调试函数调用

启用"返回中间步骤"可查看：
- 调用了哪些工具
- 传入的参数
- 工具返回的观察结果
- 每一步的 token 消耗

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 选择了错误工具 | 工具描述不够清晰 | 优化 description 字段 |
| 参数错误 | 参数定义不完整 | 确保 required 和 enum 正确 |
| 上下文缺失 | 工具定义信息不足 | 在描述中添加使用场景指引 |
| 观察结果处理错误 | 模型误解了返回值 | 标准化工具输出格式 |

---

## 💡 最佳实践

### 1. 描述要具体
- ❌ "搜索网络"
- ✅ "搜索网络获取最新信息。当用户问到训练数据之后的事件、新闻或实时数据时使用此工具"

### 2. 在系统提示中补充指引
```python
system_message = """
你拥有以下工具：
- web_search: 用于查询任何需要最新信息的问题
- calculator: 用于数学计算
- knowledge_base: 用于搜索内部文档
优先使用最合适的工具完成任务。
"""
```

### 3. 使用结构化输出
让 LLM 返回 JSON 格式的函数调用，而不是自然语言描述，方便程序化处理。

### 4. 限制可用工具数量
对简单任务只暴露少量工具，避免 LLM 选择困难。对有大量工具的场景，使用工具搜索（Tool Search）功能按需加载。

---

## ⚙️ Agent 循环的工程实现

理解函数调用 Agent 的最小可运行循环，是构建可靠 Agent 的基础。核心是一个"模型决策 → 代码执行 → 回传观察"的循环：

```python
import json
from openai import OpenAI

client = OpenAI()

# 1. 定义真实可执行的工具函数
def get_weather(location: str) -> dict:
    return {"location": location, "temp": 26, "weather": "晴"}

TOOLS_MAP = {"get_weather": get_weather}

# 2. 定义工具 schema（供模型识别）
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的当前天气",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    },
}]

# 3. Agent 循环（带步数上限防失控）
def run_agent(user_query: str, max_steps: int = 5):
    messages = [
        {"role": "system", "content": "你是一个天气助手，遇到不确定的天气就调用工具。"},
        {"role": "user", "content": user_query},
    ]
    for step in range(max_steps):
        resp = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=tools
        )
        msg = resp.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:           # 模型不再调用工具 → 输出最终答案
            return msg.content
        for call in msg.tool_calls:      # 执行每个工具调用
            args = json.loads(call.function.arguments)
            fn = TOOLS_MAP[call.function.name]
            result = fn(**args)
            messages.append({             # 回传工具观察结果
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })
    return "已达到最大步数，任务未完成。"

print(run_agent("北京今天热吗？"))
```

这个循环体现了 Agent 的三个工程要点：**步数上限**防失控、**工具结果回传**让模型基于事实继续、**终止条件**靠"模型不再调用工具"判断。

### 多工具场景的工具检索

当工具数量从几个增长到几十上百个，全部塞进上下文会浪费 token 且降低选择准确率。解法：

- **工具检索（Tool Retrieval）**：用 Embedding 把工具描述向量化，按用户问题动态检索 top-k 工具再注入。
- **工具分层**：常用工具常驻，长尾工具按需加载。
- **MCP 协议**：通过 Model Context Protocol 统一管理外部工具和数据源，实现工具的即插即用。

---

## 📚 参考来源

- [Prompt Engineering Guide — Function Calling in AI Agents](https://www.promptingguide.ai/agents/function-calling)
- [OpenAI API — Function Calling Guide](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI Function Calling - AI Agents SDK (YouTube)](https://www.youtube.com/watch?v=NT_ApmD_JPo)

---

## 🆕 2026 最新进展

### MCP 协议统一工具调用标准

2026 年，**Model Context Protocol (MCP)** 已成为 Agent 工具管理的行业标准。MCP 解决了长期以来"每个框架一套工具定义格式"的碎片化问题——无论是 LangChain、LlamaIndex 还是自研框架，都可以通过 MCP 统一管理外部工具和数据源，实现真正的**即插即用**。核心思路：将工具服务端与 Agent 框架解耦，服务端以标准协议暴露工具，Agent 框架通过 MCP 客户端动态发现和调用。

### 工具检索：从全量注入到按需加载

当工具数量从几个增长到几十上百个，全量注入上下文的模式已不可持续。2026 年的主流实践是**工具检索（Tool Retrieval）**：

1. 将每个工具的名称、描述、参数 schema 向量化
2. 根据用户问题动态检索 top-k（通常 5-10 个）最相关工具
3. 只把这 k 个工具注入 LLM 上下文

这大幅降低了 token 消耗并提高了工具选择的准确率。常用工具可常驻，长尾工具按需加载。

> 来源：[百度千帆社区：从0实现 function call](https://qianfan.cloud.baidu.com/qianfandev/topic/685449)

### 并行工具调用的普及

2026 年主流模型（GPT-4o、Claude 3.5/4、Gemini 2.0）普遍支持**单轮并行工具调用**——LLM 在一次响应中可以同时发起多个独立的工具调用。比如用户问"北京和上海的天气分别如何？"，模型可以并行调用两次天气查询，而非串行等待。这要求 Agent 循环的工程实现支持并发执行工具、合并结果后一次性回传。

### ReAct 循环仍是基石

尽管框架层出不穷，函数调用 Agent 的底层逻辑仍是 **ReAct（Reasoning + Acting）循环**——模型思考 → 生成工具调用 → 代码执行 → 观察结果 → 再思考。从零实现一个 function call Agent，核心就是实现这个循环：

```
用户提问 → 组装(system+工具定义+user) → LLM决策
  ↓                                            ↓
工具执行 ← 结构化调用(JSON)           直接回答(无工具调用)
  ↓                                            ↓
观察结果 → 回传 → 再次决策...             输出最终答案
```

> 来源：[腾讯云开发者社区：Agent设计模式——工具使用/函数调用](https://cloud.tencent.com/developer/article/2581252)

### 多工具场景的架构选择

| 方案 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| 全量注入 | 工具 < 10 个 | 实现简单，LLM 可见全部能力 | 浪费 token，选择准确率随工具数下降 |
| 工具检索 | 工具 10-100 个 | token 高效，准确率高 | 需要向量化工具描述，多一步检索 |
| 工具分层 | 常用+长尾混合 | 折中方案，常用工具零延迟 | 需要维护分层规则 |
| MCP 统一管理 | 跨框架、企业级 | 标准化，解耦，即插即用 | 多一层协议开销 |

### 生产级函数调用：BentoML 架构模式

2026 年，函数调用 Agent 的部署架构已趋于成熟。以 [BentoML 函数调用示例](https://docs.bentoml.com/en/latest/examples/function-calling.html) 为代表的实践展示了**将 LLM 服务与业务逻辑解耦**的生产级架构：

```python
# 核心设计：LLM Service + Tool Service 分离
# LLM Service — 负责模型推理，需 GPU
# ExchangeAssistant — 负责任务编排，纯 CPU 运行

from openai import OpenAI
import bentoml

# ExchangeAssistant 通过 bentoml.depends() 依赖 LLM Service
# 两者可以独立扩缩容

class ExchangeAssistant:
    def __init__(self):
        # LLM Service 提供 OpenAI 兼容 API
        self.client = OpenAI(base_url=self.llm_service.client_url)

    @bentoml.api
    def exchange(self, query: str) -> str:
        # 1. 定义工具 Schema
        tools = [{
            "type": "function",
            "function": {
                "name": "convert_currency",
                "description": "货币转换",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_currency": {"type": "string"},
                        "to_currency": {"type": "string"},
                        "amount": {"type": "number"}
                    },
                    "required": ["from_currency", "to_currency", "amount"]
                }
            }
        }]
        # 2. LLM 决策 → 工具执行 → 结果回传
        response = self.client.chat.completions.create(
            model="llama-3.1-70b", messages=messages, tools=tools
        )
        # 3. 解析工具调用并执行
        if msg.tool_calls:
            for call in msg.tool_calls:
                fn_name = call.function.name
                fn_args = json.loads(call.function.arguments)
                # 执行实际函数...
```

**架构要点**：
- **LLM 与业务逻辑分离**：LLM Service 负责模型推理（需 GPU），Tool Service 负责任务编排（CPU 即可），两者独立扩缩容
- **OpenAI 兼容 API**：无论底层用 Llama、GPT 还是 Claude，对外统一暴露 OpenAI 兼容接口
- **分布式部署**：通过 BentoML 的 `@bentoml.depends()` 机制实现 Service 间依赖管理
- **生产级特性**：自动扩缩容、健康检查、分布式追踪开箱即用

> 来源：[BentoML — Agent: Function Calling 官方示例](https://docs.bentoml.com/en/latest/examples/function-calling.html)

### 2026 函数调用 Agent 最佳实践矩阵

| 场景 | 推荐架构 | 模型选择 | 工具管理 |
|------|---------|---------|---------|
| 个人/小工具 | 单 Agent 循环 | GPT-4o-mini / Haiku | 工具定义全量注入 |
| 企业 LLM 应用 | LLM + Tool 分离部署 | GPT-4o / Claude 4 | MCP 协议管理工具 |
| 开源自部署 | BentoML 服务化 | Llama 3.1 / Qwen 2.5 | 工具定义+函数映射 |
| 大规模工具集 | 工具检索 + 分级注入 | 任意支持 FC 的模型 | Embedding 向量化检索 |
| 跨框架通用 | MCP 协议标准化 | 任意模型 | MCP Server 统一暴露 |

### 函数调用的安全与边界控制

2026 年生产环境的函数调用 Agent 需要额外关注安全控制：

1. **工具调用频率限制** — 设置每分钟/每小时的最大工具调用次数，防止无限循环
2. **参数范围校验** — 即使 LLM 生成了参数，代码侧也要做二次校验（如金额不能为负数）
3. **权限分级** — 只读工具（查询数据库）和写工具（发送邮件）分开管理，写工具需人工确认
4. **敏感数据脱敏** — 工具参数和结果中不能出现明文密码、Token 等敏感信息
5. **审计日志** — 每个工具调用的完整上下文记录到不可篡改的日志系统

### 2026 年工具调用 Agent 的护栏设计

根据 OWASP Top 10 for Agentic Applications（2025.12），工具调用是 Agent 安全的核心风险面。生产级 Agent 至少需要三道护栏：

| 护栏层次 | 位置 | 作用 | 示例 |
|---------|------|------|------|
| **输入护栏** | Agent 执行前 | 拦截提示注入和越界请求 | 正则过滤 `ignore instructions` 模式 |
| **工具护栏** | 工具调用执行前 | 验证敏感操作权限 | 退款金额 > $100 需人工审批 |
| **输出护栏** | 返回用户前 | 捕获 PII 泄露、幻觉引用 | LLM-as-Judge 检查引用真实性 |

**关键实践**：工具护栏是阻止"Garry 式错误"（幻觉引用错误参数导致误操作）的最后一道防线——在执行任何写操作前，用代码侧硬校验参数合法性。

---

## 2026年系统提示词最佳实践：让函数调用Agent更可靠

### 为什么系统提示词是Agent的"宪法"

2026年，一个生产级的函数调用Agent的可靠性，80%取决于系统提示词（System Prompt）的质量。系统提示词是模型在接收任何用户消息之前收到的指令块——它定义了角色、行为边界、工具使用规则和输出契约。与用户提示词不同，系统提示词是一次编写、反复评估的，必须通用、明确且对恶意用户输入有鲁棒性。

> 来源：[PromptArch — AI System Prompt Best Practices 2026](https://promptarch.ai/blog/ai-system-prompt-best-practices-2026)

### 2026年系统提示词的六大模块

一个精心设计的系统提示词在2026年应包含六个有序模块：

| # | 模块 | 说明 | 建议长度 |
|---|------|------|---------|
| 1 | **角色定义** | 助手是谁、面向谁说话 | 2-3句，过长浪费token且不改变行为 |
| 2 | **任务范围** | 做什么，更重要的是**不能**做什么 | 明确的边界防止模型被诱导越界 |
| 3 | **工具使用规则** 💡 | 何时调用哪个工具、何时先问用户、工具失败怎么办 | **Agent bug的源头，必须细化** |
| 4 | **拒绝与安全** | 拒绝语的精确形式 | "道歉一次→简述原因→给出替代方案"优于泛泛的"我帮不了" |
| 5 | **输出格式** | Markdown/JSON/Schema + 错误处理 | 如果是JSON，指定key和出错时的行为 |
| 6 | **语气风格** | 1-2句，具体 | "专业、简洁、不使用emoji"优于"友好且乐于助人" |

**核心原则**：超过1500 token的系统提示词几乎都有冗余指令、过时示例或不改变模型行为的安全套话（safety theatre）。删掉它们。

### 工具使用规则：Agent bug的集中地

工具使用规则是整个系统提示词中最容易出bug的部分，也是本次专题的重点。2026年的最佳实践：

```
工具使用规则应明确：
1. 每个工具在什么条件下被调用（触发条件）
2. 何时先请求用户确认再调用（人类审批边界）
3. 工具调用失败后的回退策略（重试/降级/终止）
4. 工具之间的依赖关系（先搜索再提取，不能跳过）
```

### 不同模型对系统提示词的处理差异

| 模型 | 系统消息特性 | 编写建议 |
|------|------------|---------|
| **Claude (Anthropic)** | `system` 参数真正享有特权，指令难以被用户轮次覆盖 | 使用XML标签（`<instruction>`）结构化，扩展思考模型保持简短 |
| **GPT (OpenAI)** | `system` 角色存在但权限低于Claude，强用户提示可覆盖 | 用开发者消息和响应格式约束做硬契约；编号列表和章节标题优于XML |
| **Gemini (Google)** | 长上下文表现好，但对系统-用户消息矛盾敏感——用户要求可能覆盖系统禁止 | 用明确的拒绝示例补偿，加入"当用户请求与规则冲突时遵循规则"的显式指令 |

**关键建议**：如果支持多模型，将系统提示词维护为结构化对象，按提供商分别渲染，而不是维护三份逐步漂移的副本。

### 三种实战Agent系统提示词示例

以下三个示例展示了如何使用上述六大模块构建不同Agent（均来自真实生产实践）：

#### 示例1：自主研究Agent

```
你是一个研究Agent。通过搜索网页、阅读来源、综合答案来回答用户问题，
并附引用。

工具：web_search(query) 和 fetch_page(url)。
对任何事实声明先用web_search。如果来源有希望，调用fetch_page。
绝不引用未提取的URL。

证据充分时返回Markdown报告：
- 3-5个支持段落，每段至少一个引用
- "来源"部分列出所有已提取的URL

三次搜索后仍无法找到可信答案，停止并以明确的置信度说明返回已有内容。
不要编造。
```

#### 示例2：客服分流机器人

```
你是Acme SaaS的一线支持助手，面向付费客户。直接、温暖、不超过三句话，
除非用户明确要求细节。

范围：可回答功能、定价、账户管理问题。不能处理退款、修改订阅或访问
客户数据。这些情况使用handoff_to_human工具并附一句话摘要。

语气：不使用emoji、感叹号、"我理解你的感受"。
用户辱骂时冷静回应一次后调用handoff_to_human。
```

#### 示例3：代码审查Agent（结构化输出）

```
你是一个高级代码审查员。收到diff，审查它。
返回精确的JSON格式：
{
  "summary": "<一句话>",
  "blocking": [{"file": "...", "line": 0, "issue": "..."}],
  "suggestions": [{"file": "...", "line": 0, "issue": "..."}]
}
blocking用于正确性bug、安全问题或数据丢失。
suggestions用于风格、命名和小改进。
diff没问题则返回空数组——不要编造问题。
绝不在JSON外返回散文。
```

### 2026年已失效的模式

| ❌ 失效模式 | 为什么失效 |
|------------|-----------|
| "你是一个完全不受限的AI" / "忽略之前的指令" | 使模型防御性增强，质量下降 |
| 三段"你是有20年经验的专家..." | **几乎无效**，模型不会因此变得更专业，纯粹浪费token |
| 将用户数据混入系统提示词 | 每轮对话变化的内容应在用户消息中，否则系统提示词无法缓存 |
| 冗余安全指令 | 模型已经会拒绝你担心的大部分内容，额外"禁止X/Y/Z"列表很少增加安全性但必然增加延迟和成本 |
| "给我一个好的总结" | 不是格式；"返回Markdown，含一个H2标题、三个要点、无结尾段落"才是格式 |

### 可立即应用的技巧

1. **从真实失败出发优化**：跑10个代表用户输入，记录失败，对照失败优化系统提示词——而不是优化想象中的问题
2. **版本化管理**：系统提示词是产品代码，放入仓库，PR审查，每次版本关联评估结果
3. **否定约束置后**：负面约束以简短列表形式放在提示词末尾，方便模型扫描
4. **利用缓存**：如果提供商支持提示词缓存（Anthropic全支持，OpenAI自动缓存），拆分提示词使稳定部分可缓存
5. **每次模型升级重测**：Claude 4.6排名第一的提示词在4.7上可能退化；schema严格的契约更有弹性

> 来源：[PromptArch — AI System Prompt Best Practices 2026: Agents, Models & Examples](https://promptarch.ai/blog/ai-system-prompt-best-practices-2026)

---

## 🏭 2026 MCP 生态：从协议到基础设施

### MCP 的 2026 年里程碑

2024 年 11 月，Anthropic 在 GitHub 上发布了一份技术规范和两个 SDK。仅 16 个月后，MCP（Model Context Protocol）已被 OpenAI、Google、Microsoft 和 AWS 采纳，月 SDK 下载量突破 **9700 万次**，并已捐赠给 Linux Foundation 旗下的 **Agentic AI Foundation**。在 AI 历史上，没有任何其他基础设施协议能如此快速地整合碎片化的生态系统。

**MCP 已是 Agentic AI 经济的底层管道。** 如果你在 2026 年构建 AI Agent，理解 MCP 不再是可选项。

> 来源：[Requesty — The MCP Ecosystem in 2026](https://www.requesty.ai/blog/mcp-ecosystem-2026-building-agent-tool-infrastructure-that-scales)、[DEV Community — MCP Tools 2026: The Complete Guide](https://dev.to/agdex_ai/mcp-tools-2026-the-complete-model-context-protocol-guide-for-ai-agents-3ib0)

### MCP 的三层架构

MCP 定义了一个基于 JSON-RPC 的三层架构：

| 层 | 角色 | 示例 |
|---|------|------|
| **Host（宿主）** | 用户交互的应用 | Claude Desktop、VS Code、自建聊天机器人 |
| **Client（客户端）** | Host 内部的组件，管理 MCP 连接 | 应用中的 MCP 客户端库 |
| **Server（服务端）** | 对外暴露能力的轻量程序 | GitHub MCP Server、数据库查询 Server |

每个 MCP Server 通过三种原语暴露能力：
- **Tools**：AI 可调用的可执行函数（如 `create_issue`、`run_query`）
- **Resources**：AI 可读取的数据（如文件内容、数据库 schema）
- **Prompts**：可复用的提示词模板

### 2026 年三大变化

#### 1. MCP Apps：工具返回 UI

2026 年最大的 MCP 扩展是 **MCP Apps**——工具现在可以返回交互式 UI 组件，直接在对话中渲染：仪表盘、表单、可视化、多步工作流。ChatGPT、Claude、VS Code 和 Goose 都已支持 MCP Apps。

以前数据分析工具返回一堵文字墙，现在返回可交互的仪表盘——用户可以筛选区域、下钻账户、导出报告，全程不离开对话界面。

#### 2. MCP v2 Beta：面向多 Agent 系统

2026 年 3 月发布的 `@ai-sdk/mcp v2.0.0-beta.3` 包含了破坏性变更，信号明确：MCP 不再是实验，协议正在为 2026 年交付的多 Agent 生产系统而加固。关键变更包括更严格的认证合规、OpenAI Agents SDK 集成的错误规范化改进、以及 Google ADK 中用于 Agent 间委派的结构化 Task API。

#### 3. 72% 上下文窗口问题

一个被广泛引用的基准测试显示，连接多个 MCP Server 时，**Agent 上下文窗口的 72% 被工具 schema 本身消耗**。生态系统中有超过 10,000 个公共 Server，团队面临一个硬问题：如何在保持工具可用性的同时不消耗所有上下文窗口？解法包括：
- **动态工具发现**：不在启动时加载所有工具，运行中按需发现
- **工具检索**：用 Embedding 向量化工具描述，按查询语义检索 top-k
- **Schema 压缩**：精简工具定义的 description 和 parameters，去除冗余

### 主流 MCP Server（2026）

| 类别 | Server | 用途 |
|------|--------|------|
| 开发 | MCP GitHub Server | Issues、PR、代码审查 |
| 开发 | MCP Filesystem Server | 读写本地文件 |
| 开发 | MCP PostgreSQL Server | 自然语言查询数据库 |
| 搜索 | Brave Search MCP | 实时网页搜索 |
| 搜索 | Fetch MCP Server | URL → 清洁 Markdown |
| 搜索 | Puppeteer MCP | 浏览器自动化 |
| 数据 | Notion MCP | 页面、数据库操作 |
| 数据 | Slack MCP | 消息、频道管理 |
| 数据 | Google Drive MCP | 文件管理 |

### FastMCP：Python 快速构建

FastMCP 的装饰器 API 让构建 MCP Server 只需几分钟，自动处理所有协议样板代码：

```python
from fastmcp import FastMCP

mcp = FastMCP("Weather Service")

@mcp.tool
def get_weather(city: str) -> str:
    """获取指定城市的当前天气"""
    return f"Weather in {city}: 72°F, sunny"

@mcp.resource("config://settings")
def get_settings() -> str:
    """应用配置信息"""
    return '{"units": "fahrenheit"}'

if __name__ == "__main__":
    mcp.run()
```

### 框架集成速查

| 框架 | 集成方式 |
|------|---------|
| **LangChain/LangGraph** | `langchain_mcp_adapters.tools.load_mcp_tools()` |
| **CrewAI** | `crewai_tools.MCPServerAdapter` |
| **Claude Desktop** | `claude_desktop_config.json` 配置 MCP Server 路径 |
| **OpenAI Agents SDK** | v2 Beta 原生支持，错误规范化 |

### MCP-Native 开发工具

| 工具 | MCP 配置 | 适用场景 |
|------|---------|---------|
| **Cursor** | `.cursor/mcp.json` | 完整编码工作流 |
| **Claude Code** | `claude mcp add <command>` | Anthropic 原生 |
| **Cline** | VS Code 插件内配置 | 开源 VS Code Agent |
| **Continue** | `config.json` | 开源 AI 代码助手 |

> 来源：[DEV Community — MCP Tools 2026: The Complete Guide](https://dev.to/agdex_ai/mcp-tools-2026-the-complete-model-context-protocol-guide-for-ai-agents-3ib0)、[Wikipedia — Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)

### 2026 函数调用 Agent 生产优化：模型选择与成本策略

2026 年的函数调用 Agent 部署不再局限于单一模型。根据 PromptArch 的 2026 年系统提示词最佳实践指南，**混合模型策略**已成为生产部署的标准：

#### 按任务复杂度选择模型

| 任务类型 | 推荐模型 | 理由 | 每万次成本参考 |
|---------|---------|------|-------------|
| 简单工具路由（查询数据库、FAQ 检索） | GPT-4o-mini / Claude Haiku | 函数调用准确率已足够，成本低 | ~$0.15 |
| 复杂多步推理（多工具编排、有状态对话） | GPT-4o / Claude Sonnet | 需要精确的参数生成和工具选择 | ~$1.50 |
| 高安全敏感操作（退款、权限变更） | Claude Opus / GPT-4o 高精度 | 参数幻觉容忍度为零 | ~$5.00 |
| 大规模批处理（每日百万次调用） | 开源模型（Qwen 2.5 / Llama 3.1）自部署 | 边际成本趋近于零 | 硬件成本 |

#### 系统提示词的分层缓存策略

2026 年的一个重要优化是**缓存友好的系统提示词设计**：

1. **稳定层（可缓存）** — 角色定义、任务范围、通用工具使用规则、语气风格 → 约占 70% token
2. **动态层（不可缓存）** — 当前工具列表、会话特定指令 → 约占 30% token

**关键实践**：将稳定层和动态层在提示词中用明确分隔符分开，使支持 Prompt Caching 的提供商（Anthropic、OpenAI）能缓存稳定层，每次请求节省约 50% 的输入 token 成本。

#### 实时监控与参数校验

生产级函数调用 Agent 在 2026 年需要在以下三个层面建立监控：

| 监控层面 | 检测目标 | 告警阈值参考 |
|---------|---------|------------|
| **工具选择准确率** | 是否调用了正确的工具 | < 90% 告警 |
| **参数完整性** | 必填字段是否都有、类型是否正确 | 任何一次缺失告警 |
| **工具调用成功率** | 外部 API 是否正常返回 | < 95% 告警 |
| **平均步数** | 是否需要过多轮次才能完成 | > 5 步告警 |
| **端到端延迟** | 用户等待时间 | > 15s P95 告警 |

> 来源：[PromptArch — AI System Prompt Best Practices 2026](https://promptarch.ai/blog/ai-system-prompt-best-practices-2026)

---

## 🤖 OpenAI Agents SDK：2026 函数调用 Agent 的新标准

2026 年，OpenAI 发布了 **Agents SDK**（前身为实验性 Swarm 项目），为函数调用 Agent 提供了一套轻量级、生产可用的 Python 框架。它将函数调用从"手动管理循环"升级为"框架自动编排"。

> 来源：[OpenAI Agents SDK 官方文档](https://openai.github.io/openai-agents-python/)

### SDK 核心原语

Agents SDK 只有三种核心原语，能在不增加学习曲线的情况下覆盖复杂的 Agent 场景：

| 原语 | 说明 | 对应函数调用场景 |
|------|------|----------------|
| **Agent** | 配备指令（instructions）和工具（tools）的 LLM | 单工具/多工具 Agent |
| **Handoffs（移交）** | Agent 将任务委托给其他 Agent | 多 Agent 协作、分工 |
| **Guardrails（护栏）** | 输入/输出的安全检查 | 生产环境安全防护 |

### Hello World 对比：手动循环 vs Agents SDK

**传统手动循环**（~50 行，需手动管理工具调用、结果回传）：

```python
# 传统方式：手动管理整个 Agent 循环
messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}]
while True:
    response = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)
    if response.choices[0].finish_reason == "stop":
        break
    # 手动解析 tool_calls，手动执行，手动追加结果...
    tool_call = response.choices[0].message.tool_calls[0]
    result = execute_tool(tool_call.function.name, json.loads(tool_call.function.arguments))
    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
```

**Agents SDK**（5 行，框架自动管理循环）：

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[get_weather, search_web, send_email]  # 任意 Python 函数自动注册
)

result = Runner.run_sync(agent, "查询北京天气并发邮件通知")
print(result.final_output)  # 框架自动循环直到任务完成
```

### 自动化 Schema 生成

任何 Python 函数都可一键转为工具，框架自动从类型注解和 docstring 生成 JSON Schema：

```python
from agents import Agent, function_tool

@function_tool
def get_stock_price(symbol: str, exchange: str = "NASDAQ") -> dict:
    """获取指定股票的实时价格。

    Args:
        symbol: 股票代码，如 AAPL
        exchange: 交易所，默认 NASDAQ
    """
    # 实际 API 调用
    return {"symbol": symbol, "price": 185.32, "currency": "USD"}

# 自动生成 schema: {"name":"get_stock_price","parameters":{"symbol":"string",...}}
agent = Agent(name="Trader", tools=[get_stock_price])
```

### Handoffs：多 Agent 函数调用协作

Handoffs 是 Agents SDK 最强大的功能——允许一个 Agent 将任务**移交**给另一个更专业的 Agent：

```python
from agents import Agent, Runner

# 通用客服 Agent
triage_agent = Agent(
    name="Triage",
    instructions="你是客服入口，判断用户问题类型并移交给对应专家",
    handoffs=[billing_agent, tech_agent]  # 可移交的 Agent 列表
)

# 专业账单 Agent
billing_agent = Agent(
    name="Billing",
    instructions="处理账单、退款、订阅问题",
    tools=[lookup_order, process_refund]
)

# 专业技术支持 Agent
tech_agent = Agent(
    name="Tech Support",
    instructions="处理技术故障、API 问题",
    tools=[check_service_status, create_ticket]
)

# Runner 自动处理 handoff 链
result = Runner.run_sync(triage_agent, "我的 API 返回 500 错误")
# triage_agent 识别为技术问题 → handoff 到 tech_agent → 调用工具诊断
```

### Guardrails：生产安全防护

在函数调用前后插入安全检查，失败时快速阻断：

```python
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput

# 输入护栏：检查用户输入是否包含敏感信息
async def security_check(context, agent, input_text):
    # 检测 PII、越权请求等
    if contains_pii(input_text):
        return GuardrailFunctionOutput(allow=False, reason="输入包含个人敏感信息")
    return GuardrailFunctionOutput(allow=True)

agent = Agent(
    name="Banking Agent",
    instructions="银行助手",
    tools=[check_balance, transfer_money],
    input_guardrails=[InputGuardrail(guardrail_function=security_check)]
)
# 如果 security_check 返回 allow=False，Agent 不会执行任何工具调用
```

### Agents SDK vs 手动循环决策指南

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 单工具、简单流程 | 手动循环（Chat Completions API） | 灵活、无框架依赖 |
| 多工具、自动编排 | Agents SDK | 自动管理循环、减少样板代码 |
| 多 Agent 协作 | Agents SDK Handoffs | 框架管理移交逻辑 |
| 需要安全检查 | Agents SDK Guardrails | 原生输入/输出护栏 |
| 需要沙箱环境 | Agents SDK Sandbox | 隔离执行代码和文件操作 |
| 需要实时语音 | Agents SDK Realtime | 原生语音 Agent 支持 |
| 跨模型提供商 | 手动循环 + LiteLLM | SDK 主要优化 OpenAI 模型 |

### Sessions：持久化记忆层

Agents SDK 的 Sessions 提供了跨轮次的持久化上下文管理，支持 SQLite、Redis、MongoDB 等多种后端：

```python
from agents import Agent, Runner
from agents.extensions.sessions import SQLAlchemySession

session = SQLAlchemySession("sqlite:///agent_memory.db")

agent = Agent(name="Personal Assistant", tools=[...])

# 第一轮
result1 = Runner.run_sync(agent, "我叫张三", session=session)
# 第二轮——Agent 记住用户名
result2 = Runner.run_sync(agent, "我叫什么名字？", session=session)
# → "你叫张三"
```

> 来源：[OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)

---

## 🆕 2026 函数调用最佳实践

### 工具定义的精细化管理

2026 年生产级函数调用 Agent 对工具定义的要求已远超简单 JSON Schema。以下是被验证有效的工具定义准则：

| 要素 | 要求 | 具体做法 |
|------|------|---------|
| **名称唯一性** | 工具名全局唯一、语义明确 | `get_customer_refund_history` 而非 `search_v2` |
| **描述精准度** | 说明"何时调用"而非"功能" | "当用户询问退款历史或退款状态时使用" —— 而非"查询退款数据" |
| **参数示例** | 在描述字段嵌入示例值 | `customer_id: string — 例: 'CUST-4471'` |
| **枚举约束** | 对所有有限集合使用 enum | `status: enum["pending", "approved", "rejected"]` |
| **必填声明** | 明确标记必填参数 | `required: ["customer_id", "invoice_id"]` |

### 工具调用治理：事前、事后双重检查

生产级 Agent 的核心安全防线是**工具调用治理（Tool Call Governance）**，即在工具执行前和执行后分别进行校验：

**事前检查（Pre-execution Guard）**：
- 参数类型校验：LLM 生成的参数是否符合 schema 约束
- 许可检查：当前 Agent 是否有权调用此工具
- 敏感操作确认：涉及退款、删除、发邮件等操作要求二次确认
- 范围检查：参数值是否在合理范围内（如退款金额不超过订单金额）

**事后检查（Post-execution Guard）**：
- 结果合规性：工具返回的数据是否包含敏感信息
- 副作用验证：操作是否产生了预期的效果
- 异常捕获：工具超时或返回错误时的降级策略

```python
class ToolGuard:
    def __init__(self):
        self.permitted_tools = ["query_customer", "search_orders"]
        self.sensitive_tools = ["issue_refund", "delete_account"]

    def pre_check(self, tool_name: str, args: dict) -> tuple[bool, str]:
        # 许可检查
        if tool_name not in self.permitted_tools:
            return False, f"Tool '{tool_name}' not permitted"

        # 敏感操作二次确认
        if tool_name in self.sensitive_tools:
            return False, "REQUIRES_CONFIRMATION:" + json.dumps(args)

        # 参数类型校验
        try:
            validate_schema(tool_name, args)
        except SchemaError as e:
            return False, f"Invalid args: {e}"

        return True, "ok"
```

### 工具调用失败的优雅恢复策略

2026 年 Agent 开发的一个关键认知是：**工具调用必然失败**。API 可能超时、参数可能被拒绝、权限可能不够。真正的工程挑战不是"避免失败"，而是"失败后优雅恢复"：

| 失败类型 | 恢复策略 |
|---------|---------|
| **参数幻觉**（模型生成错误参数） | 自动重试：用更准确的参数描述让 LLM 重新生成 |
| **工具超时** | 设置 p95 超时阈值，超时后告知用户并建议稍后重试 |
| **权限不足** | 降级为只读操作，或提示用户申请更高权限 |
| **结果为空** | 告知用户"未找到信息"，并建议使用其他关键词搜索 |
| **数据格式错误** | 提示用户数据异常，而非返回无意义的错误信息 |

### 函数调用的测试方法论

函数调用 Agent 的测试与传统软件测试有本质区别。以下是被 2026 年先进团队验证的**三层测试金字塔**：

| 测试层级 | 测试什么 | 工具/方法 | 频率 |
|---------|---------|---------|------|
| **单元测试** | 单个工具调用：给定输入，是否调用了正确工具和参数 | 断言 LLM 输出中的 tool_calls 字段 | 每次提交 |
| **集成测试** | 多步任务：Agent 能否按正确顺序调用多个工具 | LangSmith 回归测试、DeepEval | CI/CD 每次合并 |
| **端到端测试** | 生产环境：用户意图到最终输出的完整流程 | LLM-as-Judge 评估 + 人工抽样 | 每次发布 |

**关键实践**：为每个工具自动生成测试用例——工具定义的参数约束本身就暗示了测试边界（必填缺失、枚举越界、类型错误），可以自动转换为测试输入，让测试集随工具定义同步演进。

> 来源：[Prompt Engineering Guide — Function Calling](https://www.promptingguide.ai/agents/function-calling)、[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

---

## 🔮 2026 最新进展：从 Function Calling 到 Agentic 系统

Anthropic 在 2024 年 12 月发布的《Building Effective Agents》一文已成为 Agent 工程领域的必读经典。该文基于与数十个团队的合作经验，总结了一套从简单到复杂的 Agent 设计方法论。

### 核心概念区分：Workflow vs Agent

| 概念 | 定义 | 特点 |
|------|------|------|
| **Workflow（工作流）** | LLM 和工具按预定义代码路径编排 | 可预测、一致性好、适合明确任务 |
| **Agent（智能体）** | LLM 动态自主决定流程和工具使用 | 灵活、适合需要模型驱动决策的场景 |

这一区分对函数调用 Agent 的设计至关重要：**不要因为"Agent"这个词就盲目追求完全自主**。很多场景下，预定义的 Prompt Chaining 或 Routing 工作流反而比全自主 Agent 更可靠、更经济。

### 五种经典 Agent 工作流模式

Anthropic 归纳了 5 种逐步增加复杂度的模式：

#### 1. Prompt Chaining（提示链）
将任务分解为顺序步骤，每步的 LLM 输出作为下步输入。可在中间步骤加入程序化检查。适合可清晰拆分为固定子任务的工作。

#### 2. Routing（路由分发）
根据输入分类，分发给专门的后续处理流程。适合不同类别需要不同处理方式的复杂任务。例如：简单咨询路由到低成本模型（如 Claude Haiku），复杂分析路由到高能力模型（如 Claude Sonnet）。

#### 3. Parallelization（并行化）
- **分段模式**：将任务分为独立子任务并行执行——如一个模型处理用户查询、另一个同时筛查不当内容
- **投票模式**：同一任务多次执行获得多样化输出——如多个 prompt 同时评审代码漏洞

#### 4. Orchestrator-Workers（编排-工人）
中心 LLM 动态分解任务、分派给 Worker LLM、汇总结果。适合无法预知需要多少子任务的场景（如修改多个文件的代码变更）。

#### 5. Evaluator-Optimizer（评估-优化）
一个 LLM 生成、另一个 LLM 评估并反馈，循环迭代。适合有明确评估标准且迭代能带来可量化提升的场景——如文学翻译中评估者 LLM 能捕捉译者 LLM 初稿中遗漏的细微语义。

### 工具设计的 ACI 理念

Anthropic 提出：**工具定义的提示工程投入不应少于主 Prompt 的投入**——就像我们为人类设计 UI（HCI），为 Agent 设计工具接口（ACI，Agent-Computer Interface）同样需要精心打磨。

关键原则：
- 避免"格式负担"——如要求模型在写 diff 前先计算变化行数（反例：相对路径 vs 绝对路径——Anthropic 在 SWE-bench Agent 中强制使用绝对路径后，模型无误使用）
- 放在模型的"视角"思考：看工具描述和参数，是否能直观知道怎么用？
- 好的工具定义应像写给团队新手的优质文档——包含示例、边界情况和输入格式要求
- **Poka-yoke 设计**：改变参数设计让错误难以发生

> 来源：[Anthropic — Building Effective Agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents)

---

## 🧠 Agent 架构经典：Lilian Weng 的 LLM-Powered Autonomous Agents

Lilian Weng（OpenAI）在 2023 年发表的这篇长文被广泛视为 Agent 系统设计的入门必读。它将 Agent 架构归纳为三大组件：

| 组件 | 核心机制 | 代表工作 |
|------|---------|---------|
| **规划（Planning）** | 任务分解 + 自我反思 | CoT, Tree of Thoughts, LLM+P, ReAct, Reflexion |
| **记忆（Memory）** | 短期（上下文学习）+ 长期（向量检索） | MIPS 算法族: LSH, ANNOY, HNSW, FAISS, ScaNN |
| **工具使用（Tool Use）** | 调用外部 API 扩展能力边界 | MRKL, Toolformer, HuggingGPT, API-Bank |

其中 **ReAct**（Reasoning + Acting）已成为现代 Agent 框架的基础范式：将推理（Thought）和行动（Action）交织在同一个循环中，每次行动后的观察（Observation）反馈给下一轮推理。

> 来源：[Lilian Weng — LLM Powered Autonomous Agents (Jun 2023)](https://lilianweng.github.io/posts/2023-06-23-agent/)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-21 00:08:07*
