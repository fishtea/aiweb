# GPT 系列 — OpenAI

> GPT（Generative Pre-trained Transformer）系列是 OpenAI 开发的旗舰大语言模型家族，从 2018 年的 GPT-1 发展到 2025 年的 GPT-4o / GPT-4.5，彻底改变了自然语言处理格局。

---

## 架构演进

| 模型 | 发布时间 | 参数规模 | 架构特点 |
|------|---------|---------|---------|
| GPT-1 | 2018.06 | 117M | 首个 Decoder-only Transformer，开创生成式预训练范式 |
| GPT-2 | 2019.02 | 1.5B | 扩大模型规模，展示零样本迁移能力 |
| GPT-3 | 2020.06 | 175B | 大规模 In-context Learning，涌现 Few-shot 能力 |
| GPT-3.5 | 2022.03 | 175B | InstructGPT 的 RLHF 微调版本，ChatGPT 的基础 |
| GPT-4 | 2023.03 | 未公开 (~1.8T) | 多模态（图像+文本），推理能力大幅飞跃 |
| GPT-4o | 2024.05 | 未公开 | 原生多模态，实时语音交互，速度提升 |
| GPT-4.5 | 2025.02 | 未公开 | 更强的世界知识和情感智能 |

> **核心架构:** 所有 GPT 模型均基于 Decoder-only Transformer。GPT-4 增加了多模态视觉输入能力，GPT-4o 实现了原生多模态（语音+文本+图像）端到端处理。

---

## GPT-4 关键特性

根据 OpenAI 官方报告 [GPT-4 Technical Report (arXiv:2303.08774)](https://arxiv.org/abs/2303.08774)：

- **多模态输入:** 接受文本和图像输入，生成文本输出
- **超长上下文:** 支持 25,000+ 单词（约 32K tokens），GPT-4-32K 模型支持 32K tokens
- **推理飞跃:** 律师考试从 GPT-3.5 的 10% 分位提升到 90% 分位
- **安全对齐:** 经过 6 个月的安全训练，拒绝不当请求率提升 82%

### 基准测试表现

| 测试 | GPT-3.5 | GPT-4 |
|------|---------|-------|
| Uniform Bar Exam | 10% 分位 | 90% 分位 |
| Biology Olympiad | 31% 分位 | 99% 分位 |
| MMLU | 70.0% | 86.4% |

---

## GPT-4o 与 GPT-4.5

- **GPT-4o**（2024.05）："o" 代表 "omni"，原生支持语音、文本、图像多模态。响应延迟降低到 200ms 级别。在哥斯达黎加等低成本区域提供免费访问。
- **GPT-4.5**（2025.02）：扩展了世界知识储备，改善了情感理解和创造力。OpenAI 称之为"迄今为止最有知识、最自然的对话模型"。

---

## 如何使用

### 通过 ChatGPT（网页/App）

- ChatGPT Plus（$20/月）可访问 GPT-4、GPT-4o
- Team/Enterprise 有更高配额和隐私保护

### 通过 API

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "解释一下 GPT 的架构特点。"}
    ]
)

print(completion.choices[0].message.content)
```

---

## 优势与局限

**优势:**
- 广泛的世界知识覆盖
- 强大的多步推理能力
- 成熟的安全对齐机制
- 丰富的生态和 API 工具

**局限:**
- 闭源，不可自部署
- 可能产生幻觉
- API 成本相对较高
- 缺乏透明度（架构细节未公开）

---

**参考资料：**
- [OpenAI GPT-4 官方页面](https://openai.com/index/gpt-4)
- [GPT-4 Technical Report (arXiv:2303.08774)](https://arxiv.org/abs/2303.08774)
- [Evolution of GPT Models (Medium)](https://medium.com/@vipul.koti333/evolution-of-gpt-models-gpt-1-to-gpt-4-0238ee07a29b)
- [GPT-4 Peer Review (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795998)

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:11:39*
*资源区块更新时间：2026-06-30 11:11:09*
*资源区块更新时间：2026-06-30 10:42:21*
*资源区块更新时间：2026-06-30 10:25:06*
