# GPT 系列 - OpenAI

GPT（Generative Pre-trained Transformer）是 OpenAI 的生成模型家族。本页把历史架构、ChatGPT 产品和当前 API 模型分开说明，避免把未公开参数、第三方传闻或随时变化的价格写成稳定事实。

> 时效说明：当前模型与 API 部分按 OpenAI 官方开发者文档于 **2026-07-28** 核对。模型别名、可用区域、价格、上下文限制和功能支持可能变化，生产接入前应再次查看官方模型页并运行自己的评估集。

## 历史演进

| 模型 | 首次发布 | 已公开规模 | 主要意义 |
|------|----------|------------|----------|
| GPT-1 | 2018 | 117M | 展示生成式预训练后进行任务微调的范式 |
| GPT-2 | 2019 | 最大 1.5B | 扩大自回归语言模型并展示零样本迁移能力 |
| GPT-3 | 2020 | 最大 175B | 推动 in-context learning 和 few-shot prompting |
| InstructGPT | 2022 | 论文研究多个 GPT-3 规模 | 使用人类偏好数据改进指令遵循 |
| GPT-3.5 | 2022 起 | 未公开 | 一组经过后训练的模型，而不是已证实为 175B 的单一架构 |
| GPT-4 | 2023 | 未公开 | 官方技术报告确认文本与图像输入能力，但未披露参数量和完整架构 |
| GPT-4o | 2024 | 未公开 | 将文本、视觉与语音交互推进到更统一的多模态路线 |
| o 系列 | 2024 起 | 未公开 | 通过额外推理计算强化数学、代码和复杂规划等任务 |
| GPT-5.x | 2025 起 | 未公开 | 将推理、工具调用、多模态和 Agent 工作流进一步整合 |

GPT-3.5 的参数量、GPT-4 的“1.8T 参数”等说法没有 OpenAI 官方确认，不应放入参数对比表。模型质量也不能从参数量单独推出。

## 当前 GPT-5.6 模型线

根据 [OpenAI 最新模型指南](https://developers.openai.com/api/docs/guides/latest-model)，当前 GPT-5.6 采用三档命名：

| 模型 ID | 定位 | 适合先评估的场景 |
|---------|------|------------------|
| `gpt-5.6-sol` | 旗舰能力 | 高难度编码、研究、复杂工具工作流和质量优先任务 |
| `gpt-5.6-terra` | 能力与成本平衡 | 通用生产工作负载 |
| `gpt-5.6-luna` | 高吞吐 | 分类、抽取、路由和批量处理 |

`gpt-5.6` 是指向 `gpt-5.6-sol` 的别名。别名便于跟随官方默认更新，但模型行为可能随路由更新；需要严格回归和可复现基线的系统，应记录请求日期、响应中的模型信息，并按官方提供的快照策略固定版本（若目标模型提供快照）。

“旗舰、平衡、高吞吐”是产品定位，不是对你任务的质量保证。应在代表性数据上比较任务成功率、延迟、token 使用和总成本。

## ChatGPT、GPT 模型与 API

这三个概念不要混用：

- **GPT 模型**是执行推理的模型家族。
- **OpenAI API**是开发者在程序中调用模型和工具的接口。
- **ChatGPT**是面向用户的产品，包含模型、界面、工具、记忆、文件和订阅权限等产品层能力。

ChatGPT 中显示的功能和额度不等于 API 的模型 ID、计费或数据保留设置。API key 也不自动授予 ChatGPT 订阅权益。

## Responses API

OpenAI 官方将 [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses) 推荐用于新项目；Chat Completions 仍受支持。Responses API 统一了文本/多模态输入、工具调用、多轮状态和推理相关能力。

### Python 最小示例

先在环境变量中设置 `OPENAI_API_KEY`，不要把密钥写进代码或提交到仓库。

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    input="用三句话解释自注意力，并说明一个常见误区。",
)

print(response.output_text)
```

示例使用别名便于入门。生产代码应先确认组织可用模型、版本策略、错误重试、超时、幂等和评估要求。

### 多轮状态

可以通过 `previous_response_id` 延续前一次响应，也可以由应用自行保存和重放必要上下文。服务端状态不会替你解决：

- 敏感数据最小化和保留策略。
- 超长会话的上下文压缩。
- 旧指令与新指令冲突。
- 工具结果是否仍然新鲜。

## 推理设置

GPT-5.6 支持通过 `reasoning.effort` 调整推理预算。当前官方指南列出 `none`、`low`、`medium`、`high`、`xhigh` 和 `max`，但支持范围应以具体模型文档为准。

```python
response = client.responses.create(
    model="gpt-5.6",
    reasoning={"effort": "medium"},
    input="审查这份迁移方案，找出可能导致数据丢失的步骤。",
)
```

更高 effort 通常增加延迟和 token，不保证每个任务都更准确。应在固定评估集上比较相邻档位，并把最低成本的达标设置作为候选。

API 不返回模型的原始隐藏思维链。部分模型可以返回 reasoning summary；摘要是面向用户的输出，不应视为对内部推理过程的完整审计记录。

## 工具调用

工具调用让模型生成结构化的调用意图，由应用验证并执行。可靠闭环应包含：

```text
用户请求
  -> 模型选择工具并生成参数
  -> 应用校验 schema、权限和业务规则
  -> 必要时请求人工确认
  -> 执行工具
  -> 把结果返回模型
  -> 生成最终答复并记录审计日志
```

模型输出符合 JSON Schema 只说明结构通过，不说明参数事实正确、操作被授权或业务状态仍然有效。付款、删除、发送消息和权限变更等动作必须在应用层实施确定性校验。

## 结构化输出

[Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) 可以让支持的模型按 JSON Schema 返回结果，适合抽取、分类和可编程工作流。即使启用严格模式，应用仍要处理：

- 模型拒答。
- 达到输出 token 限制导致响应不完整。
- 网络、超时和服务错误。
- schema 正确但字段值在业务上无效。
- SDK 与模型是否支持所用 schema 特性。

因此不应把“符合结构”写成“结果可靠性 100%”。

## 模型选型

### 先定义评估合同

在比较模型前明确：

- 输入分布和输出格式。
- 可接受的正确率、拒答率和引用要求。
- p95/p99 延迟、吞吐和预算。
- 工具权限与失败恢复。
- 敏感数据、地区和保留约束。

### 分层路由

常见做法是让高吞吐模型处理分类、抽取和简单请求，把少量困难任务路由到更强模型。但路由器本身也会误判，需要把误路由成本、回退和人工接管纳入评估。

不要直接复制“某模型最适合代码/长文档/中文”的榜单结论。公开 benchmark、供应商报告和真实业务分布通常不同，模型更新也会改变结果。

## 成本与性能

总成本不仅是输入/输出 token 单价，还包括：

- 推理 token、工具调用和多轮重试。
- 长上下文中重复发送的固定前缀。
- 缓存写入/读取策略。
- 失败请求、超时和降级模型。
- 评估、监控、人工复核和数据治理。

价格变化快，本页不复制价格表。以 [OpenAI API 定价文档](https://developers.openai.com/api/docs/pricing) 为准，并用真实请求日志估算。

## 安全与隐私

- 对用户输入、检索文档和工具输出按不可信内容处理，防范提示词注入。
- 工具使用最小权限凭证，并在应用层做 allowlist 和参数校验。
- 发送稳定、隐私保护的 `safety_identifier`（适用时遵循官方安全指南）。
- 不在提示词、日志或代码中保存 API key。
- 对个人信息、医疗、金融和内部数据确认组织的数据使用与保留设置。
- 高风险结论要求来源、人工复核和明确的非自动执行边界。

## 常见误区

- **GPT-3.5 就是 175B**：官方未确认 GPT-3.5 系列的参数量。
- **GPT-4 的参数量可以从传闻写入表格**：官方技术报告明确未披露架构和规模细节。
- **最新旗舰一定最划算**：高吞吐或平衡型号可能在达标前提下更合适。
- **Responses API 取代后 Chat Completions 已停用**：官方说明 Chat Completions 仍受支持，只是新项目推荐 Responses。
- **reasoning effort 越高越好**：需要对质量、延迟和成本共同评估。
- **结构化输出保证业务正确**：schema 不能验证现实世界事实和权限。
- **工具调用等于模型已经执行动作**：模型提出调用，真正执行和授权由应用负责。
- **模型别名永远固定**：别名可能更新路由，生产系统应有版本与回归策略。

## 参考资料

- [OpenAI 最新模型指南](https://developers.openai.com/api/docs/guides/latest-model)
- [迁移到 Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)
- [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)
- [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)

## 延伸阅读

- [大语言模型基础](/初级知识/大语言模型基础/)
- [提示词工程](/进阶学习/提示词工程/)
- [函数调用 Agent](/AIAgent实践/函数调用Agent/)
- [模型评估与基准](/进阶学习/模型评估与基准/)

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-26 09:04:58*
