# LLaMA 系列 — Meta

> LLaMA（Large Language Model Meta AI）是 Meta 开发的开源大语言模型系列。作为开源生态中最具影响力的模型家族，LLaMA 系列推动了 AI 民主化，让全球开发者可以在自有硬件上部署顶级模型。

---

## 模型演进

| 模型 | 发布时间 | 参数规模 | 训练数据 | 上下文窗口 |
|------|---------|---------|---------|-----------|
| LLaMA 1 | 2023.02 | 7B/13B/33B/65B | 1.0-1.4T tokens | 2K |
| LLaMA 2 | 2023.07 | 7B/13B/70B | 2T tokens | 4K |
| LLaMA 3 | 2024.04 | 8B/70B | 15T tokens | 8K |
| LLaMA 3.1 | 2024.07 | 8B/70B/405B | 15T+ tokens | 128K |
| LLaMA 4 | 2025.04 | Scout/Maverick/Heron | 22T+ tokens | 10M(Scout)/1M |

### LLaMA 4 — 原生多模态 MoE

LLaMA 4（2025.04）是 Meta 首次大规模转向 MoE + 多模态的一代：

| 模型 | 架构 | 激活参数 | 上下文 | 定位 |
|------|------|---------|--------|------|
| LLaMA 4 Scout | MoE，17B 激活 | 17B | **10M** | 超长上下文，单 H100 可运行 |
| LLaMA 4 Maverick | MoE，17B 激活 | 17B | 1M | 旗舰级，对标 GPT-4o/Claude |
| LLaMA 4 Heron | 更大 MoE | — | — | 顶级推理 |

- **原生多模态**：早期融合文本与视觉 token，无需单独视觉适配器。
- **iRoPE 架构**：交替注意力机制支持超长上下文外推，Scout 达 10M token。
- **训练数据 22T+ tokens**，多语言覆盖更广，中文能力较 LLaMA 3 显著提升。
- **开源许可延续**，但超大规模应用仍需 Meta 授权。

> 局限：LLaMA 4 发布初期基准表现引发争议（Meta 承认评测版本配置问题），实际能力以官方更新为准。中文场景建议优先对比 Qwen3、DeepSeek。

---

## LLaMA 3 架构详解

根据 Meta 官方博客 [Introducing Meta Llama 3](https://ai.meta.com/blog/meta-llama-3/) 和技术报告 [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783)：

### 核心架构

- **Decoder-only Transformer** — 标准架构但做了多项优化
- **Tokenizer:** 128K tokens 词汇量（LLaMA 2 为 32K），编码效率提升 15%
- **Grouped Query Attention (GQA):** 8B 和 70B 均使用，提升推理效率
- **训练序列长度:** 8,192 tokens，带文档边界掩码

### 训练数据

- **15T tokens**（LLaMA 2 的 7 倍，代码数据增加 4 倍）
- 超过 **5% 高质量非英语数据**，覆盖 30+ 语言
- 使用 LLaMA 2 生成训练数据用于文本质量分类器
- 数据过滤管道：启发式过滤、NSFW 过滤、语义去重

### 训练基础设施

- **16K GPU**（两个定制 24K GPU 集群）
- 单 GPU 计算利用率 > **400 TFLOPS**
- 集群运行时间 > **95%**
- 整体训练效率约为 LLaMA 2 的 **3 倍**

---

## LLaMA 3.1 405B — 最大的开源模型

根据 [Wikipedia LLaMA 词条](https://en.wikipedia.org/wiki/Llama_(language_model))：

- 405B 参数是目前最大的开源大语言模型
- 上下文窗口扩展到 **128K tokens**
- 与 GPT-4 和 Claude 3.5 Sonnet 在多项基准上竞争
- 采用 MoE（Mixture of Experts）风格的训练策略

---

## 指令微调

根据 [DebuggerCafe LLaMA 3 技术分析](https://debuggercafe.com/meta-llama-3-an-overview)：

- 组合使用 **SFT + 拒绝采样 + PPO + DPO**
- 提示质量和偏好排序至关重要
- PPO/DPO 显著提升了推理和编码能力
- 70B Instruct 在人类偏好排名中超越了 Claude Sonnet、Mistral Medium 和 GPT-3.5

---

## 如何使用

### 通过 Hugging Face

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "介绍 LLaMA 3 的主要特性。"}
]

input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt")
output = model.generate(input_ids, max_new_tokens=512)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

### 通过 Ollama 本地运行

```bash
ollama run llama3.1:8b
# 或
ollama run llama3.1:70b
# 或更大的 405B
ollama run llama3.1:405b
```

---

## 优势与局限

**优势:**
- **开源权重:** 可自由下载、部署、微调
- **强大生态:** Meta、Hugging Face、企业广泛支持
- **极致性价比:** 8B 可在消费级 GPU 运行，405B 接近闭源旗舰水平
- **丰富的工具链:** torchtune、Llama Recipes、Llama Guard 安全工具

**局限:**
- 中文能力不如英文（非英语数据仅 5%+）
- 大型模型（70B/405B）对硬件要求高
- 许可协议禁止某些商业用途（月活 >7 亿需 Meta 授权）
- 405B 推理延迟较高

---

**参考资料：**
- [Meta Llama 3 官方发布博客](https://ai.meta.com/blog/meta-llama-3/)
- [Wikipedia — Llama (language model)](https://en.wikipedia.org/wiki/Llama_(language_model))
- [DebuggerCafe — Meta Llama 3 Overview](https://debuggercafe.com/meta-llama-3-an-overview)
- [The Llama 3 Herd of Models (arXiv:2407.21783)](https://arxiv.org/abs/2407.21783)
- [Towards Data Science — Deep Dive into LLaMA 3](https://towardsdatascience.com/deep-dive-into-llama-3-by-hand-%EF%B8%8F-6c6b23dc92b2)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-03 00:15:41*
