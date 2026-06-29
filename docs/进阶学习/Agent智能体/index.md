# Agent 智能体：从被动问答到自主行动

## 什么事 Agent？

**普通 LLM 调用**（被动）：

```
你："上海的天气怎么样？"
模型："上海的天气是 25°C，多云。"
```

这就是一个问-答循环。模型**只有信息**，**没有行动能力**。它不知道上海的天气信息需要去查实时 API，它只是在训练数据中见过类似的问题和答案的配对。

**Agent 调用**（主动）：

```
你："帮我安排明天在上海的商务行程，包括航班、酒店和会议提醒。"

Agent 开始执行：
  — 工具调用：search_flights("深圳", "上海", "明天")
  — 工具调用：search_hotels("上海陆家嘴", "明晚")
  — 工具调用：get_weather("上海", "明天")
  — 工具调用：create_calendar_event(...)
  
Agent："已为您预订明天早上 8:30 深圳→上海的航班，..."
```

区别清晰：Agent **拥有工具**，并且**自主决定调用顺序**。它不是一个问答机器人，它是一个**自主行动体**。

---

## ReAct 循环：Agent 的运行内核

ReAct = Reasoning + Acting。这是目前最主流的 Agent 范式。看一个完整的执行 trace：

### 实际问题

> "我刚把代码推到 GitHub，请帮我对 main 分支做一次 code review，如果发现问题就提交 issue。"

### 执行日志

```
=== ReAct 循环开始 ===

[THOUGHT 1]
用户要求做 code review。我需要：
1. 获取 main 分支的最新 diff
2. 逐文件审查代码
3. 如果发现问题，创建 issue
先获取 diff。

[ACTION 1]  
工具：run_command
参数：{"command": "git diff main~1 main --stat"}
结果："src/auth.py    | 15 +++++++
     src/api.py     | 8 +++---
     src/db.py      | 23 +++++++++++----
     3 files changed, 38 insertions(+), 8 deletions(-)"

[OBSERVATION 1]
有三个文件被修改。先看 auth.py 的详细 diff。

[THOUGHT 2]
auth.py 的修改涉及用户认证模块，风险较高。先看完整 diff。

[ACTION 2]
工具：run_command
参数：{"command": "git diff main~1 main -- src/auth.py"}
结果："+def validate_token(token):
    +    if len(token) < 32:
    +        raise ValueError('Token too short')
    +    # TODO: add signature verification
    +    return True"

[OBSERVATION 2]
validate_token 函数有一个 TODO 注释标注了签名验证缺失。这是一个安全问题。
需要创建一个 issue 标记这个漏洞。

[THOUGHT 3]
发现安全漏洞：validate_token 缺少签名验证。这应该标记为 high priority issue。
立即创建 issue。

[ACTION 3]
工具：github_create_issue
参数：{
  "repo": "user/project",
  "title": "Security: validate_token missing signature verification",
  "body": "在 auth.py 新增的 validate_token 函数中，**没有实现 token 签名验证**。\n\n当前实现只检查了 token 长度，但没有验证 token 是否由可信签发者签名。\n\n风险等级：高\n建议：在 TODO 标注处实现 JWT 或 HMAC 签名验证。",
  "labels": ["security", "bug"]
}
结果："Issue #42 created"

[THOUGHT 4]
问题已创建。继续审查剩余文件。

[ACTION 4]
工具：run_command
参数：{"command": "git diff main~1 main -- src/api.py"}
...

=== 最终输出 ===
"Code review 完成。发现 2 个问题：
1. 🔴 [高] auth.py: validate_token 缺少签名验证 → Issue #42 已创建
2. 🟡 [中] api.py: 删除了一个重复的输入校验，建议保留至少一层校验

其他文件无重大问题。"
```

### 循环结构

```
      ┌──────────────────────────┐
      │         THOUGHT          │  ← 推理当前状态，决定下一步
      │     （思考当前状态）       │
      └──────────┬───────────────┘
                 │
                 ▼
      ┌──────────────────────────┐
      │         ACTION           │  ← 调用工具执行操作
      │     （执行具体动作）       │
      └──────────┬───────────────┘
                 │
                 ▼
      ┌──────────────────────────┐
      │      OBSERVATION         │  ← 获取工具返回的结果
      │     （观察工具输出）       │
      └──────────┬───────────────┘
                 │
                 │（回到 THOUGHT，继续循环）
                 ▼
         直到任务完成 → FINAL ANSWER
```

**关键洞察**：Agent 的"思考"不是真的思考——它是通过语言推理来规划下一步。模型在"自言自语"中逐步逼近目标。

---

## Agent 的三个核心组件

### 1. 工具（Tools）

工具是 Agent 与外部世界交互的接口。没有工具的 Agent 就是一个普通 LLM。

```
┌─ 信息获取类工具 ─────────────────────────────┐
│  search_web(query)       → 搜索引擎结果      │
│  read_file(path)         → 读取本地文件      │
│  query_database(sql)     → 执行 SQL 查询     │
│  call_api(endpoint)      → 调用外部 API      │
└──────────────────────────────────────────────┘

┌─ 执行操作类工具 ─────────────────────────────┐
│  run_command(cmd)        → 执行命令行        │
│  write_file(path, text)  → 写入文件          │
│  send_email(to, body)    → 发送邮件          │
│  create_issue(repo, ...) → 创建 Issue       │
└──────────────────────────────────────────────┘

┌─ 辅助推理类工具 ─────────────────────────────┐
│  python_repl(code)       → 执行 Python 计算  │
│  calculator(expr)        → 精确数学计算      │
│  decompress_pdf(path)    → PDF 文本提取      │
└──────────────────────────────────────────────┘
```

**工具设计的黄金法则**：每个工具只做一件事，且接口清晰。工具描述对于 Agent 选对工具至关重要——写描述时不是写给人类看的，是写给 LLM 看的。

```
# ❌ 差的工具描述
"这个工具可以处理数据"

# ✅ 好的工具描述
"search_web(query: str) → list[dict]: 执行 Google 搜索并返回 Top-5 结果。
当用户问及时事、最新信息、或外部数据时使用此工具。
如果用户的问题涉及本地文件，请勿使用此工具。"
```

### 2. 记忆（Memory）

Agent 需要记忆来维持一致性。三个层级：

| 记忆类型 | 存储内容 | 生命周期 | 访问速度 |
|---------|---------|---------|---------|
| 短期记忆 | 当前对话的完整上下文 | 单次对话 | 快（上下文窗口内） |
| 长期记忆 | 跨会话的关键信息 | 持久化 | 慢（需要检索） |
| 工作记忆 | 当前任务的中间状态 | 任务完成即丢弃 | 最快（显式状态） |

**实现模式**：

```python
class AgentMemory:
    def __init__(self):
        self.short_term = []           # 当前对话历史
        self.long_term = VectorStore()  # 跨会话记忆
        self.working = {}              # 结构化中间状态
    
    def add_to_short(self, entry):
        self.short_term.append(entry)
        if len(self.short_term) > self.max_turns:
            self.summarize_and_compact()  # 压缩历史
    
    def retrieve_relevant(self, query, k=5):
        return self.long_term.search(query, k)
    
    def set_working(self, key, value):
        self.working[key] = value
    
    def get_working(self, key):
        return self.working.get(key)
```

### 3. 规划（Planning）

复杂任务需要规划。两种主要模式：

**ReAct（实时规划）**：想到哪做到哪，边做边调整。适合探索性任务。
**Plan-and-Execute（先计划再执行）**：先制定完整计划，再逐步执行。适合确定性任务。

```
Plan-and-Execute 示例：

[PLAN]
Step 1: 搜索"2024 年新能源汽车销量排名"
Step 2: 获取每家公司 Q1 2025 的财报数据
Step 3: 对比增长率并生成分析报告
Step 4: 将报告保存为 markdown 文件

[EXECUTION]
执行 Step 1 → 结果：比亚迪 300 万辆，特斯拉 180 万辆...
执行 Step 2 → 结果：比亚迪 Q1 增长 15%，特斯拉 Q1 下降 8%...
执行 Step 3 → 生成报告...
执行 Step 4 → 已保存
```

**混合策略（推荐）**：先做高层面规划，然后在每个步骤中采用 ReAct 式探索。

---

## Agent vs RAG：核心区别

| 维度 | RAG | Agent |
|------|-----|-------|
| 核心目标 | 让模型知道"不知道的事" | 让模型做"不会做的事" |
| 交互方式 | 单轮：检索→生成 | 多轮：思考→行动→观察→... |
| 复杂度 | 低，流水线式 | 高，循环式 |
| 工具数量 | 0-1 个（检索器） | 多个，可组合 |
| 状态管理 | 无状态 | 有状态 |
| 失败模式 | 检索不到相关内容 | 陷入死循环/错误决策 |

**两者不是互斥的**。最佳实践是 Agent + RAG 结合——Agent 使用 RAG 工具来获取信息，再基于获取的信息做推理和行动。

---

## Agent 实战：构建一个简单 Agent

```python
# 一个最小化 Agent 实现（完整版见附录）
class MinimalAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_steps = 10
    
    def run(self, task):
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": task}]
        
        for step in range(self.max_steps):
            response = self.llm(messages)
            action = self.parse_action(response)
            
            if action["type"] == "finish":
                return action["result"]
            
            observation = self.tools[action["name"]](**action["args"])
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "tool", "content": str(observation)})
        
        return "Max steps reached"
```

**生产级 Agent 框架**（选一个即可）：

| 框架 | 语言 | 特色 | 适用场景 |
|------|------|------|---------|
| LangChain | Python | 生态最丰富 | 通用 Agent 开发 |
| CrewAI | Python | 多 Agent 协作 | 角色分工场景 |
| AutoGen | Python | 多 Agent 对话 | 复杂任务分解 |
| Semantic Kernel | C#/Python | Azure 集成 | 企业 .NET 环境 |
| DSPy | Python | 编译优化 | 需要调优 Agent 行为 |

---

## 常见失败模式

```
□ 工具幻觉：Agent 调用了一个不存在的工具名
   → 解决方案：约束工具选择空间，用 JSON schema 做验证

□ 死循环：Agent 反复调用同一个工具
   → 解决方案：设置 max_steps，加入"重复检测"逻辑

□ 累积误差：早期步骤的微小错误被放大
   → 解决方案：关键步骤加入人工确认节点（human-in-the-loop）

□ 上下文溢出：多轮工具调用后上下文窗口被撑满
   → 解决方案：压缩历史、滚动窗口、总结中间结果

□ 权限越界：Agent 执行了不应该执行的操作
   → 解决方案：工具层做权限校验，敏感操作需二次确认
```

## 下一步

要设计更好的 Agent，你需要精通 [提示词工程 →](../提示词工程/index.md)——因为 Agent 的思考逻辑本质上是由 prompt 驱动的推理链路。
