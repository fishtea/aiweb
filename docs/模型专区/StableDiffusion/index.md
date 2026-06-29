# Stable Diffusion

> Stability AI 开发的 Stable Diffusion 是开源文生图领域的标杆模型，让 AI 图像生成从实验室走向大众。

---

## 发展历程

| 版本 | 发布时间 | 参数量 | 关键特性 |
|-----|---------|-------|---------|
| SD 1.4 | 2022.08 | 0.86B | 首个公开版本 |
| SD 1.5 | 2022.10 | 0.86B | 社区广泛采用的基准版 |
| SD 2.1 | 2022.12 | 0.86B | 改进的人体生成 |
| SDXL | 2023.07 | 2.6B | 分辨率翻倍、质量飞跃 |
| SDXL Turbo | 2023.11 | 2.6B | 实时生成（1-4步） |
| SD 3 | 2024.06 | 2B/8B | 全新架构、文字渲染 |
| SD 3.5 | 2024.10 | 2B/8B | 质量与稳定性提升 |

---

## 核心技术原理

### 潜在扩散模型（LDM）

Stable Diffusion 基于 **潜在扩散模型**，核心流程：

1. **编码**：VAE 编码器将图像压缩到潜在空间
2. **扩散**：在潜在空间中进行前向加噪和反向去噪
3. **引导**：文本提示通过 CLIP 编码器引导去噪方向
4. **解码**：VAE 解码器将潜在表示恢复为图像

```
文本提示 → [CLIP编码器] → 文本嵌入
                               ↓
随机噪声 → [U-Net去噪] → 潜在表示 → [VAE解码器] → 生成图像
            ↑ 迭代 T 步
```

### SDXL vs SD1.5 架构对比

| 特性 | SD 1.5 | SDXL |
|-----|-------|------|
| 参数 | 0.86B | 2.6B |
| 基础分辨率 | 512×512 | 1024×1024 |
| U-Net 结构 | 单阶段 | 双阶段（Base+Refiner） |
| CLIP 模型 | 1 个 | 2 个（OpenCLIP + CLIP） |
| 生成质量 | 中等 | 高 |
| 文字支持 | 差 | 较好 |

---

## 使用界面

### 1. AUTOMATIC1111（A1111）— 最流行

```bash
# 安装
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui
./webui.sh  # macOS/Linux
```

### 2. ComfyUI — 更高效、可组合

```bash
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
python main.py
```

### 3. Fooocus — 极简入门

无需复杂配置，类似 Midjourney 的体验。

---

## 提示工程（Prompt Engineering）

### 好提示的要素

```
质量词 + 主体 + 细节描述 + 环境 + 光照 + 风格 + 艺术家参考
```

**示例：**
```
masterpiece, best quality, a samurai warrior in cyberpunk city,
neon lights reflecting on armor, rain, cinematic lighting,
detailed face, dynamic pose, art by Yoji Shinkawa
```

### 负面提示（Negative Prompt）

排除不想要的元素：
```
worst quality, low quality, blurry, ugly, deformed,
bad anatomy, extra limbs, watermark, text
```

### 参数指南

| 参数 | 作用 | 推荐值 |
|-----|------|-------|
| `Steps` | 去噪步数 | SDXL: 20-30, SD1.5: 20-50 |
| `CFG Scale` | 提示跟随度 | 7-12（越高越严格） |
| `Sampler` | 采样算法 | DPM++ 2M Karras / Euler |
| `Seed` | 随机种子 | -1（随机）/ 固定值（复现） |
| `Size` | 图像尺寸 | SDXL: 1024×1024, SD1.5: 512×512 |
| `Batch Size` | 单次生成数量 | 1-4 |

---

## LoRA 模型

LoRA（Low-Rank Adaptation）是 SD 生态的重要扩展：

### 常见 LoRA 类型

- **角色 LoRA**：固定角色风格
- **风格 LoRA**：特定艺术风格
- **概念 LoRA**：特定物体/场景
- **姿势 LoRA**：特定构图

### 使用方式

```
加载 LoRA 权重 → 设置权重系数 (0.3-1.5) → 在提示中触发
```

权重过高会导致过拟合，建议从 0.6-0.8 开始调试。

---

## ControlNet

ControlNet 通过额外条件控制生成：

| 控制类型 | 输入 | 用途 |
|---------|------|------|
| Canny Edge | 边缘检测图 | 保持原图构图 |
| Depth | 深度图 | 保持空间结构 |
| OpenPose | 姿态骨架 | 控制人物姿势 |
| Scribble | 手绘草图 | 草图转精图 |
| IP-Adapter | 参考图 | 风格/内容迁移 |

---

## 优势

- **完全开源**：模型权重、代码全公开
- **高度可控**：ControlNet、LoRA、区域提示等多种控制
- **离线运行**：无需联网，数据安全
- **社区庞大**：海量模型、教程、工具
- **硬件门槛低**：6GB+ 显存即可运行 SDXL

## 局限

- **构图能力**：复杂构图和多人交互不如 Midjourney
- **文字渲染**：SD3 虽改进但仍有不足
- **人体解剖**：手部和肢体细节有时不准确
- **抽象概念**：复杂抽象概念的理解有限

---

## 应用场景

- **概念设计**：产品设计、角色设计、场景概念图
- **内容创作**：配图、封面、社交媒体图片
- **游戏开发**：素材生成、纹理制作
- **建筑设计**：效果图、室内设计
- **AI 视频**：与 AnimateDiff、Runway 结合做 AI 视频

---

## 下一步

- 安装 AUTOMATIC1111 或 ComfyUI
- 下载 SDXL 模型开始生图
- 学习提示工程，建立自己的提示词库
- 尝试 LoRA 训练，创建专属风格
- 探索 ControlNet 的高级控制技巧
