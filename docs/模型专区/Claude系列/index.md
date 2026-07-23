# Claude 系列 — Anthropic

> Claude 是由 Anthropic 开发的大语言模型家族，以 Constitutional AI、安全性、长上下文和编程体验著称。按 Anthropic 2026-07-06 官方模型文档，生产选型应重点关注 Claude Fable 5、Claude Sonnet 5、Claude Opus 4.8、Claude Haiku 4.5 与 Claude 3.7 Sonnet。

---

## 模型演进

| 模型 | 发布时间 | 上下文窗口 | 特点 |
|------|---------|-----------|------|
| Claude 1 | 2023.03 | 9K | 首个版本，以安全性和诚实性为特色 |
| Claude 2 | 2023.07 | 100K | 扩展上下文窗口，提升推理能力 |
| Claude 3 系列 | 2024.03 | 200K | Opus/Sonnet/Haiku 三级分层，多模态 |
| Claude 3.5 Sonnet | 2024.06 | 200K | 编程能力大幅提升，Agent 能力 |
| Claude 3.7 Sonnet | 2025.02 | 200K | 混合推理模型，可在快速回答和延长思考之间切换 |
| Claude 4 系列 | 2025.05 | 200K | Sonnet 4 与 Opus 4，面向编程、Agent 和长任务 |
| Claude Haiku 4.5 | 2026 | 200K | 低延迟高吞吐，适合分类、抽取和路由 |
| Claude Opus 4.8 | 2026 | 200K | 旗舰高能力模型，适合最高难度推理、审查和长任务 |
| Claude Sonnet 5 | 2026 | 1M | 最新平衡模型，适合编码、Agent、长上下文和知识工作 |
| Claude Fable 5 | 2026 | 1M | 最新高能力模型，面向复杂 Agent、推理和创造性任务 |

---

## 架构特点

根据 Anthropic 官方模型文档与 Claude 3 / 4 发布资料：

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

## 2026 最新模型线

根据 Anthropic 官方发布与模型文档：

- **Claude Fable 5**：Anthropic 官方模型文档列出的 2026 最新高能力模型，适合复杂 Agent、深度推理、创作和高价值分析。
- **Claude Sonnet 5**：2026 默认生产候选，平衡质量、速度与成本，适合作为工程团队的默认编码和知识工作模型。
- **Claude Opus 4.8**：旗舰高能力模型，适合复杂代码库修改、长时间 Agent、法律/安全审查和高价值分析。
- **Claude Haiku 4.5**：低延迟高吞吐模型，适合分类、抽取、路由、快速摘要、批处理和前置过滤。
- **Claude 3.7 Sonnet**：引入混合推理能力，适合需要可控思考预算的复杂任务。
- **Claude 3.5 / 3.7 系列**：仍适合已有系统的稳定基线，但新系统应优先评估 Claude 4.7 / 4.8。

### Claude 的差异化能力

- **超长上下文处理**：200K 窗口配合"上下文记忆"优化，可在长文档中保持高召回，适合代码库分析、法律合同审查。
- **Agentic Coding**：Claude Code（CLI）和 Agent SDK 让 Claude 能自主读写文件、运行命令、执行多步工程任务，SWE-Bench 表现长期领先。
- **MCP（Model Context Protocol）**：Anthropic 主导的开放协议，让模型标准化接入外部工具和数据源，已成为 Agent 生态基础设施（见 [实际应用案例](/AIAgent实践/实际应用案例/)）。
- **宪法 AI 与安全**：通过 Constitutional AI 训练，在拒绝率和无害性上长期领先，适合对安全敏感的企业场景。

> 生产建议：Claude 的优势集中在长上下文阅读、代码修改、工具调用和安全拒答策略。对高并发低成本任务，通常用 Haiku / Sonnet 做主力，把 Opus 留给少量高难度步骤。

---

## 2026 年 6 月：Claude Fable 5 与模型格局重塑

根据 [Anthropic 官方模型文档](https://docs.anthropic.com/en/docs/about-claude/models)（2026-07 访问）及 [Claude Fable 5 发布公告](https://www.anthropic.com/news/claude-fable-5)：

### Claude Fable 5 — 新一代旗舰

2026 年 6 月 9 日，Anthropic 正式发布 **Claude Fable 5**（`claude-fable-5`），这是 Anthropic 迄今为止最强大的广泛发布模型。Fable 5 专为长运行 Agent 场景设计，号称"面向长期 Agent 的下一代智能"：

| 维度 | 详情 |
|------|------|
| 上下文窗口 | **1M tokens** |
| 最大输出 | 128K tokens |
| 定价 | $10/百万输入 tokens，$50/百万输出 tokens |
| 知识截止 | 2026 年 1 月 |
| 自适应思考 | 始终开启（Always On） |
| 延迟 | 较慢（旗舰级） |
| 可用平台 | Claude API、AWS Bedrock、Google Cloud、Microsoft Foundry |

Fable 5 的使用场景定位包括：复杂多步 Agent、深度推理、创造性写作和高价值分析。

### Claude Mythos 5 — Project Glasswing 专属

同期发布的 **Claude Mythos 5**（`claude-mythos-5`）规格与 Fable 5 相同，但仅供 Project Glasswing 计划中的受邀客户使用，专注于防御性网络安全工作流。该模型**不在公开 API 中提供**。

### 当前模型选型矩阵

| 模型 | API ID | 定位 | 上下文 | 定价（每百万 token） | 延迟 | 自适应思考 |
|------|--------|------|--------|-------------------|------|-----------|
| **Claude Fable 5** | `claude-fable-5` | 下一代 Agent 智能 | 1M | $10 输入 / $50 输出 | 较慢 | 是（始终开启） |
| **Claude Opus 4.8** | `claude-opus-4-8` | 复杂编码与企业工作 | 1M | $5 输入 / $25 输出 | 中等 | 是 |
| **Claude Sonnet 5** | `claude-sonnet-5` | 速度与智能最佳平衡 | 1M | $3 输入 / $15 输出 | 快速 | 是 |
| **Claude Haiku 4.5** | `claude-haiku-4-5-20251001` | 最快近前沿模型 | 200K | $1 输入 / $5 输出 | 最快 | 否 |

> 注意：Sonnet 5 的价格至 2026 年 8 月 31 日有优惠价 $2/$10 每百万 token。

## Claude Sonnet 5 深度解析（2026 年 6 月发布）

根据 [Anthropic 官方发布公告](https://www.anthropic.com/news/claude-sonnet-5)（2026 年 6 月 30 日）和 [MarkTechPost 基准对比](https://www.marktechpost.com/2026/07/13/anthropic-claude-sonnet-5-vs-sonnet-4-6-vs-opus-4-8-agentic-coding-benchmarks-api-pricing-and-cost-performance-tradeoffs-compared/)（2026 年 7 月 13 日）：

### 核心定位

Claude Sonnet 5 被 Anthropic 称为「有史以来最具 Agent 能力的 Sonnet 模型」。它能够制定计划、使用浏览器和终端等工具，并以接近 Opus 4.8 的水平自主运行——而仅在几个月前，这些能力还需要更大、更昂贵的 Opus 级模型。

### 关键基准测试

| 基准 | Sonnet 4.6 | Sonnet 5 | Opus 4.8 | 解读 |
|------|-----------|----------|----------|------|
| SWE-bench Pro（编码） | 未公布 | **63.2%** | — | 自主修复真实 GitHub Issue |
| OSWorld-Verified（计算机使用） | — | **81.2%** | — | 真实操作系统任务完成 |
| HLE（知识工作） | — | **57.4%** | — | Humanity's Last Exam 难度 |
| GDPval-AA v2（知识工作） | — | **1,618** | 1,615 | 略超 Opus 4.8 |
| Terminal-Bench 2.1 | — | 显著提升 | — | 终端操作能力 |

### 成本与性能权衡

Sonnet 5 引入了 **effort level（努力级别）** 机制：low / medium / high / xhigh，通过控制推理 token 消耗来平衡质量和成本：

| 努力级别 | 适用场景 | 成本特征 |
|---------|---------|---------|
| Low | 简单问答、分类、抽取 | 最省 token |
| Medium | 常规编码、知识工作 | 推荐默认级别 |
| High | 复杂多步推理、长 Agent 任务 | token 消耗增加 |
| XHigh | 极难任务，接近 Opus 4.8 水平 | 成本可能超过 Opus 4.8 |

**定价**（2026 年 8 月 31 日前优惠价）：
- 输入：$2/百万 tokens（标准价 $3）
- 输出：$10/百万 tokens（标准价 $15）
- 对比 Opus 4.8：$5 输入 / $25 输出

### Tokenizer 变更

Sonnet 5 使用了与 Opus 4.7 相同的新版 tokenizer。相同文本映射的 token 数量大约是旧版的 **1.0~1.35 倍**，实际成本估算时需考虑这一因素。

### 安全性

Anthropic 的安全评估显示 Sonnet 5 整体不良行为率低于 Sonnet 4.6，且在 Agent 场景下更安全。网络安全能力远低于 Opus 级模型——如果你需要最高准确度的安全关键任务，Opus 仍是首选。

### 生产选型建议

| 场景 | 推荐 | 原因 |
|------|------|------|
| 日常编码 + 知识工作 | **Sonnet 5**（medium effort） | 性价比最优 |
| 复杂 Agent（浏览器/终端操作） | **Sonnet 5**（high effort） | 接近 Opus 4.8 水平 |
| 最高准确度 + 安全审查 | **Opus 4.8** | 旗舰能力 + 更低风险 |
| 高吞吐分类/抽取/路由 | **Haiku 4.5** | 最低延迟 + 最低成本 |
| 极致 Agent 推理 | **Fable 5** | 1M 上下文 + 始终开启思考 |

> **一句话总结**：Sonnet 5 把 Opus 级的 Agent 能力带到了 Sonnet 价位。对大多数工程团队来说，这是 2026 年下半年最值得评估的模型。

### Claude Code 与 The Making of Claude Code

根据 [Anthropic 官方文章](https://www.anthropic.com/features/making-of-claude-code)，Claude Code（CLI 编程 Agent）是 Anthropic 在 Agentic Coding 领域的重要实践。核心设计理念：

- **自主编辑与执行**：Claude Code 可以直接读写文件、运行命令，在多步工程任务中自主决策。
- **SWE-Bench 长期领先**：从 Claude 3.5 Sonnet 开始，Anthropic 的模型在 SWE-Bench 基准测试中持续保持顶尖表现。
- **MCP 生态赋能**：Model Context Protocol（MCP）作为开放的 Agent 工具协议，已在 Claude Code、IDE 插件和自定义 Agent 中广泛集成。

**生产建议**：如果团队需要实现代码库级别的 Agent（如自动 PR 审查、代码重构、Bug 修复），Claude Code + Claude Sonnet 5 是 2026 年推荐的组合方案。

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
    model="claude-sonnet-5-20260611",
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

---

## 2026 年 7 月最新进展

### Claude Sonnet 5 — 迄今最具 Agent 能力的 Sonnet（2026 年 6 月 30 日）

Anthropic 于 **2026 年 6 月 30 日** 发布 Claude Sonnet 5，定位为"最具 Agent 能力的 Sonnet 模型"。它可以自主制定计划、使用浏览器和终端等工具，并在无需人类介入的情况下长时间运行。

**关键提升：**
- **Agent 能力飞跃：** 接近 Opus 4.8 的 Agent 推理水平，但价格大幅降低
- **编码：** 在 SWE-bench 等 Agent 编码评测上显著超越 Sonnet 4.6
- **工具使用：** 原生支持函数调用、结构化输出和长时间 Agent 编排
- **Computer Use：** 增强的桌面/浏览器操控能力
- **安全性：** 不良行为率低于 Sonnet 4.6，Agent 场景更安全

**定价（2026 年 7-8 月推广价）：** $2/M 输入 token，$10/M 输出 token
**正式定价（2026 年 9 月起）：** $3/M 输入 token，$15/M 输出 token

Sonnet 5 提供广泛的性价比选择范围——在中等推理预算下可以匹配 Opus 4.8 的部分任务表现，在高推理预算下进一步缩小差距。

### Claude Fable 5 — Mythos 级旗舰（2026 年 6 月 9 日）

Claude **Fable 5** 是 Anthropic 首个公开的 Mythos 级模型，代表第五代智能，面向最复杂的编码和知识工作。

**核心能力：**
- **长时间自主 Agent：** 可在 Claude Code 或 Managed Agents 中连续工作数天，规划多阶段任务、委派子 Agent、自我检查
- **编码：** 能够处理大型迁移、复杂实现和多日自主编码会话，自动编写测试验证自己的工作
- **视觉理解：** 理解嵌套在文档和 PDF 中的图表、表格，辅助评估编码输出
- **企业工作流：** 处理多阶段知识工作，从深度研究到交付物

**可用时间线：**
- 6 月 9 日：发布上线
- 6 月 12 日：因需求过大暂停访问
- 7 月 1 日：恢复访问，正式面向 Pro/Max/Team/Enterprise 用户

**定价：** $10/M 输入 token，$50/M 输出 token（支持提示缓存 90% 输入折扣）

### Claude Opus 4.8 — 当前旗舰

截至 2026 年 7 月，Claude Opus 4.8 仍是 Anthropic 最高能力模型，适合最高难度推理、长任务审查和高风险决策。

### Claude 2026 全线产品

| 模型 | 定位 | 定价（输入/输出 per M tokens） |
|------|------|-------------------------------|
| Claude Fable 5 | Mythos 级旗舰，长时间 Agent | $10 / $50 |
| Claude Opus 4.8 | 高能力推理与审查 | — |
| Claude Sonnet 5 | Agent 性价比首选 | $3 / $15（正式） |
| Claude Haiku 4.5 | 低延迟高吞吐 | — |

### Claude Skills 新特性

2026 年 Anthropic 推出了 **Claude Skills** 功能，允许用户创建可复用的定制化能力模块，让 Claude 在特定领域（如代码审查、数据分析、内容创作）表现出更一致的专业水平。

**资料来源：**
- [Introducing Claude Sonnet 5 (Anthropic Official)](https://www.anthropic.com/news/claude-sonnet-5)
- [Claude Fable 5 (Anthropic Official)](https://www.anthropic.com/claude/fable)
- [Latest Claude Updates 2026: Fable 5 Shutdown, Opus 4.8, Skills](https://appscribed.com/claude-updates-list/)
- [Claude Fable 5 vs Sonnet 5: Full Benchmark Comparison (July 2026)](https://codingfleet.com/blog/claude-fable-5-vs-claude-sonnet-5/)

---

**参考资料：**
- [Anthropic Claude 3.5 Sonnet 发布公告](https://www.anthropic.com/news/claude-3-5-sonnet)
- [Anthropic Claude 4 发布公告](https://www.anthropic.com/news/claude-4)
- [Anthropic Claude 3.7 Sonnet 发布公告](https://www.anthropic.com/news/claude-3-7-sonnet)
- [Anthropic Models 文档](https://docs.anthropic.com/en/docs/about-claude/models)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-24 00:15:31*
