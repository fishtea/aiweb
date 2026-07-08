# DeepSeek — 深度求索

> DeepSeek（深度求索）是由中国 AI 公司深度求索开发的大语言模型系列。DeepSeek 以极致性价比、MLA、MoE 和推理模型闻名；按 2026-07-06 官方 API 文档与官方 Hugging Face 组织页，可重点关注 V3 / R1、R1-0528、DeepSeek-OCR 以及蒸馏模型。

---

## 模型演进

| 模型 | 发布时间 | 总参数量 | 激活参数量 | 架构特点 |
|------|---------|---------|-----------|---------|
| DeepSeek-V2 | 2024.05 | 236B | 21B | 引入 MLA + MoE |
| DeepSeek-V3 | 2024.12 | 671B | 37B | 更激进的 MoE + FP8 训练 |
| DeepSeek-R1 | 2025.01 | 671B | 37B | 基于 V3 的推理增强模型 |
| DeepSeek-V3-0324 | 2025.03 | 671B | 37B | V3 增强版，API 中对应 `deepseek-chat` |
| DeepSeek-R1-0528 | 2025.05 | 671B | 37B | R1 增强版 |
| DeepSeek-OCR | 2026 | 3B / MoE-570M | — | OCR、文档理解与视觉文本压缩 |

---

## 架构创新

根据 [Fireworks AI 的 DeepSeek 架构分析](https://fireworks.ai/blog/deepseek-model-architecture)：

### 1. Multi-Head Latent Attention (MLA)

传统 MHA（Multi-Head Attention）在推理时需要缓存完整的 KV 矩阵，消耗大量显存。MLA 的核心创新是：

- 将 Key 和 Value 投影到 **低维潜在空间**
- 推理时只需缓存低维的潜在向量，而非完整的 KV 矩阵
- **大幅降低显存占用**，同时保持甚至提升注意力质量

### 2. 激进 MoE

根据 [DeepSeek-V3 GitHub](https://github.com/deepseek-ai/deepseek-v3) 的技术细节：

- 总参数 671B，每 token 仅激活 **37B 参数**
- 从 V2 的 1 个所有专家激活层增加到 V3 的 **3 个共享专家层**
- 采用 **auxiliary-loss-free** 负载均衡策略——消除辅助损失对模型质量的负面影响
- FP8 混合精度训练，显著降低训练成本

### 3. Multi-Token Prediction (MTP)

DeepSeek-V3 在训练中引入多 Token 预测目标：模型同时预测下一个 token 和后多个 token，增强对长期依赖的理解能力。

### 4. DeepSeek 对开源生态的影响

DeepSeek 的意义超越单一模型，它重新定义了"开源 + 极致性价比"的路线：

- **R1 蒸馏系列**将推理能力下沉到 1.5B-70B 小模型，让消费级硬件也能跑推理模型，带动了本地部署热潮。
- **MLA + 辅助损失免费 MoE** 被后续多个开源模型借鉴，降低了大模型推理的显存门槛。
- **训练成本透明化**（V3 约 $5.5M）打破了"大模型只能巨头玩"的叙事，推动中小团队参与。
- 其推理链（`<think>` 标签）输出风格成为行业事实标准之一，被众多蒸馏模型沿用。

> 局限提醒：DeepSeek 在中文、代码、数学推理上表现突出，但部分国际知识和英文长尾不如 GPT/Claude；内容合规策略较严格，敏感话题可能拒答。

---

## DeepSeek-R1 — 推理增强

根据 DeepSeek-R1 论文、官方 GitHub 与官方 2025-05-28 更新公告：

- **R1-Zero:** 完全通过强化学习（RL）训练，无监督数据，展现出"顿悟"式的推理能力
- **R1:** 在 RL 基础上加入冷启动数据和多阶段训练，提升了可读性和稳定性
- **蒸馏版本:** 将 R1 的推理能力蒸馏到 Qwen (1.5B-32B) 和 LLaMA (8B-70B) 等小模型
- **R1-0528:** 推理质量和工具使用稳定性进一步提升，官方 API 中对应 `deepseek-reasoner`

## 2026 新增方向

- **DeepSeek-OCR:** 官方 Hugging Face 组织页列出的视觉文档模型，强调 OCR、文档解析、图像中文本压缩和多模态预处理。
- **蒸馏模型继续重要:** DeepSeek-R1-Distill-Qwen / Llama 系列仍适合本地推理实验、低成本部署和教学。
- **API 名称仍以能力路由为主:** 官方 API 使用 `deepseek-chat` 与 `deepseek-reasoner`，生产系统应按任务选择，而不是只按底层 checkpoint 名称选择。

### 🚀 DeepSeek-V4 发布（2026-06-27）

根据 [DeepSeek-V4 技术报告 (arXiv:2606.19348)](https://arxiv.org/abs/2606.19348) 和 [HuggingFace 官方模型页](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)，DeepSeek 于 2026 年 6 月底发布了 **DeepSeek-V4 系列**，包含两个 MoE 模型：

| 模型 | 总参数 | 激活参数 | 上下文长度 | 精度 |
|------|--------|---------|-----------|------|
| **DeepSeek-V4-Flash** | 284B | 13B | 1M | FP4 + FP8 Mixed |
| **DeepSeek-V4-Pro** | 1.6T | 49B | 1M | FP4 + FP8 Mixed |

#### 架构三大创新

**1. 混合注意力架构（Hybrid Attention）**
结合 **压缩稀疏注意力（CSA, Compressed Sparse Attention）** 和 **重度压缩注意力（HCA, Heavily Compressed Attention）**，在 1M-token 上下文下，V4-Pro 仅需 V3.2 **27% 的单 token FLOPs** 和 **10% 的 KV 缓存**，极大降低了长上下文推理成本。

**2. 流形约束超连接（mHC, Manifold-Constrained Hyper-Connections）**
增强传统残差连接，在保持模型表达力的同时提升跨层信号传播的稳定性。

**3. Muon 优化器**
采用 Muon 优化器实现更快的收敛速度和更高的训练稳定性。

#### 训练与后训练

- 在 **32T+** 多样化高质量 token 上进行预训练
- 后训练采用**两阶段范式**：先独立培养领域专家（通过 SFT + GRPO 强化学习），再通过 **on-policy 蒸馏**将不同领域的专长统一整合到单一模型

#### 三种推理模式

| 模式 | 特点 | 适用场景 |
|------|------|---------|
| **Non-think** | 快速直观响应 | 日常任务、低风险决策 |
| **Think High** | 有意识的逻辑分析 | 复杂问题求解、规划 |
| **Think Max** | 推理能力推到极限 | 探索模型推理边界 |

#### 基准表现

**DeepSeek-V4-Pro-Max**（最高推理努力模式）在多项基准上达到开源模型最强水平：

- **LiveCodeBench**: 93.5%（超越 Opus 4.6 Max 的 88.8% 和 Gemini 3.1 Pro 的 91.7%）
- **Codeforces Rating**: 3206（所有模型中最高）
- **Apex Shortlist**: 90.2%（最高）
- **MMLU-Pro**: 87.5%（与 GPT-5.4 持平）
- **SWE Verified**: 80.6%（解决率接近前沿闭源模型）

#### 开源生态影响

- **MIT 许可证**：权重完全开源，允许商业使用
- **DSpark 推测解码**：通过 vLLM 一行配置即可启用，加速推理
- **FP4 + FP8 混合精度**：MoE 专家参数使用 FP4，大幅降低存储和推理成本
- **V4-Flash（284B/13B 激活）**：在较小参数规模下仍能通过 Think Max 模式接近 Pro 的推理水平

> **选型更新**：2026 年下半年，DeepSeek-V4 系列是开源模型中的首选。Pro 适合高难度推理和 Agent 任务，Flash 在成本和能力间取得了出色的平衡。已有 V3/R1 部署的团队应考虑迁移评估。

### 架构细节

根据 [Towards AI 的 DeepSeek-R1 架构分析](https://pub.towardsai.net/deepseek-r1-model-architecture-853fefac7050)：

- 基于 DeepSeek-V3-Base 架构
- **61 层 Transformer**（前 3 层为标准 FFN，第 4-61 层使用 MoE）
- 全部使用 MLA 替代标准多头注意力
- 上下文长度：**128K tokens**

---

## 性能表现

DeepSeek-V3 在多个基准上达到或超越了 GPT-4 和 Claude 3.5 Sonnet 水平：

| 基准 | DeepSeek-V3 | GPT-4 | Claude 3.5 Sonnet |
|------|-------------|-------|-------------------|
| MMLU (5-shot) | **87.1** | 86.4 | 88.7 |
| MMLU-Pro | 75.9 | — | 78.0 |
| WinoGrande | **86.3** | — | — |

*数据来源: [DeepSeek-V3 GitHub README](https://github.com/deepseek-ai/deepseek-v3)*

---

## 如何使用

### API 调用

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com"
)

completion = client.chat.completions.create(
    model="deepseek-chat",  # 或 deepseek-reasoner
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "解释 DeepSeek 的 MoE 架构。"}
    ]
)

print(completion.choices[0].message.content)
```

### 本地运行

```bash
# 通过 Ollama
ollama run deepseek-v3

# 通过 vLLM
vllm serve deepseek-ai/DeepSeek-V3
```

---

## 优势与局限

**优势:**
- **极致性价比:** 训练成本仅约 $5.5M，推理成本远低于 GPT-4
- **顶级推理能力:** R1 在数学和编程推理任务上达到 GPT-4o 级别
- **开源权重:** 模型权重和蒸馏版本均可下载
- **MLA 创新:** 显存效率极高

**局限:**
- 内容过滤较为严格（中国公司背景）
- 英文能力略逊于 GPT-4（中文场景表现极佳）
- 超大模型需多 GPU 才能运行
- 稳定性偶有波动

## 2026 生产选型建议

| 场景 | 推荐 |
|------|------|
| 通用中文问答、代码解释、低成本 API | `deepseek-chat`（V3-0324） |
| 数学、代码修复、复杂规划 | `deepseek-reasoner`（R1 / R1-0528） |
| OCR、文档解析、版面理解 | DeepSeek-OCR |
| 本地推理模型学习 | DeepSeek-R1-Distill-Qwen / Llama 系列 |
| 私有化高吞吐服务 | DeepSeek-V3 / R1 + vLLM、SGLang 或 TensorRT-LLM |

> 截至本次更新，正文只保留官方 API 文档、官方 GitHub 或 DeepSeek 官方 Hugging Face 组织页可核验的模型。没有把未发布技术报告的传闻模型写成事实。

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-09 00:14:29*
