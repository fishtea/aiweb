# DeepSeek — 深度求索

> DeepSeek（深度求索）是由中国 AI 公司深度求索开发的大语言模型系列。DeepSeek 以极致的性价比和创新的 MoE 架构闻名，其 V3 和 R1 模型在 2024-2025 年震撼了全球 AI 社区。

---

## 模型演进

| 模型 | 发布时间 | 总参数量 | 激活参数量 | 架构特点 |
|------|---------|---------|-----------|---------|
| DeepSeek-V2 | 2024.01 | 236B | 21B | 引入 MLA + MoE |
| DeepSeek-V3 | 2024.12 | 671B | 37B | 更激进的 MoE + FP8 训练 |
| DeepSeek-R1 | 2025.01 | 671B | 37B | 基于 V3 的推理增强模型 |
| DeepSeek-V3.1 | 2025.03 | 671B | 37B | V3 增强版 |
| DeepSeek-R1-0528 | 2025.05 | 671B | 37B | R1 增强版 |
| DeepSeek-V3.2-Exp | 2025.09 | 671B | 37B | 架构实验版，稀疏注意力 |
| DeepSeek-V4 | 2026 | — | — | 新旗舰 |

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

根据 [BentoML DeepSeek 完全指南](https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond)：

- **R1-Zero:** 完全通过强化学习（RL）训练，无监督数据，展现出"顿悟"式的推理能力
- **R1:** 在 RL 基础上加入冷启动数据和多阶段训练，提升了可读性和稳定性
- **蒸馏版本:** 将 R1 的推理能力蒸馏到 Qwen (1.5B-32B) 和 LLaMA (8B-70B) 等小模型

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

---

---

## 10. 2026 年 DeepSeek 生态新发展

### 10.1 DeepSeek-V4：新一代旗舰

2026 年，DeepSeek 发布了新一代旗舰模型 **DeepSeek-V4**，标志着该系列从"追平 GPT-4"进入"架构创新引领"的新阶段。根据官方信息和社区分析，V4 的主要升级方向包括：

| 维度 | V3 / R1 | V4 |
|------|---------|-----|
| 架构基础 | MoE (671B total / 37B active) | **新一代混合架构** |
| 注意力机制 | MLA（Multi-Head Latent Attention） | **增强版 MLA + 稀疏注意力** |
| 训练规模 | 约 14.8T tokens, FP8 | **更大规模、长上下文训练** |
| 推理能力 | R1 引入 think 标签推理链 | **原生推理能力集成，无需推理开关** |
| 上下文长度 | 128K tokens | **显著扩展** |
| 多模态支持 | 纯文本 | **原生多模态（文本+图像+代码）** |

V4 的关键设计理念是**不再区分"聊天模型"和"推理模型"**——基础模型本身就具备深层推理能力，用户无需显式选择 `deepseek-chat` 或 `deepseek-reasoner`。

### 10.2 开源生态与衍生项目

DeepSeek 系列在 GitHub 上的影响力持续增长：

- **DeepSeek-V3**（103,857 ⭐）—— 开源 MoE 大模型的里程碑
- **DeepSeek-R1**（91,982 ⭐）—— 推理增强模型，定义了 think 标签推理范式
- 多个社区蒸馏版本（1.5B-70B）让推理能力下沉到消费级硬件

### 10.3 行业影响

- **MLA 架构**已成为主流开源模型的标准设计选择，多个后续模型（如 Kimi、Qwen 的部分版本）借鉴了其 KV 缓存压缩思路
- **极致的训练成本透明化**推动行业更广泛地讨论"高效训练"而非"堆算力"
- R1 的 `<think>` 推理标签格式已成为行业事实标准，被 Claude 和 Gemini 等模型在不同程度上采纳

> 注意：以上关于 V4 的信息基于 2026 年上半年公开资料。DeepSeek 官方尚未发布完整的技术报告，部分细节仍需等待正式披露。

### 10.4 参考来源

- [DeepSeek-V3 GitHub](https://github.com/deepseek-ai/deepseek-v3)
- [DeepSeek-R1 GitHub](https://github.com/deepseek-ai/DeepSeek-R1)
- [DeepSeek 官方 API 文档](https://api-docs.deepseek.com/)
- [BentoML: Complete Guide to DeepSeek Models](https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-05 05:14:27*
