# Qwen 系列 — 阿里巴巴

> Qwen（通义千问）是由阿里巴巴 Qwen 团队开发的大语言模型系列。Qwen 走 Dense（稠密）和 MoE（混合专家）双路线，并覆盖文本、代码、视觉、音频和 Omni 多模态。按 2026-07-06 可核验的 Qwen 官方博客与模型仓库，新项目应优先评估 Qwen3、Qwen3-Coder、Qwen2.5-VL / Omni 相关模型。

---

## 模型演进

| 模型 | 发布时间 | 参数规模 | 架构 | 训练数据 | 上下文 |
|------|---------|---------|------|---------|-------|
| Qwen-7B | 2023.08 | 7B | Dense | 3T tokens | 8K |
| Qwen-14B | 2023.09 | 14B | Dense | 3T tokens | 8K |
| Qwen-72B | 2023.11 | 72B | Dense | 3T tokens | 8K |
| Qwen1.5 | 2024.02 | 0.5B-110B | Dense | — | 32K |
| Qwen2 | 2024.06 | 0.5B-72B | Dense | — | 128K |
| Qwen2.5 | 2024.12 | 0.5B-72B | Dense | 18T tokens | 128K |
| Qwen2.5-Max | 2025.01 | 未公开 | **MoE** | >20T tokens | 128K |
| Qwen2.5-VL | 2025.01 | 3B/7B/72B | 视觉语言 | — | — |
| Qwen3 系列 | 2025.04 | 0.6B-235B(A22B) | Dense + MoE | 36T+ tokens | 32K-128K |
| Qwen3-Coder | 2025.07 | 多规格 | Dense / MoE | 代码与 Agent 数据 | 长上下文 |

### Qwen3 — 统一推理与思考模式

Qwen3（2025.04）是 Qwen 走向"思考模式可控"的一代：

- **混合思考模式**：支持 `thinking`（深度推理）与 `non-thinking`（快速直答）两种模式，兼顾准确率与延迟。
- **Dense + MoE 双规格**：从 0.6B 端侧到 235B（激活 22B）旗舰 MoE，覆盖从手机到数据中心的部署需求。
- **Agent 与工具调用强化**：原生支持函数调用、结构化输出和 MCP，在 Agent 基准上表现领先。
- **多语言与中文优势**：延续 Qwen 系列的中文能力，同时大幅提升多语言覆盖。

### Qwen3 完整规格表

根据 [Qwen3 官方博客](https://qwenlm.github.io/blog/qwen3/)（2025.04 发布），Qwen3 提供了从端侧到数据中心的完整模型链：

| 模型 | 参数（总/激活） | 架构 | 层数 | Q/KV 头数 | 上下文 |
|------|---------------|------|------|----------|--------|
| Qwen3-0.6B | 0.6B | Dense | 28 | 16/8 | 32K |
| Qwen3-1.7B | 1.7B | Dense | 28 | 16/8 | 32K |
| Qwen3-4B | 4B | Dense | 36 | 32/8 | 32K |
| Qwen3-8B | 8B | Dense | 36 | 32/8 | 128K |
| Qwen3-14B | 14B | Dense | 40 | 40/8 | 128K |
| Qwen3-32B | 32B | Dense | 64 | 64/8 | 128K |
| **Qwen3-30B-A3B** | 30B / **3B 激活** | **MoE（128专家/8激活）** | 48 | 32/4 | 128K |
| **Qwen3-235B-A22B** | 235B / **22B 激活** | **MoE（128专家/8激活）** | 94 | 64/4 | 128K |

所有 Qwen3 模型均以 **Apache 2.0** 许可开源。

### 混合思考模式详解

Qwen3 引入了自主可控的**双模推理**能力：

- **思考模式（Thinking Mode）**：模型在给出最终答案前逐步推理（chain-of-thought），适合数学、编程、逻辑推理等复杂问题。可通过在系统提示中添加 `'thinking'` 或 `'deep-thinking'` 风格触发。
- **非思考模式（Non-Thinking Mode）**：快速近即时响应，适合简单的知识问答和日常对话。
- **思考预算控制（Thinking Budget Control）**：用户可以精细控制模型投入的推理计算量，在成本和响应质量之间取得平衡。随着推理预算增加，模型表现展现可预测的平滑提升。

### 119 种多语言支持

Qwen3 支持 **119 种语言和方言**，覆盖主要语系：

- **印欧语系**：英语、法语、德语、西班牙语、葡萄牙语、意大利语、俄语、印地语、乌尔都语、孟加拉语等 60+ 语言
- **汉藏语系**：简体中文、繁体中文、粤语、缅甸语
- **亚非语系**：阿拉伯语（含 7 种方言）、希伯来语、马耳他语
- **南岛语系**：印尼语、马来语、他加禄语等 10+ 语言
- **德拉维达语系**：泰米尔语、泰卢固语等 5 种
- **其他**：日语、韩语、越南语、泰语、匈牙利语、芬兰语等

### Qwen 生态扩展

根据 Qwen 官方博客系列：

- **Qwen3Guard**（2025.09）：Qwen 首个安全护栏模型，基于 Qwen3 微调，支持提示词和回复的双向安全分类，在多项安全基准上达到 SOTA。
- **Qwen-Image**（2025.08）：20B MMDiT 图像基础模型，原生文本渲染能力突出，支持多行文字、段落级语义排版。
- **Qwen-Image-Edit**（2025.08）：在 Qwen-Image 基础上扩展的图像编辑版本，结合 Qwen2.5-VL 的视觉语义理解实现精确编辑。
- **Qwen-MT**（2025.07）：机器翻译模型系列，支持 92 种语言间翻译，采用 RL 技术提升翻译准确性和流畅度。
- **GSPO 算法**（2025.07）：Group Sequence Policy Optimization，旨在解决 GRPO 等强化学习算法在长训练过程中的稳定性问题，推动 RL Scaling。

### 2026 选型建议

| 场景 | 推荐 |
|------|------|
| 中文通用问答与企业知识库 | Qwen3-14B / 32B / 235B-A22B |
| 本地轻量部署 | Qwen3-0.6B / 1.7B / 4B / 8B |
| 代码生成与 Coding Agent | Qwen3-Coder、Qwen2.5-Coder |
| 视觉文档理解 | Qwen2.5-VL、Qwen-VL 系列 |
| 语音、视频、跨模态 Agent | Qwen-Omni / Qwen-Audio 相关模型 |

> 截至 2026-07-06，未找到 Qwen 官方发布的 Qwen4 主线资料；本文按官方可核验的 Qwen3 / Qwen3-Coder / Qwen2.5-VL / Omni 相关模型更新。

---

## 2026 年 7 月补充：新模型与实战指南

### Qwen3-Coder 深度解析

根据 [Qwen3-Coder 官方博客](https://qwenlm.github.io/blog/qwen3-coder/)（2025 年 7 月发布），Qwen3-Coder Qwen 家族中首个 **Agentic Coding** 专用模型，其旗舰版本 **Qwen3-Coder-480B-A35B-Instruct** 在多项 Agent 编码基准上达到了开源模型最强水平：

**模型规格：**
- 总参数 480B，激活参数 35B（MoE 架构）
- 原生支持 **256K tokens** 上下文，通过外推方法可扩展至 **1M tokens**
- 覆盖多个规格：从 7B 开源版到 480B 旗舰版

**Agent 编码能力：** 在 Agentic Coding、Agentic Browser-Use 和 Agentic Tool-Use 三大维度上表现领先，性能与 **Claude Sonnet 4** 相当。这意味着 Qwen3-Coder 不仅能写代码，还能:
- 自主浏览网页并提取信息
- 使用工具完成端到端开发任务
- 在复杂编码工作流中做决策和规划

**部署建议：**
- 旗舰版（480B-A35B）需要多 GPU 部署（建议 4×A100 80GB 以上），使用 vLLM 或 SGLang
- 轻量版可在单卡上运行，适合日常编码辅助和 CI/CD 管线集成
- 支持 OpenAI 兼容 API 格式，可直接替换现有的代码模型后端

### Qwen3Guard — 安全护栏模型

根据 [Qwen3Guard 官方博客](https://qwenlm.github.io/blog/qwen3guard/)（2025 年 9 月），Qwen3Guard 是 Qwen 家族首个安全护栏模型：

- 基于 **Qwen3 基础模型**微调，专用于安全分类任务
- 支持**提示词和回复的双向安全检测**，包含风险等级和分类标签
- 在多项安全基准上达到 SOTA（State-of-the-Art）
- 支持中英文及多语言环境
- **开源可部署**：可作为中间件部署在模型服务之前或之后，过滤不安全内容

生产部署中，可将 Qwen3Guard 作为 API 网关的安全过滤层，在 LLM 调用前后分别做输入安全检测和输出安全检测。

### 部署框架对比与实践建议

Qwen3 系列的官方推荐部署方式，根据场景选择：

| 框架 | 优点 | 适合场景 | 部署难度 |
|------|------|---------|---------|
| **SGLang (>=0.4.6.post1)** | 原生支持 Qwen3 推理解析器，结构化输出好 | 推理场景、精确控制 | 中等 |
| **vLLM (>=0.8.4)** | 高吞吐、生态成熟、与现有系统集成好 | 高并发生产部署 | 低 |
| **Ollama** | 一键运行、零配置 | 本地实验、个人学习 | 最低 |
| **Hugging Face Transformers** | 灵活、易于调试 | 研究实验、模型微调 | 中等 |

> 选型建议：生产系统优先选 **vLLM**（高吞吐优先）或 **SGLang**（推理质量优先）。Ollama 适合快速实验。注意所有框架均需 `--enable-reasoning` 和 `--reasoning-parser` 参数来启用 Qwen3 的思考模式。

---

## Qwen2.5 系列

根据 [Qwen2.5 技术报告 (arXiv:2412.15115)](https://arxiv.org/abs/2412.15115)：

### 核心升级
- **18T tokens** 预训练数据，覆盖广泛的知识领域
- **128K tokens** 上下文窗口
- 提供从 0.5B 到 72B 多个规格，适配不同硬件
- 显著提升了代码和数学能力
- 增强了指令跟随与结构化输出能力

### 多规格选择

| 规格 | 适合场景 | 最低硬件 |
|------|---------|---------|
| Qwen2.5-0.5B | 端侧/移动设备 | CPU |
| Qwen2.5-1.5B | 轻量级任务 | CPU/4GB GPU |
| Qwen2.5-7B | 通用推理 | 8GB GPU |
| Qwen2.5-14B | 高质量推理 | 16GB GPU |
| Qwen2.5-32B | 复杂任务 | 24GB GPU |
| Qwen2.5-72B | 旗舰级 | 多 GPU |

---

## Qwen2.5-Max — MoE 旗舰

根据 [Qwen2.5-Max 官方博客](https://qwenlm.github.io/blog/qwen2.5-max)：

- 采用 **MoE (Mixture-of-Experts)** 架构
- >20T tokens 预训练，SFT + RLHF 后训练
- 在 Arena-Hard、LiveBench、LiveCodeBench、GPQA-Diamond 等基准上**超越 DeepSeek V3**
- 与 GPT-4o、Claude-3.5-Sonnet 在 MMLU-Pro 等测试中竞争
- 通过 Alibaba Cloud API 提供服务

### 性能对比

| 基准 | Qwen2.5-Max | DeepSeek V3 | GPT-4o |
|------|-------------|-------------|--------|
| Arena-Hard | **领先** | — | — |
| LiveCodeBench | **领先** | — | — |
| GPQA-Diamond | **领先** | — | — |
| MMLU-Pro | 竞争 | 竞争 | 竞争 |

---

## Qwen2.5-VL — 视觉语言模型

根据 [Qwen2.5-VL 发布公告](https://qwen.ai/blog?id=qwen2.5-vl)：

- 3B/7B/72B 三种规格
- 增强时空感知能力
- 简化的网络结构，提升效率
- 在文档理解、视频理解、视觉 Agent 等任务上表现出色

---

## 如何使用

### 通过 Qwen Chat（免费）

访问 [chat.qwenlm.ai](https://chat.qwenlm.ai/) 直接体验。

### 通过 API

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "介绍 Qwen3 系列的特点。"}
    ]
)

print(completion.choices[0].message.content)
```

### 本地部署 (Hugging Face)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-8B")
```

### 生产部署：SGLang / vLLM

Qwen3 官方推荐使用 **SGLang (>=0.4.6.post1)** 或 **vLLM (>=0.8.4)** 搭建 OpenAI 兼容 API 服务：

```bash
# SGLang 部署（推荐结构化和推理场景）
python -m sglang.launch_server \
  --model-path Qwen/Qwen3-30B-A3B \
  --reasoning-parser qwen3

# vLLM 部署（高吞吐场景）
vllm serve Qwen/Qwen3-30B-A3B \
  --enable-reasoning \
  --reasoning-parser deepseek_r1
```

### 思考模式控制

Qwen3 支持在 tokenizer 中通过 `enable_thinking` 参数控制推理模式：

```python
# 思考模式（深度推理）
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True,
    enable_thinking=True  # 默认开启
)

# 非思考模式（快速问答）
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True,
    enable_thinking=False
)
```

在多轮对话中，可以通过 `/think` 和 `/no_think` 标签动态切换模式：

```text
User: 1+1等于多少？ /no_think
Assistant: 2

User: 证明哥德巴赫猜想 /think
Assistant: <think>这是一个未解决的数学难题...
```

### Agent 集成：Qwen-Agent + MCP

Qwen3 原生支持 MCP（Model Context Protocol）和工具调用。使用 [Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) 框架可快速搭建 Agent：

```python
from qwen_agent.agents import Assistant

bot = Assistant(
    llm={
        "model": "Qwen3-30B-A3B",
        "model_server": "http://localhost:8000/v1",  # 本地 SGLang/vLLM 端点
        "api_key": "EMPTY",
    },
    function_list=[{
        "mcpServers": {
            "time": {"command": "uvx", "args": ["mcp-server-time", "--local-timezone=Asia/Shanghai"]},
            "fetch": {"command": "uvx", "args": ["mcp-server-fetch"]}
        }
    }]
)

messages = [{"role": "user", "content": "搜索最新的 AI 新闻"}]
for responses in bot.run(messages=messages):
    pass
print(responses)
```

### 本地快速体验（Ollama）

```bash
ollama run qwen3:30b-a3b
# 或较小的密集模型
ollama run qwen3:8b
ollama run qwen3:4b
```

---

## 优势与局限

**优势:**
- **顶级中文能力:** 原生中文训练数据，中文任务表现最佳
- **双路线（Dense+MoE）:** 灵活选择，适配不同场景
- **完整规格链:** 从 0.5B 到 72B（Dense）到 MoE 旗舰
- **开源友好:** 大部分模型开源可下载
- **视觉语言:** Qwen2.5-VL 在多模态方面领先

**局限:**
- 英文能力略逊于 GPT-4 和 Claude
- MoE 版本（Qwen2.5-Max）非开源
- 国际社区影响力不及 LLaMA
- 阿里巴巴云依赖（API 用户）

---

**参考资料：**
- [Qwen2.5 Technical Report (arXiv:2412.15115)](https://arxiv.org/abs/2412.15115)
- [Qwen3 官方博客](https://qwenlm.github.io/blog/qwen3/)
- [Qwen3-Coder 官方博客](https://qwenlm.github.io/blog/qwen3-coder/)
- [Qwen2.5-Max 官方博客](https://qwenlm.github.io/blog/qwen2.5-max)
- [Qwen2.5-VL 发布公告](https://qwen.ai/blog?id=qwen2.5-vl)

---

## 2026 最新进展

### Qwen3-Coder-Next（2026.02）：80B/3A 的极致代码 Agent

2026 年 2 月，Qwen 团队发布 [Qwen3-Coder-Next](https://arxiv.org/abs/2603.00729)，一个专为代码 Agent 设计的 80B 参数模型，**推理时仅激活 3B 参数**——用极小的计算预算实现了强大的编码能力。

**架构与训练**：

- **高效 MoE**：80B 总参数，每 Token 仅激活 3B（激活率 ~3.75%），在保持强能力的同时将推理成本压缩到极致。
- **Agentic Training**：通过大规模合成可验证编码任务 + 可执行环境，在 Mid-Training 和 Reinforcement Learning 阶段直接从环境反馈中学习。
- **Fill-in-the-Middle (FIM)**：原生支持代码补全，提升 IDE 场景下的实用性。

**基准表现**：

- SWE-Bench、Terminal-Bench 等 Agent 编码基准上，以仅 3B 激活参数取得了有竞争力的成绩，效率比（性能/激活参数）远超同类。
- 同时发布 Base 和 Instruct 版本，以开源权重形式供研究和实际开发使用。

> 来源：[Qwen3-Coder-Next Technical Report (arXiv)](https://arxiv.org/abs/2603.00729)、[Qwen3-Coder 官方博客](https://qwenlm.github.io/blog/qwen3-coder/)

### Qwen3.5-Omni（2026.04）：全能多模态旗舰

2026 年 4 月，Qwen 团队发布 [Qwen3.5-Omni](https://arxiv.org/abs/2604.15804)，千亿参数级全模态模型，将文本、音频、图像、视频统一到一个架构中。

**核心能力**：

- **超长上下文**：256K Token，支持 10+ 小时音频理解和 400 秒 720P 视频（1FPS）。
- **Hybrid Attention MoE**：Thinker 和 Talker 均采用混合注意力 MoE 架构，高效处理超长序列。
- **ARIA 语音合成**：引入动态对齐技术（ARIA），解决文本和语音 Tokenizer 编码效率差异导致的流式语音不稳定问题，在不增加显著延迟的前提下大幅提升对话的自然度和韵律感。
- **多语言 + 情感表达**：支持 10 种语言的理解与语音生成，带有人类级别的情感细腻度。

**基准表现**：

- 在 215 个音频和音视频理解、推理、交互子任务和基准上取得 **SOTA**。
- 关键音频任务**超越 Gemini-3.1 Pro**，综合音视频理解与之持平。
- 具备脚本级结构化字幕生成能力，支持精确时间同步和自动场景分割。

**Audio-Visual Vibe Coding**：最引人注目的涌现能力——模型可以直接基于音视频指令进行编码，被团队称为「音视频氛围编程」。

> 来源：[Qwen3.5-Omni Technical Report (arXiv)](https://arxiv.org/abs/2604.15804)

### 2026 年 Qwen 系列全景

| 模型 | 发布时间 | 核心定位 | 关键创新 |
|------|---------|---------|---------|
| Qwen3 | 2025.04 | 通用旗舰 | 混合思考模式、Dense+MoE 双路线 |
| Qwen3-Coder | 2025.07 | 代码 Agent | Agentic Coding、多尺寸覆盖 |
| **Qwen3-Coder-Next** | **2026.02** | **极致效率代码 Agent** | **80B/3A MoE、环境反馈 RL** |
| **Qwen3.5-Omni** | **2026.04** | **全模态旗舰** | **Hybrid Attention MoE、ARIA、AV Vibe Coding** |

Qwen 系列已形成从端侧 0.6B 到千亿级全模态的完整产品矩阵，在开源模型生态中与 DeepSeek、LLaMA 形成三足鼎立之势。

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-25 00:09:45*
