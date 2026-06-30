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
      text: 知识库指南
      link: /知识库/
    - theme: alt
      text: Agent 实践
      link: /AIAgent实践/

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
  - icon: 🧭
    title: 知识库指南
    details: 说明学习路径、内容入库标准、文档模板和维护清单，帮助持续把资料沉淀成高质量知识库。
    link: /知识库/
---

<section class="home-section">
  <div class="home-panel">
    <h2>📊 知识库概览</h2>
    <p>持续自动化采集 AI 前沿内容，英文资料翻译为中文，并按学习路径、专题知识和工程实践重新组织。每篇内容都尽量补齐概念解释、适用场景、实践步骤、来源线索与维护说明，便于检索、复用和持续扩展。</p>
    <div class="metric-grid">
      <div class="metric"><strong>42+</strong><span>已整理教程文档</span></div>
      <div class="metric"><strong>7</strong><span>知识库入口与分类</span></div>
      <div class="metric"><strong>8</strong><span>主流模型专题</span></div>
      <div class="metric"><strong>4+</strong><span>Agent 实战案例</span></div>
    </div>
  </div>
</section>

<section class="home-section">
  <div class="home-panel">
    <h2>推荐学习路径</h2>
    <p>如果不确定从哪里开始，可以先按目标选择路径，再进入对应栏目查找专题文档。</p>
    <ul class="update-list">
      <li><time>入门</time><span><a href="/初级知识/AI学习路线图/">AI 学习路线图</a> → <a href="/初级知识/人工智能入门/">人工智能入门</a> → <a href="/初级知识/Python与数据处理基础/">Python 与数据处理基础</a> → <a href="/初级知识/机器学习基础/">机器学习基础</a> → <a href="/初级知识/大语言模型基础/">大语言模型基础</a></span></li>
      <li><time>应用</time><span><a href="/进阶学习/提示词工程/">提示词工程</a> → <a href="/进阶学习/Embedding与向量数据库/">Embedding 与向量数据库</a> → <a href="/进阶学习/RAG检索增强/">RAG 检索增强</a> → <a href="/进阶学习/Agent智能体/">Agent 智能体</a> → <a href="/进阶学习/模型评估与基准/">模型评估</a></span></li>
      <li><time>工程</time><span><a href="/进阶学习/LLM应用架构/">LLM 应用架构</a> → <a href="/模型专区/开源模型部署选型/">开源模型部署选型</a> → <a href="/工具专区/部署运维/">部署运维</a> → <a href="/高级知识/模型训练与优化/">训练与优化</a></span></li>
    </ul>
  </div>
</section>

<section class="home-section">
  <div class="home-panel">
    <h2>最新更新</h2>
    <p>自动生成内容会持续追加到对应栏目，首页保留最近的站点级更新记录。</p>
    <ul class="update-list">
      <li><time>2026-06-30</time><span>重构采集逻辑：新增统一分类配置、结构化资源库、精选资源区块重建和每日采集报告，避免文章被无限追加成链接列表。</span></li>
      <li><time>2026-06-30</time><span>补齐初级知识体系：新增 AI 学习路线图、数学基础、Python 与数据处理、数据与特征工程、模型训练评估、NLP、CV、生成式 AI、提示词入门、AI 伦理安全与隐私。</span></li>
      <li><time>2026-06-29</time><span>补充 7 篇专题文档：Embedding 与向量数据库、LLM 应用架构、数据工程与合成数据、开源模型部署选型、LlamaIndex、部署运维、Agent 评估与可观测性。</span></li>
      <li><time>2026-06-29</time><span>新增 <a href="/知识库/">知识库指南</a>：补充学习路径、内容入库标准、文档模板和维护清单。</span></li>
      <li><time>2026-06-29</time><span>新增 <a href="/AIAgent实践/">AI Agent 实践</a> 专区：函数调用 Agent、RAG Agent 实战、多 Agent 协作。</span></li>
      <li><time>2026-06-29</time><span>切换为 VitePress 文档站结构，优化首页、导航、搜索、侧边栏和 Vercel 构建输出。</span></li>
    </ul>
  </div>
</section>
