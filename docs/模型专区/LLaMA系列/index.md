# LLaMA 系列 — Meta

> Llama（Large Language Model Meta AI）是 Meta 开发的开放权重大语言模型系列。按 2026-07-06 可核验的 Meta 官方发布页，最新主线仍是 Llama 4；生产选型应重点评估 Llama 4 Scout / Maverick、Llama 3.3 70B 和 Llama 3.1 405B。

---

## 模型演进

| 模型 | 发布时间 | 参数规模 | 训练数据 | 上下文窗口 |
|------|---------|---------|---------|-----------|
| LLaMA 1 | 2023.02 | 7B/13B/33B/65B | 1.0-1.4T tokens | 2K |
| LLaMA 2 | 2023.07 | 7B/13B/70B | 2T tokens | 4K |
| LLaMA 3 | 2024.04 | 8B/70B | 15T tokens | 8K |
| LLaMA 3.1 | 2024.07 | 8B/70B/405B | 15T+ tokens | 128K |
| Llama 3.2 | 2024.09 | 1B/3B（文本）+ 11B/90B（多模态视觉） | — | 128K |
| Llama 3.3 | 2024.12 | 70B | 15T+ tokens | 128K |
| Llama 4 | 2025.04 | Scout / Maverick / Behemoth(预览) | 未完全公开 | 10M(Scout)/1M(Maverick) |

### LLaMA 4 — 原生多模态 MoE

Llama 4（2025.04）是 Meta 首次大规模转向 MoE + 多模态的一代：

| 模型 | 架构 | 激活参数 | 上下文 | 定位 |
|------|------|---------|--------|------|
| Llama 4 Scout | MoE，16 专家，17B 激活 | 17B / ~109B 总 | **10M** | 超长上下文，适合文档和代码库分析 |
| Llama 4 Maverick | MoE，128 专家，17B 激活 | 17B / ~400B 总 | 1M | 通用多模态旗舰，质量高于 Scout |
| Llama 4 Behemoth | 更大 MoE，训练中/预览 | — | — | 作为教师模型和未来旗舰方向 |

根据 [Hugging Face 官方博客](https://huggingface.co/blog/llama4-release)（2025.04）及 Meta 发布资料：

#### 架构核心特性

- **MoE 架构差异**：Maverick 使用 **128 个专家**（每 token 激活 1 个），Scout 使用 **16 个专家**（每 token 激活 1 个）。两者均有 17B 活跃参数，但总参数 Maverick（~400B）远超 Scout（~109B）。
- **原生多模态（Early Fusion）**：视觉 token 在模型输入端即与文本 token 融合，无需单独的视觉编码器或 adapter。支持文本和图像输入。
- **iRoPE 位置编码**：改进的旋转位置编码，支持超长上下文外推。Scout 的 10M token 上下文窗口是目前开源模型中最大的。
- **训练数据**：使用 **40 万亿 tokens** 训练，涵盖 **200 种语言**，其中 12 种语言有专门的微调支持（包括阿拉伯语、西班牙语、德语、印地语等）。

#### 部署与量化

- **Scout**：设计为可在**单张服务器级 GPU** 上运行，支持 4-bit 或 8-bit 动态量化（on-the-fly int4 量化代码由 Hugging Face 提供）。
- **Maverick**：提供 BF16 和 FP8 两种格式，需要多 GPU 部署。
- **许可协议**：Llama 4 Community License，与 Llama 3 系列许可类似，月活超 7 亿用户需 Meta 授权。

#### Hugging Face 集成

Hugging Face 与 Meta 密切合作，确保 Llama 4 在发布当天即可在以下框架中使用：

- **Transformers（v4.51.0+）**：支持完整的多模态推理、加载和微调 API，自动 tensor-parallel 和设备映射。
- **TGI（Text Generation Inference）**：支持优化和高吞吐生产部署。
- **TRL 集成**：支持使用 Transformers Reinforcement Learning 库进行微调。

#### 评测与争议

Llama 4 发布初期，其评测分数引发了**广泛争议**——社区发现 Maverick 在多个基准上与 Llama 3 相比提升有限，Meta 随后承认评测版本存在配置问题并发布了修正。以下为 Hugging Face 官方博客引用修正后的评测：

- Maverick Instruct 在 MMLU、MATH、HumanEval 等基准上**接近或持平 GPT-4o 和 Claude 3.5 Sonnet**。
- Scout 在长上下文任务（如 Needle-in-a-Haystack）上展示了对 10M token 的支持能力。
- 多模态评测（MMMU、MathVista）中，Maverick 表现与同代多模态模型相当。

> 综合来看，Llama 4 的主要价值在于：**① 开放权重的超长上下文（Scout 10M），② MoE 架构的效率尝试，③ 原生多模态的简化部署。** 但在中文场景和部分数学推理基准上，Qwen3 和 DeepSeek 仍是更好的选择。

### Llama 3.2 — 轻量文本与多模态视觉

根据 [Meta Llama Models GitHub](https://github.com/meta-llama/llama-models) 官方仓库（截至 2026-07），Llama 3.2 是 Llama 系列中第一个引入**视觉能力**的版本，同时提供了极轻量的文本模型：

| 模型 | 参数 | 类型 | 定位 |
|------|------|------|------|
| Llama 3.2 1B | 1B | 纯文本 | 边缘设备、移动端、嵌入式场景 |
| Llama 3.2 3B | 3B | 纯文本 | 消费级 GPU 本地运行 |
| Llama 3.2 11B Vision | 11B | 多模态（文本+图像） | 轻量级视觉理解 |
| Llama 3.2 90B Vision | 90B | 多模态（文本+图像） | 旗舰级视觉推理 |

**关键特点：**
- **1B 和 3B 文本模型**：支持 128K 上下文，TikToken 分词器，可在手机和低功耗设备上运行
- **Vision 模型**：支持图像输入，可进行图文理解、图表分析、OCR 等任务
- 与 Llama 3.1 共享分词器和许可框架

### 量化部署：FP8 与 Int4

根据 [llama-models README](https://github.com/meta-llama/llama-models)，Llama 4 支持混合精度量化推理：

| 量化模式 | 说明 | 硬件需求示例 |
|----------|------|-------------|
| `fp8_mixed` | FP8 权重 + BF16 激活 | Llama-4-Scout 需 2×80GB GPU |
| `int4_mixed` | Int4 权重 + BF16 激活 | Llama-4-Scout 仅需 1×80GB GPU |

```bash
# 使用 Int4 量化的 Llama 4 Scout 推理
torchrun --nproc_per_node=1 \
  -m models.llama4.scripts.chat_completion $CHECKPOINT_DIR \
  --quantization-mode int4_mixed
```

### Llama 生态系统与工具链

根据 [llama-models](https://github.com/meta-llama/llama-models) 和 [llama-cookbook](https://github.com/meta-llama/llama-cookbook)：

#### `llama-model` CLI 工具

Meta 官方提供的命令行工具用于管理 Llama 模型：

```bash
pip install llama-models

llama-model list              # 列出可用模型
llama-model list --show-all   # 列出所有版本（含旧版）
llama-model describe -m MODEL_ID    # 查看模型详细信息
llama-model download --source meta --model-id MODEL_ID  # 从 Meta 下载
llama-model verify-download   # 验证下载完整性
llama-model remove -m MODEL_ID      # 删除已下载模型
llama-model prompt-format -m MODEL_ID  # 查看模型的提示模板格式
```

#### Llama Cookbook（Llama 食谱）

[`meta-llama/llama-cookbook`](https://github.com/meta-llama/llama-cookbook) 是官方维护的 Llama 使用示例集合，涵盖：
- 推理与部署最佳实践
- 微调配方（LoRA、QLoRA、全参数微调）
- RAG 管道构建
- 多模态应用示例
- 安全护栏（Llama Guard、Prompt Guard、Code Shield）

> Llama 生态的优势在于 Meta 不仅是发布模型权重，还持续维护配套工具链——从下载管理（CLI）到最佳实践（Cookbook），再到安全工具（Llama Guard 系列），形成完整的开源 AI 开发闭环。

### 2026 最新可用列表

| 场景 | 推荐 |
|------|------|
| 超长上下文、整库代码和海量文档 | Llama 4 Scout |
| 通用多模态、质量优先 | Llama 4 Maverick |
| 开放权重旗舰基线、蒸馏和评估 | Llama 3.1 405B |
| 成本可控的生产文本模型 | Llama 3.3 70B |
| 消费级 GPU 本地实验 | Llama 3.1 8B / 70B 量化版 |

> 截至 2026-07-06，未找到 Meta 官方发布的 Llama 5 或 Llama 4.5。文档按可核验的 Llama 4 与 Llama 3.x 更新。

---

## LLaMA 3 架构详解

根据 Meta 官方博客 [Introducing Meta Llama 3](https://ai.meta.com/blog/meta-llama-3/) 和技术报告 [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783)：

### 核心架构

- **Decoder-only Transformer** — 标准架构但做了多项优化
- **Tokenizer:** 128K tokens 词汇量（LLaMA 2 为 32K），编码效率提升 15%
- **Grouped Query Attention (GQA):** 8B 和 70B 均使用，提升推理效率
- **训练序列长度:** 8,192 tokens，带文档边界掩码

### 训练数据

- **15T tokens**（LLaMA 2 的 7 倍，代码数据增加 4 倍）
- 超过 **5% 高质量非英语数据**，覆盖 30+ 语言
- 使用 LLaMA 2 生成训练数据用于文本质量分类器
- 数据过滤管道：启发式过滤、NSFW 过滤、语义去重

### 训练基础设施

- **16K GPU**（两个定制 24K GPU 集群）
- 单 GPU 计算利用率 > **400 TFLOPS**
- 集群运行时间 > **95%**
- 整体训练效率约为 LLaMA 2 的 **3 倍**

---

## Llama 3.1 / 3.3 — 仍然重要的生产基线

根据 Meta Llama 3.1 官方发布与技术报告：

- Llama 3.1 提供 8B / 70B / 405B 三档，均支持 **128K tokens** 上下文。
- 405B 是重要的开放权重旗舰模型，可作为蒸馏、评估和企业私有化基线。
- Llama 3.3 70B 在更小部署成本下接近 405B 的部分能力，适合作为生产默认候选。
- 与 GPT-4 和 Claude 3.5 Sonnet 在多项基准上竞争
- Llama 3.1 / 3.3 仍是 Dense 模型路线，生态、量化和微调资料最成熟。

---

## 指令微调

根据 Meta Llama 3 技术报告：

- 组合使用 **SFT + 拒绝采样 + PPO + DPO**
- 提示质量和偏好排序至关重要
- PPO/DPO 显著提升了推理和编码能力
- 70B Instruct 在人类偏好排名中超越了 Claude Sonnet、Mistral Medium 和 GPT-3.5

---

## 如何使用

### 通过 Hugging Face Transformers（v4.51.0+）

Llama 4 需要使用 **Transformers v4.51.0+** 和 `Llama4ForConditionalGeneration` 类（而非 `AutoModelForCausalLM`），以支持原生多模态加载和自动设备映射：

```python
import torch
from transformers import Llama4ForConditionalGeneration, AutoTokenizer

model = Llama4ForConditionalGeneration.from_pretrained(
    "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",        # 自动 tensor-parallel 和设备映射
)

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-4-Scout-17B-16E-Instruct"
)

messages = [
    {"role": "user", "content": [
        {"type": "text", "text": "描述这张图片中的内容。"},
        {"type": "image", "url": "https://example.com/photo.jpg"}  # 多模态输入
    ]}
]

input_ids = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
inputs = tokenizer(input_ids, return_tensors="pt").to(model.device)
output = model.generate(**inputs, max_new_tokens=512)
print(tokenizer.decode(output[0][len(inputs.input_ids[0]):], skip_special_tokens=True))
```

> 注意：Llama 4 使用原生多模态 Early Fusion 架构，视觉 token 在输入端与文本 token 融合，无需单独的视觉编码器或 adapter。`AutoModelForCausalLM` 在 v4.51.0+ 版本中会通过 `AutoModel` 自动匹配到 `Llama4ForConditionalGeneration`，但显式导入更可靠。

### 通过 Ollama 本地运行

```bash
ollama run llama3.1:8b
# 或
ollama run llama3.1:70b
# 或更大的 405B
ollama run llama3.1:405b
```

---

## 优势与局限

**优势:**
- **开源权重:** 可自由下载、部署、微调
- **强大生态:** Meta、Hugging Face、企业广泛支持
- **极致性价比:** 8B 可在消费级 GPU 运行，405B 接近闭源旗舰水平
- **丰富的工具链:** torchtune、Llama Recipes、Llama Guard 安全工具

**局限:**
- 中文能力不如英文（非英语数据仅 5%+）
- 大型模型（70B/405B）对硬件要求高
- 许可协议禁止某些商业用途（月活 >7 亿需 Meta 授权）
- 405B 推理延迟较高

---

**参考资料：**
- [Meta Llama 3 官方发布博客](https://ai.meta.com/blog/meta-llama-3/)
- [Meta Llama 4 官方发布博客](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)
- [The Llama 3 Herd of Models (arXiv:2407.21783)](https://arxiv.org/abs/2407.21783)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-23 00:09:06*
