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

*资源区块更新时间：2026-07-09 00:14:29*
