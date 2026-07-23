# GPT 系列 — OpenAI

> GPT（Generative Pre-trained Transformer）系列是 OpenAI 开发的旗舰大语言模型家族。按 OpenAI 2026-07-06 官方模型列表，生产选型应重点关注 GPT-5.6、GPT-5.5、GPT-5.5-mini、GPT-4.1 和 o 系列推理模型。

---

## 架构演进

| 模型 | 发布时间 | 参数规模 | 架构特点 |
|------|---------|---------|---------|
| GPT-1 | 2018.06 | 117M | 首个 Decoder-only Transformer，开创生成式预训练范式 |
| GPT-2 | 2019.02 | 1.5B | 扩大模型规模，展示零样本迁移能力 |
| GPT-3 | 2020.06 | 175B | 大规模 In-context Learning，涌现 Few-shot 能力 |
| GPT-3.5 | 2022.03 | 175B | InstructGPT 的 RLHF 微调版本，ChatGPT 的基础 |
| GPT-4 | 2023.03 | 未公开 | 多模态（图像+文本），推理能力大幅飞跃 |
| GPT-4o | 2024.05 | 未公开 | 原生多模态，实时语音交互，速度提升 |
| o1 (preview) | 2024.09 | 未公开 | 首个推理模型，通过 RL 学会\"思考\"再回答 |
| o1 正式版 | 2024.12 | 未公开 | 推理能力大幅提升，竞赛级数学/编程 |
| o3-mini | 2025.01 | 未公开 | 低成本推理模型，支持函数调用 |
| GPT-4.5 | 2025.02 | 未公开 | 更强的世界知识和情感智能 |
| o3 / o4-mini | 2025.04 | 未公开 | 推理 + 工具调用 + 多模态，o4-mini 性价比极高 |
| GPT-4.1 系列 | 2025.04 | 未公开 | 强化编码、指令遵循和长上下文，提供 mini / nano 档位 |
| GPT-5.5 系列 | 2026 | 未公开 | 2026 主力通用模型，含 mini 与 nano 档位 |
| GPT-5.6 | 2026 | 未公开 | 最新旗舰预览模型，面向复杂任务、Agent 和编码 |

> **核心架构:** GPT 系列仍以 Decoder-only Transformer 为基础。GPT-4o 将文本、图像、音频交互统一到更低延迟的多模态体验；o 系列是面向复杂推理的模型线，会在内部消耗推理 token；GPT-5.5 / 5.6 系列把通用对话、编码、工具调用和 Agent 执行能力继续合并到更统一的模型路线。

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

## 2026 最新模型线

- **GPT-5.6**：OpenAI 官方模型页列出的最新旗舰预览模型，定位为复杂任务、长期 Agent、编码和高难度推理的首选。
- **GPT-5.5**：2026 主力旗舰模型，适合通用对话、多模态理解、工具调用和生产级 Agent。
- **GPT-5.5-mini / nano**：面向低成本、高吞吐和低延迟场景，适合路由、抽取、摘要、批处理和简单工具调用。
- **GPT-4.1 / 4.1-mini / 4.1-nano**：仍适合代码、长上下文和稳定结构化输出；如果系统已经围绕 4.1 做评估，可作为保守生产基线。
- **GPT-4o / GPT-4o-mini**：多模态交互和低延迟体验仍有价值，但新项目应优先评估 GPT-5.5 系列。

### GPT-5.6 三档分级（2026 年 7 月最新）

根据 [OpenAI 官方模型文档](https://platform.openai.com/docs/models)（2026 年 7 月访问），GPT-5.6 系列已正式扩展为 **三档分级模型线**，覆盖从旗舰推理到成本敏感的大规模调用：

| 模型 | 定位 | 适用场景 |
|------|------|---------|
| **GPT-5.6 Sol** | 旗舰模型 | 复杂推理、编程、科学研究、高难度 Agent 任务 |
| **GPT-5.6 Terra** | 平衡型 | 智能与成本平衡，适合通用生产级部署 |
| **GPT-5.6 Luna** | 轻量高吞吐 | 成本敏感的大规模调用、批量处理、路由 |

三个模型均支持文本和图像输入、文本输出、多语言能力、视觉理解和多模态推理，通过 Responses API 和 OpenAI Client SDKs 访问。

#### GPT-5.6 Sol — 旗舰推理与编码模型（2026-06-26 预览）

根据 [OpenAI 官方博客](https://openai.com/index/previewing-gpt-5-6-sol)（2026 年 6 月 26 日发布），GPT-5.6 Sol 在编码、科学研究和网络安全三个领域实现了显著的能力跃升：

- **编码能力**：在复杂软件工程任务、多文件重构和长链工具调用上的表现大幅超越 GPT-5.5
- **科学研究**：在 GeneBench-Pro 等基因组学和生物学基准测试中展现出前沿水平
- **网络安全**：配备 OpenAI 最先进的安全栈（safety stack），在保持高风险能力的同时强化了拒绝不当请求的准确性
- **预览状态**：面向早期测试者和企业客户开放

#### GPT-5.6 Terra — 平衡智能与成本

GPT-5.6 Terra 定位为"智能与成本的最佳折中点"，适合作为日常生产部署的默认选择。Terra 在保持高推理质量的同时，通过更高效的推理路径降低了每 token 成本，适合需要持续运行的大多数生产场景。

#### GPT-5.6 Luna — 成本敏感的高吞吐选择

GPT-5.6 Luna 面向成本优先的大规模调用场景，是 GPT-5.6 系列中最经济的选项。适合批量抽取、摘要、分类、路由和轻量级 Agent 编排等不需要最高推理质量的任务。

> **选型建议**：GPT-5.6 三档模型实现了从旗舰到经济型的完整覆盖。新项目应优先评估三个模型在各档位上的推理质量和成本，按任务复杂度路由：Sol 处理高难度步骤，Terra 处理日常生产负载，Luna 处理大批量低成本任务。

### OpenAI × Broadcom Jalapeño 推理芯片（2026-06-24）

根据 [OpenAI 官方公告](https://openai.com/index/openai-broadcom-jalapeno-inference-chip)（2026 年 6 月 24 日），OpenAI 与 Broadcom 联合发布了 **Jalapeño**——一款专为大语言模型推理优化的定制 AI 芯片：

- **定位**：LLM 推理专用芯片，旨在提升性能、效率和规模化部署能力
- **意义**：OpenAI 首次涉足自研 AI 硬件，减少对外部 GPU 供应（主要是 NVIDIA）的依赖
- **产业影响**：标志着头部 AI 公司从纯模型研发向"模型+芯片"垂直整合的战略转型，类似 Google TPU 和 Amazon Trainium 的路径

### Agent 正在改变工作方式（2026-06-25）

根据 [OpenAI 研究论文](https://openai.com/index/how-agents-are-transforming-work)（2026 年 6 月 25 日发布），OpenAI 发布了关于 AI Agent 对工作方式影响的实证研究：

- **任务复杂度提升**：Agent 能完成更长、更复杂的多步任务，不再局限于单轮问答
- **生产力扩展**：Agent 的使用正在从个人辅助扩展到跨角色、跨团队的协作场景
- **产业趋势**：研究指出 Agent 正在从"工具"演进为"数字同事"，改变知识工作的组织方式

> 这项研究与 GPT-5.6 Sol 的发布方向一致——OpenAI 正在将其模型能力向 Agent 化方向集中，而非单纯追求基准分数。

### OpenAI 发布新一代语音模型（2026-07-09）

根据 [TechCrunch 报道](https://techcrunch.com/category/artificial-intelligence/)（2026 年 7 月 9 日），OpenAI 发布了**新一代语音模型**，旨在实现更自然的实时语音对话：

- **更自然的对话体验**：新模型在语音语调、停顿和情感表达上更接近真人，减少机械感
- **实时交互优化**：降低语音响应延迟，支持更流畅的打断和插话
- **应用场景**：面向语音助手、客服系统、实时翻译和 AI 陪伴等场景

这次发布延续了 OpenAI 从 GPT-4o 开启的语音交互路线，将语音能力从"能用"推向"自然"，标志着语音 AI 正在从辅助功能转变为核心交互方式。

> 同时关注：OpenAI × Broadcom 联合推出的 **Jalapeño 推理芯片**（2026-06-24）标志着 OpenAI 从纯模型公司向"模型+芯片"垂直整合的战略转型，减少对 NVIDIA GPU 的依赖。

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

## 2026 生产选型建议

截至 2026-07-06，OpenAI 的实用选型可以按任务拆分：

- **默认旗舰**：GPT-5.5。适合通用助手、多模态、工具调用和生产 Agent。
- **最高质量 / 前沿能力验证**：GPT-5.6。适合复杂编码、规划、研究和高价值任务。
- **成本敏感**：GPT-5.5-mini / nano。适合批量抽取、摘要、分类、路由和轻量对话。
- **专门推理**：o3、o4-mini 或 o3-mini。适合需要显式推理预算和可控延迟的数学、规划、复杂代码修复。
- **保守迁移**：GPT-4.1 系列。适合已有评估体系且暂不想切换到 GPT-5.5 的生产系统。

### 选择建议

| 场景 | 推荐 |
|------|------|
| 日常对话、写作、翻译 | GPT-5.5 / GPT-5.5-mini |
| 复杂推理、数学、竞赛编程 | GPT-5.6 / o3 / o4-mini |
| Agent 多步工具编排 | GPT-5.6 / GPT-5.5 |
| 成本敏感的大规模调用 | GPT-5.5-mini / GPT-5.5-nano |

> 趋势：生产系统越来越少依赖单一模型。常见做法是用便宜模型做路由、抽取和简单回答，用推理模型处理少量高难度任务，并通过评估集控制成本和质量。

---

## 如何使用

### 通过 ChatGPT（网页/App）

- ChatGPT 付费档位可访问更高能力模型和更高配额；具体模型与限额会随地区和订阅层级变化。
- Team/Enterprise 有更高配额和隐私保护

### 通过 API

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

completion = client.chat.completions.create(
    model="gpt-5.5",
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
    model="gpt-5.5",
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

---

## 2026 年 7 月最新进展

### GPT-5.5 — 2026 年 4 月前沿模型

OpenAI 于 **2026 年 4 月 23 日** 发布 GPT-5.5（内部代号"Spud"），定位为面向真实工作的前沿模型。距 GPT-5.4 仅间隔 6 周，展示了 OpenAI 加速迭代的节奏。

**三个变体：**

| 变体 | 说明 | 可用范围 |
|------|------|---------|
| GPT-5.5（标准） | 默认版，更快的思考速度，更少 token 消耗 | ChatGPT 全档位、Codex |
| GPT-5.5 Thinking | 扩展推理预算，适合复杂电子表格、研究简报、多文件调试 | ChatGPT(约 3000 条/周) |
| GPT-5.5 Pro | 最高精度版，面向正确性关键任务 | Pro/Business/Enterprise |

**核心指标：**
- **SWE-bench：88.7%** — 多步编码能力大幅领先
- **MMLU：92.4%** — 知识广度保持领先
- **幻觉率降低 60%** — 相比 GPT-5.4 显著改善
- **定价：** $5/M 输入 token，$30/M 输出 token（约为 GPT-5.4 两倍，但 token 消耗更高效）
- **Computer Use：** 支持浏览器操控、桌面交互等 Agent 场景

### GPT-5.6 — 2026 年 7 月最新旗舰

OpenAI 于 **2026 年 7 月 9 日** 公开发布 GPT-5.6，作为最新的前沿预览模型，面向付费用户。GPT-5.6 进一步提升了复杂任务、Agent 执行和高难度编码的能力，被视为即将到来的 GPT-6 的技术验证。

### ChatGPT 全面升级 + Codex 集成

2026 年中，ChatGPT 界面进行了彻底改造，不再是单纯的聊天框。主要变化：

- **Codex 集成：** OpenAI 开发环境 Codex 成为 ChatGPT 的一部分，支持直接编写、运行和调试代码
- **Agent 模式：** 模型可自主规划、使用浏览器和终端工具、运行多步工作流
- **Computer Use 增强：** GPT-5.5/5.6 可直接操控桌面应用，实现自动化操作
- **免费档位可体验：** 免费和 Go 用户也可临时使用 GPT-5.5（有限额）

### 生产选型更新（2026 年 7 月）

| 场景 | 2026 Q2 推荐 | 新增选型 |
|------|-------------|---------|
| 前沿能力验证 | GPT-5.6/GPT-5.5 Pro | GPT-5.6 可选 |
| Agent 多步工具编排 | GPT-5.6/GPT-5.5 | GPT-5.5 Thinking 可选 |
| 复杂编码 | GPT-5.5 Thinking | GPT-5.6 候选 |
| 成本平衡 | GPT-5.5-mini | 已稳定可用 |

**资料来源：**
- [What Is GPT-5.5? OpenAI's New Frontier Model Explained (Apidog)](https://apidog.com/blog/what-is-gpt-5-5/)
- [OpenRouter — GPT-5.5 API Pricing & Benchmarks](https://openrouter.ai/openai/gpt-5.5)
- [ChatGPT Free Plan Limits 2026: GPT-5.5 & the Caps](https://freeacademy.ai/blog/chatgpt-free-plan-limits-2026)
- [OpenAI API Models 文档](https://platform.openai.com/docs/models)

---

**参考资料：**
- [OpenAI GPT-4 官方页面](https://openai.com/index/gpt-4)
- [OpenAI API Models 文档](https://platform.openai.com/docs/models)
- [GPT-4 Technical Report (arXiv:2303.08774)](https://arxiv.org/abs/2303.08774)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-24 00:15:31*
