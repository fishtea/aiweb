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

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:37:40*
