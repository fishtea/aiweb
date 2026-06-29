import { defineConfig } from 'vitepress'

const nav = [
  { text: '首页', link: '/' },
  { text: '初级知识', link: '/初级知识/' },
  { text: '进阶学习', link: '/进阶学习/' },
  { text: '高级知识', link: '/高级知识/' },
  { text: '模型专区', link: '/模型专区/' },
  { text: '工具专区', link: '/工具专区/' },
  { text: 'AI Agent 实践', link: '/AIAgent实践/' }
]

const sidebar = {
  '/初级知识/': [
    {
      text: '初级知识',
      items: [
        { text: '总览', link: '/初级知识/' },
        { text: '人工智能入门', link: '/初级知识/人工智能入门/' },
        { text: '机器学习基础', link: '/初级知识/机器学习基础/' },
        { text: '深度学习入门', link: '/初级知识/深度学习入门/' },
        { text: '大语言模型基础', link: '/初级知识/大语言模型基础/' }
      ]
    }
  ],
  '/进阶学习/': [
    {
      text: '进阶学习',
      items: [
        { text: '总览', link: '/进阶学习/' },
        { text: '模型微调技术', link: '/进阶学习/模型微调技术/' },
        { text: 'RAG 检索增强', link: '/进阶学习/RAG检索增强/' },
        { text: 'Agent 智能体', link: '/进阶学习/Agent智能体/' },
        { text: '提示词工程', link: '/进阶学习/提示词工程/' },
        { text: '模型评估与基准', link: '/进阶学习/模型评估与基准/' }
      ]
    }
  ],
  '/高级知识/': [
    {
      text: '高级知识',
      items: [
        { text: '总览', link: '/高级知识/' },
        { text: '模型训练与优化', link: '/高级知识/模型训练与优化/' },
        { text: 'AI 安全与对齐', link: '/高级知识/AI安全与对齐/' },
        { text: '多模态模型', link: '/高级知识/多模态模型/' },
        { text: '模型架构研究', link: '/高级知识/模型架构研究/' }
      ]
    }
  ],
  '/模型专区/': [
    {
      text: '模型专区',
      items: [
        { text: '总览', link: '/模型专区/' },
        { text: 'GPT 系列', link: '/模型专区/GPT系列/' },
        { text: 'Claude 系列', link: '/模型专区/Claude系列/' },
        { text: 'LLaMA 系列', link: '/模型专区/LLaMA系列/' },
        { text: 'DeepSeek', link: '/模型专区/DeepSeek/' },
        { text: 'Gemini 系列', link: '/模型专区/Gemini系列/' },
        { text: 'Qwen 系列', link: '/模型专区/Qwen系列/' },
        { text: 'Stable Diffusion', link: '/模型专区/StableDiffusion/' },
        { text: 'Mixtral 系列', link: '/模型专区/Mixtral系列/' }
      ]
    }
  ],
  '/工具专区/': [
    {
      text: '工具专区',
      items: [
        { text: '总览', link: '/工具专区/' },
        { text: 'LangChain', link: '/工具专区/LangChain/' },
        { text: 'AutoGPT', link: '/工具专区/AutoGPT/' },
        { text: 'ComfyUI', link: '/工具专区/ComfyUI/' },
        { text: 'vLLM', link: '/工具专区/vLLM/' },
        { text: 'Hugging Face', link: '/工具专区/HuggingFace/' },
        { text: 'PyTorch', link: '/工具专区/PyTorch/' },
        { text: 'TensorFlow', link: '/工具专区/TensorFlow/' },
        { text: 'Ollama', link: '/工具专区/Ollama/' }
      ]
    }
  ],
  '/AIAgent实践/': [
    {
      text: 'AI Agent 实践',
      items: [
        { text: '总览', link: '/AIAgent实践/' },
        { text: '函数调用 Agent', link: '/AIAgent实践/函数调用Agent/' },
        { text: 'RAG Agent 实战', link: '/AIAgent实践/RAGAgent实战/' },
        { text: '多 Agent 协作', link: '/AIAgent实践/多Agent协作/' }
      ]
    }
  ]
}

export default defineConfig({
  lang: 'zh-CN',
  title: 'AI 学习路径导航',
  description: '每日自动更新的中文 AI 教程、模型、工具与 Agent 实践知识库',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,
  head: [
    ['meta', { name: 'theme-color', content: '#2563eb' }],
    ['meta', { name: 'keywords', content: 'AI教程,人工智能,大语言模型,AI Agent,RAG,提示词工程,模型微调' }]
  ],
  themeConfig: {
    logo: '/logo.svg',
    nav,
    sidebar,
    outline: {
      level: [2, 3],
      label: '本页目录'
    },
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
              modal: {
                displayDetails: '显示详情',
                resetButtonTitle: '清除搜索',
                backButtonTitle: '关闭搜索',
                noResultsText: '没有找到相关内容',
                footer: {
                  selectText: '选择',
                  selectKeyAriaLabel: '回车',
                  navigateText: '切换',
                  navigateUpKeyAriaLabel: '向上',
                  navigateDownKeyAriaLabel: '向下',
                  closeText: '关闭',
                  closeKeyAriaLabel: 'Esc'
                }
              }
            }
          }
        }
      }
    },
    editLink: {
      pattern: 'https://github.com/fishtea/aiweb/edit/master/docs/:path',
      text: '在 GitHub 上编辑此页'
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/fishtea/aiweb' }
    ],
    footer: {
      message: '每日自动采集、翻译与生成 AI 学习内容',
      copyright: 'Copyright © 2026 AI 学习路径导航'
    },
    lastUpdated: {
      text: '最后更新',
      formatOptions: {
        dateStyle: 'medium',
        timeStyle: 'short'
      }
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '回到顶部',
    langMenuLabel: '语言'
  }
})
