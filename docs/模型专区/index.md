# 🤖 模型专区

各主流 AI 模型的详细学习指南。

| 模型 | 简介 |
|------|------|
| [GPT 系列](GPT系列/index.md) | OpenAI GPT-4、GPT-4o、API 使用与开发实战 |
| [Claude 系列](Claude系列/index.md) | Anthropic Claude 3.5、Opus、API 与提示工程 |
| [LLaMA 系列](LLaMA系列/index.md) | Meta LLaMA 3 开源模型，部署与微调 |
| [DeepSeek](DeepSeek/index.md) | 深度求索 V3、R1 推理模型、API 使用 |
| [Gemini 系列](Gemini系列/index.md) | Google Gemini Nano 到 Ultra |
| [Qwen 系列](Qwen系列/index.md) | 阿里通义千问 Qwen2.5、VL 视觉模型 |
| [Stable Diffusion](StableDiffusion/index.md) | SDXL、SD3 图像生成，ComfyUI 工作流 |
| [Mixtral 系列](Mixtral系列/index.md) | Mistral AI MoE 模型，Mixtral 8x22B |
| [开源模型部署选型](开源模型部署选型/index.md) | 从能力、成本、显存、许可证和推理引擎角度选择开源模型 |

> 每篇包含：模型概述、能力特点、学习资源、使用方式

## 选型入口

- 商业 API 集成：优先对比 GPT、Claude、Gemini 等闭源模型的能力边界、上下文、工具调用和成本。
- 私有化或本地运行：先读 [开源模型部署选型](开源模型部署选型/index.md)，再进入 LLaMA、Qwen、DeepSeek、Mixtral 等专题。
- 图像生成工作流：阅读 [Stable Diffusion](StableDiffusion/index.md)，并结合 [ComfyUI](/工具专区/ComfyUI/) 实践。

## 对比维度

- 能力：文本、代码、推理、多模态、长上下文、工具调用。
- 成本：输入输出价格、本地显存、吞吐、延迟和缓存策略。
- 部署：API、私有化、本地运行、推理框架和运维复杂度。
- 生态：SDK、文档、社区、示例、评估报告和企业支持。
- 风险：许可证、数据隐私、内容安全、地区可用性和供应商锁定。
