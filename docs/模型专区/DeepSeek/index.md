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

**参考资料：**
- [DeepSeek-V3 GitHub](https://github.com/deepseek-ai/deepseek-v3)
- [DeepSeek v3 and R1 Architecture (Fireworks AI)](https://fireworks.ai/blog/deepseek-model-architecture)
- [Complete Guide to DeepSeek Models (BentoML)](https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond)
- [DeepSeek-R1 Model Architecture (Towards AI)](https://pub.towardsai.net/deepseek-r1-model-architecture-853fefac7050)
- [DeepSeek-R1 Model Architecture (Founders Creative)](https://www.founderscreative.org/model-architecture-behind-deepseek-r1)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 10:42:21*
*资源区块更新时间：2026-06-30 10:25:06*
