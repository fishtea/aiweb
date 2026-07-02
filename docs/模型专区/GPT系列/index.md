# GPT 系列 — OpenAI

> GPT（Generative Pre-trained Transformer）系列是 OpenAI 开发的旗舰大语言模型家族，从 2018 年的 GPT-1 发展到 2025 年的 GPT-4o / GPT-4.5 与 o 系列推理模型，彻底改变了自然语言处理格局。

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
| o1 (preview) | 2024.09 | 未公开 | 首个推理模型，通过 RL 学会\"思考\"再回答 |
| o1 正式版 | 2024.12 | 未公开 | 推理能力大幅提升，竞赛级数学/编程 |
| o3-mini | 2025.01 | 未公开 | 低成本推理模型，支持函数调用 |
| GPT-4.5 | 2025.02 | 未公开 | 更强的世界知识和情感智能 |
| o3 / o4-mini | 2025.04 | 未公开 | 推理 + 工具调用 + 多模态，o4-mini 性价比极高 |
| GPT-5 | 2025.08 | 未公开 | 统一推理与对话，自动决定思考深度 |
| GPT-5.1 | 2026.04 | 未公开 | 编码与 Agent 能力增强，更长持续操作 |

> **核心架构:** 所有 GPT 模型均基于 Decoder-only Transformer。GPT-4 增加了多模态视觉输入能力，GPT-4o 实现了原生多模态（语音+文本+图像）端到端处理。o 系列在基座模型上叠加了大规模强化学习训练的"内部思维链"，回答前先生成隐藏的推理过程。GPT-5 进一步统一了"快思考"与"慢思考"——模型自主判断问题难度，简单问题快速直答，复杂问题自动展开推理。

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

## o 系列 — 推理模型（Reasoning Models）

o 系列是 OpenAI 在 2024-2025 年推出的**推理增强模型线**，与传统 GPT 模型形成互补。其核心区别在于：模型在输出最终答案前，会先在隐藏的"思维链"（chain-of-thought）中进行多步推理，再给出结论。

### 为什么需要推理模型

| 任务类型 | 传统 GPT-4o | o 系列模型 |
|---------|------------|-----------|
| 日常对话、写作、翻译 | ✅ 更快、更自然 | ⚠️ 思考时间长，略显刻板 |
| 竞赛数学（AIME） | 部分正确 | ✅ 接近满分 |
| 复杂编程（Codeforces） | 中等水平 | ✅ 竞赛级表现 |
| 多步逻辑推理 | 容易出错 | ✅ 显著更强 |
| 科学研究问题（GPQA） | 中等 | ✅ 博士级表现 |

### o 系列演进

| 模型 | 发布 | 关键特性 |
|------|------|---------|
| **o1-preview / o1-mini** | 2024.09 | 首次引入隐藏思维链，擅长编程和数学 |
| **o1 正式版** | 2024.12 | AIME 2024 准确率 83.3%（preview 仅 13.4%），达到竞赛选手水平 |
| **o3-mini** | 2025.01 | 低成本推理模型，首次在推理模型中支持函数调用和结构化输出 |
| **o3 / o4-mini** | 2025.04 | 支持多模态输入和工具调用；o4-mini 以极低成本达到 o1 级推理能力 |

> **生产建议：** o 系列模型适合需要深度推理、代码生成或复杂规划的场景；对延迟敏感、以对话为主的任务，GPT-4o 仍是更经济的选择。从 o3-mini 起已支持函数调用，可与 Agent 框架结合使用。

### 使用方式

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# 推理模型用法与普通模型一致，但会增加 reasoning_effort 参数
completion = client.chat.completions.create(
    model="o4-mini",
    reasoning_effort="medium",  # low / medium / high，控制思考深度
    messages=[
        {"role": "user", "content": "证明根号 2 是无理数。"}
    ]
)

print(completion.choices[0].message.content)
```

> 推理模型会消耗更多 token（用于隐藏的推理过程），在计费和延迟评估时需要额外考虑。API 响应中可读取 `usage.completion_tokens_details.reasoning_tokens` 查看推理 token 消耗。

---

## GPT-5 与统一推理范式

GPT-5（2025.08）标志着 OpenAI 从"对话模型 + 推理模型双线"转向"单一模型自适应推理"：

- **思考模式自适应**：模型自行判断问题难度，简单对话快速直答，复杂推理自动展开思维链，无需用户手动选择 `reasoning_effort`。
- **Codex 与 Agent 增强**：GPT-5 及 GPT-5.1（2026.04）强化了多步骤编码、工具编排和长时任务执行能力，可在一个会话中持续操作数十步。
- **多模态原生**：统一处理文本、图像、音频，减少模态切换开销。
- **指令遵循与安全**：后训练阶段引入更多真实场景偏好数据，减少越狱和有害输出。

### 选择建议

| 场景 | 推荐 |
|------|------|
| 日常对话、写作、翻译 | GPT-5（默认快速模式）或 GPT-4o |
| 复杂推理、数学、竞赛编程 | GPT-5（深度思考）或 o4-mini |
| Agent 多步工具编排 | GPT-5.1 / GPT-5 |
| 成本敏感的大规模调用 | GPT-4o-mini / o4-mini |

> 趋势：模型间"会不会推理"的边界正在消失，差异化更多体现在成本、延迟、上下文长度和 Agent 稳定性上。

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

### 结构化输出（Structured Outputs）

OpenAI 在 2024 年 8 月推出 Structured Outputs，通过 JSON Schema 约束模型输出，保证返回严格符合指定格式，可靠性接近 100%：

```python
from pydantic import BaseModel

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "解方程 8x + 7 = -23"}],
    response_format=MathReasoning,  # 模型输出会被约束为该结构
)

result = completion.choices[0].message.parsed  # 直接得到 Python 对象
print(result.final_answer)
```

> **适用场景：** 需要从非结构化文本中提取结构化数据、保证 Agent 工具调用参数格式正确、生成可被程序直接消费的 JSON 输出。这是构建可靠 Agent 系统的关键能力。

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

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-03 00:15:41*
