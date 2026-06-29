#!/usr/bin/env python3
"""创建所有分类索引页"""
import os

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

categories = {
    "初级知识": {
        "emoji": "book",
        "desc": "适合零基础入门的AI基础知识",
        "subs": {
            "人工智能入门": "AI基本概念、发展历史、应用场景",
            "机器学习基础": "监督学习、无监督学习、强化学习等基础算法",
            "深度学习入门": "神经网络基础、CNN、RNN、Transformer入门",
            "大语言模型基础": "LLM原理、Prompt基础、常见模型介绍",
        }
    },
    "进阶学习": {
        "emoji": "tools",
        "desc": "掌握核心实践技能，提升AI应用能力",
        "subs": {
            "模型微调技术": "Fine-tuning、LoRA、QLoRA、PEFT等微调方法",
            "RAG检索增强": "RAG架构、向量数据库、检索策略、文档分块",
            "Agent智能体": "LLM Agent框架、工具使用、多Agent协作",
            "提示词工程": "Prompt设计技巧、Chain-of-Thought、Few-shot等",
            "模型评估与基准": "模型评测方法、Benchmark、评估指标",
        }
    },
    "高级知识": {
        "emoji": "brain",
        "desc": "深入AI前沿领域，理解核心技术原理",
        "subs": {
            "模型训练与优化": "分布式训练、FSDP、量化、蒸馏等技术",
            "AI安全与对齐": "红队测试、对抗攻击、RLHF、模型安全",
            "多模态模型": "CLIP、BLIP、LLaVA等多模态模型原理与应用",
            "模型架构研究": "MoE、Mamba、RWKV等新型架构探索",
        }
    },
    "模型专区": {
        "emoji": "robot",
        "desc": "各主流AI模型的详细学习指南与资源汇总",
        "subs": {
            "GPT系列": "OpenAI GPT系列模型学习资源",
            "Claude系列": "Anthropic Claude系列模型学习资源",
            "LLaMA系列": "Meta LLaMA系列开源模型学习资源",
            "DeepSeek": "深度求索DeepSeek系列模型学习资源",
            "Gemini系列": "Google Gemini系列多模态模型学习资源",
            "Qwen系列": "阿里通义千问Qwen系列学习资源",
            "StableDiffusion": "Stable Diffusion图像生成模型学习资源",
            "Mixtral系列": "Mistral AI Mixtral系列模型学习资源",
        }
    },
    "工具专区": {
        "emoji": "wrench",
        "desc": "必备AI工具的使用指南与学习路径",
        "subs": {
            "LangChain": "LangChain框架：链、Agent、RAG等完整教程",
            "AutoGPT": "AutoGPT自主Agent系统学习资源",
            "ComfyUI": "ComfyUI节点式图像生成工作流",
            "vLLM": "vLLM高效大模型推理框架",
            "HuggingFace": "HuggingFace生态：Transformers、Datasets、Spaces",
            "PyTorch": "PyTorch深度学习框架学习资源",
            "TensorFlow": "TensorFlow机器学习框架学习资源",
            "Ollama": "Ollama本地大模型运行工具",
        }
    }
}

emoji_map = {
    "book": "U+1F4DA",
    "tools": "U+1F527",
    "brain": "U+1F9E0",
    "robot": "U+1F916",
    "wrench": "U+1F527",
}

for cat, info in categories.items():
    lines = []
    lines.append(f"# {cat}")
    lines.append("")
    lines.append(f"> {info['desc']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 子分类")
    lines.append("")
    for sub_name, sub_desc in info["subs"].items():
        lines.append(f"- **[{sub_name}]({sub_name}/)** — {sub_desc}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*该分类下的资源每日自动更新中...*")
    lines.append("")
    
    with open(os.path.join(BASE, cat, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    for sub_name, sub_desc in info["subs"].items():
        sub_lines = []
        sub_lines.append(f"# {sub_name}")
        sub_lines.append("")
        sub_lines.append(f"> {sub_desc}")
        sub_lines.append("")
        sub_lines.append("---")
        sub_lines.append("")
        sub_lines.append("## 资源列表")
        sub_lines.append("")
        sub_lines.append('<!-- RESOURCES_START -->')
        sub_lines.append("")
        sub_lines.append("*资源采集进行中，每日更新...*")
        sub_lines.append("")
        sub_lines.append('<!-- RESOURCES_END -->')
        sub_lines.append("")
        sub_lines.append("---")
        sub_lines.append("")
        sub_lines.append("*最后更新：待首次采集*")
        sub_lines.append("")
        
        with open(os.path.join(BASE, cat, sub_name, "index.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(sub_lines))

print("Done!")
print(f"Categories: {len(categories)}")
print(f"Sub-categories: {sum(len(v['subs']) for v in categories.values())}")
