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

### 6. 从静态基准到动态评估

静态基准（MMLU、HumanEval）面临"基准污染"和"刷榜"问题，2025-2026 评估方法向动态化演进：

| 方法 | 思路 | 解决的问题 |
|------|------|-----------|
| LiveBench / LMArena | 持续更新新题，防止训练数据泄漏 | 基准污染、刷榜 |
| LMSYS Chatbot Arena | 真实用户盲测对战，Elo 评分 | 与人类偏好对齐 |
| LLM-as-a-Judge | 用强模型给被测模型打分 | 人工评估成本高 |
| Agentic 基准 | 评估多步任务成功率（SWE-Bench、OSWorld） | 单轮问答不代表 Agent 能力 |
| 动态对抗集 | 自动生成针对模型弱点的测试 | 暴露盲区 |

### 7. 评估的常见陷阱

- **基准污染**：测试题混入训练数据，分数虚高 → 用 LiveBench 等动态基准。
- **刷榜优化**：模型针对公开榜单过拟合 → 关注 Arena 真实对战和自建评估集。
- **只看平均分**：平均分掩盖长尾失败 → 分析分任务、分难度、分人群表现。
- **忽视方差**：单次跑分有随机性 → 报告标准差，多次运行取均值。
- **基准≠业务**：榜单第一不等于你的场景最好 → 必须建业务评估集。

> 经验：不要只看模型厂商的官方跑分。一个针对你业务场景的 50 条人工评估集，比任何公开榜单都更有参考价值。

---

## 8. 2026年评估体系新进展

### 8.1 LM Evaluation Harness 最新更新

**来源：** [LM Evaluation Harness GitHub README](https://github.com/EleutherAI/lm-evaluation-harness)（2025-2026，持续更新）

EleutherAI 的 LM Evaluation Harness 在 2025-2026 年进行了多项重大更新，标志着评估工具从"能用"走向"好用"：

| 更新时间 | 特性 | 说明 |
|----------|------|------|
| 2025/12 | **CLI 重构为子命令** | `lm-eval run` / `lm-eval ls` / `lm-eval validate`，支持 YAML 配置文件（`--config`） |
| 2025/12 | **轻量化安装** | 基础包不再捆绑 transformers/torch，按需安装后端：`pip install lm_eval[hf]` / `[vllm]` / `[api]` |
| 2025/07 | **CoT 推理剥离** | `think_end_token` 参数支持自动剥离 CoT 推理痕迹，避免污染生成评估 |
| 2025/03 | **HF 模型引导（Steering）** | 支持对 HuggingFace 模型进行激活引导实验 |
| 2025/02 | **SGLang 后端支持** | 新增 SGLang 推理后端，与 vLLM 互补 |
| 2024/09 | **多模态评估原型** | `hf-multimodal` 和 `vllm-vlm` 模型类型 + `mmmu` 任务，支持图文多模态输入 |

> **重要变化**：v0.4.0 引入了基于配置的任务创建、Jinja2 提示词设计、Promptsource 集成、更灵活的 fewshot 配置和数据并行加速。

```bash
# 新版 CLI 用法示例
lm-eval ls tasks                          # 列出所有可用任务
lm-eval run --config my_eval.yaml         # 使用 YAML 配置运行
lm-eval run --tasks mmlu,gsm8k            # 指定任务
  --model hf --model_args pretrained=xxx  # 选择模型后端
```

### 8.2 Chatbot Arena 与动态评估生态

**来源：** [LMSYS Chatbot Arena](https://chat.lmsys.org/)（2026 年持续运营）

LMSYS Chatbot Arena 已成为模型评估的"黄金标准"之一，其核心价值在于：

- **真实用户盲测**：数十万真实用户参与匿名对战投票，计算 Elo 评分
- **难以作弊**：新模型持续加入，旧模型评分随用户偏好变化而更新
- **细粒度排行榜**：按类别（编码、写作、数学、长文本等）、语言、难度分层排名

2026 年 Chatbot Arena 已迁移到 HuggingFace Spaces（由 `lmarena-ai` 组织维护），评估类别进一步细化，引入了 **Arena-Hard-Auto** 等自动化变体，降低人工评估成本。

与静态基准（MMLU、HumanEval）的互补关系：

| 评估方式 | 优势 | 局限 |
|----------|------|------|
| 静态基准 | 可复现、低成本、快速 | 易被刷榜、数据污染 |
| Chatbot Arena | 反映真实偏好、难作弊 | 成本高、结果慢、受用户群体偏差影响 |
| LiveBench | 持续更新新题 | 出题质量波动 |

> **建议**：不要只看一个榜单。静态基准（MMLU-Pro）+ 动态基准（LiveBench）+ Arena Elo 三方交叉验证，才能全面评估模型。

### 8.3 Agent 评估基准的崛起

随着 Agent 应用爆发，传统单轮问答基准已不足以评估 Agent 能力。2025-2026 年涌现出一批面向 Agent 的评估基准：

| 基准 | 评估维度 | 特点 |
|------|----------|------|
| **SWE-Bench Verified** | 真实 GitHub Issue 修复 | 500 个经过人工验证的软件工程任务，测试编码 Agent |
| **SWE-bench Multimodal** | 多模态软件工程 | 处理 UI 截图、设计稿等视觉输入的编码任务 |
| **OSWorld** | 计算机操作 | 在真实操作系统环境中完成多步任务 |
| **WebArena** | Web 交互 | 模拟电商、社交、CMS 等网站的自主操作 |
| **τ²-bench** | 工具使用与规划 | 评估 Agent 的多工具协同和长期规划能力 |
| **MCP Benchmark** | 协议互操作 | 测量 Agent 使用 MCP 协议工具的效率和正确率 |

> 趋势：Agent 评估从"答对题"走向"完成任务"——更多强调多步规划、工具使用正确率和端到端成功率。

### 8.4 LLM-as-Judge 的成熟与争议

用 LLM 评判 LLM 的实践在 2026 年已广泛采用，但争议仍在：

**适用场景**：
- 开放式生成质量评估（写作、摘要、翻译），人工评估成本过高
- 多轮对话连贯性评估，客观指标难以定义
- 快速原型验证阶段的反馈环路

**已知问题**：
- **位置偏差**：评判 LLM 倾向于偏好第一个/最后一个选项
- **长度偏差**：倾向于给更长的回答更高分
- **自我增强**：评判 LLM 偏好与自己风格相似的输出
- **风格偏见**：对冗长、权威语气的回答有系统性偏好

**缓解策略**：
- 交换候选答案顺序，多次评判取平均
- 使用多个评判模型交叉验证
- 结合人工抽检校准（每 100 条中抽 10 条人工比对）

### 8.5 2026 评估实践建议

1. **建立三层评估体系**：自动化基准（日常监控）→ LLM-as-Judge（生成质量）→ 人工抽检（校准兜底）
2. **关注评估的一致性而非绝对值**：不同框架跑出来的 MMLU 分数不可直接比较，用同一框架对比才有意义
3. **Agent 评估优先考虑 SWE-Bench Verified**：这是目前最接近真实工程场景的 Agent 基准
4. **定期更新评估集**：任何静态基准在 6-12 个月后都可能被模型"学习"，切换至 LiveBench 或自建动态评估集
5. **记录评估配置的完整信息**：模型版本、prompt 模板、fewshot 数量、解码参数——LM Evaluation Harness 的 YAML 配置可以很好地解决这个问题

### 8.6 参考来源

- [LM Evaluation Harness GitHub](https://github.com/EleutherAI/lm-evaluation-harness)（2026-07 获取最新 README）
- [LMSYS Chatbot Arena (HuggingFace)](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard)
- [SWE-Bench Verified](https://www.swebench.com/)
- [Open LLM Leaderboard v2](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)

---

## 🔗 参考资料

- [LLM Eval Harness Guide - Morphllm](https://www.morphllm.com/llm-eval-harness)
- [EleutherAI - Evaluating LLMs](https://www.eleuther.ai/projects/large-language-model-evaluation)
- [LM Evaluation Harness GitHub](https://github.com/EleutherAI/lm-evaluation-harness)
- [MMLU-Pro Paper](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/mmlu_pro/README.md)
- [NVIDIA NeMo LM Harness Evaluation](https://docs.nvidia.com/nemo/microservices/25.8.0/evaluate/evaluation-types/lm-harness.html)

## 2026 年模型评估实践：从公开榜单到自定义管线

> 来源：[Evidently AI - LLM Benchmarks Guide](https://www.evidentlyai.com/llm-guide/llm-benchmarks)（2026 年更新），[LLM-Stats - AI Benchmarks 2026](https://llm-stats.com/benchmarks)（300+ 基准排行榜），[SuperCLUE中文大模型测评基准](https://www.superclueai.com/)

### 2026 年 LLM 基准测试全景

2026 年，公开的 LLM 基准测试已超过 **300 个**，覆盖从基础语言理解到多模态 Agent 的各个能力维度：

| 能力维度 | 代表性基准 | 说明 |
|---------|-----------|------|
| 通用知识 | MMLU-Pro, ARC-Challenge, SimpleQA | 多学科知识、推理、事实准确性 |
| 数学推理 | GSM8K, MATH, LiveMathBench | 从小学到竞赛级数学 |
| 代码生成 | HumanEval, MBPP, SWE-Bench Verified | 函数级到工程级编码 |
| 指令跟随 | IFEval, AlpacaEval | 格式、约束遵从度 |
| Agent 能力 | SWE-Bench, OSWorld, WebArena, τ²-Bench | 多步任务、工具使用、自主操作 |
| 对话质量 | Chatbot Arena (Elo), Arena-Hard-Auto | 真实用户盲测 |
| 安全与对齐 | TruthfulQA, SafetyBench, RedTeam | 准确性、有害内容拒答 |

### Open LLM Leaderboard v2：当前最受关注的公开榜单

HuggingFace 的 **Open LLM Leaderboard v2** 已成为开源模型评估的行业标准，使用 LM Evaluation Harness 统一运行以下任务：

| 基准 | 测试内容 | 评测方式 |
|------|---------|---------|
| **MMLU-Pro** | 10 选 1 多学科知识（更难版 MMLU） | Loglikelihood |
| **IFEval** | 指令跟随（格式、长度、约束） | 生成式 + 规则评分 |
| **BBH** | BIG-Bench 困难任务（23 个子任务） | 生成式 |
| **MATH Lvl 5** | 高中数学竞赛难度 | 生成式 |
| **GPQA** | 博士级专家问题 | Loglikelihood |
| **MUSR** | 多步软推理（Murder Mystery） | 生成式 |

> **重要变化**：v2 移除了 ARC-Challenge 和 HellaSwag（已被模型刷透），增加了更具区分度的 MATH Lvl 5 和 MUSR。

### 构建自定义评估管线的实践建议

公开榜单只能反映通用能力，生产级评估必须建设**业务自定义评估管线**：

#### 步骤 1：定义评估维度

| 维度 | 示例指标 | 评估方式 |
|------|---------|---------|
| 准确性 | 精确答案匹配率 | 规则评分（期望输出 vs 模型输出） |
| 完整性 | 关键信息覆盖率 | LLM-as-Judge 打分 |
| 格式遵从 | JSON schema 验证 | 规则评分（pydantic 验证） |
| 安全合规 | 敏感内容拒答率 | 对抗测试集 |
| 延迟 | P50/P95/P99 | 基础设施监控 |

#### 步骤 2：准备评估数据集

- **最小可行评估集**：30-50 条覆盖核心场景的代表性样本
- **生产评估集**：200-500 条，含正常、边界和异常输入
- **对抗集**：50-100 条 prompt 注入/越狱测试

#### 步骤 3：搭建评估流水线

```python
# 使用 pytest + LLM-as-Judge 的简化评估示例
import pytest
from openai import OpenAI

TEST_CASES = [
    {"input": "总结这段文字...", "expected_keywords": ["关键字1", "关键字2"]},
    {"input": "提取JSON格式的实体...", "expected_schema": {"name": str, "amount": float}},
]

@pytest.mark.parametrize("case", TEST_CASES)
def test_llm_output(case):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4o-mini",
        input=case["input"]
    )
    output = response.output_text
    # 规则验证
    for kw in case.get("expected_keywords", []):
        assert kw in output, f"缺少关键内容: {kw}"
```

### LLM-as-Judge 在 2026 年的最佳实践

用 LLM 评判 LLM 已成为评估流程的标准环节，但需要克服已知偏差：

| 偏差类型 | 缓解策略 |
|----------|---------|
| 位置偏差 | 交换候选顺序，多次评判取平均 |
| 长度偏差 | 在评判 prompt 中明确"不因长度加分" |
| 自我增强 | 使用多个评判模型交叉验证 |
| 风格偏见 | 结合规则评分，降低风格权重 |

**实践建议**：建立**三层评估体系**
1. **自动化基准**（如 LM Evaluation Harness）— 日常监控，可复现
2. **LLM-as-Judge** — 生成质量评估，快速反馈
3. **人工抽检** — 每 100 条中抽 10 条人工校准

### Agent 评估在 2026 年的重要性

随着 Agent 应用的爆发，传统单轮问答基准已不足以评估能力。2026 年涌现了一批面向 Agent 的基准：

| 基准 | 评估维度 | 现状 |
|------|----------|------|
| **SWE-Bench Verified** | 真实 GitHub Issue 修复（500 个任务） | Agent 编码的首选基准 |
| **OSWorld** | 真实操作系统操作（多步任务） | 评估自主 Agent 的全面能力 |
| **τ²-Bench** | 工具使用与规划（零售/电信领域） | 评估多工具协作能力 |
| **BrowseComp** | 互联网深度检索 | 评估 Agent 的持久搜索能力 |

### 参考来源

- [30 LLM evaluation benchmarks and how they work - Evidently AI](https://www.evidentlyai.com/llm-guide/llm-benchmarks)
- [AI Benchmarks 2026 - LLM-Stats](https://llm-stats.com/benchmarks)
- [Open LLM Leaderboard v2 - HuggingFace](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)
- [Evaluating LLM-Generated Code - arXiv](https://arxiv.org/html/2605.09059v1)
- [SuperCLUE中文大模型测评基准](https://www.superclueai.com/)
- [LLM Agent Evaluation Metrics 2026 - Zencoder](https://zencoder.ai/blog/llm-agent-evaluation-metrics-2026)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-16 00:08:55*
