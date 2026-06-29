# ComfyUI

> ComfyUI 是一个基于节点/流程图界面的 Stable Diffusion 图像生成工具，以其高效性、可重现性和灵活的工作流系统在 AI 绘画社区中备受推崇。

---

## 为什么选择 ComfyUI？

与主流的 AUTOMATIC1111（A1111）相比，ComfyUI 采用完全不同的设计理念：

| 特性 | ComfyUI | A1111 |
|-----|---------|-------|
| **界面** | 节点流程图 | 传统表单式 |
| **工作流** | 可视化图形 | 选项卡切换 |
| **显存效率** | 高（按需加载） | 中等 |
| **执行速度** | 快（优化管道） | 标准 |
| **可重现性** | 极高（工作流文件） | 中等 |
| **学习曲线** | 较陡 | 平缓 |
| **高级控制** | 极强 | 强 |

---

## 核心概念

### 节点（Nodes）

节点是 ComfyUI 的基本构建块，每个节点执行一个特定功能：

```
[Checkpoint Loader] → [VAE Decode] → [Save Image]
         ↓
[CLIP Text Encode] → [KSampler] → [VAE Decode]
         ↓
[Empty Latent Image]
```

### 常见节点类型

| 节点类型 | 功能 | 示例 |
|---------|------|------|
| **模型节点** | 加载模型 | Checkpoint Loader, LoRA Loader |
| **输入节点** | 提供输入 | CLIP Text Encode, Empty Latent |
| **采样节点** | 执行去噪 | KSampler, SamplerCustom |
| **图像节点** | 图像处理 | VAE Decode, Upscale Image |
| **遮罩节点** | 遮罩操作 | Mask to Image, Composite |
| **控制节点** | 高级控制 | ControlNet, IP-Adapter |

---

## 快速开始

### 安装

```bash
# 标准安装
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt

# 启动
python main.py

# 访问 http://localhost:8188
```

### 模型目录结构

```
ComfyUI/
├── models/
│   ├── checkpoints/    # 主模型 (SDXL, SD3 等)
│   ├── loras/          # LoRA 模型
│   ├── vae/            # VAE 模型
│   ├── controlnet/     # ControlNet 模型
│   ├── upscale_models/ # 放大模型
│   └── clip/           # CLIP 模型
├── custom_nodes/       # 自定义节点
├── input/              # 输入图片
├── output/             # 输出图片
└── workflows/          # 工作流文件
```

---

## 核心工作流示例

### 基础文生图工作流

```
1. [Checkpoint Loader] → 加载 SDXL 模型
2. [CLIP Text Encode] → 输入正向提示词
3. [CLIP Text Encode] → 输入负向提示词
4. [Empty Latent Image] → 设置图片尺寸
5. [KSampler] → 连接以上输入，设置参数
6. [VAE Decode] → 将潜在表示解码为图像
7. [Save Image] → 保存生成结果
```

### 图生图工作流

```
[Load Image] → [VAE Encode] ──────────────────┐
                                                ↓
[Checkpoint Loader] → [CLIP Text Encode] → [KSampler] → [VAE Decode] → [Save Image]
```

### ControlNet 工作流

```
[Load Image] → [Canny Edge Detection] ──┐
                                         ↓
[Checkpoint Loader] → [CLIP Encode] → [ControlNet Apply] → [KSampler] → [输出]
```

---

## 提高效率的技巧

### 队列批处理

```python
# ComfyUI API 批量调用
import requests
import json

with open("workflow.json", "r") as f:
    workflow = json.load(f)

# 修改提示词
workflow["6"]["inputs"]["text"] = "a cat, masterpiece"

response = requests.post(
    "http://localhost:8188/prompt",
    json={"prompt": workflow}
)
print(response.json())
```

### 快捷键

| 快捷键 | 功能 |
|-------|------|
| Ctrl+Enter | 执行队列 |
| Ctrl+Shift+Enter | 执行当前节点 |
| Tab | 搜索并添加节点 |
| Ctrl+C/V | 复制粘贴节点 |
| Ctrl+D | 禁用选中节点 |
| Space+拖拽 | 平移画布 |
| 滚轮 | 缩放 |

---

## 自定义节点

ComfyUI 的强大之处在于其**丰富的自定义节点生态**：

| 节点集 | 功能 |
|-------|------|
| **ComfyUI-Manager** | 节点管理器，一键安装 |
| **WAS Node Suite** | 图像处理工具集 |
| **Efficiency Nodes** | 工作流效率优化 |
| **AnimateDiff** | AI 视频生成 |
| **IP-Adapter** | 图像提示适配器 |
| **Face Restoration** | 人脸修复（GFPGAN） |

### 安装自定义节点

通过 ComfyUI-Manager 安装，或手动克隆到 `custom_nodes/`：

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
# 重启 ComfyUI
```

---

## 优势

- **显存效率高**：按需加载模型，SDXL 可在 6GB 显存运行
- **执行速度快**：优化计算管道，减少冗余操作
- **可重现性**：工作流文件分享，完全复现结果
- **灵活性强**：可视化流程图，组合灵活
- **生态丰富**：大量高质量自定义节点
- **API 友好**：可通过 API 批量调用

## 局限

- **学习曲线陡**：节点式界面需要适应
- **新手不友好**：需要理解 Stable Diffusion 技术概念
- **工作流管理**：复杂工作流可能很混乱
- **调试困难**：节点连接错误不易排查

---

## 应用场景

- **精控图像生成**：ControlNet + 多次迭代
- **批量图像处理**：自动化流水线
- **AI 视频制作**：AnimateDiff 工作流
- **工作流分享**：社区共享高质量工作流
- **进阶用户**：需要精细控制的研究和创作

---

## 下一步

- 安装 ComfyUI 并加载 SDXL 模型
- 从社区下载工作流文件学习
- 学习使用 ControlNet 和 IP-Adapter
- 探索 AnimateDiff 做 AI 视频
- 安装 ComfyUI-Manager 扩展节点生态
