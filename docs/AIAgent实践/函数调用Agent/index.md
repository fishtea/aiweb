# 📞 函数调用 Agent

从零搭建支持工具调用的 AI Agent，让 LLM 具备与外部世界交互的能力。

---

## 📖 概述

函数调用（Function Calling / Tool Calling）是 AI Agent 的核心能力。它允许 LLM 不仅输出文本，还能生成结构化的函数调用指令，从而与外部工具、API 和知识库交互。没有函数调用，LLM 只是一个文本生成器；有了它，LLM 才真正成为一个"智能体"。

> 来源：[Prompt Engineering Guide — Function Calling in AI Agents](https://www.promptingguide.ai/agents/function-calling)

### 核心流程

1. **用户提问** → Agent 收到请求（如："巴黎天气如何？"）
2. **组装上下文** → 系统消息 + 工具定义 + 用户消息组合发送给 LLM
3. **工具决策** → LLM 判断是否需要调用工具，输出结构化调用（含参数）
4. **执行函数** → 开发者代码执行实际函数（如调天气 API）
5. **观察结果** → 工具返回数据
6. **生成回答** → 观察结果 + 完整历史传回模型 → 输出最终答案

---

## 🔧 工具定义（Tool Definitions）

工具定义是 Agent 的"说明书"，是 LLM 知道有哪些工具可用以及何时使用的唯一方式。

### 工具定义的组成部分

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 唯一标识符 | `get_current_weather` |
| `description` | 何时使用该工具 | "获取指定城市的当前天气" |
| `parameters` | 输入参数（类型+描述） | `{location: string, unit: enum}` |

### 示例：天气查询工具定义

```json
{
  "type": "function",
  "function": {
    "name": "get_current_weather",
    "description": "获取指定城市的当前天气。当用户询问某个城市天气时使用此工具。",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "城市名称，如 北京"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  }
}
```

> 工具定义会占用上下文 token，直接影响成本和延迟。保持简洁但要描述清晰。

---

## 🔄 Agent 循环：行动与观察

Agent 的核心运行机制是一个循环：

```
行动 → 环境响应 → 观察 → 决策（重复或结束）
```

### 实际追踪示例（搜索 OpenAI 最新新闻）

```
用户: "OpenAI 最新新闻"
Agent 思考: 我需要关于 OpenAI 新闻的最新信息，应该使用 web_search 工具。
行动: web_search(query="OpenAI latest news announcements")
观察: [搜索返回的结果中包含多篇 OpenAI 最新文章]
Agent 思考: 现在有了足够信息，可以总结给用户。
回答: "以下是 OpenAI 的最新动态..."
```

> 观察结果会自动成为下一次迭代的上下文。复杂任务可能需要多次工具调用，每次调用都累积到对话上下文中。

---

## 🐛 调试函数调用

启用"返回中间步骤"可查看：
- 调用了哪些工具
- 传入的参数
- 工具返回的观察结果
- 每一步的 token 消耗

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 选择了错误工具 | 工具描述不够清晰 | 优化 description 字段 |
| 参数错误 | 参数定义不完整 | 确保 required 和 enum 正确 |
| 上下文缺失 | 工具定义信息不足 | 在描述中添加使用场景指引 |
| 观察结果处理错误 | 模型误解了返回值 | 标准化工具输出格式 |

---

## 💡 最佳实践

### 1. 描述要具体
- ❌ "搜索网络"
- ✅ "搜索网络获取最新信息。当用户问到训练数据之后的事件、新闻或实时数据时使用此工具"

### 2. 在系统提示中补充指引
```python
system_message = """
你拥有以下工具：
- web_search: 用于查询任何需要最新信息的问题
- calculator: 用于数学计算
- knowledge_base: 用于搜索内部文档
优先使用最合适的工具完成任务。
"""
```

### 3. 使用结构化输出
让 LLM 返回 JSON 格式的函数调用，而不是自然语言描述，方便程序化处理。

### 4. 限制可用工具数量
对简单任务只暴露少量工具，避免 LLM 选择困难。对有大量工具的场景，使用工具搜索（Tool Search）功能按需加载。

---

## 📚 参考来源

- [Prompt Engineering Guide — Function Calling in AI Agents](https://www.promptingguide.ai/agents/function-calling)
- [OpenAI API — Function Calling Guide](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI Function Calling - AI Agents SDK (YouTube)](https://www.youtube.com/watch?v=NT_ApmD_JPo)

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:11:39*
*资源区块更新时间：2026-06-30 11:11:09*
*资源区块更新时间：2026-06-30 10:42:21*
*资源区块更新时间：2026-06-30 10:25:06*
