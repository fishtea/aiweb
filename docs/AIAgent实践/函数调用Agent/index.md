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

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-05 05:14:27*
