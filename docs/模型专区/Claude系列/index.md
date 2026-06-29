# Claude 系列

> Anthropic 开发的 Claude 系列模型，以"合宪法 AI"（Constitutional AI）为核心方法论，在安全性、长上下文处理和细致理解方面树立了行业标杆。

---

## 发展历程

| 版本 | 发布时间 | 关键特性 |
|-----|---------|---------|
| Claude 1 | 2023.03 | 首批合宪法 AI 模型 |
| Claude 2 | 2023.07 | 100K 上下文、代码能力提升 |
| Claude 3 Haiku | 2024.03 | 轻量快速、高性价比 |
| Claude 3 Sonnet | 2024.03 | 平衡性能与速度 |
| Claude 3 Opus | 2024.03 | 最强版本、深度推理 |
| Claude 3.5 Sonnet | 2024.06 | 全面超越 Opus 的性价比之王 |
| Claude 3.5 Haiku | 2024.10 | 速度最快的智能模型 |
| Claude 3.5 Opus | 2024.10 | 全新巅峰 |

---

## 模型家族对比

| 特性 | Haiku（轻量） | Sonnet（均衡） | Opus（旗舰） |
|-----|-------------|---------------|-------------|
| 速度 | ⚡ 极快 | 快速 | 标准 |
| 推理能力 | 良好 | 优秀 | 卓越 |
| 代码能力 | 良好 | 优秀 | 卓越 |
| 成本 | 低 | 中等 | 高 |
| 适用场景 | 实时对话、简单任务 | 日常使用、开发辅助 | 复杂推理、研究分析 |

---

## 合宪法 AI（Constitutional AI）

### 核心理念
Claude 采用 **合宪法 AI** 方法，通过一套价值观准则（宪法）来指导模型行为，而非仅依赖大量人工反馈。

### 实现方式
1. **监督阶段**：使用宪法准则对模型输出进行自我批评和修订
2. **RLHF 阶段**：基于宪法原则训练偏好模型，而非纯人工偏好

### 优势
- 减少对大量人工标注的依赖
- 行为准则透明、可审查
- 在帮助性与安全性之间取得更好平衡

---

## 200K 上下文窗口

Claude 3.5 系列支持 **200,000 token** 上下文窗口，可处理：

- 整本《三体》三部曲
- 数百页技术文档
- 完整代码仓库
- 长时间对话历史

### 实际应用

```python
# 分析长文档示例
import anthropic

client = anthropic.Anthropic(api_key="your-key")

with open("长文档.pdf", "rb") as f:
    document = f.read()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4000,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": document}},
                {"type": "text", "text": "请总结这份文档的核心论点并提供关键证据。"}
            ]
        }
    ]
)

print(response.content[0].text)
```

---

## 核心优势

- **安全性领先**：合宪法 AI 让 Claude 更谨慎、更少有害输出
- **长上下文处理**：200K token 窗口，行业顶级
- **细致理解**：擅长解析复杂指令和微妙语境
- **拒绝机制**：面对不确定时，倾向承认而非编造
- **代码能力**：Claude 3.5 Sonnet 编程能力与 GPT-4o 相当甚至更优

## 局限

- **创意自由度较低**：安全约束有时会限制创意产出
- **不支持多模态输入**（截至当前版本）
- **API 可用地区有限**：部分区域需特殊方式访问
- **无插件/工具生态**：不像 GPTs 有丰富的第三方扩展

---

## API 使用

### 消息 API

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="你是专业的 Python 开发导师。",
    messages=[
        {"role": "user", "content": "解释一下 Python 装饰器的工作原理。"}
    ]
)

print(message.content[0].text)
```

### 流式响应

```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "写一首关于 AI 的诗"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## 应用场景

- **长文档分析**：论文审阅、合同审查、报告总结
- **代码审查**：大型代码库的理解与优化
- **内容审核**：安全合规的内容过滤
- **教育辅导**：耐心细致的知识讲解
- **写作辅助**：高质量的写作与润色

---

## 下一步

- 访问 [Anthropic Console](https://console.anthropic.com) 获取 API Key
- 阅读 Claude 提示工程指南
- 体验 Claude.ai 网页版对比不同版本
- 研究合宪法 AI 论文了解更多理论细节
