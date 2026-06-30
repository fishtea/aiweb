# 模型评估与基准

> 模型评估是 LLM 开发流程中至关重要的一环。标准化的评估基准和工具可以客观比较不同模型的能力，并追踪训练进展。

---

## 1. 为什么需要标准化评估？

**来源：** [EleutherAI - Evaluating LLMs](https://www.eleuther.ai/projects/large-language-model-evaluation)

LLM 的性能往往受小实现细节影响，不同代码库之间的结果难以直接比较。为了解决这一问题，EleutherAI 推出了 **LM Evaluation Harness**——一个统一的评估框架。

> *"The LM Evaluation Harness provides a ground-truth location to evaluate new LLMs and saves practitioners time implementing few-shot evaluations repeatedly while ensuring that their results can be compared against previous work."*

**核心优势：**
- 同一提示词、评分和报告标准
- YAML 配置 + commit hash 完全可复现
- 支持 HuggingFace、vLLM、GGUF、OpenAI 兼容 API
- 已被 NVIDIA、Cohere、Nous Research 及 Open LLM Leaderboard 采用

---

## 2. 核心 Benchmark

**来源：** [LLM Eval Harness: Benchmark Any Model on 200+ Tasks (2026 Guide)](https://www.morphllm.com/llm-eval-harness)

| Benchmark | 测试内容 | 格式 | 典型用途 |
|-----------|---------|------|----------|
| **MMLU** | 57 个学科通用知识 | 4 选 1 选择题 | 通用能力评估 |
| **MMLU-Pro** | 更难的 MMLU（10 选项 + 推理） | 10 选 1 | Open LLM Leaderboard v2 |
| **HellaSwag** | 常识推理 | 4 选 1 补全 | 语言理解基线 |
| **ARC-Challenge** | 小学科学题（困难版） | 4 选 1 | 推理能力 |
| **GSM8K** | 小学数学应用题 | 生成式 | 数学推理 |
| **GPQA** | 博士级科学问题 | 4 选 1 | 专家知识 |
| **TruthfulQA** | 常见误解 | MC + 生成 | 事实准确性 |
| **BBH** | 23 个 BIG-Bench 困难任务 | 混合 | 挑战性推理 |
| **IFEval** | 指令跟随 | 生成式 + 评分 | 指令遵从度 |
| **HumanEval** | 代码生成 | 生成式 | 编程能力 |

---

## 3. LM Evaluation Harness 使用指南

### 3.1 安装

```bash
# 基础安装（仅 API 评估）
pip install lm-eval

# 含 HuggingFace 支持
pip install "lm-eval[hf]"

# 含 vLLM 支持
pip install "lm-eval[vllm]"

# 完整安装
pip install "lm-eval[all]"
```

### 3.2 运行基准测试

**评估 GPT-2 的 HellaSwag：**
```bash
lm-eval \
  --model hf \
  --model_args pretrained=gpt2,dtype=float32 \
  --tasks hellaswag \
  --output_path results/gpt2/
```

**评估 Llama 3.1 8B 的多项能力：**
```bash
lm-eval \
  --model hf \
  --model_args pretrained=meta-llama/Meta-Llama-3.1-8B-Instruct,dtype=bfloat16 \
  --tasks mmlu,hellaswag,arc_challenge,gsm8k \
  --num_fewshot 5 \
  --batch_size auto \
  --output_path results/llama-3.1-8b/
```

### 3.3 使用 vLLM 后端（更快）

```bash
lm-eval \
  --model vllm \
  --model_args pretrained=meta-llama/Meta-Llama-3.1-8B-Instruct,dtype=auto,gpu_memory_utilization=0.8 \
  --tasks mmlu,hellaswag,gsm8k \
  --num_fewshot 5
```

### 3.4 通过 OpenAI 兼容 API 评估

```bash
lm-eval \
  --model local-chat-completions \
  --model_args model=meta-llama/Meta-Llama-3.1-8B-Instruct,base_url=http://localhost:8000/v1/chat/completions,num_concurrent=32 \
  --tasks gsm8k,ifeval \
  --apply_chat_template
```

---

## 4. 评估方法论

### 4.1 评分方式

| 方式 | 说明 | 适用任务 |
|------|------|----------|
| **Loglikelihood** | 基于 token 概率评分 | MMLU、HellaSwag（需模型输出 logprobs） |
| **Generative** | 模型生成文本，提取答案评分 | GSM8K、HumanEval、IFEval |

### 4.2 结果解读

```json
{
  "results": {
    "hellaswag": {
      "acc": 0.6153,
      "acc_stderr": 0.0049
    },
    "mmlu": {
      "acc": 0.6874,
      "acc_stderr": 0.0031
    }
  }
}
```

- `acc`：准确率
- `acc_stderr`：标准差（评估不确定性）
- `--log_samples`：保存每个输入/输出到 JSONL，便于调试

---

## 5. MMLU-Pro：更难的 MMLU

**来源：** [MMLU-Pro - EleutherAI GitHub](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/mmlu_pro/README.md)

MMLU-Pro 是 MMLU 的增强版本，主要改进：

- **选项从 4 个扩展到 10 个**，减少猜测准确率
- **增加更多推理型问题**，减少纯知识记忆
- **提示词敏感性从 4-5% 降低到 2%**，评估更稳定
- **思维链（CoT）在 MMLU-Pro 上比直接回答效果更好**

---

## 4. 2026 年最新进展

### 4.1 评测体系的三大支柱

2026 年权威的 LLM 评测体系由三类方法构成：

| 类型 | 代表 | 特点 |
|------|------|------|
| **静态基准测试** | MMLU-Pro, HumanEval, GSM8K | 可复现、横向对比 |
| **动态人类偏好评估** | Arena AI (原 Chatbot Arena), MT-Bench | 反映真实使用体验 |
| **垂直场景专项评测** | GPQA Diamond, SWE-Bench, MedQA | 决定落地适配性 |

最佳实践：**综合使用三类方法**，优先参考 Arena AI 人类偏好榜 + 与自身场景匹配的垂直基准。

### 4.2 主流基准现状（2026）

| 基准 | 测试内容 | 2026 年状态 |
|------|---------|------------|
| **MMLU** | 57 学科选择题 | ⚠️ 饱和 >90%，顶级模型间无区分度 |
| **MMLU-Pro** | 更难版本 | 接近饱和 |
| **GPQA Diamond** | 博士级科学问题 | ✅ 仍能区分 60-90% 区间 |
| **HLE** | 新基准 | ✅ 未饱和，最高 50.7%（Grok 4） |
| **HumanEval** | Python 代码生成 | ⚠️ 饱和 + 数据污染 |
| **SWE-Bench Verified** | 真实 GitHub Issue | ✅ 编程 Agent 黄金标准（注意脚手架偏差 25pp+） |
| **LiveCodeBench** | 持续新题 | ✅ 最抗污染 |
| **IFEval** | 复杂指令遵循 | ✅ 对 RAG/Agent/结构化输出至关重要 |
| **Arena AI Elo** | 人类盲测投票 | ✅ 最贴近实际使用体验 |

### 4.3 2026 年榜单格局

截至 2026 年初，各赛道领跑模型：

| 场景 | 领跑模型 | 关键分数 |
|------|---------|---------|
| 综合知识 | Claude Opus 4.6, Gemini 3 Pro, GPT-5 系列 | MMLU-Pro 前三 |
| 博士级推理 | Grok 4 | HLE 50.7%（最高） |
| 编程/Agent | GLM-5.1 | SWE-Bench Pro 58.4%（超越 GPT-5.4 和 Claude Opus 4.6） |
| 指令遵循 | Kimi K2.5 | IFEval 94.0 |
| 计算机使用 | GPT-5.4 | OSWorld 75%（超越人类专家基线） |
| 中文场景 | DeepSeek, Qwen 系列 | C-Eval 领先 |

> 据 Arena AI 官方数据，**排名前 10 的模型 Elo 分差不超过 50 分**，说明顶级模型的实际能力差距正在收窄，场景匹配度和 API 成本逐渐成为选型决定性因素。

### 4.4 单基准选型的三大陷阱

1. **饱和（Saturation）**——顶级模型 MMLU 同刷 90%+，2% 差距是噪音
2. **数据污染（Contamination）**——旧基准被爬入训练集，HumanEval 问题最严重
3. **脚手架依赖（Scaffold Dependence）**——SWE-Bench 评分因评估框架不同可差 25 个百分点

### 4.5 模型路由：2026 年架构新范式

> **不要选一个模型**——按任务复杂度、延迟、成本进行路由。

- 简单查询走轻量模型 → 复杂推理走旗舰模型
- 成本降低 **50-80%** 同时保持质量
- 路由分类器：小型模型，50-100ms 决策

### 4.6 2026 年评测工具生态

| 工具 | 特点 |
|------|------|
| **Arena AI**（原 Chatbot Arena） | 融资 1.5 亿美元，推出企业级 AI 评估服务 |
| **DeepEval** | 14+ LLM 指标，Agent 级评测（工具正确性、步骤效率、计划遵循） |
| **Patronus AI** | 多模态评测，91% 人类判断一致率 |
| **Future AGI** | 全栈生产级，RAG 指标 + 格式验证 + 合规检查 |
| **LangSmith** | LangChain深度集成，详细工作流追踪 |

### 4.7 2026 年趋势总结

1. **单基准分数不再重要**——场景匹配度比榜单排名更关键
2. **Arena AI 争议升温**——基于主观偏好的评估是否科学？Vibes-based 评估受到质疑
3. **自定义 Eval 成为标配**——构建 100-200 条真实业务测试集，比任何公开基准都更有价值
4. **模型路由取代单一选型**——按任务 routing 可降本 50-80%
5. **EU AI Act 合规驱动评估**——高风险场景必须有正式评估文档

> 来源参考：[大模型测评完全指南 2026](https://segmentfault.com/a/1190000047645758)、[LLM Benchmarks 2026: Which Model for Which Job](https://datavlab.ai/post/llm-benchmarks-2026-which-model-for-which-job)、[LLM Evaluation 2026 - FutureAGI](https://futureagi.substack.com/p/llm-evaluation-frameworks-metrics)、[AI 下半场，LLM Benchmark 要补全什么？](https://finance.sina.com.cn/tech/roll/2026-03-09/doc-inhqkhiq9940891.shtml)、[Which LLM to Choose 2026](https://iternal.ai/llm-selection-guide)

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:11:39*
*资源区块更新时间：2026-06-30 11:11:09*
*资源区块更新时间：自动更新*
