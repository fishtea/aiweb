---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "AI 学习路径导航"
  text: "自动更新的中文 AI 教程库"
  tagline: 每天采集 AI 新内容，英文资料翻译为中文，沉淀成可检索、可持续扩展的教程、模型、工具与 Agent 实战知识库。
  image:
    src: /logo.svg
    alt: AI 学习路径导航
  actions:
    - theme: brand
      text: 开始学习
      link: /初级知识/
    - theme: alt
      text: Agent 实践
      link: /AIAgent实践/
    - theme: alt
      text: 模型专区
      link: /模型专区/

features:
  - icon: 📚
    title: 初级知识
    details: 人工智能入门、机器学习基础、深度学习入门、大语言模型基础，适合从零建立 AI 知识框架。
    link: /初级知识/
  - icon: 🔧
    title: 进阶学习
    details: 覆盖模型微调、RAG、提示词工程、Agent 智能体与模型评估，连接概念和工程落地。
    link: /进阶学习/
  - icon: 🧠
    title: 高级知识
    details: 持续整理训练优化、AI 安全、多模态模型和前沿架构研究，便于跟踪技术演进。
    link: /高级知识/
  - icon: 🤖
    title: 模型专区
    details: 统一沉淀 GPT、Claude、LLaMA、DeepSeek、Gemini、Qwen、Stable Diffusion、Mixtral 等模型资料。
    link: /模型专区/
  - icon: 🛠️
    title: 工具专区
    details: 汇总 LangChain、ComfyUI、vLLM、Hugging Face、PyTorch、TensorFlow、Ollama 等工具教程。
    link: /工具专区/
  - icon: 🧪
    title: AI Agent 实践
    details: 增加函数调用 Agent、RAG Agent、多 Agent 协作等可复用实战案例，后续适合持续自动扩展。
    link: /AIAgent实践/
---

<section class="home-section">
  <div class="home-panel">
    <h2>📊 知识库概览</h2>
    <p>持续自动化采集 AI 前沿内容，英文资料翻译为中文，沉淀为结构化文档并自动发布。覆盖学习路径、主流模型、热门工具与 Agent 实战，随内容增长持续扩展。</p>
    <div class="metric-grid">
      <div class="metric"><strong>35+</strong><span>已整理教程文档</span></div>
      <div class="metric"><strong>6</strong><span>核心学习分类</span></div>
      <div class="metric"><strong>8</strong><span>主流模型专题</span></div>
      <div class="metric"><strong>3+</strong><span>Agent 实战案例</span></div>
    </div>
  </div>
</section>

<section class="home-section">
  <div class="home-panel">
    <h2>最新更新</h2>
    <p>自动生成内容会持续追加到对应栏目，首页保留最近的站点级更新记录。</p>
    <ul class="update-list">
      <li><time>2026-06-30</time><span>新增 <a href="/AIAgent实践/">AI Agent 实践</a> 专区：函数调用 Agent、RAG Agent 实战、多 Agent 协作。</span></li>
      <li><time>2026-06-29</time><span>切换为 VitePress 文档站结构，优化首页、导航、搜索、侧边栏和 Vercel 构建输出。</span></li>
      <li><time>2026-06-28</time><span>完成 35 篇 AI 学习文档整理，内容面向中文读者重新组织。</span></li>
    </ul>
  </div>
</section>
