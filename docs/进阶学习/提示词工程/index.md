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

## 🔗 参考资料

- [Prompt Engineering Guide - DAIR.AI](https://www.promptingguide.ai)
- [Ultimate Guide to Prompt Engineering 2026 - Lakera AI](https://www.lakera.ai/blog/prompt-engineering-guide)
- [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
- [Prompt Engineering Techniques - K2View](https://www.k2view.com/blog/prompt-engineering-techniques)
- [Advanced 2026 Guide to Prompt Engineering - YouTube](https://www.youtube.com/watch?v=qBlX6FhDm2E)

---

## 5. 2026 年最新进展

### 5.1 提示词工程的进化：从灵感到结构

2026 年，Prompt 工程没有消失，而是完成了一次关键进化——从"灵感型提示词"进化为**结构化提示词**。主流实践框架为 **PTCF 四支柱**：

| 支柱 | 说明 |
|------|------|
| **Persona（角色）** | 先定义 AI 扮演谁（资深开发者、安全审计师、数学导师） |
| **Task（任务）** | 明确要 AI 完成什么 |
| **Context（背景）** | 提供必要上下文信息 |
| **Format（格式）** | 指定输出格式（JSON、Markdown、YAML） |

### 5.2 2026 年六大核心技术

| 技术 | 核心思想 | 最佳实践 |
|------|---------|---------|
| **Zero-Shot** | 不提供示例，直接执行 | 清晰简洁的指令 |
| **Few-Shot** | 提供 3-8 个示例引导输出 | 保持格式一致性 |
| **Chain-of-Thought (CoT)** | 分解为逐步推理 | 结构化框架替代简单的"一步步思考" |
| **Meta Prompting** | 定义抽象逻辑结构而非具体示例 | 注重 Token 效率 |
| **Self-Consistency** | 生成多条推理路径，选一致性最高的 | 适合数学/逻辑问题 |
| **Role Prompting** | 赋予角色塑造推理方式 | 角色要真实且任务相关 |

### 5.3 增强型思考链（Advanced CoT 模板）

推荐的结构化推理框架：

```
1. 需求拆解：列出所有明确要求 + 隐含约束 + 边界条件
2. 方案设计：提出 3 种不同实现思路
3. 方案选型：对比性能、可维护性、安全性
4. 代码实现：编写完整可运行代码
5. 验证与优化：编写测试用例，指出潜在问题
```

**模型专属优化**：千问Cyber → `preserve_thinking: true`；GPT-6 → `think_budget: 1000`；字节TRAE → "用中文思考，用英文写注释"。

### 5.4 负面提示词（Negative Prompting）

2026 年的重要发现：**告诉 AI "不要做什么"比"要做什么"更有效**。示例：

```
- 不要使用全局变量
- 不要省略错误处理
- 不要引入新的第三方依赖
- 不要硬编码任何配置值
```

要求应具体可执行，避免模糊指令。

### 5.5 跨模型适配指南

| 模型 | 最强领域 | 提示词优化要点 |
|------|---------|---------------|
| GPT-6 | 复杂系统设计、多 Agent 协同 | 强调架构，分配更多思考 Token |
| 千问Cyber | 智能体编程、前端开发 | 开启 `preserve_thinking` |
| 字节TRAE | 中文理解、设计稿转代码 | 用中文写详细需求 |
| Claude Opus 4.6 | 长文档处理、安全审计 | 提供完整代码库上下文 |

核心建议：**为项目选择最匹配的模型**。

### 5.6 多 Agent 协同提示

2026 年最有价值的模式：同时启动多个角色 Agent 协作完成复杂任务。比如把"架构师"+"开发者"+"测试工程师"三个 Agent 串联起来——前者输出设计文档，后者基于设计写代码，最后进行测试验证。

### 5.7 上下文工程（Context Engineering）

2026 年提示词工程的前沿——不仅要设计问什么，还要设计模型如何理解上下文。通过 RAG、摘要、结构化输入等技术引导模型更准确地输出，LLM-as-a-Judge 等自我评估模式也正在兴起。

> 来源参考：[IBM 2026 Prompt Engineering Guide](https://www.ibm.com/cn-zh/think/prompt-engineering)、[2026后端开发者提示词实战](https://www.cnblogs.com/ljbguanli/p/20130505)、[K2View Top 6 Techniques 2026](https://www.k2view.com/blog/prompt-engineering-techniques)、[结构化提示词进化 - 知乎](https://zhuanlan.zhihu.com/p/2002315607635412900)
