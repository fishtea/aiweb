# 模型选购指南：你要做 X 任务，该选哪个模型？

> 这不是技术评测，是给你的购物清单。2025 年的大模型市场比超市货架还挤，每家都宣称自己"最强"。别信广告，看需求。

---

## 快速决策表

| 你的任务 | 首选模型 | 备选方案 | 上下文 | 开源？ | 成本 |
|----------|----------|----------|--------|--------|------|
| 日常聊天、写作辅助 | **GPT-4o** | Claude 3.5 Sonnet | 128K | ❌ | 中等 |
| 长文档分析、合同审查 | **Claude 3 Opus** | Gemini 1.5 Pro | 200K | ❌ | 高 |
| 代码生成、Debug | **Claude 3.5 Sonnet** | GPT-4o / DeepSeek Coder | 200K | ❌/✅ | 中低 |
| 数学推理、逻辑题 | **DeepSeek R1** | GPT o1 / o3 | 128K | ✅ (MIT) | 极低 |
| 中文任务、本地部署 | **Qwen 2.5 (72B)** | DeepSeek V3 | 128K | ✅ (Apache 2.0) | 极低 |
| 自己跑开源模型 | **LLaMA 3 (70B)** | Mistral 8x22B | 128K | ✅ (自定义) | 按硬件 |
| 图像生成 | **FLUX.1** | SD3.5 / Midjourney | - | ✅ (部分) | 低-中 |
| 多模态（图+文+音） | **Gemini 2.0 Flash** | GPT-4o | 1M | ❌ | 低 |
| 低成本推理 API | **DeepSeek V3** | Gemini 2.0 Flash | 128K | ✅ | **极低** |
| Agent / 工具调用 | **Claude 3.5 Sonnet** | GPT-4o | 200K | ❌ | 中 |
| 翻译、改写 | **GPT-4o mini** | Qwen 2.5 (7B) | 128K | ❌/✅ | 极低 |
| 科研论文阅读 | **Claude 3 Opus** | Gemini 1.5 Pro | 200K / 1M | ❌ | 高 |

---

## 按场景深度分析

### 🗣️ 日常对话与创意写作

**推荐：GPT-4o > Claude Sonnet > Gemini Flash**

GPT-4o 在对话流畅度、语气把控和创意发散上仍然是标杆。Claude Sonnet 写作更有"文学感"，但有时候过于规矩。Gemini Flash 速度快但深度略逊。

**成本建议**：日常用 GPT-4o mini 或 Gemini Flash 就够，省钱且快。

### 💻 编程与软件开发

**推荐：Claude 3.5 Sonnet > DeepSeek Coder V2 > GPT-4o**

Claude 在生成完整代码文件、重构和调试上表现突出。DeepSeek Coder 性价比极高——API 价格只有 GPT-4 的 1/20。GPT-4o 在理解和修改已有代码库方面不错。

**开源方案**：DeepSeek Coder V2 (236B MoE) 本地部署需要 2× A100，但 API 调用极便宜。

### 📄 长文档处理

**推荐：Gemini 1.5 Pro (1M) > Claude 3 Opus (200K) > GPT-4o (128K)**

Gemini 1.5 Pro 的 100 万 token 上下文是目前无敌的——一次塞进整套《三体》三部曲不是问题。Claude 200K 也够用，而且检索更精准。

**注意**：长上下文 ≠ 长上下文利用能力。大多数模型在超过 64K 后注意力会稀释。

### 🧮 数学推理

**推荐：DeepSeek R1 > GPT o1 > Gemini 2.0**

DeepSeek R1 是开源推理模型之首。o1 的"思考链"也很强但极其缓慢且贵。R1 在 MATH 基准上接近 o1，价格只有 1/30。

### 🌏 中文任务

**推荐：Qwen 2.5 (72B) > DeepSeek V3 > GPT-4o**

Qwen 对中文理解深度（成语、古诗、梗）远超所有西方模型。DeepSeek V3 在技术文档翻译上也很强。

---

## 一句话总结

```
要做 → 聊天     → 闭源选 GPT-4o，开源选 Qwen 72B
要做 → 代码     → 闭源选 Claude，开源选 DeepSeek Coder
要做 → 长文     → Gemini 1.5 Pro
要做 → 推理     → DeepSeek R1
要做 → 省钱     → DeepSeek V3 API
要做 → 画图     → FLUX + ComfyUI
要做 → 省心     → 随便选，现在模型都够强
```

> **最终建议**：别绑定一家。搭建一个"模型路由"方案——简单任务走便宜模型，复杂任务走旗舰模型。聪明人用工具，聪明团队用组合。
