# 模型微调技术：当通用模型不够用时

## 问题现场

```
你：请用标准的法律文书格式，为原告起草一份诉讼请求。
GPT-4：[输出一份格式凌乱、条款不全、引用错误的法律文书]
你：请严格按照《民事诉讼法》格式要求重写。
GPT-4：[格式对了，但内容明显是模板填充]
你：我给你 5 个示例，请参照这个格式写。
GPT-4：[这次好很多，但遇到专业条款还是瞎编]
```

**根因**：通用模型的知识广度 vs 你的专业深度，存在结构性矛盾。模型见过海量法律文本，但它不是法律专家——它只是在概率上"猜"下一个词。

**解法**：模型微调。

---

## 三种微调路线

### 路线 A：全量微调（Full Fine-tuning）

```
输入：模型权重
过程：所有参数参与训练
输出：全新权重文件
成本：高（6×A100 起）
质量：取决于数据量
适配度：专机专用
```

更新所有参数，相当于给模型做"全身整容"。效果上限最高，但成本也最高。适用于：
- 你有大量（10 万+）高质量标注数据
- 你需要模型彻底改变输出行为（比如学会某种特殊协议）
- 预算不是问题

### 路线 B：LoRA（Low-Rank Adaptation）

```
输入：原模型权重（不修改）
过程：注入低秩适配矩阵，只训练这些矩阵
输出：一个几 MB 的 adapter 文件
成本：低（单张 4090 可行）
质量：与全量微调差距在 5% 以内
适配度：热插拔，随时切换
```

LoRA 的核心思想——"不要重新训练模型，而是教它如何调整自己的行为"。在原权重的旁边旁路一个小的可训练矩阵（秩 r=8 或 r=16），训练时只更新这个旁路。推理时把旁路合并回去，几乎无额外开销。

### 路线 C：QLoRA（Quantized LoRA）

```
输入：4-bit 量化后的模型权重
过程：在量化模型上做 LoRA
输出：一个 adapter 文件
成本：极低（单张 3060 可行）
质量：与 LoRA 差距约 1%
适配度：消费级显卡就能跑
```

QLoRA = LoRA + 量化。把模型权重量化到 4-bit（使用 NF4 格式），显存需求降到原来的 1/4。你可以在 24GB 显存上微调 70B 模型。

---

## 对比表

| 维度 | 全量微调 | LoRA | QLoRA |
|------|---------|------|-------|
| 可训练参数 | 100% | ~0.1-1% | ~0.1-1% |
| 显存需求（7B） | ~56GB | ~16GB | ~6GB |
| 显存需求（70B） | ~560GB | ~140GB | ~24GB |
| 训练时间（相对） | 10x | 1x | 1.2x |
| 推理延迟差异 | 无 | 可忽略 | 略微增加 |
| 输出质量（相对） | 基准（100%） | 95-99% | 94-98% |
| 数据需求 | 10万+ | 50-1000条 | 50-1000条 |
| 切换任务 | 需重新训练 | 换 adapter 文件 | 换 adapter 文件 |

**结论**：90% 的场景下，LoRA/QLoRA 是正确选择。全量微调只在极其特殊的场景下有必要。

---

## 上手：LoRA 微调一个 7B 模型（PyTorch + PEFT）

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset

# 1. 加载基础模型
model_name = "mistralai/Mistral-7B-v0.1"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,         # 使用 BF16 节省显存
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# 2. 配置 LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,                                # 秩的大小——8 是个好起点
    lora_alpha=32,                      # 缩放系数
    lora_dropout=0.1,                   # 防止过拟合
    target_modules=["q_proj", "v_proj"],# 只训练 Q 和 V 投影层
)

model = get_peft_model(model, lora_config)

# 3. 查看可训练参数
model.print_trainable_parameters()  
# 输出示例: trainable params: 4,194,304 / 7,000,000,000 ≈ 0.06%

# 4. 训练
training_args = TrainingArguments(
    output_dir="./mistral-lora-legal",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,      # 等效 batch size = 16
    learning_rate=2e-4,
    num_train_epochs=3,
    logging_steps=10,
    save_strategy="epoch",
    fp16=False,
    bf16=True,                          # BF16 比 FP16 更稳定
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=your_dataset,         # 你的训练数据
)
trainer.train()

# 5. 保存 adapter (只有几 MB)
model.save_pretrained("./mistral-lora-legal-adapter")
```

**关键参数调优指南**：

| 参数 | 小数据（<200条） | 中数据（200-2000条） | 大数据（>2000条） |
|------|:---:|:---:|:---:|
| r（秩） | 8 | 16 | 32 |
| lora_alpha | 16 | 32 | 64 |
| learning_rate | 1e-4 | 2e-4 | 5e-5 |
| num_epochs | 5-10 | 3-5 | 2-3 |
| dropout | 0.2 | 0.1 | 0.05 |

**警告**：秩不是越大越好。r=8 和 r=64 的差距经常在统计上不显著（甚至更大的 r 可能过拟合）。

---

## 什么时候不该微调

```
┌─ 你的问题能用 prompt 解决吗？ ──────── 是 → 别微调，先优化 prompt
│
└─ 你的问题能用 few-shot 解决吗？ ────── 是 → 别微调，加示例
    │
    └─ 你的问题能用 RAG 解决吗？ ──────── 是 → 别微调，先建检索
        │
        └─ 都不是 → 微调是你的工具
```

微调不是万能药。它解决的是**输出行为的结构性问题**（格式、风格、领域知识深度），不是**事实准确性**（那是 RAG 的领地）或**逻辑推理**（那是 prompt 设计的事）。

---

## 下一步

数据怎么准备？清洗、格式、质量检查？参见 [RAG 检索增强 →](../RAG检索增强/index.md) 中的数据处理方法论。
