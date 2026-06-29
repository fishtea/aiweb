# 多模态模型：当 AI 长出眼睛和耳朵

## 从一个场景开始

> 你拍了一张厨房的照片，照片里有香蕉、苹果和一个标签写着"有机"的牛奶盒。你把照片发给 AI，问：
>
> "这张照片里有乳制品吗？"

**VLM 的处理过程大致是这样的：**

```
[输入图像]
     ↓
[Vision Encoder] ← CLIP ViT 将图像转为视觉特征向量
     ↓
[Projection Layer] ← 将视觉特征映射到 LLM 的 embedding 空间
     ↓
[LLM Decoder] ← "照片中有一个标着'有机'的牛奶盒，所以答案是：是"
     ↓
[输出文本] ← "有，照片右下角有一盒有机牛奶，属于乳制品。"
```

这个看起来简单的流水线背后，是三个领域的交叉融合：计算机视觉 + 自然语言处理 + 多模态对齐。

---

## 视觉理解：VLM（Visual Language Model）

### 核心架构

当前 VLM 的通用框架——**CLIP + LLM Bridge**：

```
┌────────────────────────────────────────────────┐
│  [图像输入]                                     │
│      │                                          │
│      ▼                                          │
│  ┌──────────────┐                               │
│  │ Vision Encoder│  ← 通常是 ViT (Vision Transformer)│
│  │ (CLIP ViT-L) │     将 224×224 图像转为 257 个     │
│  │              │     视觉 token（每个 patch 一个）   │
│  └──────┬───────┘                               │
│         │                                        │
│         ▼                                        │
│  ┌──────────────┐                               │
│  │  Projector   │  ← 可学习的映射层              │
│  │  (MLP/Q-Former)│   将视觉 token 映射到 LLM     │
│  └──────┬───────┘     能理解的 embedding 空间     │
│         │                                        │
│         ▼                                        │
│  ┌──────────────┐                               │
│  │  LLM Decoder │  ← 接收到融合的视觉+文本 token  │
│  │  (LLaMA/Qwen)│     像处理文本一样生成回答      │
│  └──────────────┘                               │
│         │                                        │
│         ▼                                        │
│  [文本输出]                                       │
└────────────────────────────────────────────────┘
```

### 关键组件详解

**Vision Encoder（视觉编码器）**：
- 将图像分解为固定大小的 patch（如 16×16 像素）
- 每个 patch 转换为一个向量（token）
- 一张标准 224×224 的图像 ≈ 196 个 patch token + 1 个 [CLS] token
- 高分辨率图像（如 448×448）会产生 4x 的 token 数

**Projection Layer（投影层）**：
- 核心挑战：视觉空间 vs 文本空间是**异构的**
- 简单的方案：一个两层的 MLP，将视觉 token 维度映射到 LLM 的 hidden size
- 复杂的方案：Q-Former（BLIP-2）——用可学习的 query token 在视觉特征上做"注意力池化"

**为什么视觉 token 这么多？**
- 一张 224×224 的图像 → 257 个 token（ViT-L）
- 这个数量级和中长文本相当
- 处理高分辨率图像时，token 数会爆炸（448×448 → 1025 token）
- 这就是为什么 VLM 在处理多张图片或高分辨率图像时速度明显变慢

### 实战：用一个小 VLM 做演示

```python
# 使用 transformers 加载 LLaVA
from transformers import LlavaForConditionalGeneration, AutoProcessor
import torch
from PIL import Image

model = LlavaForConditionalGeneration.from_pretrained(
    "llava-hf/llava-1.5-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

image = Image.open("kitchen.jpg")
prompt = "USER: <image>\n这张照片里有什么乳制品？\nASSISTANT:"

inputs = processor(text=prompt, images=image, return_tensors="pt").to("cuda")
output = model.generate(**inputs, max_new_tokens=100)
print(processor.decode(output[0], skip_special_tokens=True))
# 输出: "照片中有一盒有机牛奶，位于照片右下角。"
```

---

## 图像生成：扩散模型

### 一句话说清扩散模型

> **扩散模型 = 给图片加噪声学毁图 → 学会如何一步步去噪还原图**

过程可以理解为：
```
正向过程（训练时）：
清晰图像 → [逐步加噪声] → 纯噪声

反向过程（生成时）：
纯噪声 → [逐步去噪，每一步模型预测该去除的噪声] → 清晰图像
```

### 采样过程的数学直觉

```
第 T 步: 纯噪声 z (100% 噪声)
第 T-1 步: z - ε_θ(z, T) + 少量噪声 (80% 噪声, 20% 信号)
第 T-2 步: ... (60% 噪声, 40% 信号)
...
第 0 步: 最终图像 (0% 噪声, 100% 信号)
```

每一步，模型 ε_θ 预测当前状态 z 中的噪声成分，减去它，就得到更清晰的状态。

**Stable Diffusion 的关键创新**：把扩散过程从像素空间搬到**潜空间（latent space）**。像素空间 512×512×3 ≈ 786K 维度 → 潜空间 64×64×4 ≈ 16K 维度。**计算量减少约 50 倍**。

### 条件控制

```
text:"一只橘猫坐在沙发上看电视"
     │
     ▼
┌──────────────────────────────┐
│  Text Encoder (CLIP)          │
│  "一只橘猫" → 向量             │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  UNet + Cross-Attention       │  ← 文本条件通过 cross-attention
│  噪声预测 ← 文本条件             │     注入去噪过程
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  VAE Decoder                  │  ← 从潜空间解码回像素空间
│  潜空间 → 像素空间              │
└──────────────────────────────┘
           │
           ▼
     [生成图像]
```

---

## 语音理解：Whisper

Whisper 的工作方式更接近"分而治之"：

```
[音频波形] 
     ↓
分帧（每帧 30 秒，重叠） 
     ↓
Spectrogram（声谱图）—— 用 STFT 将时域信号转为频域表示
     ↓
Encoder（类似 ViT 的分 patch 方式处理声谱图） 
     ↓
Decoder（输出文本 token，支持多语言）
     ↓
[文本转录]
```

Whisper 的训练数据覆盖 96 种语言，370 万小时音频。它的优势不是架构创新，而是**数据规模和多样性**带来的鲁棒性。

**关键能力**：
- 语言识别（自动检测输入语言）
- 语音转文字（96 种语言）
- 翻译（非英语 → 英语）
- 时间戳（逐词标记时间点）

---

## 多模态融合管线演示

下面是一个完整的多模态处理流水线——输入包含图像、音频和文本：

```python
from PIL import Image
import whisper
from transformers import pipeline

# 1. 加载多模态组件
vlm = pipeline("image-to-text", model="llava-hf/llava-1.5-7b-hf")
whisper_model = whisper.load_model("base")
 
# 2. 输入多模态数据
image = Image.open("meeting_photo.jpg")
audio = whisper_model.transcribe("meeting_recording.wav")
text = "总结一下这次会议的核心内容"

# 3. 跨模态信息提取
# 从音频中提取文字转录
meeting_transcript = audio["text"]

# 从图像中提取视觉描述
image_description = vlm(image, "描述这张照片中的场景")

# 4. 融合所有模态信息到统一上下文
multi_modal_context = f"""
【会议录音转录】
{meeting_transcript}

【会议照片描述】
{image_description[0]['generated_text']}

【用户要求】
{text}
"""

# 5. 用 LLM 做跨模态推理
llm = pipeline("text-generation", model="Qwen/Qwen-7B-Chat")
result = llm(multi_modal_context)
```

---

## 视频理解：把视频当图像序列处理

视频理解的核心挑战：**时间维度**。视频不是"会动的图像"，是包含时间因果关系的序列。

### 当前的主流做法

```
[视频 → 均匀采样 N 帧] → [每帧过 ViT] → [帧 token 序列]
→ [添加时间位置编码] → [LLM 理解时间线] → [输出]
```

**关键问题**：
- 采样多少帧？（16 帧 vs 64 帧 vs 128 帧——精度×成本的权衡）
- 如何表示时间关系？（绝对位置编码 vs 相对时间差）
- 运动信息如何捕捉？（光流特征 vs 帧间差分）

**Sora（OpenAI）的不同路线**：直接对视频 patch 建模（时空 patch），不用帧概念。每个 patch 是 (时间×宽度×高度) 的立方体。

---

## 当前多模态模型的局限

| 能力 | 当前水平 | 人类水平 | 差距 |
|------|:-------:|:-------:|:----:|
| 图像描述 | ★★★★☆ | ★★★★★ | 细节遗漏 |
| 物体计数 | ★★☆☆☆ | ★★★★★ | 超过 10 个物体开始混乱 |
| 空间关系（A在B的左边） | ★★★☆☆ | ★★★★★ | 左右混淆常见 |
| 文字识别（OCR in image） | ★★★★☆ | ★★★★★ | 手写体差 |
| 视频因果推理 | ★★☆☆☆ | ★★★★★ | 几乎为零 |
| 跨模态推理 | ★★★☆☆ | ★★★★★ | 模态间对齐仍弱 |
| 图像生成的真实感 | ★★★★☆ | ☆ | 但会犯物理错误（手指数量）|
| 音频理解（语气/情绪） | ★★☆☆☆ | ★★★★★ | 刚起步 |

**结论**：单模态能力在快速追赶，但**真正的多模态融合**（一个模型真正理解不同模态的语义关系）仍处于早期阶段。当前大多数"多模态模型"本质上还是"多个单模态模型拼在一起"。
