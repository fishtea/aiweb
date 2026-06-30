# ComfyUI — 图像生成工作流

> ComfyUI 是一个基于**节点式编辑器**的 AI 图像生成工具。它将 Stable Diffusion 等模型的图像生成过程可视化为可拖拽、可连接的工作流节点，为创作者提供了无与伦比的灵活性和控制力。

---

## 工具概述

| 属性 | 详情 |
|------|------|
| **开发者** | Comfyanonymous (comfyanonymous) |
| **首次发布** | 2023 年初 |
| **最新版本** | 持续更新（2025/2026 活跃） |
| **许可** | GPL-3.0 |
| **核心语言** | Python + JavaScript (Web UI) |
| **GitHub** | [comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI) |

---

## 核心概念

根据 [ComfyUI 2025 入门指南](https://weirdwonderfulai.art/comfyui/getting-started-with-comfyui-in-2025) 和 [Sebastian Kamph 的 ComfyUI 教程](https://www.youtube.com/watch?v=23VkGD-4uwk)：

### 节点（Nodes）

ComfyUI 中的每个操作都是一个"节点"。常见的节点类型：

| 节点类型 | 功能 | 示例 |
|---------|------|------|
| **模型加载** | 加载 Checkpoint / LoRA | Load Checkpoint, Load LoRA |
| **输入** | 提示词、图像输入 | CLIP Text Encode, Load Image |
| **采样器** | 生成过程核心 | KSampler（控制步数、CFG、种子） |
| **潜空间处理** | VAE 编解码 | VAE Encode, VAE Decode |
| **输出** | 保存/预览结果 | Save Image, Preview Image |

### 工作流（Workflows）

工作流是节点的连接图。典型的 Text-to-Image 工作流：

```
[Checkpoint Loader] → [CLIP Text Encode (正面)]
                    → [CLIP Text Encode (负面)]
                    → [KSampler] → [VAE Decode] → [Save Image]
```

### 颜色编码

根据 Sebastian Kamph 的教程，ComfyUI 使用颜色标记数据类型：

- **粉色:** 模型权重
- **蓝色:** 潜在空间（Latent）
- **灰色:** 张量/数值数据
- **黄色:** 文本/提示词

---

## 为什么选择 ComfyUI？

对比其他图像生成工具：

| 特性 | ComfyUI | Automatic1111 WebUI | Midjourney |
|------|---------|-------------------|------------|
| 工作流可视化 | ✅ 节点式连接 | ❌ 表单式 | ❌ 封闭 |
| 灵活性 | ✅ 最高 | ⚠️ 中等 | ❌ 低 |
| 内存效率 | ✅ 极高（按需加载） | ⚠️ 中等 | N/A |
| 自定义节点 | ✅ 丰富的社区扩展 | ✅ 扩展插件 | ❌ 无 |
| 学习曲线 | ⚠️ 中等偏高 | ✅ 低 | ✅ 最低 |
| 批量处理 | ✅ 原生支持 | ✅ 支持 | ❌ 有限 |

---

## 如何开始

### 本地安装

**最低硬件要求:**
- GPU 8GB+ VRAM（推荐 12GB+）
- 支持 CUDA 的 NVIDIA 显卡

**安装方式:**

```bash
# 方式 1: 直接 Git 克隆
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
python main.py

# 方式 2: 一键安装器（推荐初学者）
# 下载 ComfyUI 一键安装包
```

安装完成后，浏览器访问 `http://127.0.0.1:8188`

### 基础工作流

1. 加载 Checkpoint 模型（从 HuggingFace 或 CivitAI 下载）
2. 添加 CLIP Text Encode 节点（正面和负面提示词）
3. 添加 KSampler 节点，设置步数（20-50）、CFG（7-10）
4. 添加 VAE Decode 和 Save Image 节点
5. 连接所有节点，点击 Queue Prompt 生成

### 云部署

使用 **RunPod** （$0.40/小时起）等云 GPU 服务部署 ComfyUI，无需本地 GPU。

---

## 自定义节点生态

ComfyUI 拥有庞大的自定义节点社区，推荐值得关注的节点包：

| 节点包 | 功能 |
|--------|------|
| **ComfyUI-Manager** | 节点包管理器（必装） |
| **WAS Node Suite** | 丰富的图像处理节点 |
| **ComfyUI-Impact-Pack** | 增强的工作流节点 |
| **Efficiency Nodes** | 简化和加速工作流 |
| **AnimateDiff** | 视频生成支持 |

---

## 优势与局限

**优势:**
- **极致灵活:** 可构建任何图像生成工作流
- **内存高效:** 仅加载工作流所需的组件
- **丰富的扩展:** 数千个社区自定义节点
- **支持多模型:** SD1.5、SDXL、SD3、FLUX、MaskGCT 等
- **可复现:** 工作流可以 .json 格式共享和导出

**局限:**
- **学习曲线较陡:** 需要理解节点连接逻辑
- **调试困难:** 工作流错误不易定位
- **UI 直观性不足:** 相比 Automatic1111 不够友好
- **节点碎片化:** 太多选择让人困惑

---

**参考资料：**
- [Getting Started with ComfyUI 2025 (WeirdWonderfulAI)](https://weirdwonderfulai.art/comfyui/getting-started-with-comfyui-in-2025)
- [ComfyUI for Beginners (Sebastian Kamph YouTube)](https://www.youtube.com/watch?v=23VkGD-4uwk)
- [ComfyUI Absolute Beginner Guide (Winbush YouTube)](https://www.youtube.com/watch?v=6dXpgL1-YdM)
- [ComfyUI Reddit Getting Started 2025](https://www.reddit.com/r/StableDiffusion/comments/1icbucd/getting_started_with_comfyui_2025)
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 10:42:21*
*资源区块更新时间：2026-06-30 10:25:06*
