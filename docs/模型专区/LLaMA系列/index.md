# LLaMA 生态：开源 LLM 的大爆炸

> 2023 年 2 月，Meta 悄悄发布了一篇论文和一组模型权重。没人想到，这将是开源 AI 领域的"原子弹"。
> 两年后，LLaMA 生态已经统治了整个开源大模型世界。

---

## 时间线：从闭源到开源革命

### LLaMA 1（2023.2）— 泄漏的潘多拉魔盒

Meta 最初只发布权重（7B、13B、33B、65B），需要申请。这本质上是一个"半开源"——你可以在研究中使用，但不能商用。

**然后它泄漏了**。

2023 年 3 月，有人把权重上传到了 BitTorrent。一夜之间，全球的研究者和开发者都能在消费级 GPU 上运行接近 GPT-3 能力的模型。

**争议**：
- Meta 说"不，不是我们泄漏的"
- 开源社区说"太棒了，开源万岁"
- 法律团队说"这个 license 到底是什么意思？"

**历史意义**：LLaMA 1 的泄漏让"在笔记本上运行大模型"从幻想变成了现实。

### LLaMA 2（2023.7）— 正式开源

Meta 这次学聪明了：**Apache 2.0 协议 + 商用许可**。任何人都可以免费使用、修改、商用。

**关键升级**：
- 训练数据增加 40%
- 上下文长度翻倍（4096 tokens）
- RLHF（基于 100 万条人类反馈数据）
- 7B、13B、70B 三个版本

**行业影响**：
- 各大云厂商立即上线 LLaMA 2 服务
- 开源社区的"二次创新"开始爆发
- 诞生了第一代"LLaMA 杀手"（Mistral、Zephyr）

### LLaMA 3 / 3.1（2024）— 追赶 GPT-4

2024 年 4 月发布 LLaMA 3（8B、70B），7 月升级到 LLaMA 3.1 并新增 **405B** 版本。

| 版本 | 参数 | 上下文 | 训练数据 | 基准对比 |
|------|------|--------|---------|---------|
| LLaMA 3 8B | 8B | 8K | 15T tokens | 超过 Mistral 7B |
| LLaMA 3 70B | 70B | 8K | 15T tokens | 接近 GPT-3.5 |
| LLaMA 3.1 8B | 8B | 128K | 15T+ | 同量级最强 |
| LLaMA 3.1 70B | 70B | 128K | 15T+ | 超过 GPT-4（部分基准）|
| LLaMA 3.1 405B | **405B** | 128K | 15T+ | GPT-4 级+ |

> 405B 是当时最大的**开源** dense 模型。训练用了 16K H100 GPU，耗时 54 天。

---

## 生态：LLaMA 的"App Store"

LLaMA 真正的力量不在于模型本身，而在于围绕它的**生态**。

### 微调变体（社区贡献）

| 变体 | 基础模型 | 特点 | 影响力 |
|------|---------|------|--------|
| **Alpaca** | LLaMA 7B | 用 Self-Instruct 生成 52K 指令数据微调 | 第一个流行的 LLaMA 微调 |
| **Vicuna** | LLaMA 13B | 用 ShareGPT 对话微调，质量很高 | 一度是"最好的开源聊天模型" |
| **Llama-3-Chinese** | LLaMA 3 8B | 中文增强 + 增量预训练 | 中文社区首选 |
| **OpenBuddy** | LLaMA 系列 | 多语言会话模型 | 跨语言对话 |
| **WizardCoder** | LLaMA / CodeLLaMA | 代码专项优化 | HumanEval 表现优异 |
| **Hermes** | LLaMA 系列 | 高质量指令微调 | Nous Research 出品 |

### 量化方案

在消费级硬件上运行 LLaMA 的关键：

```
LLaMA 3 8B (FP16) = 16GB VRAM
LLaMA 3 8B (Q4_K_M) = 5.7GB VRAM ← 一张 RTX 3060 就够

LLaMA 3 70B (FP16) = 140GB VRAM
LLaMA 3 70B (Q4_K_M) = 41GB VRAM ← 两台 Mac Studio 或一台 A100
```

**推荐量化工具**：llama.cpp、AutoGPTQ、EXL2。

---

## 本地部署：从零到跑起来

最简单的方式——Ollama（一条命令）：

```bash
# 安装 Ollama（Mac/Linux）
curl -fsSL https://ollama.ai/install.sh | sh

# 运行 LLaMA 3.1
ollama run llama3.1:70b

# 或尝试中文微调版
ollama run shisa-ai/llama3.1-8b-japanese
```

高级部署用 vLLM（生产环境）：

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3.1-70B \
  --tensor-parallel-size 4
```

---

## 选择指南：该用哪个 LLaMA？

```
你的条件                          → 推荐版本
只有一张 RTX 4090（24GB）         → LLaMA 3.1 8B（Q4）+ ollama
有 2× A100（160GB）              → LLaMA 3.1 70B（FP16）
需要中文能力                      → Llama-3-Chinese 8B
需要代码能力                      → CodeLLaMA 34B
有企业级 GPU 集群                 → LLaMA 3.1 405B + vLLM
做研究、微调                      → LLaMA 3.1 8B（开始）+ 70B（最终）
完全不能接受 Meta License          → Mistral / Qwen（Apache 2.0）
```

---

## 争议：LLaMA License 到底能不能商用？

LLaMA 2/3 的协议比 Apache 2.0 多了一条限制：

> **"如果产品或服务的月活用户超过 7 亿，需要 Meta 特别授权。"**

这基本上只针对 Facebook、微信、WhatsApp 这个量级的公司。对于 99.99% 的开发者来说不是问题。

但有些公司（尤其是大公司）的法务团队会对这条持保留态度。如果你们法务卡住了，可以考虑 Qwen（Apache 2.0）或 Mistral（Apache 2.0）。

---

> **LLaMA 的意义**：它不是最强的，也不是最早的。但它做对了一件事——**把 GPT-3 级别的能力交到了每个人手里**。开源社区的集体智慧在此基础上创造了数百个有价值的变体。LLaMA 是开源 AI 运动的"Linux 内核"。
