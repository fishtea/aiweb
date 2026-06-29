# Gemini 系列

> Google DeepMind 开发的 Gemini 系列，以原生多模态和超长上下文为核心特色，深度集成 Google 生态。

---

## 发展历程

| 版本 | 发布时间 | 关键特性 |
|-----|---------|---------|
| Gemini 1.0 Pro | 2023.12 | 初代多模态模型 |
| Gemini 1.0 Ultra | 2024.02 | 最强版本 |
| Gemini 1.5 Pro | 2024.02 | **1M token 上下文** |
| Gemini 1.5 Flash | 2024.05 | 快速轻量版本 |
| Gemini 2.0 Flash | 2024.12 | 下一代架构、工具使用 |
| Gemini 2.0 Pro | 2025.03 | 旗舰能力增强 |
| Gemini 2.5 Pro | 2025.05 | 推理能力突破 |

---

## 核心特色

### 1. 原生多模态

Gemini 从设计之初就是**原生多模态**模型，而非文本模型加视觉模块：

- **文本**：理解与生成
- **图像**：图片分析与理解
- **音频**：语音识别与分析
- **视频**：视频内容理解
- **代码**：代码生成与执行

### 2. 超长上下文

Gemini 1.5 Pro 支持 **1,048,576 token（1M）** 上下文，是业界最高之一：

| 用途 | 可处理内容量 |
|-----|------------|
| 文字 | 约 75 万英文单词 / 15 万中文字符 |
| 代码 | 约 30,000 行代码 |
| 音频 | 约 11 小时录音 |
| 视频 | 约 1 小时视频 |

### 3. Google 生态集成

- **Google Workspace**：Gmail、Docs、Sheets 中的智能辅助
- **Google Cloud Vertex AI**：企业级部署
- **Android**：设备端 AI 能力
- **Google Search**：联网搜索增强

---

## 模型版本对比

| 特性 | Gemini 1.5 Pro | Gemini 1.5 Flash | Gemini 2.0 Flash | Gemini 2.5 Pro |
|-----|---------------|-----------------|-----------------|---------------|
| 上下文 | 1M tokens | 1M tokens | 1M tokens | 1M+ tokens |
| 速度 | 标准 | 快速 | 快速 | 标准 |
| 推理 | 强 | 中 | 强 | 极强 |
| 多模态 | 文本+图像+音频+视频 | 同左 | 同左+工具调用 | 同左 |
| 代码 | 强 | 中 | 强 | 极强 |
| 成本 | 中等 | 低 | 低 | 较高 |

---

## API 使用

### Python SDK

```python
import google.generativeai as genai

genai.configure(api_key="your-key")

# 文本生成
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content("解释量子计算的原理。")
print(response.text)

# 多模态输入
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content([
    "描述这张图片的内容",
    genai.upload_file("photo.jpg")
])
print(response.text)

# 流式输出
response = model.generate_content("写一篇 500 字的短文", stream=True)
for chunk in response:
    print(chunk.text, end="")
```

### 视频分析示例

```python
# 上传并分析视频
video_file = genai.upload_file("lecture.mp4")

response = model.generate_content([
    video_file,
    "请总结这个讲座的要点，并列出三个关键概念。"
])
print(response.text)
```

---

## 优势

- **原生多模态**：文本、图像、音频、视频一站式处理
- **超长上下文**：1M token 可处理整本书或长视频
- **Google 生态**：与 Google 产品深度集成
- **速度快**：Flash 版本延迟极低
- **工具调用**：2.0 系列支持函数调用和工具使用

## 局限

- **可用地区受限**：部分国家/地区不可用
- **中文能力**：中文处理不如专业中文模型
- **生态锁定**：与 Google 平台绑定较深
- **创意写作**：创意类任务有时偏保守
- **API 配额**：免费配额有限

---

## 应用场景

- **视频理解**：讲座摘要、视频内容审核
- **长文档分析**：论文研究、法律文档审查
- **多模态搜索**：基于图像和文本的联合搜索
- **企业知识库**：集成 Google Workspace 的智能助手
- **实时交互**：快速响应的客服和对话系统

---

## 下一步

- 访问 [Google AI Studio](https://aistudio.google.com) 免费体验
- 获取 Gemini API Key
- 尝试使用 Gemini 分析一段视频或音频
- 研究 Gemini 1M 上下文在实际项目中的应用
