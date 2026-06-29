# DeepSeek

> 深度求索（DeepSeek）开发的中国开源大模型系列，以创新的 MoE 架构、卓越的推理能力和极致的性价比在全球 AI 社区引起广泛关注。

---

## 发展历程

| 版本 | 发布时间 | 参数量 | 关键特性 |
|-----|---------|-------|---------|
| DeepSeek LLM | 2023.11 | 7B/67B | 初始版本，中文优化 |
| DeepSeek-V2 | 2024.05 | 236B (MoE) | MLA 架构，极致成本 |
| DeepSeek-Coder | 2024.06 | 1.3B-33B | 代码专项 SOTA |
| DeepSeek-V2.5 | 2024.09 | 236B (MoE) | 综合能力增强 |
| DeepSeek-R1 | 2025.01 | 671B (MoE) | 推理能力突破 |
| DeepSeek-V3 | 2025.01 | 671B (MoE) | 综合性能比肩 GPT-4o |

---

## 核心架构创新

### MLA（Multi-head Latent Attention）

DeepSeek-V2 引入的 MLA 机制：
- 在注意力计算中引入**潜在向量**，压缩 KV 缓存
- 推理时 KV 缓存减少约 **75%**
- 显著降低推理成本和显存占用

### MoE（Mixture of Experts）

DeepSeek-V2/V3 采用 **稀疏混合专家** 架构：

| 规格 | DeepSeek-V2 | DeepSeek-R1 |
|-----|------------|-------------|
| 总参数量 | 236B | 671B |
| 激活参数量 | 21B | 37B |
| 专家数量 | — | 多专家路由 |
| 推理效率 | 极高 | 高 |

每个 token 仅激活部分专家，达到 **全参数模型的性能，但只有几分之一的计算成本**。

---

## DeepSeek-R1：推理能力突破

### 核心技术

DeepSeek-R1 通过 **强化学习** 实现推理能力突破：

1. **冷启动**：使用少量高质量推理数据进行 SFT
2. **强化学习**：通过 GRPO 算法自我改进推理过程
3. **推理链扩展**：模型学会在复杂问题上"深思熟虑"
4. **自我验证**：生成推理链后自行检查正确性

### 推理对比

| 任务 | DeepSeek-R1 | GPT-4o | Claude 3.5 |
|-----|------------|--------|------------|
| 数学竞赛 (AIME) | 79.8% | 76.9% | — |
| 编程竞赛 (Codeforces) | 96.3 百分位 | 81.4 百分位 | — |
| 科学推理 (GPQA) | 71.5% | 73.3% | — |

---

## 成本优势

DeepSeek 以极低的价格提供顶级性能：

| 模型 | 输入价格（每百万 token） | 输出价格 |
|-----|------------------------|---------|
| GPT-4o | $2.50 | $10.00 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| **DeepSeek-V3** | **$0.27** | **$1.10** |
| DeepSeek-R1 | $0.55 | $2.19 |

DeepSeek-V3 的价格约为 GPT-4o 的 **十分之一**。

---

## 本地部署

### 使用 Ollama

```bash
# 运行 DeepSeek-R1 蒸馏版本
ollama run deepseek-r1:7b   # 7B 蒸馏版
ollama run deepseek-r1:14b  # 14B 蒸馏版
ollama run deepseek-r1:32b  # 32B 蒸馏版
ollama run deepseek-r1:70b  # 70B 蒸馏版
```

### 使用 vLLM 部署

```python
from vllm import LLM, SamplingParams

# 加载 DeepSeek-V3
llm = LLM(model="deepseek-ai/DeepSeek-V3", tensor_parallel_size=4)

params = SamplingParams(temperature=0.7, max_tokens=1024)

outputs = llm.generate(["用 Python 实现一个快速排序算法"], params)
print(outputs[0].outputs[0].text)
```

---

## 优势

- **推理能力顶尖**：R1 在数学和编程竞赛中达到前沿水平
- **极致性价比**：API 价格仅为闭源模型的 5-10%
- **中文优化**：中文理解与生成能力优秀
- **开源透明**：模型权重和技术报告公开
- **MoE 高效**：激活参数少，推理速度快

## 局限

- **硬件门槛高**：完整版 671B 模型需要多卡集群
- **生态成熟度**：社区工具链不如 LLaMA 丰富
- **创意写作**：某些创意任务上略逊于 GPT-4o
- **服务稳定性**：API 偶尔有排队和限流

---

## 应用场景

- **数学与科学推理**：论文辅助、公式推导
- **编程竞赛与开发**：复杂算法实现、代码优化
- **中文内容生成**：文档、报告、翻译
- **企业级应用**：高性价比的 AI 服务部署
- **教育辅导**：解题思路讲解、逻辑推理训练

---

## 下一步

- 访问 [DeepSeek 官网](https://chat.deepseek.com) 体验在线版本
- 获取 API Key 调用 DeepSeek API
- 使用 Ollama 在本地运行蒸馏版本
- 阅读 DeepSeek-R1 技术论文了解推理机制
