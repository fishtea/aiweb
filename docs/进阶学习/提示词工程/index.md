# 提示词工程

> 提示词工程（Prompt Engineering）是设计和优化提示词，以高效利用大语言模型完成各种任务的学科。

---

## 1. 什么是提示词工程？

**来源：** [Prompt Engineering Guide - DAIR.AI](https://www.promptingguide.ai)

> *"Prompt engineering is a relatively new discipline for developing and optimizing prompts to efficiently use language models (LMs) for a wide variety of applications and research topics."*

**来源：** [Ultimate Guide to Prompt Engineering 2026 - Lakera AI](https://www.lakera.ai/blog/prompt-engineering-guide)

> *"Prompt engineering is a soft skill with hard consequences — the quality of your prompts directly affects usefulness, safety, and reliability."*

提示词工程不仅关乎"怎么写提示词"，它涵盖了与 LLM 交互和开发的广泛技能：
- 理解模型能力与局限
- 设计高效提示结构
- 控制输出格式、风格和安全
- 防御对抗性攻击

---

## 2. 提示词类型与技巧

**来源：** [Prompt Engineering Guide - DAIR.AI](https://www.promptingguide.ai), [K2View - Prompt Engineering Techniques](https://www.k2view.com/blog/prompt-engineering-techniques)

### 2.1 零样本提示（Zero-shot）

直接给出任务指令，不提供示例。

```
将以下句子翻译成法语："Hello, how are you?"
```

### 2.2 少样本提示（Few-shot）

在提示词中包含多个示例，帮助模型理解任务模式和格式。

```
将英文翻译成法语：
English: "Good morning" → French: "Bonjour"
English: "Thank you" → French: "Merci"
English: "How much does this cost?" → French:
```

### 2.3 思维链提示（Chain-of-Thought, CoT）

引导模型逐步推理，特别适合数学、逻辑等复杂任务。

**来源：** [OpenAI Prompt Engineering Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

```
问题：一个长方形的长是 8 米，宽是 5 米，它的面积是多少？
让我们一步步思考：
面积 = 长 × 宽
面积 = 8 米 × 5 米
面积 = 40 平方米
答案：40 平方米
```

### 2.4 自一致性（Self-Consistency）

生成多个推理路径并投票选取最一致的答案。在 CoT 基础上进一步提高准确性。

### 2.5 角色提示（Role-based）

为模型分配特定角色，控制输出风格和专业性。

```
你是一位资深网络安全分析师。请分析以下日志...
```

### 2.6 提示链（Prompt Chaining）

将复杂任务拆分为多个子提示，逐步执行。适合需要多步处理的任务。

### 2.7 思维树（Tree of Thoughts, ToT）

在每个推理步骤探索多个可能性分支，进行广度优先搜索。

---

## 3. 提示词设计最佳实践

**来源：** [OpenAI Best Practices for Prompt Engineering](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

### ✅ 基本原则

| 原则 | 说明 |
|------|------|
| **指令放开头** | 使用 `###` 或 `"""` 分隔指令和上下文 |
| **具体明确** | 详细描述期望的输出内容、长度、格式、风格 |
| **分步指令** | 复杂任务拆分为步骤 |
| **提供示例** | 少样本提示通常优于零样本 |
| **指定输出格式** | JSON、Markdown、列表等 |
| **使用分隔符** | 清晰区分提示词的不同部分 |

### ❌ 常见错误

| 错误 | 示例 | 改进 |
|------|------|------|
| 模糊指令 | "写个摘要" | "用三句话总结以下文本，突出主要观点和结论" |
| 缺少约束 | "写一首诗" | "写一首 14 行十四行诗，主题是人工智能" |
| 未指定格式 | "列出要点" | "用 Markdown 无序列表列出 5 个要点" |

---

## 4. 提示词安全与风险

**来源：** [Lakera AI - Prompt Engineering Guide](https://www.lakera.ai/blog/prompt-engineering-guide)

提示词工程不仅是可用性工具，也涉及安全风险：

| 风险类型 | 描述 |
|----------|------|
| **提示注入** | 恶意输入覆盖系统指令 |
| **提示泄露** | 诱导模型输出系统提示词 |
| **越狱攻击** | 绕过模型安全限制 |
| **对抗性提示** | 利用模型漏洞产生有害输出 |

> *"You can often bypass LLM guardrails by simply reframing a question — the line between aligned and adversarial behavior is thinner than most people think."*

---

## 5. 提示词组件

| 组件 | 用途 | 示例 |
|------|------|------|
| **系统消息** | 设定行为、语气、角色 | "你是一位乐于助人的法律助手" |
| **指令** | 指导具体操作 | "用两个要点总结以下文本" |
| **上下文** | 提供背景信息 | 用户对话记录、文档等 |
| **示例** | 展示格式/语气 | 少样本/一样本示例 |
| **输出约束** | 限制输出格式/长度 | Markdown / JSON / 200 字以内 |
| **分隔符** | 区分提示词各部分 | `### 指令`、`"""`、`——` |

---

## 6. 进阶提示词技术

### 6.1 结构化提示词框架

生产环境中，提示词从"自然语言段落"演进为结构化模板，便于版本管理和复用。常见框架元素：

| 元素 | 作用 | 示例 |
|------|------|------|
| 角色（Role） | 设定专业身份和视角 | "你是资深数据分析师" |
| 任务（Task） | 明确要做什么 | "从日志中提取异常事件" |
| 上下文（Context） | 提供背景资料 | 历史对话、检索片段 |
| 约束（Constraints） | 限定范围和边界 | "不臆测未提供的数据" |
| 格式（Format） | 约束输出结构 | "输出 JSON，字段如下" |
| 示例（Examples） | 演示期望行为 | Few-shot 样例 |
| 思考（Reasoning） | 引导推理过程 | "先分析再回答" |

将提示词模板与变量分离（如 Jinja2、Mustache），可以让业务侧修改措辞而无需改动代码。

### 6.2 CoT 与推理引导

思维链（Chain-of-Thought）在推理模型出现后仍有价值，关键在于引导模型显式推理而非直接给答案：

| 技巧 | 指令片段 | 适用 |
|------|----------|------|
| 显式分步 | "请逐步分析，最后给出结论" | 数学、逻辑 |
| 自我提问 | "先列出解决这个问题需要哪些信息" | 规划类任务 |
| 验证回看 | "给出答案后，检查是否满足所有约束" | 约束满足问题 |
| 多路径投票 | "给出三种解法并比较" | 提高稳定性 |

### 6.3 防御性提示词设计

针对提示注入和越狱，推荐分层防御：

1. **指令分层**：系统提示用强约束语气，与用户输入用分隔符（`<user_input>`）物理隔离。
2. **输出校验**：要求模型输出结构化结果，后处理验证 schema，不合规则重试或拒答。
3. **能力边界**：明确列出"模型不该做什么"，例如"不得执行未列出的工具调用"。
4. **最小暴露**：不要在用户可见的回复中回显系统提示或工具定义。

### 6.4 提示词评估与版本管理

提示词是代码，需要工程化管理：

- **版本化**：每个提示词记录版本号、变更说明、对应模型和参数。
- **评估集**：准备 30-100 条代表性输入，对比新旧版本的输出质量，避免"改一处坏多处"。
- **A/B 测试**：线上分流对比点击率、采纳率、人工评分。
- **回归检测**：模型升级或参数调整后，自动跑评估集确认无显著退步。

> 经验：提示词的改动往往比换模型更便宜，但更难追踪。建立评估集是提示词工程从"手艺"走向"工程"的分水岭。

---

## 🔗 参考资料

- [Prompt Engineering Guide - DAIR.AI](https://www.promptingguide.ai)
- [Ultimate Guide to Prompt Engineering 2026 - Lakera AI](https://www.lakera.ai/blog/prompt-engineering-guide)
- [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
- [Prompt Engineering Techniques - K2View](https://www.k2view.com/blog/prompt-engineering-techniques)
- [Advanced 2026 Guide to Prompt Engineering - YouTube](https://www.youtube.com/watch?v=qBlX6FhDm2E)

---

## 7. 系统消息设计与生产级提示工程

> 来源：[System message design for Azure OpenAI - Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/advanced-prompt-engineering?pivots=programming-language-chat-completions)（2026 更新）

系统消息（System Message，也称 System Prompt 或 Metaprompt）是生产环境中**最重要但最容易忽视**的提示工程环节。它定义了助手的行为边界、语气和输出契约。

### 7.1 系统消息的核心作用

| 作用 | 说明 |
|------|------|
| **定义角色与边界** | 设定助手是什么、能做什么、不能做什么 |
| **设定语气与风格** | 正式/友好/简洁/详细…… |
| **指定输出格式** | JSON / Markdown / 固定 schema |
| **添加安全约束** | 拒绝越界请求、保护敏感信息 |

**关键原则**：系统消息可以影响模型行为，但不能保证完全合规。需要与过滤、评估等其他手段配合使用。

### 7.2 系统消息设计清单

Microsoft 推荐的六步设计法：

**① 明确助手的工作**
```
"你是一个内部产品的技术支持助手。"
```

**② 定义边界**
列出助手必须避免的主题、动作和内容类型：
```
- 不讨论政治、宗教话题
- 不提供医疗、法律建议
- 不执行未在工具列表中声明的操作
```

**③ 指定输出格式**
如果需要结构化输出，必须显式指定：
```
仅返回 JSON，使用以下 schema：
{"name": "", "amount": 0, "currency": "USD"}
```

**④ 添加"不确定时"策略**
明确告诉模型在以下情况该怎么做：
- 用户请求不明确 → 追问澄清
- 请求超出范围 → 礼貌拒绝
- 模型缺乏信息 → 说"我不知道"

**⑤ 测试、度量、迭代**
系统消息可能过拟合到特定示例，或在边缘情况下失效。需要：
- 用真实和对抗性提示进行测试
- 建立评估集（30-100 条）
- 每次修改后对比新旧版本

**⑥ 保持简洁**
系统消息越长，消耗的上下文窗口越大，留给用户内容的空间越小。能用一句话说清的，不要写一段。

### 7.3 三种典型系统消息模板

**场景一：技术支持（含回退策略）**
```
你是一个内部产品的技术支持助手。
如果你没有足够信息回答问题，请追问澄清。
如果仍然无法回答，请说你不知道。
```

**场景二：结构化实体提取**
```
你从用户文本中提取实体。
仅返回 JSON，使用以下 schema：
{"name": "", "company": "", "phone_number": ""}
```

**场景三：多约束问答助手**
```
你是一个财务合规助手，帮助员工理解公司政策。
- 只回答基于公司已发布的政策文档
- 如果政策文档未覆盖该问题，说"我需要在政策中查找相关信息"
- 不提供个人建议或主观判断
- 响应使用中文，术语可保留英文
```

### 7.4 常见陷阱

| 陷阱 | 示例 | 改进 |
|------|------|------|
| **指令冲突** | "保持简洁" + "全面覆盖所有细节" | 明确优先级："优先简洁，再补充关键细节" |
| **过于冗长** | 3000 token 的系统消息 | 压缩到 500 token 以内，将细节放在使用说明中 |
| **隐含需求** | 期望 JSON 输出但未提及 | "仅返回 JSON，使用以下 schema" |
| **缺少回退策略** | 未说明"不知道怎么办" | 添加明确的不确定处理流程 |
| **不安全默认值** | 未限制工具调用范围 | 添加白名单："只能调用 search_docs 和 get_policy 两个工具" |

### 7.5 系统消息 vs 用户消息

| 对比维度 | 系统消息 | 用户消息 |
|---------|---------|---------|
| 优先级 | 最高（多数模型优先遵循） | 次之 |
| 可见性 | 对用户不可见 | 用户可见 |
| 变更频率 | 低频（随版本发布） | 每次对话都可能不同 |
| 安全风险 | 低（受控输入） | 高（可能包含对抗性内容） |
| 长度限制 | 占用上下文窗口 | 动态变化 |

### 7.6 参考来源

- [System message design for Azure OpenAI - Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/advanced-prompt-engineering)
- [Microsoft Safety system message templates](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/safety-system-message)
|- [Prompt Engineering Techniques - OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/articles/techniques_to_improve_reliability.md)

---

## 8. 面向推理模型的新一代提示词工程

2025-2026 年，推理模型（Reasoning Models）如 OpenAI o1/o3、DeepSeek-R1、Claude 3.5 Sonnet（Thinking Mode）、Gemini 2.5 Pro Thinking 等彻底改变了提示词工程的范式。与传统模型直接输出答案不同，推理模型在内部进行"思考"（Chain-of-Thought 隐藏在模型内部），然后给出答案。

### 8.1 推理模型 vs 传统模型的提示差异

**来源：** [Reasoning Models: A New Era of AI - DeepLearning.AI](https://www.deeplearning.ai/the-batch/reasoning-models-and-the-future-of-ai/), [o1 Prompting Guide - OpenAI](https://platform.openai.com/docs/guides/reasoning)

| 维度 | 传统模型（GPT-4o, Claude 3） | 推理模型（o1, DeepSeek-R1, Gemini 2.5 Pro） |
|------|------------------------------|---------------------------------------------|
| 推理方式 | 外部 CoT（需提示引导分步） | 内部隐式推理（模型自主深度思考） |
| 提示风格 | 需详细说明推理步骤 | 直接给任务，模型自行推理 |
| Few-shot 效果 | 极好（示例引导模式） | 常规（内部推理可能被示例局限） |
| 最佳实践 | "Let's think step by step" | 简洁指令 + 清晰目标 |
| 延迟 | 低 | 中-高（内部推理耗时） |
| 输出格式 | 不稳定，需格式约束 | 较稳定，可指定结构 |

### 8.2 推理模型的提示原则

**原则一：简化指令，明确目标**

推理模型擅长自主规划推理路径，不需要在提示词中手把手教它如何推理：

```
❌ 不推荐："首先分析已知条件，列出解决方案，评估优缺点..."
✅ 推荐："分析这个定价优化问题，给出最优策略及依据。"
```

**原则二：将约束条件放在系统消息中**

推理模型对系统消息中的约束遵循度较高，可将输出格式、安全边界等放在系统消息层：

```
你是一个金融分析助手。
- 只基于给定的数据做分析，不臆测数据之外的结论
- 输出使用 JSON 格式
- 如果数据不充分，明确指出信息缺口
```

**原则三：提供明确的质量标准**

推理模型能理解并优化到指定的质量水平：

```
生成一份项目风险评估报告。
- 深度：分析每个风险的根因、概率、影响和应对策略
- 格式：Markdown 表格 + 要点说明
- 标准：每个风险项必须有至少 2 个备选方案
```

### 8.3 推理模型的三种提示模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **零样本直接提问** | 直接给任务，让模型自行推理 | 复杂分析、数学物理、代码生成 |
| **限定推理范围** | 在系统消息中划定推理边界 | 需要控制成本和延迟的场景 |
| **引导式提问** | 给出结构化框架但留推理空间 | 报告生成、多角度分析 |

### 8.4 推理模型的成本控制策略

推理模型的内部推理消耗大量 token，成本比传统模型高 3-10 倍：

| 策略 | 方法 | 效果 |
|------|------|------|
| **设置 max_tokens 上限** | 限制总输出长度（含内部推理） | 直接控制成本 |
| **推理预算（Reasoning Effort）** | OpenAI o1 支持 low/medium/high | low ≈ 降低 60% 推理成本 |
| **路由策略** | 简单问题走传统模型，复杂问题走推理模型 | 综合成本最优 |
| **缓存复用** | 对同一问题的推理过程做 KV Cache | 重复查询零额外推理成本 |

> **经验：** 80% 的日常查询不需要推理模型。建议搭建路由层：简单问答 → 传统模型（GPT-4o-mini），复杂推理 → 推理模型（o1/R1），可在保持质量的同时将推理成本降低 70-80%。

### 8.5 与传统模型提示的迁移指南

| 保留的做法 | 放弃的做法 |
|-----------|-----------|
| 清晰的任务描述 | 手写分步推理指令（"Let's think step by step"） |
| 输出格式约束 | 过多的 Few-shot 示例 |
| 安全边界和约束 | 角色扮演式的冗长背景故事 |
| 上下文/参考材料 | 过度详细的中间推理引导 |

> **关键洞察：** 推理模型的出现不是提示词工程的终结，而是提示词工程从"教模型怎么推理"转变为"告诉模型要解决什么问题"。提示词变得更简洁，但对目标定义、质量标准和约束条件的精确度要求更高。

### 8.6 参考来源

- [Reasoning Models: What They Are and Why They Matter - DeepLearning.AI](https://www.deeplearning.ai/the-batch/reasoning-models-and-the-future-of-ai/)
- [OpenAI o1 Reasoning Model Prompting Guide](https://platform.openai.com/docs/guides/reasoning)
- [Extended Thinking (Reasoning) - Anthropic Claude Docs](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Prompt Engineering for Reasoning Models - LangChain Blog](https://blog.langchain.dev/reasoning-models-prompting/)

## 2026 年提示词工程进阶实践：缓存、结构化输出与生产模式

> 来源：[OpenAI Responses API 指南](https://developers.openai.com/api/docs/guides/latest-model)（2026 更新），[Prompt Caching 排查实践 - 菠萝AI笔记](https://www.boluoblog.com/coding/openai-responses-prompt-caching-miss-2026/)，[GPT Prompting Production Patterns](https://gptprompts.ai/chatgpt-api-prompting)

### 生产级提示词工程的三层架构

2026 年，成熟的提示词工程体系已从"写提示词"演进为**多层级系统工程**：

| 层级 | 组件 | 职责 |
|------|------|------|
| **系统层** | System Prompt / Meta Prompt | 定义行为边界、角色、安全约束（低频变更） |
| **应用层** | 模板引擎（Jinja2 / Mustache） + 变量注入 | 将动态内容填入固定模板（中频变更） |
| **运行时层** | Prompt Caching / 语义路由 / 质量门禁 | 控制成本、延迟和输出质量（自动运行） |

### Prompt Caching：成本优化的第一道防线

OpenAI Responses API 的 **Prompt Caching** 是 2026 年控制推理成本最直接的手段。命中缓存的输入 token 享有折扣价，但实际命中率取决于工程实现：

#### 缓存命中条件

| 条件 | 说明 | 常见故障 |
|------|------|---------|
| 前缀精确匹配 | 请求开头的 token 序列必须完全一致 | 动态值（时间戳、trace_id）放在了最前面 |
| 最小 1024 tokens | 低于 1024 tokens 的请求不参与缓存 | 短查询永远 miss |
| 128-token 台阶增长 | 命中按 128-token 增量计费 | 980-token 请求显示 cached_tokens=0 是正常结果 |

#### 缓存命中排查三步骤

```python
# 步骤 1：检查 cached_tokens 字段
response = client.responses.create(...)
cached = response.usage.input_tokens_details.cached_tokens
if cached == 0 and total_input > 1024:
    print("需要排查请求前缀稳定性")

# 步骤 2：固定可复用前缀的顺序
# ✅ 正确：将稳定内容放在开头
instructions = "You are a code reviewer."  # 放最前面
tools = [readRepoTool, searchIssueTool]    # 固定顺序
user_input = f"Review this diff: {diff}"   # 动态部分放最后

# ❌ 错误：将动态值放在开头
instructions = f"You are a code reviewer. Request time: {datetime.now()}"
```

#### 工程实践建议

| 策略 | 方法 | 效果 |
|------|------|------|
| **固定工具定义顺序** | 不要每次重组 tools 数组 | 避免前缀变化导致 miss |
| **使用 prompt_cache_key** | 为同类请求分配相同分桶键 | 同前缀请求路由到同一缓存节点 |
| **系统提示与用户输入分离** | 系统消息在前，用户消息在后 | 最大化可复用前缀长度 |
| **Structured Outputs 固定 schema** | 输出 schema 顺序不变 | schema 定义参与缓存键计算 |

> **经验**：Prompt Caching 的收益不只看命中率。cached_tokens 上升但账单没降时，通常是因为输出 token、reasoning 或工具调用费用在同步增长。

### 结构化输出的生产级方案

2026 年，结构化输出已成为生产级应用的标准配置。主流方案对比：

| 方案 | 实现方式 | 保证级别 | 适用场景 |
|------|---------|---------|---------|
| **OpenAI Structured Outputs** | API 原生支持，server-side 校验 | 100% JSON schema 合规 | OpenAI 模型 |
| **Outlines** | 基于 logit 正则约束的生成 | 严格语法保证 | 开源模型本地部署 |
| **JSON mode + Pydantic** | 提示词要求 JSON + 后处理校验 | 高（依赖模型） | 任意 API 兼容 |
| **LMQL** | 声明式约束语言 | 严格语法保证 | 需要自定义约束 |

#### 典型实现：Pydantic + LLM 的结构化提取

```python
from pydantic import BaseModel
from openai import OpenAI

class ExtractedEntity(BaseModel):
    name: str
    company: str
    position: str
    confidence: float

client = OpenAI()
response = client.responses.create(
    model="gpt-4o-mini",
    input="从以下文本中提取实体...",
    text={
        "format": {
            "type": "json_schema",
            "name": "entity_extraction",
            "schema": ExtractedEntity.model_json_schema()
        }
    }
)
entity = ExtractedEntity.model_validate_json(response.output_text)
```

### GPT-5.6 时代的提示词新特性

OpenAI GPT-5.6（2026 年发布）引入了多项提示词相关的突破性特性：

| 特性 | 说明 | 对提示词设计的影响 |
|------|------|------------------|
| **Programmatic Tool Calling** | 模型可编写 JS 脚本调用工具，串行执行无需每次调用模型 | 减少多步工具调用中的模型往返次数 |
| **Multi-Agent Coordination** | 单一 GPT-5.6 实例可协调多个子 Agent 并行工作 | 提示词需要定义子任务边界和汇总策略 |
| **Reasoning Effort 控制** | low/medium/high 三级推理预算 | 简单任务用 low effort，复杂推理用 high |
| **Cross-Turn Reasoning** | 跨轮次复用推理状态 | 长篇对话不再需要重复推理过程 |
| **自动推断任务复杂度** | 模型根据上下文自动选择推理深度 | 不需要人工猜测该用哪个 effort 级别 |

**对提示词工程师的影响**：
- 不再需要手写"Let's think step by step" — 推理模型自行决定推理路径
- 提示词从"教模型怎么做"转向"告诉模型要什么结果"
- 质量标准和约束条件的精确度要求更高

### 提示词质量门禁：输出校验自动化

生产环境中，提示词的输出质量需要自动校验而非人工检查：

| 门禁层级 | 检查内容 | 工具/方法 |
|---------|---------|----------|
| **Schema 校验** | JSON/YAML 格式正确性 | Pydantic / JSON Schema |
| **内容校验** | 必填字段、长度限制、关键词覆盖 | 规则引擎 |
| **语义校验** | 与期望分布的相似度 | LLM-as-Judge |
| **安全门禁** | PII 泄漏、敏感内容、注入检测 | 内容过滤 + 正则 |

**实践建议**：每次提示词变更后自动运行 30-100 条评测集，对比新旧版本的通过率。提示词的改动比换模型更便宜，但更难追踪——建立评估集是提示词工程从"手艺"走向"工程"的分水岭。

### 参考来源

- [Compare model features, migration guidance, and prompting best practices - OpenAI](https://developers.openai.com/api/docs/guides/latest-model)
- [Prompt Caching 排查实践 - 菠萝AI笔记](https://www.boluoblog.com/coding/openai-responses-prompt-caching-miss-2026/)
- [ChatGPT API Prompting: Production Patterns & Examples](https://gptprompts.ai/chatgpt-api-prompting)
- [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

---

## 11. 2026年7月提示词工程前沿

### 11.1 从提示词工程到认知提示（Epistemic Prompting）

**来源：** [From Prompt Engineering to Epistemic Prompting: Prompt Trajectories as AI-Mediated Problem Framing in Science Education - arXiv:2607.11680 (2026-07-13)](https://arxiv.org/abs/2607.11680v1)

这篇来自意大利卡利亚里大学的研究重新定义了 STEM 教育场景下的提示词设计范式。作者 Matteo Tuveri 认为，传统"提示词工程"过于强调**技术性产出（准确性、格式、相关性）**，但在教育场景中，提示词更应该被理解为一种**持续的认知实践（epistemic practice）**。

**核心框架：Framing-Prompting Loop（框架-提示循环）**

```
初始提示 → 建立临时宏框架（问题、表示、假设、标准、人机分工）
    ↓
模型响应 → 学习者理解/吸收
    ↓
学习者下一轮提示 → 维持 / 细化 / 挑战 / 修复 / 转换框架
    ↓
学科检查 → 验证知识是否符合学科规范
    ↓
重新框架（Reframing）→ 循环继续
```

**与传统提示词工程的本质区别：**

| 维度 | 传统提示词工程 | 认知提示（Epistemic Prompting） |
|------|-------------|---------------------------|
| **目标** | 获得"正确"输出 | 发展知识和理解能力 |
| **评估标准** | 准确性、相关性、格式 | 学科规范、推理深度、概念转变 |
| **提示词角色** | 一次性指令 | 持续的框架协商工具 |
| **人机关系** | 人类指挥、AI 执行 | 人类与 AI 共同构建知识 |
| **成功标志** | 输出匹配预期 | 学习者的概念理解和推理能力提升 |

**提示框架轨迹（Prompt Framing Trajectory）：**

论文提出，教育的真正产出不是单次提示词的结果，而是整个**提示框架轨迹**——即从初始提示到最终理解的完整发展路径。这条轨迹包含：
- 初始宏框架（决定了后续所有交互的"游戏规则"）
- 每一轮的框架操作（维持、细化、挑战、修复、转换）
- 学科检查点的介入时机

> **实践意义**：在 AI 辅助教育产品设计中，不应仅关注"如何写出更好的提示词"，而应设计支持框架演化的交互界面——让学生能够看到并反思自己的提示词如何塑造了 AI 的回答，以及这些回答又如何反过来塑造了他们对问题的理解。

---

### 11.2 ThinkLog：将推理注入提示词实现日志语句生成

**来源：** [ThinkLog: Leveraging Reasoning for Log Statement Generation - arXiv:2607.11615 (2026-07-13)](https://arxiv.org/abs/2607.11615v1)

来自日本九州大学和南山大学的研究团队提出了 ThinkLog——一种基于 LLM 的端到端日志语句生成方法，其核心创新在于**将推理过程注入提示词**。

**传统日志生成的三难困境：**

软件工程中，日志语句生成需要同时决定三个要素：
1. **日志位置（Where）**：在代码的什么位置插入日志
2. **严重级别（Severity）**：INFO / WARNING / ERROR
3. **日志消息（Message）**：写什么内容

传统方法将这三个决策分离处理，导致准确性受限。ThinkLog 的创新在于让 LLM **通过推理链一次性完成三个决策**。

**提示词设计：推理注入模式**

ThinkLog 在 few-shot 示例中嵌入了完整的推理过程：

```
示例：
代码片段: [Java method]
推理: (1) 在该方法的数据库操作后需要记录执行状态
      (2) 如果出现异常应记录 ERROR 级别
      (3) 日志消息应包含方法名、参数和返回值
日志: [location: line 42] [severity: INFO] "UserService.createUser completed, userId={}"
```

**实验结果（在 9,619 个 Java 方法上评测）：**

| 方法 | 日志生成准确率 | 推理成本（USD） |
|------|-------------|---------------|
| 此前最佳方法 | 17.81% | 基准（100%） |
| **ThinkLog** | **20.55%** | **约 50%** |

> **关键洞察**：ThinkLog 以约一半的推理成本实现了 15.4% 的相对提升。这验证了一个重要模式：**在 few-shot 提示词中提供推理示例，比增加更多"正确输出"的示例更高效**。推理过程让模型学到了"为什么这样决策"，而非仅仅模仿输出格式。

**提示词工程启示：**
- 对于需要多步决策的生成任务，在 few-shot 示例中加入"为什么"而不仅仅是"是什么"
- 推理链的成本可以通过优化推理长度来控制——ThinkLog 通过更精准的推理降低了 token 消耗
- 这一模式可推广到代码审查、测试生成、配置生成等其他软件工程任务

---

### 11.3 Prompt Generation（PG）框架：配置驱动的工业级提示词生成

**来源：** [Prompt Generation Technical Report - arXiv:2607.11326 (2026-07-13)](https://arxiv.org/abs/2607.11326v1)

来自阿里巴巴淘宝搜索团队的技术报告，描述了一种已在生产环境中验证的配置驱动提示词生成框架。这不是关于"如何写提示词"的指南，而是一个**将特征工程从模型架构中解耦的工程框架**。

**问题背景：工业搜索/推荐系统的特征-模型耦合困境**

在淘宝搜索等工业场景中，生成式检索模型依赖丰富的用户行为特征，但传统做法将**特征处理逻辑与模型架构紧密耦合**：
- 每次特征变更需要同时修改训练和推理代码
- 不同业务场景之间无法复用特征逻辑
- 在线延迟预算紧张，特征计算开销需要精细控制

**PG 框架的三层加速：**

```
声明式配置（两个 JSON 文件）→ 特征类型 → 可组合处理组件 → 统一训练/推理管道
```

| 加速层级 | 机制 | 效果 |
|---------|------|------|
| **训练迭代加速** | 特征实验只需修改配置文件，内置 token 压缩 | 实验周期从天级降至小时级 |
| **部署加速** | 新场景只需符合 PG schema 即可接入通用管道 | 无需场景专属工程开发 |
| **推理加速** | 引擎对标准化配置应用统一优化 | PG 开销降至可忽略水平 |

**在线 A/B 实验结果：**
- 成交笔数（Transaction Count）：**+0.47%**（统计显著）
- GMV（成交总额）：**+0.51%**（统计显著）

> **实践意义**：对于构建 LLM 应用的团队，PG 框架提供了一个重要的架构参考——将"提示词构建"提升为独立的配置层，使其与模型和服务代码解耦。这种解耦带来的迭代速度提升，往往比模型本身的性能提升更直接地影响业务指标。

---

## 12. 推理模型时代的提示词工程新范式

### 12.1 推理模型 vs GPT 模型：两种完全不同的提示策略

**来源：** [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)（2026年7月版）

2026年，以 OpenAI o-series、DeepSeek R1、Claude Opus 为代表的**推理模型（Reasoning Models）** 已与传统 GPT 系列模型在提示策略上形成了根本差异。OpenAI 的最新官方指南对此做了清晰的定义：

| 对比维度 | GPT 模型（如 GPT-5、GPT-4o） | 推理模型（如 o3、o4-mini） |
|---------|---------------------------|-------------------------|
| **提示风格** | 需要极精确的指令，明确提供逻辑和所需数据 | 只需高层级目标，模型自主推理出细节 |
| **提示长度** | 较长的提示通常效果更好（提供完整上下文） | 简洁的高层级指引即可，过度约束反而限制推理 |
| **比喻** | 像初级员工 —— 需要明确每一步该做什么 | 像资深同事 —— 告知目标即可信任其规划 |
| **示例使用** | few-shot 示例极其重要 | 示例可能限制推理路径，更依赖思维链 |
| **结构化输出** | 需要精确的 JSON schema 约束 | 原生理解复杂结构，较少需要显式约束 |
| **成本/速度** | 更快、更便宜 | 较慢（内部思维链过程）、相对更贵 |

**实践启示：**

```
GPT 模型的提示方式（精确指令）：
"请分析以下客户反馈，按[积极/消极/中性]分类，
输出 JSON 数组：[{text: string, sentiment: string}]..."

推理模型的提示方式（高层目标）：
"分析这些客户反馈的情感倾向。"
（推理模型自行分解：理解→分类→结构化→输出）
```

> **核心洞察**：如果你在 2026 年还在用面向 GPT-3.5 的"样板式"提示词来调用推理模型，可能得不偿失——过度的约束反而压制的正是推理模型最擅长的地方：自主推理与规划。

---

### 12.2 OpenAI 六步提示工程方法论

**来源：** [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)（2026年7月版）

OpenAI 官方在 2026 年提出了系统化的六步提示工程方法论，将提示词开发提升到软件工程的高度：

| 步骤 | 操作 | 说明 |
|------|------|------|
| **Step 1** | 明确定义目标（Define the goal） | 提取 5 个要点 vs 写一篇 500 字评论 —— 目标差异决定了提示设计 |
| **Step 2** | 选择正确的模型（Choose the right model） | 推理模型 vs GPT 模型决定了后续所有策略 |
| **Step 3** | 构建消息结构（Craft message roles） | System → Developer → User → Assistant 的角色层次 |
| **Step 4** | 设计评分标准（Apply a rubric） | 在 developer message 中定义"什么算好"的明确标准 |
| **Step 5** | 迭代优化（Iterate on the optimal solution） | 用 rubric 评估输出 → 调整提示 → 再次评估 |
| **Step 6** | 添加例示（Add examples） | 展示多样化的输入-输出对，让模型"悟出"模式 |

**关于 System/Developer Message 的最佳实践：**

OpenAI 推荐 System/Developer message 按以下顺序组织：
```
1. 角色定义（Role）—— 你是谁？
2. 业务逻辑与规则（Business logic）—— 必须遵守的约束
3. 任务描述（Task description）—— 具体要做什么
4. 输出格式（Output format）—— 理想输出的样子
5. 评分标准（Rubric）—— 什么算好的输出
```

> **关键更新**：2026 年 OpenAI 不再强调"系统提示词越详细越好"——对推理模型而言，developer message 应该更聚焦于**业务逻辑和约束**，而非微观管理模型的每一步。

---

### 12.3 2026 年提示词工程十大最佳实践总结

综合 OpenAI、Anthropic 和前沿研究在 2026 年的最新指南，以下是当前提示词工程的核心实践：

| # | 实践 | 说明 |
|---|------|------|
| 1 | **区分模型类型** | 推理模型要"高层目标"，GPT 模型要"精确指令" |
| 2 | **结构化消息角色** | System/Developer → User → Assistant 层次分明 |
| 3 | **定义评分标准** | 在提示词中嵌入"什么算好"的评估标准 |
| 4 | **迭代式开发** | 用评估-调试循环替代一次性"写好"提示词 |
| 5 | **使用结构化输出** | JSON Schema 约束确保输出可解析（对 GPT 模型更关键） |
| 6 | **控制上下文长度** | 注意上下文窗口限制，优先展示最相关的信息 |
| 7 | **外部知识优先** | RAG 检索 > 提示词内嵌长文本 > 依赖于模型参数知识 |
| 8 | **测试+版本管理** | 在修改生产提示词前添加 fixture、测试和评估检查 |
| 9 | **避免过度约束推理模型** | 给推理模型留出自主思考空间 |
| 10 | **温度参数随模型调** | 推理模型通常不需要高温度（0.5-0.7 是安全范围） |

> **趋势判断**：提示词工程正在从"秘诀式"（找到最佳的 prompt 措辞）转向"工程式"（建立评估管线 + 版本控制 + 自动化优化）。DSPy、PG 框架等工具的出现标志着这一转变正在加速。

---

---

## 2026 高级提示词技术：五种方法让模型输出可控可验证

> **来源：** [Prompt Engineering in 2026: Advanced Techniques - DEV Community](https://dev.to/lufumeiying/prompt-engineering-in-2026-advanced-techniques-for-better-ai-results-2o52), [Advanced Prompt Techniques: Chain-of-Thought and Beyond - AIUnpacking](https://aiunpacking.com/blog/advanced-prompt-techniques-chain-of-thought/)

### 当基础提示词不够用

直接提示（「总结这段文字」「翻译这句话」）在线性任务中表现良好——一个输入、一条指令、一个输出。当任务含多个决策点时，灾难开始：合规审查需要读合同、标风险条款、建议修订、解释法律推理。挤进一个提示词就是在赌博——模型可能找到条款但跳过推理，或写出看似合理但微妙偏移法律含义的修订。

高级提示技术通过**将难题拆解为更小、可验证的片段**来让你在错误叠加之前就发现它们。

### 2026 年五大核心技巧

#### 1. 思维链（Chain-of-Thought, CoT）

CoT 提示（Wei et al., 2022）的核心发现简明有力：给模型展示中间推理步骤的示例，能显著提升多步任务表现。但 **2026 年出现了重要的新认知**：

- **推理模型不需要 CoT**：GPT-5.x、Claude 4.x Opus（extended thinking 模式）、Gemini 2.5 Pro 已经在背后做了隐藏推理。对它们显式要求「一步步思考」往往**只增加延迟和 token 成本，不提升准确率**。对推理模型，写清晰的 brief 让内部机制自己工作。
- **非推理模型仍需 CoT**：在数学、逻辑、结构化分析上有可测量的增益。关键是让推理轨迹**可审查**，不只是长。一个好的 prompt 应让模型披露假设、证据和风险：「返回 1. 建议 2. 关键假设 3. 使用的证据 4. 风险 5. 什么会改变建议」——五条清晰可验证的条目比一篇漫无边际的独白有价值得多。

#### 2. 自一致性（Self-Consistency）

自一致性（Wang et al., 2023）听起来几乎太简单：**不要只生成一条推理路径然后照单全收，生成多条独立路径，选择最一致出现的答案。** 如果模型用三种不同方式解决同一个问题，都收敛到「问题在认证中间件」，你可以比较有信心。如果三条路径分歧很大——模型在猜，你需要人工介入。

一个实用的内置自一致性 prompt：
```
用三种独立方法解决这个问题。
每种方法：说明方法 → 给出最终答案 → 指出最大不确定性。
然后比较答案，给出最终建议。
```

自一致性**有代价**（更多 token、更高延迟）。保留给高风险场景：金融计算、根因分析、风险评估、文档审查。速度和成本更重要的场景就跳过。

#### 3. 思维树（Tree-of-Thought, ToT）

CoT 从问题到答案走一条单线，ToT（Yao et al., 2023）绘制多条可能路径并在投入前评估。这是「推演一个方案」和「把三个方案并排比较」的区别。

ToT 在战略问题中最强大：产品发布、架构选择、招聘计划、合作谈判——选错路径的真金白银成本高，比较多个替代方案能真正改善决策。

实用 ToT prompt：
```
需要决定如何发布这个产品。探索三条路径：
1. 小范围 beta 测试（50 用户）
2. 通过现有平台合作发布
3. 全面公开发布加营销推动

每条路径评估：收益、风险、所需资源、可逆性、什么证据会支持或否定它。
然后推荐在当前约束下最强的路径。
```

> 最后一条——「什么证据会支持或否定它」——是大多数人忽略的。要求模型指定「什么会改变它的判断」，迫使它暴露自己的假设，使分析对真人决策者更有用。

#### 4. ReAct 提示（推理 + 行动）

ReAct（Yao et al., 2022）将推理与工具使用融合：模型交替在「思考做什么」和「实际去做」之间切换——查询数据库、调用 API、运行搜索。ReAct 循环：思考 → 行动 → 观察 → 更新思考，直到有足够信息回答。这个模式是现代 AI Agent 系统的主干。

#### 5. 结构化提示链（Structured Prompt Chaining）

将复杂工作流分解为多个顺序提示，每个提示的输出成为下一个的输入。适用于代码审查、研究综述、多文档合规检查等场景。每个环节独立可验证。

### 2026 各模型最佳实践

| 模型 | 强项 | 提示策略 |
|------|------|---------|
| **Claude（Anthropic）** | 长上下文 200K tokens、复杂指令遵循 | 用 XML 标签结构化：`<document>`、`<instructions>`、`<request>` |
| **GPT-4/5（OpenAI）** | 创意写作、代码生成 | 用 system message 设定角色，拆分复杂任务 |
| **Gemini（Google）** | 多模态、事实准确 | 利用多模态能力，善用免费 tier |

### 核心原则速查

| # | 原则 | 要点 |
|---|------|------|
| 1 | **具体明确** | 「写一篇 500 字新手友好的神经网络解释，用教孩子认动物的类比，含一个实例」vs「写AI相关」 |
| 2 | **提供上下文** | 「这个 Python 函数验证邮箱但拒绝了含 + 号的合法地址，修它并解释」（附代码 + 使用场景） |
| 3 | **指定格式** | Markdown 表格 / JSON Schema / 约束条件（字数、语气、禁止词汇） |
| 4 | **使用示例** | Few-shot 比 zero-shot 准确率高约 40% |
| 5 | **迭代优化** | 初始 prompt → 审阅输出 → 精炼 → 再审阅，按需重复 |

> **趋势判断**：提示词工程正在从「秘诀式」（找到最佳措辞）转向「工程式」（建立评估管线 + 版本控制 + 自动化优化）。DSPy 等工具标志着这一转变加速。2026 年的一份研究表明：优化过的 prompt 使有用输出率从 40% 提升到 95%，且首次尝试成功率大幅提高——好的 prompt 节省 70% 的 AI 交互时间。

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-24 00:15:31*
