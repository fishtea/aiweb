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

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-09 00:14:29*
