# 进阶学习

> 本页面整理了机器学习工程师进阶所需的核心知识与技能路线，涵盖 MLOps、生产化部署、模型微调、RAG、Agent 等前沿方向。

---

## 🎯 学习路线概览

从基础到进阶的典型成长路径：

1. **机器学习工程基础** — 数据预处理、模型开发、评估
2. **深度学习与 NLP** — Transformer、预训练模型、Prompt Engineering
3. **模型微调技术** — LoRA、QLoRA、PEFT 参数高效微调
4. **检索增强生成 (RAG)** — 向量数据库、检索管道、混合搜索
5. **AI Agent 智能体** — ReAct 模式、LangChain/LangGraph、工具调用
6. **MLOps 与生产化** — CI/CD、模型监控、A/B 测试
7. **模型评估与基准** — MMLU、HumanEval、lm-eval-harness

---

## 📚 推荐资源

### 1. MLOps 完整学习路线

**来源：** [Coursera MLOps Learning Roadmap (2026)](https://www.coursera.org/resources/mlops-learning-roadmap)

- MLOps 将 DevOps 理念（自动化、CI/CD、基础设施即代码、监控）扩展到 ML 特有的需求：数据依赖、实验追踪、模型漂移和重训练
- 推荐学习路径：Python 基础 → ML 基础 → MLOps 工具链 → 云平台实践
- 关键技能：自动化流水线、可复现性、模型治理

### 2. 全栈机器学习工程师路线图

**来源：** [Advanced Machine Learning Engineer Roadmap 2024 - GitHub](https://github.com/farukalamai/advanced-machine-learning-engineer-roadmap-2024)

- 涵盖数据收集与预处理、模型开发、部署和维护的全流程技能
- 重点工具：NumPy/Pandas（数据处理）、Matplotlib/Seaborn（可视化）、Scikit-learn/TensorFlow/PyTorch（建模）
- 进阶方向：MLOps、深度学习、NLP、计算机视觉

### 3. Chip Huyen 的 MLOps 指南

**来源：** [MLOps Guide - Huyenchip.com](https://huyenchip.com/mlops)

- 从入门到高级的系统化材料集合
- 强调 ML + 工程基础的重要性，包括强化学习、NLP 基础
- 生产化 ML 的挑战和对策
- 2025 年更新：正在开发 ML/AI 工程最小可行课程

### 4. 进阶 MLOps 路线图 (2024)

**来源：** [MLOps Roadmap 2024 - Maria Vechtomova](https://www.marvelousmlops.io/p/mlops-roadmap-2024)

- 构建 MLOps 平台所需的多元化技能
- 包括：容器化（Docker）、编排（Kubernetes）、特征存储、模型注册中心
- 强调实验追踪（MLflow）、数据版本控制（DVC）、监控（Prometheus/Grafana）

---

## 🛠️ 进阶技能树

```
├── 数据处理
│   ├── 大规模数据管道 (Spark, Ray)
│   ├── 特征工程与特征存储 (Feast)
│   └── 数据版本控制 (DVC, LakeFS)
├── 模型开发
│   ├── 参数高效微调 (LoRA, QLoRA, Adapter)
│   ├── 检索增强生成 (RAG)
│   ├── AI Agent 框架 (LangChain, LangGraph, CrewAI)
│   └── 提示词工程 (CoT, Few-shot, ReAct)
├── 生产化部署
│   ├── 模型服务 (vLLM, TGI, Triton)
│   ├── 容器化与编排 (Docker, K8s)
│   └── CI/CD for ML (GitHub Actions, ArgoCD)
├── 监控与运维
│   ├── 模型监控 (MLflow, Prometheus)
│   ├── 漂移检测 (Evidently, WhyLabs)
│   └── A/B 测试与实验管理
└── 评估与基准
    ├── LM Evaluation Harness
    ├── MMLU/MMLU-Pro
    ├── HumanEval/GSM8K
    └── 自定义评估管道
```

---

## 📖 本目录内容

| 子页面 | 描述 |
|--------|------|
| [模型微调技术](/进阶学习/模型微调技术/) | LoRA、QLoRA、PEFT 及 Hugging Face TRL 实战 |
| [RAG 检索增强](/进阶学习/RAG检索增强/) | 检索增强生成架构、向量搜索、重排序 |
| [Agent 智能体](/进阶学习/Agent智能体/) | ReAct 模式、LangChain/LangGraph Agent 开发 |
| [提示词工程](/进阶学习/提示词工程/) | 零样本/少样本、思维链、自一致性等技术 |
| [模型评估与基准](/进阶学习/模型评估与基准/) | MMLU、LM Evaluation Harness、评估方法论 |

---

## 🔗 参考资料

- [Coursera MLOps Learning Roadmap](https://www.coursera.org/resources/mlops-learning-roadmap)
- [Advanced Machine Learning Engineer Roadmap](https://github.com/farukalamai/advanced-machine-learning-engineer-roadmap-2024)
- [MLOps Guide - Huyenchip.com](https://huyenchip.com/mlops)
- [MLOps Roadmap 2024](https://www.marvelousmlops.io/p/mlops-roadmap-2024)
