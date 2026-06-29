# ComfyUI：像搭乐高一样组装图像生成

> 当大部分人在使用 Automatic1111 的"一键生成"时，追求精确的人转向了 ComfyUI。
> 它不是"更难的替代品"，而是"更可控的创作工具"。

---

## 为什么叫"节点式"工作流？

想象你在做一碗拉面：

**Automatic1111（类比：拉面套餐）**
```
店员：你要什么拉面？
你：豚骨拉面（选 preset）
店员：3 分钟后给你一碗
【你无法调整火候、面硬度、汤浓度】
```

**ComfyUI（类比：开放式厨房）**
```
你：
  1. 烧水（KSampler 节点）
  2. 煮面（Checkpoint Loader + 正/负提示词）
  3. 调汤（ControlNet 调节）
  4. 加溏心蛋（LoRA 注入）
  5. 摆盘（VAE Decode → Save Image）
【每一步你都可以精确调整参数】
```

**ComfyUI 的核心理念**：把图像生成拆解为可独立控制、可串联、可复用的节点。

---

## 基础节点解释（从零开始）

### 最简单的 T2I 工作流

```
Load Checkpoint ──→ CLIP Text Encode (正面提示词) ──┐
                    CLIP Text Encode (负面提示词) ──┤
                                                    ↓
                                               KSampler ──→ VAE Decode ──→ Save Image
                                                    ↑
                                             Empty Latent Image
```

**每个节点的角色**：
| 节点 | 中文名 | 功能 |
|------|-------|------|
| Load Checkpoint | 加载模型 | 选择 SD1.5 / SDXL / FLUX 底模 |
| CLIP Text Encode | 编码提示词 | 把文字变成模型能理解的向量 |
| Empty Latent Image | 初始化潜图 | 设置宽高，生成纯噪声 |
| KSampler | 采样器 | 核心——逐步去噪，把噪声变成潜图 |
| VAE Decode | 解码器 | 把潜空间的图转为像素图 |
| Save Image | 保存 | 输出 PNG/JPG |

### 关键参数解析

**KSampler 里的参数决定了 80% 的出图质量**：

**Steps（步数）**：
- 默认 20 | SDXL 推荐 25-30 | FLUX 推荐 28-50
- 步数越多越精细，但边际效益递减
- 技巧：先用 20 步快速摸草图，定稿后用 40 步出最终图

**CFG（Classifier Free Guidance）**：
- 范围 1-20+ | 默认 7
- CFG 越高→越忠实于提示词→但可能偏"味精感"
- CFG 越低→模型自由发挥空间越大→可能偏离提示词
- 技巧：高 CFG(12-15) 配写真风，低 CFG(4-6) 配艺术风

**Sampler Name（采样器）**：
- **DPM++ 2M Karras**：高质素，速度快（默认推荐）
- **Euler a**：收敛快，适合快速测试
- **DPM++ 2M SDE Karras**：质量最高，但慢
- **DDIM**：支持步数很少（4-10 步）就出图

---

## 常用工作流模板

### ① 文生图（T2I）—— 标准

最基本的流程，适合概念设计、插图生成。

```
[Checkpoint] → [正面提示词] ─┐
                [负面提示词]  ├→ [KSampler] → [VAE Decode] → [Save]
                              │
                 [Latent Image]
```

### ② 图生图（I2I）—— 改图

把已有图片按新提示词重新生成。

```
[Load Image] → [VAE Encode] ─┐
                              ├→ [KSampler] (denoise=0.6)
[Checkpoint] → [提示词] ────┘    → [VAE Decode] → [Save]

关键参数：denoise (降噪强度)
0.0 = 完全不变  0.3 = 微调颜色/光影
0.6 = 改变构图  1.0 = 完全重画
```

### ③ Inpainting —— 局部重绘

只修改图片的特定区域。

```
[Load Image + Mask] → [VAE Encode] ─┐
                                      ├→ [KSampler] (denoise=0.8-1.0)
[Checkpoint (inpaint版)] → [提示词] ─┘
                                      → [VAE Decode] → [Save]

Mask = 你画的选区，白色=要改的部分
```

### ④ 文生视频 —— AnimateDiff

用 AnimateDiff 插件把静态图变成短视频。

```
[Checkpoint] → [提示词] → [KSampler] + [AnimateDiff Loop]
                           → 连续 16 帧 → [Video Combine] → .mp4
```

---

## 自定义节点生态

ComfyUI 最强大的地方——社区贡献的**第三方节点**。

### 必装节点管理器

```bash
# 在 ComfyUI 安装目录
git clone https://github.com/ltdrdata/ComfyUI-Manager custom_nodes/
```

**有了 Manager 后，你可以直接在 UI 里搜索安装节点。**

### 核心扩展推荐

| 节点包 | 功能 | 必装指数 |
|--------|------|---------|
| **ComfyUI-Manager** | 节点安装/更新/管理 | ⭐⭐⭐⭐⭐ |
| **ComfyUI-Impact-Pack** | 综合工具集（分割、放大、遮罩） | ⭐⭐⭐⭐⭐ |
| **Efficiency Nodes** | 简化工作流节点 | ⭐⭐⭐⭐ |
| **WAS Node Suite** | 文本/图像工具包 | ⭐⭐⭐⭐ |
| **rgthree-comfy** | 快捷节点（超级提示词、种子箱） | ⭐⭐⭐⭐ |
| **ComfyUI-KJNodes** | 批处理/动画 | ⭐⭐⭐ |
| **AnimateDiff-Evolved** | 视频生成 | ⭐⭐⭐ |
| **ComfyUI-Frame-Interpolation** | 视频帧插值 | ⭐⭐⭐ |

---

## ComfyUI 为什么更好？

| 维度 | ComfyUI | Automatic1111 |
|------|---------|--------------|
| **可复现性** | ✅ 工作流存为 JSON，下次直接加载 | ❌ 需要记参数，手动设置 |
| **显存效率** | ✅ 更少显存消耗 | ❌ 资源浪费 |
| **批处理** | ✅ 原生支持批量队列 | ⚠️ 需要插件 |
| **工作流分享** | ✅ JSON 文件，社区丰富 | ⚠️ 只能截图 |
| **学习曲线** | ❌ 陡峭 | ✅ 简单 |
| **新手友好** | ❌ 需要理解原理 | ✅ 入门快 |
| **定制化** | ✅ 无限可能 | ❌ 受限 |
| **调试** | ✅ 能可视化每一步 | ❌ 黑盒 |

**最简单的选择建议**：
- 你只偶尔生成几张图 → **A1111**
- 你要每天工作、批量生成、精确控制 → **ComfyUI**
- 你想用 FLUX / SD3 / AnimateDiff → **ComfyUI（很多模型只在 ComfyUI 上可用）**

---

## 工作流分享文化

ComfyUI 有一个独特的文化——分享工作流。

**工作流文件**：一个 `.json` 文件，包含所有节点、参数、连接关系。

**如何分享**：直接把 JSON 拖入 ComfyUI 窗口，自动加载完整工作流。

**去哪里找**：
- [OpenArt Workflows](https://openart.ai/workflows)
- [CivitAI](https://civitai.com) 的工作流板块
- [ComfyUI Workflows 网站](https://comfyworkflows.com)
- Reddit r/comfyui

---

> **一句话总结**：ComfyUI 是面向"创造者"而非"使用者"的工具。如果你愿意花时间搭建工作流，你能获得全方位的控制权和最高质量的输出。门槛高，天花板也高。
