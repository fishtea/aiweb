# 模型专区

各主流 AI 模型的学习指南与选型入口。以下内容按公开资料更新至 **2026-07-06**；模型厂商更新很快，生产选型前仍应再查一次官方模型列表和价格页。

| 模型 | 简介 |
|------|------|
| [GPT 系列](GPT系列/index.md) | OpenAI GPT-5.6、GPT-5.5、o3 / o4-mini 与 2026 API 选型 |
| [Claude 系列](Claude系列/index.md) | Anthropic Claude Fable 5、Sonnet 5、Opus 4.8、Haiku 4.5 与 2026 Agent 能力 |
| [LLaMA 系列](LLaMA系列/index.md) | Meta Llama 3 / 3.1 / 3.3 / 4，开源部署、许可与微调 |
| [DeepSeek](DeepSeek/index.md) | DeepSeek-V3、R1、DeepSeek-OCR 与官方仓库最新可用模型 |
| [Gemini 系列](Gemini系列/index.md) | Google Gemini 3 Pro、Gemini 2.5、Gemini Embedding 与图像模型 |
| [Qwen 系列](Qwen系列/index.md) | Qwen2.5、Qwen3、Qwen3-Coder、Qwen-VL / Omni 等开源模型 |
| [Stable Diffusion](StableDiffusion/index.md) | SD3.5、Stable Image、FLUX.2 与 ComfyUI 工作流 |
| [Mixtral 系列](Mixtral系列/index.md) | Mistral Large、Medium 3.1、Devstral、Magistral 与 Mixtral |
| [开源模型部署选型](开源模型部署选型/index.md) | 从能力、成本、显存、许可证和推理引擎角度选择开源模型 |

> 每篇包含：模型概述、能力特点、学习资源、使用方式

## 选型入口

- 商业 API 集成：优先对比 GPT-5.6 / GPT-5.5、Claude Fable 5 / Sonnet 5 / Opus 4.8、Gemini 3 Pro、Mistral Medium 3.1 / Large 等模型的上下文、工具调用、价格和区域可用性。
- 私有化或本地运行：先读 [开源模型部署选型](开源模型部署选型/index.md)，再进入 Llama、Qwen、DeepSeek、Mistral / Mixtral 等专题。
- 中文、代码和推理：重点评估 Qwen3、DeepSeek-R1 / V3、Llama 4、Mistral Medium / Magistral，并用自己的业务数据复测。
- 图像生成工作流：阅读 [Stable Diffusion](StableDiffusion/index.md)，并结合 [ComfyUI](/工具专区/ComfyUI/) 实践。

## 2026 快速对比

| 使用目标 | 优先候选 | 说明 |
|---------|----------|------|
| 通用对话与多模态 API | GPT-5.5、Claude Sonnet 5、Gemini 3 Pro / 2.5 Flash | 闭源模型生态成熟，适合快速上线 |
| 深度推理与数学代码 | GPT-5.6、Claude Fable 5 / Opus 4.8、DeepSeek-R1、Qwen3 | 关注延迟、推理 token 成本和可解释性 |
| 长上下文与文档分析 | Gemini 3 Pro、Claude 200K、Llama 4 Scout | 长上下文仍需评估中段召回和成本 |
| 本地中文与私有化 | Qwen3、DeepSeek、Llama 3.1 / 4 | 优先看许可证、量化质量和推理框架支持 |
| 图像生成与可控工作流 | SDXL、SD3.5、FLUX.2、ControlNet / IPAdapter | ComfyUI 生态仍是本地创作主力 |

## 对比维度

- 能力：文本、代码、推理、多模态、长上下文、工具调用。
- 成本：输入输出价格、本地显存、吞吐、延迟和缓存策略。
- 部署：API、私有化、本地运行、推理框架和运维复杂度。
- 生态：SDK、文档、社区、示例、评估报告和企业支持。
- 风险：许可证、数据隐私、内容安全、地区可用性和供应商锁定。
