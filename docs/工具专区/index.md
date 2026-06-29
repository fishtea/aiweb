# 🛠️ 工具专区

必备 AI 工具与框架的学习资源。

| 工具 | 简介 |
|------|------|
| [LangChain](LangChain/index.md) | LLM 应用开发框架，链式调用、Agent、RAG |
| [AutoGPT](AutoGPT/index.md) | 自主 AI Agent 框架，任务分解与工具使用 |
| [ComfyUI](ComfyUI/index.md) | 节点式 AI 图像生成工作流 |
| [vLLM](vLLM/index.md) | 高性能 LLM 推理引擎，PagedAttention |
| [Hugging Face](HuggingFace/index.md) | AI 模型与数据集平台，Transformers 库 |
| [LlamaIndex](LlamaIndex/index.md) | LLM 数据接入、索引、检索和查询引擎框架 |
| [PyTorch](PyTorch/index.md) | 深度学习框架，张量操作与分布式训练 |
| [TensorFlow](TensorFlow/index.md) | Google 深度学习框架，Keras API |
| [Ollama](Ollama/index.md) | 本地 LLM 运行工具，模型管理与 API 服务 |
| [部署运维](部署运维/index.md) | AI 应用上线后的监控、日志、降级、安全和质量闭环 |

> 每篇包含：工具简介、核心功能、入门教程、进阶用法

## 工具选择建议

- LLM 应用编排：先看 LangChain，再根据 RAG 数据层需求补充 LlamaIndex。
- 本地模型运行：先看 Ollama，生产推理再看 vLLM 和部署运维。
- 图像生成：以 ComfyUI 为工作流入口，结合 Stable Diffusion 模型专题。
- 训练和微调：按 PyTorch、Hugging Face、TensorFlow 的生态支持选择。
