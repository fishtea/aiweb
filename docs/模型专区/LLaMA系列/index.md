# LLaMA 系列 — Meta

> Llama（Large Language Model Meta AI）是 Meta 开发的开放权重大语言模型系列。按 2026-07-06 可核验的 Meta 官方发布页，最新主线仍是 Llama 4；生产选型应重点评估 Llama 4 Scout / Maverick、Llama 3.3 70B 和 Llama 3.1 405B。

---

## 模型演进

| 模型 | 发布时间 | 参数规模 | 训练数据 | 上下文窗口 |
|------|---------|---------|---------|-----------|
| LLaMA 1 | 2023.02 | 7B/13B/33B/65B | 1.0-1.4T tokens | 2K |
| LLaMA 2 | 2023.07 | 7B/13B/70B | 2T tokens | 4K |
| LLaMA 3 | 2024.04 | 8B/70B | 15T tokens | 8K |
| LLaMA 3.1 | 2024.07 | 8B/70B/405B | 15T+ tokens | 128K |
| Llama 3.3 | 2024.12 | 70B | 15T+ tokens | 128K |
| Llama 4 | 2025.04 | Scout / Maverick / Behemoth(预览) | 未完全公开 | 10M(Scout)/1M(Maverick) |

### LLaMA 4 — 原生多模态 MoE

Llama 4（2025.04）是 Meta 首次大规模转向 MoE + 多模态的一代：

| 模型 | 架构 | 激活参数 | 上下文 | 定位 |
|------|------|---------|--------|------|
| Llama 4 Scout | MoE，17B 激活 | 17B | **10M** | 超长上下文，适合文档和代码库分析 |
| Llama 4 Maverick | MoE，17B 激活 | 17B | 1M | 通用多模态旗舰，质量高于 Scout |
| Llama 4 Behemoth | 更大 MoE，训练中/预览 | — | — | 作为教师模型和未来旗舰方向 |

- **原生多模态**：早期融合文本与视觉 token，无需单独视觉适配器。
- **iRoPE 架构**：交替注意力机制支持超长上下文外推，Scout 达 10M token。
- **训练数据 22T+ tokens**，多语言覆盖更广，中文能力较 LLaMA 3 显著提升。
- **开放权重许可延续**，但超大规模商业应用仍需遵守 Meta 的许可限制。

> 局限：LLaMA 4 发布初期基准表现引发争议（Meta 承认评测版本配置问题），实际能力以官方更新为准。中文场景建议优先对比 Qwen3、DeepSeek。

### 2026 最新可用列表

| 场景 | 推荐 |
|------|------|
| 超长上下文、整库代码和海量文档 | Llama 4 Scout |
| 通用多模态、质量优先 | Llama 4 Maverick |
| 开放权重旗舰基线、蒸馏和评估 | Llama 3.1 405B |
| 成本可控的生产文本模型 | Llama 3.3 70B |
| 消费级 GPU 本地实验 | Llama 3.1 8B / 70B 量化版 |

> 截至 2026-07-06，未找到 Meta 官方发布的 Llama 5 或 Llama 4.5。文档按可核验的 Llama 4 与 Llama 3.x 更新。

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

## Llama 3.1 / 3.3 — 仍然重要的生产基线

根据 Meta Llama 3.1 官方发布与技术报告：

- Llama 3.1 提供 8B / 70B / 405B 三档，均支持 **128K tokens** 上下文。
- 405B 是重要的开放权重旗舰模型，可作为蒸馏、评估和企业私有化基线。
- Llama 3.3 70B 在更小部署成本下接近 405B 的部分能力，适合作为生产默认候选。
- 与 GPT-4 和 Claude 3.5 Sonnet 在多项基准上竞争
- Llama 3.1 / 3.3 仍是 Dense 模型路线，生态、量化和微调资料最成熟。

---

## 指令微调

根据 Meta Llama 3 技术报告：

- 组合使用 **SFT + 拒绝采样 + PPO + DPO**
- 提示质量和偏好排序至关重要
- PPO/DPO 显著提升了推理和编码能力
- 70B Instruct 在人类偏好排名中超越了 Claude Sonnet、Mistral Medium 和 GPT-3.5

---

## 如何使用

### 通过 Hugging Face

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-4-Scout-17B-16E-Instruct")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-4-Scout-17B-16E-Instruct")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "介绍 Llama 4 Scout 的主要特性。"}
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
- [Meta Llama 4 官方发布博客](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)
- [The Llama 3 Herd of Models (arXiv:2407.21783)](https://arxiv.org/abs/2407.21783)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-05 05:14:27*
