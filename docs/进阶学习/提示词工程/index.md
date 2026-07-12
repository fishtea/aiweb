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
- [Prompt Engineering Techniques - OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/articles/techniques_to_improve_reliability.md)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-12 05:04:02*
