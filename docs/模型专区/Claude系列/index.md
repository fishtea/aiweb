# Claude 系列 — Anthropic

> Claude 是由 Anthropic 开发的大语言模型家族，以"Constitutional AI"安全训练方法著称。从 Claude 1 发展到 2025 年的 Claude Sonnet 4.5 / Opus 4.8，Claude 系列在编程、推理和安全性方面建立了领先地位。

---

## 模型演进

| 模型 | 发布时间 | 上下文窗口 | 特点 |
|------|---------|-----------|------|
| Claude 1 | 2023.03 | 9K | 首个版本，以安全性和诚实性为特色 |
| Claude 2 | 2023.07 | 100K | 扩展上下文窗口，提升推理能力 |
| Claude 3 系列 | 2024.03 | 200K | Opus/Sonnet/Haiku 三级分层，多模态 |
| Claude 3.5 Sonnet | 2024.06 | 200K | 编程能力大幅提升，Agent 能力 |
| Claude 4 系列 | 2025.05 | 200K | Sonnet 4 + Opus 4，混合推理 |
| Sonnet 4.5 | 2025.09 | 200K (1M Beta) | 最佳编程模型，Agent 编排 |
| Opus 4.8 | 2026.05 | 200K | 可靠旗舰，浏览器 Agent SOTA |

---

## 架构特点

根据 [Anthropic Claude 模型指南](https://www.codegpt.co/blog/anthropic-claude-models-complete-guide)：

- **Transformer 架构:** 基于 decoder-only transformer，持续优化
- **Constitutional AI:** 通过宪法 AI 方法训练，使模型行为符合人类价值观
- **多模态:** 从 Claude 3 开始支持图像输入理解
- **分层定位:**
  - **Opus** — 旗舰级，最强推理和创造性
  - **Sonnet** — 平衡型，最佳性价比，适合日常使用
  - **Haiku** — 轻量级，最快响应，成本最低

---

## Claude 3.5 Sonnet — 里程碑版本

根据 [Anthropic 官方发布](https://www.anthropic.com/news/claude-3-5-sonnet)：

- 在内部 Agent 编码评测中解决了 **64%** 的问题（Claude 3 Opus 为 38%）
- 可独立编写、编辑和执行代码，具备复杂推理和故障排除能力
- 在视觉推理任务上也显著优于 Claude 3 Opus

---

## 2025 年最新模型

根据 [CodeGPT Claude 完整指南](https://www.codegpt.co/blog/anthropic-claude-models-complete-guide)：

- **Sonnet 4.5**（2025.09）：被标记为"世界上最好的编码模型"和"最好的 Agent 模型"。在 OSWorld 上达 61.4%，SWE-Bench 达 69.8%。
- **Haiku 4.5**（2025.10）：达到 Sonnet 4.5 90% 的性能，但成本仅为 1/5。
- **Opus 4.1**（2025.08）：安全网模型，慢但可靠，能捕捉其他模型遗漏的关键错误。

### Claude 的差异化能力

- **超长上下文处理**：200K 窗口配合"上下文记忆"优化，可在长文档中保持高召回，适合代码库分析、法律合同审查。
- **Agentic Coding**：Claude Code（CLI）和 Agent SDK 让 Claude 能自主读写文件、运行命令、执行多步工程任务，SWE-Bench 表现长期领先。
- **MCP（Model Context Protocol）**：Anthropic 主导的开放协议，让模型标准化接入外部工具和数据源，已成为 Agent 生态基础设施（见 [实际应用案例](/AIAgent实践/实际应用案例/)）。
- **宪法 AI 与安全**：通过 Constitutional AI 训练，在拒绝率和无害性上长期领先，适合对安全敏感的企业场景。

> 2025 年底 OpenAI 与 Anthropic 联合创立 Agentic AI Foundation（归属 Linux 基金会），将 MCP、AGENTS.md 等协议标准化，推动 Agent 互操作。

---

## 如何使用

### 通过 Claude.ai（网页/App）

- Claude Pro（$20/月）可访问所有模型
- Claude Team/Enterprise 提供更多功能

### 通过 API

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-sonnet-4-20250501",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "请介绍 Claude 系列模型的架构特点。"}
    ]
)

print(message.content[0].text)
```

---

## 优势与局限

**优势:**
- 行业领先的安全性（Constitutional AI）
- 超长上下文窗口（200K，可达 1M）
- 顶级编程能力（SWE-Bench 领先）
- 出色的 Agent 编排能力
- Claude Code 工具提供强大的开发体验

**局限:**
- 闭源模型，不可自部署
- 知识截止日期不如某些竞品新
- 创意写作方面可能不如 GPT-4
- Opus 级模型推理成本较高

---

**参考资料：**
- [Anthropic Claude 3.5 Sonnet 发布公告](https://www.anthropic.com/news/claude-3-5-sonnet)
- [Anthropic Claude Models Complete Guide (CodeGPT)](https://www.codegpt.co/blog/anthropic-claude-models-complete-guide)
- [Every Claude Model Guide (Claude.fa.st)](https://claudefa.st/blog/models)
- [Claude Models Comparison (Gradually AI)](https://www.gradually.ai/en/claude-models)
- [Claude 3 Opus/Sonnet/Haiku 探索 (Medium)](https://damiandabrowski.medium.com/exploring-the-claude-3-opus-sonnet-and-haiku-models-adbf9c74acaa)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

- **[Anthropic Academy：Claude API 开发指南](https://anthropic.com/learn/build-with-claude)**
  - 来源：`anthropic.com` · 质量分：14 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - 开始构建开发人员文档。 * 查看我们的模型比较表。 * 参见 Claude 4 的定价。 * 通过提示缓存优化 API 使用。 * 使用 Amazon Bedrock API 在 Amazon 上构建。 * 使用 Vertex AI API 在 Google 上构建。 * 使用文件 API 上传和管理文件。 * 将 MCP 与 Claude Code 结合使用。 * 安装克劳德代码。 * 探索 Anthropic 的 Claude Co...

- **[Claude Code 教程 2026：完整的初学者指南（安装、命令、计划模式）| NX代码](https://nxcode.io/resources/news/claude-code-tutorial-beginners-guide-2026)**
  - 来源：`nxcode.io` · 质量分：10 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - Claude Code 教程 2026：完整的初学者指南（安装、命令、计划模式）。 * **终端原生，而不是聊天机器人**：Claude Code 直接在本地文件上运行，索引整个项目结构，并通过权限系统进行操作，您可以在其中批准每个文件更改和命令执行。 * **复杂任务的计划模式**：告诉 Claude 在进行更改之前计划其方法 - 它分析问题，概述步骤，显示推理，并在执行之前等待您的批准。 * **Sonnet 占 80%，Opus ...

- **[使用 Claude API 进行构建 - Anthropic Skilljar](https://anthropic.skilljar.com/claude-with-the-anthropic-api)**
  - 来源：`anthropic.skilljar.com` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # 使用 Claude API 进行构建。 ## 这门综合课程涵盖了使用 Claude API 处理人类模型的全部内容。这个综合视频课程教授开发人员如何使用 Anthropic API 将 Claude AI 集成到应用程序中。您正在登录以访问人择课程材料。这个独立的平台使我们能够提供交互式学习体验，跟踪您的进度，并确保您能够以有组织的方式访问所有课程资源。这些数据有助于我们了解您在课程中的进展情况，并允许我们为您提供结业证书。所有数据...

- **[Claude API：如何获取密钥并使用 API - Zapier](https://zapier.com/blog/claude-api)**
  - 来源：`zapier.com` · 质量分：7 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # Claude API：如何获取密钥并使用 API。带有《克劳德》制作者 Anthropic 标志的英雄形象。以下是如何获取 Claude API 密钥的简短版本。 1. 创建一个 Anthropic 开发者帐户并添加至少 5 美元的积分。 2. 打开您的帐户设置，单击“**API 密钥**”，然后单击“**创建密钥**”。 3. 为您的密钥命名并单击“**添加**”。如果你的人工智能应用程序正在做这些，你不需要更好的提示：你需要克劳...

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-02 11:56:59*
