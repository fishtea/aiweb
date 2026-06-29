# Qwen 系列 — 阿里巴巴

> Qwen（通义千问）是由阿里巴巴旗下 Qwen 团队开发的大语言模型系列。Qwen 系列走 Dense（稠密）和 MoE（混合专家）双路线，在中文和多语言任务上表现尤为突出，是开源生态中最重要的中国模型家族。

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
    model="qwen-max-2025-01-25",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "介绍 Qwen2.5 系列的特点。"}
    ]
)

print(completion.choices[0].message.content)
```

### 本地部署 (Hugging Face)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
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
- [Qwen2.5-Max 官方博客](https://qwenlm.github.io/blog/qwen2.5-max)
- [Qwen2.5-VL 发布公告](https://qwen.ai/blog?id=qwen2.5-vl)
- [Qwen2.5 技术报告解读 (Medium)](https://medium.com/@amanatulla1606/qwen2-5-technical-report-47c538fc4569)
- [Qwen2.5-Max 分析 (Medium)](https://medium.com/@amanatulla1606/qwen2-5-technical-report-47c538fc4569)
