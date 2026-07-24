# PyTorch — 深度学习框架

> PyTorch 是 Meta（Facebook）开发的**动态计算图**深度学习框架。它是目前 AI 研究和开发中使用最广泛的框架，从学术论文到生成式 AI 产品，PyTorch 无处不在。

---

## 框架概述

| 属性 | 详情 |
|------|------|
| **开发者** | Meta AI (Facebook AI Research) |
| **首次发布** | 2016 年 (PyTorch 0.1) |
| **当前版本** | PyTorch 2.x (2025) |
| **许可** | BSD |
| **核心语言** | Python + C++/CUDA |
| **GitHub** | [pytorch/pytorch](https://github.com/pytorch/pytorch) |

---

## 为什么 PyTorch 成为主流？

根据 [PyTorch 教程 (GeeksForGeeks)](https://www.geeksforgeeks.org/deep-learning/pytorch-tutorial-2) 和 [UvA DL Notebooks](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial2/Introduction_to_PyTorch.html)：

### 动态计算图（Define-by-Run）

与 TensorFlow 1.x 的静态图不同，PyTorch 使用**动态计算图**：
- 图在执行时即时构建
- 可以随意使用 Python 控制流（if/for/while）
- 调试直观（标准的 Python 错误信息）

```python
# 动态图示例 — 条件分支
for epoch in range(n_epochs):
    for x, y in train_loader:
        optimizer.zero_grad()
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()
```

### PyTorch 2.x 关键特性

| 特性 | 说明 |
|------|------|
| **torch.compile** | 即时编译优化，提升 40-50% 性能 |
| **TorchDynamo** | 安全捕获 Python 计算图 |
| **TorchInductor** | 生成 CUDA/CPU 优化内核 |
| **DTensor** | 分布式张量，简化模型并行 |
| **torch.export** | 模型导出到标准格式 |
| **FlexAttention** | 灵活定义注意力变体，兼顾性能与定制 |
| **TorchTitan / FSDP2** | 大模型预训练与分布式训练框架 |

### PyTorch 在 LLM 时代的地位

PyTorch 几乎是 LLM 研究与训练的事实标准：

- **HuggingFace Transformers** 默认后端，几乎所有开源 LLM 都提供 PyTorch 权重。
- **训练框架**：Megatron-LM、Torchtitan、DeepSpeed、FSDP2 都基于 PyTorch 构建分布式训练。
- **微调**：PEFT、TRL、Unsloth、LLaMA Factory 等 LoRA 微调链路均依赖 PyTorch。
- **研究友好**：动态图让论文复现和架构实验（Mamba、MoE、新注意力）极其方便。

> 注：PyTorch 在"推理部署"环节相对薄弱，生产推理更多交给 vLLM、SGLang、TensorRT 等专用引擎。典型分工是 PyTorch 训练 → 导出 → 推理引擎部署。

---

## 核心概念

### 张量（Tensor）

PyTorch 中的基本数据结构，类似 NumPy 但支持 GPU：

```python
import torch

# 创建张量
x = torch.tensor([1, 2, 3])           # 一维
y = torch.rand(2, 3)                   # 随机
z = torch.zeros(4, 4)                  # 全零

# GPU 加速
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x_gpu = x.to(device)

print(f"Using device: {device}")
```

### 自动微分（Autograd）

自动计算梯度，反向传播的核心：

```python
x = torch.randn(3, requires_grad=True)
y = x ** 2 + 2 * x
y.sum().backward()   # 自动计算梯度
print(x.grad)        # 输出梯度
```

### 模块（nn.Module）

所有神经网络的基础类：

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 5)
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.relu(self.linear(x))
```

---

## 训练循环模板

```python
# 数据加载
dataset = MyDataset(file)
train_loader = DataLoader(dataset, batch_size=16, shuffle=True)

# 模型
model = MyModel().to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练循环
for epoch in range(n_epochs):
    model.train()
    for x, y in train_loader:
        optimizer.zero_grad()
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()

# 验证
model.eval()
with torch.no_grad():
    # 验证代码
    pass
```

---

## PyTorch 生态

| 库 | 功能 | 类型 |
|----|------|------|
| **torchvision** | 计算机视觉工具 | 官方 |
| **torchaudio** | 音频处理 | 官方 |
| **torchtext** | 文本处理 | 社区 |
| **HuggingFace Transformers** | Transformer 模型 | 第三方 |
| **PyTorch Lightning** | 训练脚手架 | 第三方 |
| **torchtune** | LLM 微调 | 官方（Meta） |

---

## 如何开始

### 安装

```bash
# CPU 版本
pip install torch torchvision torchaudio

# CUDA 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 从示例开始

推荐学习路径：
1. [PyTorch 官方 60 分钟入门教程](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
2. [PyTorch 官方教程](https://pytorch.org/tutorials/)
3. 动手实现简单模型（MLP、CNN、RNN）

---

## 优势与局限

**优势:**
- **研究首选:** 学术界最广泛使用的框架
- **动态图:** 调试友好，适合实验
- **丰富的生态:** 几乎所有的 LLM 和扩散模型都用 PyTorch 实现
- **torch.compile:** 即时代码优化
- **强大的分布式训练支持**

**局限:**
- **生产部署不如 TensorFlow 成熟**
- **深度学习框架的通病：学习曲线陡峭**
- **移动端支持不如 TensorFlow Lite**
- **C++ API 不如 Python API 完善**

## 2026 年最新进展：PyTorch 2.12

根据 [PyTorch 官方教程](https://pytorch.org/tutorials/) 和 [PyTorch 官方博客](https://pytorch.org/blog/)，PyTorch 2.12 于 2026 年初发布，持续巩固其在深度学习研究与生产中的主导地位。

### 1. PyTorch 2.12 核心更新

| 特性 | 说明 |
|------|------|
| **torch.compile 持续优化** | 编译后推理速度相比 2.0 提升 40-50%，覆盖更多动态算子 |
| **FlexAttention 稳定版** | 灵活自定义注意力变体（Flash Attention、稀疏注意力等），兼顾性能与定制 |
| **TorchTitan 成熟** | Meta 官方大模型预训练框架，支持 Llama 4、Qwen 3 等主流架构的分布式训练 |
| **torch.export 增强** | 模型导出到标准格式（ExecuTorch、TensorRT）更稳定，推理部署链路完善 |
| **CUDA 12.6+ / cu130 支持** | 最新 GPU 架构原生支持，训练效率进一步提升 |

### 2. PyTorch 在 2026 年 AI 生态中的地位

| 领域 | PyTorch 角色 |
|------|-------------|
| **LLM 训练** | 事实标准。Megatron-LM、DeepSpeed、FSDP2 全栈基于 PyTorch |
| **LLM 微调** | PEFT、TRL、Unsloth、LLaMA Factory 均依赖 PyTorch |
| **AI 研究论文** | 超过 85% 的顶级会议论文（NeurIPS、ICML、ICLR）使用 PyTorch |
| **多模态模型** | LLaVA、CLIP、Stable Diffusion 3 等均基于 PyTorch 实现 |
| **边缘推理** | ExecuTorch 正在追赶 TensorFlow Lite 的移动端部署体验 |

### 3. 2026 年学习路径推荐

1. **基础入门**：完成 [PyTorch 60 分钟快速入门](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
2. **进阶实操**：跟随 [Learn the Basics 系列](https://pytorch.org/tutorials/beginner/basics/intro.html)（Tensors → DataLoaders → Build Model → Autograd → Optimization → Save/Load）
3. **torch.compile**：学习 `torch.compile(model)` 一行代码加速推理
4. **分布式训练**：研究 TorchTitan 或 FSDP2 进行大模型训练
5. **生产部署**：搭配 vLLM / TensorRT-LLM 或 ExecuTorch 部署模型

---

**参考资料：**
- [PyTorch Tutorial (GeeksForGeeks)](https://www.geeksforgeeks.org/deep-learning/pytorch-tutorial-2)
- [UvA DL Notebooks — Introduction to PyTorch](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial2/Introduction_to_PyTorch.html)
- [PyTorch 官方教程 — Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html)
- [PyTorch 官方博客](https://pytorch.org/blog/)
- [Best Resources to Learn PyTorch 2025 (Reddit)](https://www.reddit.com/r/learnmachinelearning/comments/1j5trra/best_resources_to_learn_pytorch_in_2025)

---

## PyTorch 2.13.0 发布 (2026年7月8日)

2026年7月8日，PyTorch 发布 **2.13.0 正式版**，这是 2026 下半年的第一个重大版本，带来多项面向大模型训练和推理的关键更新。

### 核心亮点

| 特性 | 说明 |
|------|------|
| **FlexAttention 登陆 Apple Silicon** | MPS 后端支持 FlexAttention，稀疏注意力模式相比 SDPA 加速最高 **~12 倍**；CUDA 端新增确定性反向路径（deterministic backward） |
| **CuTeDSL "Native DSL" 后端（原型）** | Inductor 新增第二条高性能代码路径，与 Triton 并列，编译速度更快，面向关键 GPU 算子 |
| **`nn.LinearCrossEntropyLoss`** | 融合最终预测与损失计算，大词表语言模型训练峰值显存降低最高 **4 倍** |
| **torchcomms** | PyTorch 分布式通信新后端，改进大规模集群训练的容错性、扩展性和可调试性 |
| **FSDP2 通信重叠** | 通过专用进程组（opt-in）重叠 reduce-scatter 与 all-gather 通信，提升分布式训练吞吐量 |
| **Python 3.15 wheel 支持** | Linux 平台提供 Python 3.15（含自由线程 3.15t）预编译 wheel |
| **更广泛的硬件平台** | ROCm 升级 AOTriton 0.12b + 原生 HIP CMake；Arm 新增 Armv9-A `torch.compile` 目标；Intel XPU 新增设备遥测 API |

### 向后不兼容变更

- **停止构建 CPython 3.13t（自由线程）wheel**：上游 `pypa/manylinux` 已移除 3.13t，用户应迁移至 Python 3.14t
- **Bare `PyObject` 不再允许出现在算子 schema 中**：PyTorch 2.12 中意外接受裸 `PyObject`，2.13 起拒绝解析

### 升级建议

```bash
# 升级到 PyTorch 2.13.0
pip install torch==2.13.0

# 如需 ROCm 版本
pip install torch==2.13.0+rocm7.2
```

> ⚠️ ROCm wheel 已知回归：在无 GPU 环境中 `torch.compile` CPU 路径会报 `RuntimeError: Can't detect vectorized ISA for CPU`。临时方案：在有 ROCm 镜像中运行，或无 GPU 环境使用标准 CPU/CUDA 构建。

### 参考来源

- [PyTorch 2.13.0 Release Notes](https://github.com/pytorch/pytorch/releases/tag/v2.13.0)

---

## PyTorch 生态动态（2026年7月）

### PyTorch Conference 2026

PyTorch 年度大会定于 **2026年10月20-21日** 在 **加州圣何塞（San Jose, CA）** 举行。这是 PyTorch 社区每年最重要的线下活动，通常伴随重大版本发布和技术路线图披露。

根据往年惯例，大会将涵盖：
- PyTorch 2.14 / 3.0 路线图预览
- torch.compile 下一代编译技术
- 分布式训练最新进展（FSDP2/3、torchcomms）
- 边缘推理与 ExecuTorch 生态
- 社区贡献者峰会

预计 2026 年大会焦点将围绕 **CuTeDSL 后端** 的成熟化路线以及 FlexAttention 的多后端扩展展开。

### CuTeDSL：Triton 之外的第二条路

PyTorch 2.13.0 引入的 **CuTeDSL "Native DSL" 后端**（原型阶段）是近年来 Inductor 编译器最值得关注的基础设施变革。

**背景**：PyTorch 2.0 以来，`torch.compile` 的 Inductor 后端一直依赖 OpenAI 的 **Triton** 作为 GPU 代码生成引擎。Triton 在灵活性上表现出色，但存在两个固有问题：

1. **编译开销**：Triton 的 JIT 编译在某些复杂算子上耗时较长（首次推理增加数秒到数十秒）
2. **依赖耦合**：Inductor 的优化能力受限于 Triton 的中间表示（Triton IR）的表达力

**CuTeDSL 的改进**：

| 维度 | Triton 后端 | CuTeDSL 后端 |
|------|-----------|-------------|
| 编译速度 | 中等（JIT 编译器） | 更快（直接生成 CUDA C++ 模板） |
| 优化粒度 | Triton IR 级别 | CUDA 线程/内存级别（更细粒度） |
| 成熟度 | 稳定（2020+） | 原型（2026.7） |
| 适用算子 | 通用 | 关键 GPU 算子（matmul、attention、element-wise） |

> **影响预测**：CuTeDSL 成熟后将形成 **Triton + CuTeDSL 双后端架构**——Triton 处理通用算子，CuTeDSL 加速高频关键路径。这与 NVIDIA 的 CUTLASS 库形成官方-社区互补，最终让 PyTorch 用户无需手动编写 CUDA kernel 即可逼近手写性能。

### PyTorch 2.10 正式发布（2026年7月）

2026年7月，PyTorch 基金会正式发布了 **PyTorch 2.10**，这是继 2.9 之后的又一重要里程碑。该版本包含 **4160 次提交**，来自 **536 位贡献者**，聚焦性能提升和数值调试能力。以下是核心新特性：

#### Python 3.14 支持与 Free-Threaded 构建

PyTorch 2.10 首次为 `torch.compile()` 添加 **Python 3.14** 支持，并实验性支持 Python 3.14t（Free-Threaded 构建）。这意味着在启用自由线程的 Python 解释器上，PyTorch 能更好地利用多核 CPU 并行性，对推理和数据处理管道有显著性能提升。

#### Combo-Kernels 水平融合优化

`torchinductor` 引入了 **Combo-Kernels**（组合核）技术，这是一种**水平融合**优化——将多个无数据依赖的独立操作合并为单个 GPU 内核。与传统的垂直融合（生产者-消费者）不同，水平融合能同时执行并行运算，大幅降低内核启动开销。对于包含大量 element-wise 运算的模型（如 Transformer 的 LayerNorm 和激活函数），实测推理速度提升 **15-30%**。

#### varlen_attn() — 变长序列注意力

新增 `torch.nn.functional.varlen_attn()` 操作，专门支持**不规整序列**和**打包序列**（packed sequences）。在 LLM 训练场景中，不同样本的序列长度差异很大，传统方法需要对短序列做 padding，浪费计算资源。`varlen_attn()` 直接操作打包后的变长序列，减少了约 **20-40%** 的注意力计算浪费。

#### DebugMode — 数值调试新模式

`torch.compile()` 现在支持 `use_deterministic_mode`，并新增 **DebugMode** 用于追踪分派调用和调试数值发散。该模式可以精确定位 `torch.compile` 在优化过程中的每一步操作，帮助开发者快速找到数值精度问题的根源。这对**分布式强化学习**（RLHF 等后训练场景）特别有价值——此类任务对数值确定性要求极高。

#### DnXgeev — 高效特征值分解

引入了 **DnXgeev** 算子，提供高效的特征值分解实现。特征值分解在图神经网络、主成分分析（PCA）和某些科学计算场景中频繁使用，新算子在大规模矩阵上性能提升可达 2-3 倍。

#### Intel GPU 性能优化

继续扩展对 Intel GPU 的支持，包括更多算子的集成和编译优化，使 PyTorch 能在 Intel Gaudi 和 Ponte Vecchio 等加速器上获得更好的性能。

### CuTeDSL 双后端进展

CuTeDSL（基于 NVIDIA CUTLASS 的自定义内核 DSL）在 2.10 中继续迭代。预期 **PyTorch 2.14（2026年9月）** 将达到稳定性里程碑，形成 **Triton + CuTeDSL 双后端架构**——Triton 处理通用算子，CuTeDSL 加速高频关键路径。

### PyTorch vs TensorFlow 2026 格局

据多方评测（Tech Insider、Spheron），2026 年 PyTorch 在**研究领域**已占据 **85% 的论文份额**，TensorFlow 则在**企业生产部署**中保持 **38% 的市场份额**（TF Serving、LiteRT）。两个框架都在互相靠拢：PyTorch 的 `torch.compile` 提供了接近 XLA 的静态图优化能力，而 TensorFlow 将 Keras 3 作为主要接口支持多后端切换。

| 维度 | PyTorch 2.11 | TensorFlow 2.21 |
|------|-------------|----------------|
| 研究论文份额 | 85% | ~15% |
| 企业生产份额 | ~40% | 38% |
| 编译优化 | torch.compile | OpenXLA |
| 移动端 | ExecuTorch（新兴） | LiteRT（成熟） |
| 就业市场需求 | 37.7% 职位 | 32.9% 职位 |

### 参考来源
- [PyTorch 2.10 Release Blog — PyTorch Foundation](https://pytorch.org/blog/pytorch-2-10-release-blog/)
- [PyTorch vs TensorFlow 2026: 85% Research Share Gap — Tech Insider](https://tech-insider.org/pytorch-vs-tensorflow-2026/)
- [PyTorch vs TensorFlow in 2026 — Spheron Blog](https://www.spheron.network/blog/pytorch-vs-tensorflow/)
- [PyTorch Compiler: torch.compile Overview — EmergentMind](https://www.emergentmind.com/topics/pytorch-compiler-torch-compile)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-25 00:09:45*
