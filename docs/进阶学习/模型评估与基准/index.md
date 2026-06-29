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

## 🔗 参考资料

- [LLM Eval Harness Guide - Morphllm](https://www.morphllm.com/llm-eval-harness)
- [EleutherAI - Evaluating LLMs](https://www.eleuther.ai/projects/large-language-model-evaluation)
- [LM Evaluation Harness GitHub](https://github.com/EleutherAI/lm-evaluation-harness)
- [MMLU-Pro Paper](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/mmlu_pro/README.md)
- [NVIDIA NeMo LM Harness Evaluation](https://docs.nvidia.com/nemo/microservices/25.8.0/evaluate/evaluation-types/lm-harness.html)
