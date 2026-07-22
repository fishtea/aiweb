# Stable Diffusion — Stability AI

> Stable Diffusion（稳定扩散）是由 Stability AI 主导开发的开源文本到图像生成模型系列。从 SD 1.5、SDXL 到 Stable Diffusion 3 / 3.5，它仍是本地可控图像工作流的重要基础。按 2026-07-06 可核验的图像模型生态，生产选型还应把 Black Forest Labs 的 FLUX.2 / FLUX.1、Google 的图像生成模型和闭源图像模型纳入对比。

---

## 模型演进

| 模型 | 发布时间 | 架构 | 参数规模 | 特点 |
|------|---------|------|---------|------|
| SD 1.0 | 2022.08 | Latent Diffusion + U-Net | ~1B | 首个开源文生图模型 |
| SD 1.5 | 2022.10 | Latent Diffusion + U-Net | ~1B | 社区最广泛采用 |
| SD 2.0 | 2022.11 | Latent Diffusion + U-Net | ~1B | 改进文本生成 |
| SDXL 1.0 | 2023.07 | Latent Diffusion + U-Net | ~3.5B | 大幅提升图像质量 |
| SD 3.0 | 2024.03 | **MMDiT** | 800M-8B | 架构转型为 Diffusion Transformer |
| SD 3.5 | 2024.10 | MMDiT | 8B | 改进版 |
| FLUX.1 | 2024.08 | Diffusion Transformer | 12B | Black Forest Labs 开发，社区新宠 |
| SD 3.5 Large Turbo | 2024.10 | MMDiT | 8B | 4 步快速生成 |
| FLUX.2 | 2026 | Flow Matching / DiT | 未公开 | BFL 2026 图像生成与编辑主线 |

### 扩散模型演进要点

| 趋势 | 说明 |
|------|------|
| 从 U-Net 到 DiT | SD3/FLUX 用 Transformer 替代 U-Net，扩展性更强 |
| Rectified Flow / Flow Matching | 更直的采样路径，更少步数即可出图 |
| 文本渲染突破 | FLUX.2、FLUX.1、Ideogram 等显著改善图中文字准确性 |
| 速度优化 | Turbo/Lightning 蒸馏版 4-8 步出图，接近实时 |
| ControlNet / IPAdapter | 精确控制构图、姿态、风格、角色一致性 |

---

## SD3 — MMDiT 架构革命

根据 [Stability AI 的 SD3 研究论文公告](https://stability.ai/news-updates/stable-diffusion-3-research-paper)：

### 核心创新：MMDiT

**Multimodal Diffusion Transformer (MMDiT)** 是 SD3 最大的架构变革：

- 从传统的 **U-Net** 架构转型为 **Diffusion Transformer (DiT)** 架构
- **两套独立的权重**分别处理图像和语言表示
- **联合序列进行注意力计算**：允许跨模态信息流动，同时保持各模态的独立空间
- 从 450M 到 8B 参数的扩展实验显示**没有饱和迹象**

### 文本编码器

SD3 使用三个文本编码器：
- **两个 CLIP 模型**：处理通用文本理解
- **一个 T5 (4.7B 参数)**：处理复杂文本理解（推理时可移除以节省内存）
  - 移除 T5：视觉美学 50% 胜率（无影响），文字遵循 46%（轻微下降），排版 38%（显著下降）

### Rectified Flow 改进

- 使用 Rectified Flow (RF) 公式
- 引入**新的轨迹采样调度**，更重视轨迹中间部分（更具挑战性的预测任务）
- Reweighted RF 变体在所有步数范围内持续提升性能

---

## 性能对比

根据 SD3 论文的人类偏好评估：

| 模型 | 提示遵循 | 排版 | 视觉美学 |
|------|---------|------|---------|
| **SD3 8B** | **最佳** | **最佳** | **最佳** |
| DALL·E 3 | 竞争 | 竞争 | 竞争 |
| Midjourney v6 | 竞争 | 较弱 | 较强 |
| Ideogram v1 | 竞争 | 竞争 | 竞争 |
| SDXL | — | — | — |

---

## FLUX.2 与 Black Forest Labs

根据 Black Forest Labs 官方文档与发布资料：

- 由原 Stability AI 核心团队（Black Forest Labs）开发
- 采用 **Flow Matching** 架构，基于 Diffusion Transformer
- FLUX.1 以 12B 参数打开高质量开源图像生成生态；FLUX.2 是 2026 需要重点评估的新主线
- 与 Midjourney、DALL·E 3 竞争

### FLUX 模型规格

| 版本 | 特点 | 许可 |
|------|------|------|
| FLUX.1 Pro | 完整版，最高质量 | 商业 |
| FLUX.1 Dev | 开源版，蒸馏得到 | 开源 |
| FLUX.1 Schnell | 极速版，4 步生成 | 开源 |
| FLUX.2 | 2026 主线，图像生成与编辑 | 商业/API 与生态实现并存 |

### 2026 选型建议

| 场景 | 推荐 |
|------|------|
| 社区资源和 LoRA 最丰富 | SD 1.5 / SDXL |
| 更高提示遵循和文字能力 | FLUX.2、SD3.5 Large、FLUX.1 Dev / Pro |
| 快速草图与低步数生成 | SD3.5 Turbo、FLUX.1 Schnell |
| 精确控制姿态、构图、角色 | SDXL / SD3.5 + ControlNet / IPAdapter / LoRA |
| 商业闭源质量对比 | Midjourney、DALL·E、Ideogram、FLUX Pro |

### FLUX.2 系列详解（2026 更新）

根据 Black Forest Labs 官方网站（bfl.ai，2026-07 访问）及 BFL 博客，FLUX.2 系列已发展为一个完整的产品家族：

| 模型 | 定位 | 关键特性 |
|------|------|---------|
| **FLUX.2** | 旗舰模型 | 多参考图像控制（Multi-Reference Control）、专业级场景一致性、产品植入与光照自适应 |
| **FLUX.2 [klein]** | 快速推理 | 亚秒级推理，生产质量不妥协，开放权重可本地运行 |
| **FLUX.2 [max]** | 极致质量 | 最高编辑一致性、世界知识最丰富、提示遵循最强 |
| **FLUX.1 Kontext** | 上下文感知 | 基于 Flow Matching 的图像生成与编辑，支持 BFL Playground |

**核心能力升级：**

- **多参考控制（Multi-Reference Control）**：支持多张参考图像统一风格或角色身份，实现批量资产生成的风格一致性。同一角色可生成数百张图片，角色身份保持一致。
- **产品植入（Products In Any Context）**：自动适应光照、透视和材质，将产品自然融入场景，光线自动适配，物理效果真实。
- **FLUX Erase（2026.06 发布）**：一键擦除任意图像元素，不留痕迹，类似 Photoshop 的生成式填充但更精准。
- **FLUX VTO（2026.05 发布）**：虚拟试穿（Virtual Try-On），支持在电商目录规模上进行服装试穿展示，BFL 已与多家零售商合作落地。

**开放生态：**

- **API 服务**：通过 docs.bfl.ai 接入，提供 Premium Quality、Ease of Use、Built for Scale 三个层级
- **开放权重**：FLUX.2 [klein] 开放权重，可在 Hugging Face 下载（black-forest-labs 组织）
- **Playground**：bfl.ai 提供免费在线试用
- **企业许可证**：SOC 2 + ISO 27001 认证，适合企业生产部署
- **Azure AI Foundry 集成**：FLUX 模型已在 Microsoft Azure 上线

**生态影响：** Martin Scorsese（马丁·斯科塞斯）于 2026 年 6 月加入 BFL 担任顾问，标志着 BFL 在影视创作领域的战略布局。BFL 已完成 3 亿美元的 B 轮融资（2025.12），估值 32.5 亿美元。

### BFL API 快速使用

```python
# 通过 BFL API 生成图像
import requests

response = requests.post(
    "https://api.bfl.ai/v1/image",
    headers={"Authorization": f"Bearer YOUR_API_KEY"},
    json={
        "model": "flux.2",
        "prompt": "A cat wearing a hat, cinematic lighting, photorealistic",
        "width": 1024,
        "height": 1024,
        "steps": 50
    }
)
print(response.json())
```

---

## 如何使用

### 本地运行 ComfyUI

ComfyUI 是最流行的 SD 工作流管理工具：

1. 安装 ComfyUI
2. 下载模型权重（SD3 / FLUX）
3. 搭建工作流

### 通过 API (Stability AI)

```python
import requests
import base64

response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={
        "authorization": f"Bearer your-api-key",
        "accept": "image/*"
    },
    files={
        "prompt": "A beautiful landscape with mountains and sunset, cinematic lighting",
        "output_format": "png"
    }
)
```

### 通过 Hugging Face

```python
from diffusers import StableDiffusion3Pipeline
import torch

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3-medium-diffusers",
    torch_dtype=torch.float16
).to("cuda")

image = pipe("A cat wearing a hat, digital art").images[0]
image.save("cat.png")
```

---

## 优势与局限

**优势:**
- **开源生态:** 完全开源，社区活跃
- **灵活部署:** 可在消费级 GPU 运行
- **丰富的社区资源:** 数千种 LoRA、ControlNet 扩展
- **ComfyUI 工作流:** 可视化节点编辑，无限定制
- **成本低廉:** 相比 Midjourney/DALL·E，本地运行成本极低

**局限:**
- 人体结构（特别是手部）有时不正确
- 复杂提示遵循仍有局限
- 需要 GPU 才能获得合理速度
- FLUX 等更优模型需要更高硬件配置

---

**参考资料：**
- [Stable Diffusion 3 Research Paper (Stability AI)](https://stability.ai/news-updates/stable-diffusion-3-research-paper)
- [Stable Diffusion 3.5 发布公告](https://stability.ai/news/introducing-stable-diffusion-3-5)
- [Black Forest Labs FLUX.1](https://blackforestlabs.ai/announcing-black-forest-labs/)
- [Black Forest Labs 官网 — FLUX.2](https://blackforestlabs.ai/)
- [BFL API 文档](https://docs.bfl.ai/)
- [BFL Hugging Face 组织](https://huggingface.co/black-forest-labs)
- [Diffusers Stable Diffusion 3 文档](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-23 00:09:06*
