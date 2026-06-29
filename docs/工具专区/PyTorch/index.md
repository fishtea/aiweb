# PyTorch 为什么赢？一场深度学习框架的"三国演义"

> 2017 年，Google 的 TensorFlow 还是绝对的王者。
> 2023 年，PyTorch 以 80%+ 的论文使用率碾压了所有对手。
> 这不是"同样好的产品被更多人选了"，而是"选对设计哲学"的经典案例。

---

## 历史: TensorFlow vs PyTorch 的战争

### TensorFlow 1.x（2015-2018）— 静态图的时代

TensorFlow 的设计继承自 Google Brain 的 DistBelief，核心哲学：

**静态计算图（Static Graph）**：
```python
# 1. 先建图（Graph Mode）
a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)
c = tf.add(a, b)

# 2. 然后在 Session 中执行
with tf.Session() as sess:
    result = sess.run(c, feed_dict={a: 1.0, b: 2.0})
```

**问题**：
- 🐌 调试困难：不能 print，不能断点——图只有在 session.run 时才执行
- 📝 代码冗长：占位符(placeholder)、变量作用域(variable_scope)、会话(session)
- 🔄 动态控制流：if/else/for 在静态图中需要特殊的 tf.cond/tf.while_loop

**Google 的人怎么说**？"TensorFlow 是为产品部署设计的，不是为研究设计的。"

### PyTorch（2016-至今）— 动态图的革命

PyTorch 的设计源自 Torch（Lua 框架），但用 Python 重新实现：

**动态计算图（Dynamic Graph / Define-by-Run）**：
```python
# 这就是普通 Python 代码！
a = torch.tensor(1.0, requires_grad=True)
b = torch.tensor(2.0, requires_grad=True)
c = a + b  # 图在这里才构建

# 可以随时 print
print(c)  # tensor(3.0, grad_fn=<AddBackward0>)

# 反向传播
c.backward()
print(a.grad)  # tensor(1.)
```

**PyTorch 的本质胜利**："代码即模型，模型即代码。"

- 🙌 能用 Python debugger（pdb）调试模型
- 🙌 可以用 print 看中间值
- 🙌 可以用普通的 if/else/for 循环控制流程
- 🙌 动态 Transformer、可变长度 RNN → 自然支持

### TensorFlow 2.x / Keras（2019-）— 迟到十年的道歉

Google 意识到了问题，在 TF 2.0 中引入了 Eager Execution（动态图）。

**但太晚了。研究社区已经全部迁移到了 PyTorch。**

> TensorFlow 2.x 就像是"Google 终于承认 PyTorch 的设计是对的"。

---

## PyTorch 核心组件解析

### 🔧 nn.Module — 一切的基类

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(128, 256)
        self.dropout = nn.Dropout(0.1)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.linear(x)
        x = self.dropout(x)
        x = self.activation(x)
        return x

model = MyModel()
print(model)  # 自动打印所有层
```

**Module 的神奇之处**：
- 自动注册所有参数（parameters() 和 named_parameters()）
- 自动处理 GPU 转换（model.to("cuda") 递归移动所有子模块）
- 支持嵌套（Module 里可以包含其他 Module）
- 支持 hooks（前向/反向后插入自定义操作）

### 📈 autograd — 自动求导

PyTorch 的杀手特性——自动计算梯度。

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()  # scalar 损失

z.backward()  # 自动计算所有输入的梯度
print(x.grad)  # dz/dx = [0.667, 0.667, 0.667]
```

**背后的原理**：每个 tensor 操作都在构建一个"计算图"，记录了从输入到输出的所有操作。`backward()` 从输出节点开始，沿图反向传播梯度（链式法则）。

### 🏋️ optim — 优化器

```python
import torch.optim as optim

optimizer = optim.AdamW(
    model.parameters(),
    lr=1e-4,
    weight_decay=0.01
)
```

**支持的优化器**：SGD、Adam、AdamW、Adamax、RMSprop、LBFGS……

### 📦 DataLoader — 数据加载

```python
from torch.utils.data import DataLoader, Dataset

class MyDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4  # 并行加载
)
```

---

## 训练循环解剖

```python
model = MyModel().to("cuda")
optimizer = optim.AdamW(model.parameters(), lr=1e-4)

for epoch in range(10):
    model.train()  # 训练模式（dropout 开启）
    for batch in dataloader:
        x, y = batch
        x, y = x.to("cuda"), y.to("cuda")

        # 1. 前向
        pred = model(x)
        loss = nn.CrossEntropyLoss()(pred, y)

        # 2. 清零梯度
        optimizer.zero_grad()

        # 3. 反向传播
        loss.backward()

        # 4. 梯度裁剪（防止梯度爆炸）
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        # 5. 更新参数
        optimizer.step()

    # 评估
    model.eval()  # 评估模式（dropout 关闭）
    with torch.no_grad():  # 不计算梯度（节省显存和计算）
        for batch in val_loader:
            ...
```

**5 步循环是所有 PyTorch 训练的标准写法**。不管是 1B 还是 70B 的模型，循环结构都一样。区别只在于分布式策略。

---

## 分布式训练：从小到大的路径

### DDP（Distributed Data Parallel）

同机多卡或多机多卡的标准方案。每个 GPU 有完整模型副本，处理不同批次数据，同步梯度。

```bash
# 一条命令启动
torchrun --nproc_per_node=4 train.py
```

### FSDP（Fully Sharded Data Parallel）

把模型参数、梯度、优化器状态分片到多个 GPU 上。

```
传统 DDP:
GPU0: [全部参数 + 全部优化器状态]
GPU1: [全部参数 + 全部优化器状态]
GPU2: [全部参数 + 全部优化器状态]
GPU3: [全部参数 + 全部优化器状态]
总显存: 4 × 模型大小 × 3（参数+梯度+状态）

FSDP:
GPU0: [参数 1/4 + 优化器 1/4]
GPU1: [参数 1/4 + 优化器 1/4]
GPU2: [参数 1/4 + 优化器 1/4]
GPU3: [参数 1/4 + 优化器 1/4]
总显存: 模型大小 × 3（没有复制）
```

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

model = FSDP(model)
```

**让 70B 模型的微调从 8×A100 降到 4×A100**。

---

## PyTorch + HuggingFace 生态

PyTorch 的胜利很大程度上是因为它成为了 HuggingFace Transformers 的"默认框架"。

```
PyTorch ← HuggingFace Transformers ← 全世界的模型和数据集
```

```python
# 用 HF 加载 → 用 PyTorch 训练 → 上传回 HF
from transformers import AutoModelForCausalLM, Trainer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
trainer = Trainer(model=model, ...)
trainer.train()
model.push_to_hub("my-fine-tuned-llama")
```

---

## PyTorch 2.x：编译时代

2023 年发布的 PyTorch 2.0 引入了 `torch.compile()`：

```python
model = MyModel()
compiled_model = torch.compile(model)  # 一行加速 30-50%
```

**原理**：将 Python 代码编译成 GPU 内核（通过 Triton 编译器）。不需要修改任何模型代码。

---

> **一句话总结**：PyTorch 赢了因为它尊重 Python 程序员的使用习惯。动态图、Pythonic API、强大的社区生态。它不是最强的框架，它是**最自然的框架**。
>
> 行业内现在有一个共识：**"PyTorch 用于研究，JAX 用于实验，TensorFlow 用于……切换。"**
