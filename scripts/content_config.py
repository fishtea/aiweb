#!/usr/bin/env python3
"""Shared content taxonomy for docs, collection, and index generation."""

CATEGORIES = {
    "初级知识": {
        "desc": "适合零基础入门的 AI 基础知识",
        "subs": {
            "AI学习路线图": {
                "desc": "30 天入门计划、学习顺序、项目选择和检查点",
                "queries": ["AI learning roadmap beginners", "人工智能 学习路线 零基础"],
                "tags": ["路线图", "入门", "学习路径"],
                "level": "beginner",
            },
            "人工智能入门": {
                "desc": "AI 基本概念、发展历史、应用场景",
                "queries": ["AI beginner tutorial 2026", "人工智能入门教程 2026"],
                "tags": ["入门", "AI基础", "教程"],
                "level": "beginner",
            },
            "数学基础": {
                "desc": "线性代数、概率统计、微积分、优化和信息论的最小必要知识",
                "queries": ["math for machine learning beginners", "机器学习 数学基础 入门"],
                "tags": ["数学", "线性代数", "概率", "微积分"],
                "level": "beginner",
            },
            "Python与数据处理基础": {
                "desc": "Python、NumPy、Pandas、可视化和机器学习代码骨架",
                "queries": ["Python data analysis tutorial beginners", "Python 数据处理 Pandas 入门"],
                "tags": ["Python", "Pandas", "NumPy", "数据处理"],
                "level": "beginner",
            },
            "数据与特征工程": {
                "desc": "数据类型、标签、特征工程、数据泄漏和数据质量检查",
                "queries": ["feature engineering machine learning beginner guide", "特征工程 数据清洗 机器学习 入门"],
                "tags": ["特征工程", "数据清洗", "数据质量"],
                "level": "beginner",
            },
            "机器学习基础": {
                "desc": "监督学习、无监督学习、强化学习等基础算法",
                "queries": ["machine learning basics tutorial", "机器学习基础教程"],
                "tags": ["机器学习", "基础", "算法"],
                "level": "beginner",
            },
            "模型训练与评估基础": {
                "desc": "训练集、验证集、测试集、过拟合、评估指标和上线检查",
                "queries": ["machine learning model evaluation metrics beginner", "模型评估 过拟合 训练集 验证集 测试集"],
                "tags": ["评估", "过拟合", "训练", "指标"],
                "level": "beginner",
            },
            "深度学习入门": {
                "desc": "神经网络基础、CNN、RNN、Transformer 入门",
                "queries": ["deep learning tutorial beginners", "深度学习入门教程"],
                "tags": ["深度学习", "神经网络", "入门"],
                "level": "beginner",
            },
            "自然语言处理基础": {
                "desc": "文本分类、信息抽取、token、Embedding 和 NLP 任务全景",
                "queries": ["NLP basics tutorial beginners", "自然语言处理 入门 教程"],
                "tags": ["NLP", "自然语言处理", "文本", "Embedding"],
                "level": "beginner",
            },
            "计算机视觉基础": {
                "desc": "图像分类、检测、分割、OCR、CNN 和视觉评估指标",
                "queries": ["computer vision basics tutorial beginners", "计算机视觉 入门 教程"],
                "tags": ["计算机视觉", "图像", "CNN", "OCR"],
                "level": "beginner",
            },
            "生成式AI基础": {
                "desc": "文本、图像、代码、音视频生成的基本机制、参数和风险",
                "queries": ["generative AI basics beginner guide", "生成式AI 入门 教程"],
                "tags": ["生成式AI", "AIGC", "文本生成", "图像生成"],
                "level": "beginner",
            },
            "大语言模型基础": {
                "desc": "LLM 原理、Prompt 基础、常见模型介绍",
                "queries": ["large language model beginner guide", "大语言模型入门教程"],
                "tags": ["LLM", "大语言模型", "Transformer"],
                "level": "beginner",
            },
            "提示词入门": {
                "desc": "任务、背景、约束、格式、示例和提示词常见误区",
                "queries": ["prompt engineering basics beginners", "提示词 入门 教程"],
                "tags": ["提示词", "Prompt", "入门"],
                "level": "beginner",
            },
            "AI伦理安全与隐私": {
                "desc": "幻觉、偏见、隐私、提示词注入、人在回路和安全检查",
                "queries": ["AI ethics privacy safety beginners", "AI伦理 隐私 安全 入门"],
                "tags": ["伦理", "隐私", "安全", "AI安全"],
                "level": "beginner",
            },
        },
    },
    "进阶学习": {
        "desc": "掌握核心实践技能，提升 AI 应用能力",
        "subs": {
            "提示词工程": {
                "desc": "Prompt 设计技巧、Chain-of-Thought、Few-shot 等",
                "queries": ["prompt engineering guide 2026", "提示词工程 教程 最佳实践"],
                "tags": ["提示词", "Prompt", "工程"],
                "level": "intermediate",
            },
            "Embedding与向量数据库": {
                "desc": "Embedding、向量检索、语义搜索和向量数据库选型",
                "queries": ["embedding vector database tutorial", "向量数据库 Embedding 教程"],
                "tags": ["Embedding", "向量数据库", "语义搜索"],
                "level": "intermediate",
            },
            "RAG检索增强": {
                "desc": "RAG 架构、向量数据库、检索策略、文档分块",
                "queries": ["RAG retrieval augmented generation tutorial", "RAG 架构 教程 2026"],
                "tags": ["RAG", "检索增强", "向量数据库"],
                "level": "intermediate",
            },
            "Agent智能体": {
                "desc": "LLM Agent 框架、工具使用、多 Agent 协作",
                "queries": ["LLM agent tutorial 2026", "多Agent系统 教程"],
                "tags": ["Agent", "智能体", "AI代理"],
                "level": "intermediate",
            },
            "模型微调技术": {
                "desc": "Fine-tuning、LoRA、QLoRA、PEFT 等微调方法",
                "queries": ["LLM fine-tuning tutorial 2026", "大模型微调 LoRA QLoRA 教程"],
                "tags": ["微调", "LoRA", "PEFT", "Fine-tuning"],
                "level": "intermediate",
            },
            "模型评估与基准": {
                "desc": "模型评测方法、Benchmark、评估指标",
                "queries": ["LLM evaluation benchmark 2026", "大模型评测 基准 指标"],
                "tags": ["评测", "基准", "Benchmark"],
                "level": "intermediate",
            },
            "LLM应用架构": {
                "desc": "LLM 应用分层、质量闭环、成本控制和工程边界",
                "queries": ["LLM application architecture patterns", "大模型 应用架构 最佳实践"],
                "tags": ["架构", "LLM应用", "工程"],
                "level": "intermediate",
            },
        },
    },
    "高级知识": {
        "desc": "深入 AI 前沿领域，理解核心技术原理",
        "subs": {
            "模型训练与优化": {
                "desc": "分布式训练、FSDP、量化、蒸馏等技术",
                "queries": ["distributed LLM training guide", "分布式训练 量化 蒸馏 教程"],
                "tags": ["训练", "分布式", "量化", "优化"],
                "level": "advanced",
            },
            "AI安全与对齐": {
                "desc": "红队测试、对抗攻击、RLHF、模型安全",
                "queries": ["AI safety alignment research 2026", "AI安全 对齐 RLHF 教程"],
                "tags": ["安全", "对齐", "RLHF", "红队"],
                "level": "advanced",
            },
            "多模态模型": {
                "desc": "CLIP、BLIP、LLaVA 等多模态模型原理与应用",
                "queries": ["multimodal AI tutorial 2026", "多模态模型 教程 CLIP LLaVA"],
                "tags": ["多模态", "视觉", "CLIP", "LLaVA"],
                "level": "advanced",
            },
            "模型架构研究": {
                "desc": "MoE、Mamba、RWKV 等新型架构探索",
                "queries": ["Mixture of Experts architecture explained", "前沿模型架构 MoE Mamba RWKV"],
                "tags": ["MoE", "Mamba", "架构", "前沿"],
                "level": "advanced",
            },
            "数据工程与合成数据": {
                "desc": "训练数据治理、合成数据、数据质量和数据闭环",
                "queries": ["synthetic data LLM data engineering", "大模型 数据工程 合成数据"],
                "tags": ["数据工程", "合成数据", "数据质量"],
                "level": "advanced",
            },
        },
    },
    "模型专区": {
        "desc": "各主流 AI 模型的详细学习指南与资源汇总",
        "subs": {
            "GPT系列": {
                "desc": "OpenAI GPT 系列模型学习资源",
                "queries": ["OpenAI GPT model guide 2026", "GPT API 教程"],
                "tags": ["GPT", "OpenAI", "ChatGPT"],
                "level": "reference",
            },
            "Claude系列": {
                "desc": "Anthropic Claude 系列模型学习资源",
                "queries": ["Claude tutorial guide 2026", "Anthropic Claude API tutorial"],
                "tags": ["Claude", "Anthropic"],
                "level": "reference",
            },
            "LLaMA系列": {
                "desc": "Meta LLaMA 系列开源模型学习资源",
                "queries": ["LLaMA tutorial guide 2026", "LLaMA 部署 教程 本地运行"],
                "tags": ["LLaMA", "Meta", "开源"],
                "level": "reference",
            },
            "DeepSeek": {
                "desc": "深度求索 DeepSeek 系列模型学习资源",
                "queries": ["DeepSeek model tutorial guide", "DeepSeek API 使用教程"],
                "tags": ["DeepSeek", "深度求索"],
                "level": "reference",
            },
            "Gemini系列": {
                "desc": "Google Gemini 系列多模态模型学习资源",
                "queries": ["Google Gemini tutorial 2026", "Gemini API tutorial Python"],
                "tags": ["Gemini", "Google"],
                "level": "reference",
            },
            "Qwen系列": {
                "desc": "阿里通义千问 Qwen 系列学习资源",
                "queries": ["Qwen model tutorial 2026", "通义千问 Qwen 教程"],
                "tags": ["Qwen", "通义千问", "阿里"],
                "level": "reference",
            },
            "StableDiffusion": {
                "desc": "Stable Diffusion 图像生成模型学习资源",
                "queries": ["Stable Diffusion tutorial 2026", "ComfyUI Stable Diffusion workflow tutorial"],
                "tags": ["Stable Diffusion", "图像生成", "ComfyUI"],
                "level": "reference",
            },
            "Mixtral系列": {
                "desc": "Mistral AI Mixtral 系列模型学习资源",
                "queries": ["Mixtral model guide", "Mistral AI model guide"],
                "tags": ["Mixtral", "Mistral", "MoE"],
                "level": "reference",
            },
            "开源模型部署选型": {
                "desc": "开源模型部署方式、硬件成本、推理框架和选型建议",
                "queries": ["open source LLM deployment guide", "开源大模型 部署 选型"],
                "tags": ["开源模型", "部署", "推理"],
                "level": "reference",
            },
        },
    },
    "工具专区": {
        "desc": "必备 AI 工具的使用指南与学习路径",
        "subs": {
            "LangChain": {
                "desc": "LangChain 框架：链、Agent、RAG 等完整教程",
                "queries": ["LangChain tutorial 2026", "LangChain RAG agent tutorial"],
                "tags": ["LangChain", "框架", "Agent"],
                "level": "tool",
            },
            "LlamaIndex": {
                "desc": "LlamaIndex 数据索引、RAG、Agent 和工作流",
                "queries": ["LlamaIndex tutorial 2026", "LlamaIndex RAG workflow tutorial"],
                "tags": ["LlamaIndex", "RAG", "索引"],
                "level": "tool",
            },
            "AutoGPT": {
                "desc": "AutoGPT 自主 Agent 系统学习资源",
                "queries": ["AutoGPT tutorial 2026", "自主AI Agent 搭建教程"],
                "tags": ["AutoGPT", "自主Agent"],
                "level": "tool",
            },
            "ComfyUI": {
                "desc": "ComfyUI 节点式图像生成工作流",
                "queries": ["ComfyUI tutorial beginner 2026", "ComfyUI 节点 工作流 教程"],
                "tags": ["ComfyUI", "工作流", "图像生成"],
                "level": "tool",
            },
            "vLLM": {
                "desc": "vLLM 高效大模型推理框架",
                "queries": ["vLLM deployment tutorial 2026", "vLLM 模型部署 教程"],
                "tags": ["vLLM", "推理", "部署"],
                "level": "tool",
            },
            "HuggingFace": {
                "desc": "Hugging Face 生态：Transformers、Datasets、Spaces",
                "queries": ["Hugging Face tutorial 2026", "HuggingFace 模型 使用 教程"],
                "tags": ["HuggingFace", "Transformers", "模型库"],
                "level": "tool",
            },
            "PyTorch": {
                "desc": "PyTorch 深度学习框架学习资源",
                "queries": ["PyTorch tutorial 2026", "PyTorch 深度学习 教程"],
                "tags": ["PyTorch", "深度学习框架"],
                "level": "tool",
            },
            "TensorFlow": {
                "desc": "TensorFlow 机器学习框架学习资源",
                "queries": ["TensorFlow tutorial 2026", "TensorFlow Keras tutorial"],
                "tags": ["TensorFlow", "Keras", "ML框架"],
                "level": "tool",
            },
            "Ollama": {
                "desc": "Ollama 本地大模型运行工具",
                "queries": ["Ollama tutorial 2026", "Ollama 本地部署 大模型 教程"],
                "tags": ["Ollama", "本地部署", "LLM"],
                "level": "tool",
            },
            "部署运维": {
                "desc": "AI 应用部署、监控、成本、日志和运维实践",
                "queries": ["LLM application deployment monitoring", "AI 应用 部署 运维 监控"],
                "tags": ["部署", "运维", "监控"],
                "level": "tool",
            },
            "GitHub热门项目": {
                "desc": "热门 AI 开源项目、Star 增长、项目成熟度和实践价值追踪",
                "queries": ["trending AI projects GitHub", "GitHub AI 热门项目 周榜"],
                "tags": ["GitHub", "开源", "热门项目", "AI项目"],
                "level": "tool",
            },
        },
    },
    "AIAgent实践": {
        "desc": "把 Agent 概念落到函数调用、RAG、多 Agent 和评估实践",
        "subs": {
            "函数调用Agent": {
                "desc": "函数调用、工具选择、参数约束和执行闭环",
                "queries": ["function calling agent tutorial", "函数调用 Agent 教程"],
                "tags": ["函数调用", "Agent", "工具调用"],
                "level": "practice",
            },
            "RAGAgent实战": {
                "desc": "把 RAG 检索和 Agent 工具调用结合到知识库问答",
                "queries": ["RAG agent tutorial", "RAG Agent 实战"],
                "tags": ["RAG", "Agent", "知识库"],
                "level": "practice",
            },
            "多Agent协作": {
                "desc": "多 Agent 分工、协作、冲突处理和流程编排",
                "queries": ["multi agent collaboration tutorial", "多Agent 协作 教程"],
                "tags": ["多Agent", "协作", "编排"],
                "level": "practice",
            },
            "Agent评估与可观测性": {
                "desc": "Agent 运行日志、轨迹评估、质量监控和调试方法",
                "queries": ["LLM agent evaluation observability", "Agent 评估 可观测性"],
                "tags": ["Agent", "评估", "可观测性"],
                "level": "practice",
            },
            "PRD方案库": {
                "desc": "实用 AI Agent 产品需求文档、MVP 范围、成功指标和风险边界",
                "queries": ["AI agent product requirements examples", "AI Agent PRD 方案 MVP"],
                "tags": ["PRD", "产品需求", "MVP", "Agent方案"],
                "level": "practice",
            },
            "实际应用案例": {
                "desc": "企业落地案例、行业最佳实践、Agent 方案选型和实施复盘",
                "queries": ["AI agent real world case studies", "AI Agent 企业落地 案例"],
                "tags": ["案例", "落地", "Agent", "企业实践"],
                "level": "practice",
            },
        },
    },
}

CATEGORY_EMOJI = {
    "初级知识": "book",
    "进阶学习": "tools",
    "高级知识": "brain",
    "模型专区": "robot",
    "工具专区": "wrench",
    "AIAgent实践": "robot",
}

TRUSTED_DOMAINS = {
    "openai.com": 5,
    "anthropic.com": 5,
    "ai.google.dev": 5,
    "developers.google.com": 5,
    "huggingface.co": 5,
    "pytorch.org": 5,
    "tensorflow.org": 5,
    "scikit-learn.org": 5,
    "docs.llamaindex.ai": 5,
    "python.langchain.com": 5,
    "docs.vllm.ai": 5,
    "ollama.com": 5,
    "arxiv.org": 4,
    "github.com": 4,
    "deeplearning.ai": 4,
    "coursera.org": 4,
    "microsoft.github.io": 4,
    "ibm.com": 4,
    "cloud.google.com": 4,
    "aws.amazon.com": 4,
}

BLOCKED_DOMAINS = {
    "pinterest.com",
    "facebook.com",
    "instagram.com",
    "tiktok.com",
}

RESOURCE_LIMIT_PER_TOPIC = 4
