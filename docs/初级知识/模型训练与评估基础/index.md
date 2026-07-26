# 模型训练与评估基础

训练模型不是只看一个分数，而是要判断模型是否真正学到了可泛化的规律，是否能在真实场景中稳定工作。

## 训练过程

```text
准备数据 → 选择模型 → 训练 → 验证 → 调参 → 测试 → 部署 → 监控
```

每一步都可能影响最终效果。初学者应先掌握最小闭环，再追求复杂模型。

## 训练集、验证集、测试集

| 数据集 | 作用 | 是否参与训练 |
|--------|------|--------------|
| 训练集 | 学习模型参数 | 是 |
| 验证集 | 选择模型和调参 | 间接参与 |
| 测试集 | 最终评估泛化能力 | 不应参与 |

如果反复根据测试集调参，测试集就不再是客观评估。

## 欠拟合与过拟合

| 问题 | 表现 | 可能原因 | 处理方式 |
|------|------|----------|----------|
| 欠拟合 | 训练集和测试集都差 | 模型太简单、特征不足 | 增加特征、换更强模型 |
| 过拟合 | 训练集好、测试集差 | 模型记住噪声 | 正则化、更多数据、早停 |

一个模型训练分数很高，不能直接说明它好。关键是新数据上的表现。

## 常见评估指标

| 任务 | 指标 | 说明 |
|------|------|------|
| 分类 | Accuracy | 样本均衡时直观 |
| 分类 | Precision | 预测为正的样本中有多少是真的 |
| 分类 | Recall | 真实正样本中有多少被找出来 |
| 分类 | F1 | Precision 和 Recall 的平衡 |
| 回归 | MAE | 平均绝对误差，直观易解释 |
| 回归 | RMSE | 对大误差更敏感 |
| 排序/推荐 | AUC、NDCG | 衡量排序质量 |
| 语言模型 | 困惑度、人工评估 | 衡量生成质量和可用性 |

## 混淆矩阵

二分类中常用四个概念：

| 名称 | 含义 |
|------|------|
| TP | 真实为正，预测为正 |
| FP | 真实为负，预测为正 |
| TN | 真实为负，预测为负 |
| FN | 真实为正，预测为负 |

医疗筛查更关注漏检，所以重视 Recall；垃圾邮件拦截更怕误伤重要邮件，所以也要关注 Precision。

## 基线模型

训练复杂模型前，先建立一个简单基线：

- 分类任务：总是预测最多的类别。
- 回归任务：总是预测平均值或中位数。
- 文本任务：使用关键词规则或简单 TF-IDF。

如果复杂模型没有明显超过基线，就需要重新检查数据、特征和任务定义。

## 上线前检查

- 测试集是否和真实场景一致？
- 是否评估了不同人群、地区、设备或时间段的表现？
- 错误样本是否做过人工分析？
- 是否有置信度阈值和人工兜底？
- 是否能记录输入、输出、版本和反馈？
- 是否监控数据漂移和效果下降？

## 偏差与方差权衡（Bias-Variance Tradeoff）

模型的误差可以分解为三个部分：偏差（Bias）、方差（Variance）和不可约噪声。

| 概念 | 含义 | 表现 |
|------|------|------|
| 高偏差 | 模型过于简单，未能捕捉数据规律 | 训练集和测试集表现都差（欠拟合） |
| 高方差 | 模型过于复杂，记住了训练集的噪声 | 训练集好、测试集差（过拟合） |
| 理想状态 | 偏差和方差达到平衡 | 两者都低，泛化能力好 |

选择模型时需要在偏差和方差之间做权衡。过于简单的模型（如线性回归拟合非线性数据）会产生高偏差；过于复杂的模型（如深度决策树）会产生高方差。交叉验证是找到这个平衡点的有效方法。

## 交叉验证

交叉验证是评估模型泛化能力的重要技术，比单次划分训练/测试集更稳健。

| 方法 | 说明 | 适用场景 |
|------|------|----------|
| K 折交叉验证 | 数据分成 K 份，轮流用 K-1 份训练、1 份验证 | 中等规模数据（建议 K=5 或 10） |
| 留一交叉验证 | 每次留 1 个样本做验证 | 小样本数据 |
| 分层交叉验证 | 每折保持类别比例一致 | 类别不均衡的分类任务 |

K 折交叉验证的流程：将数据集随机分成 K 份（通常是 5 份或 10 份），每次取其中 K-1 份训练，剩余 1 份验证，重复 K 次后取平均作为最终评估分数。这比单次划分更可靠，因为它减少了数据划分方式带来的随机性。

需要注意的是：交叉验证的结果分数只是一个估计，不能完全代表模型在真实世界中的表现。交叉验证分数很高，不等于在实际部署中表现好。部署前还要考虑数据漂移、环境差异等因素。

## 学习曲线

学习曲线展示训练集和验证集误差随训练数据量增加的变化趋势，是诊断模型状态的实用工具。

| 曲线形态 | 诊断结论 | 建议 |
|----------|----------|------|
| 训练误差和验证误差都高且接近 | 高偏差（欠拟合） | 增加特征、换更强模型 |
| 训练误差低、验证误差高，且差距大 | 高方差（过拟合） | 增加数据、正则化、简化模型 |
| 训练误差和验证误差都低且接近 | 模型状态良好 | 可以上线测试 |

用学习曲线判断数据量是否充足：如果验证误差的曲线在数据量增加后仍在下降，说明增加数据仍可能改善模型。

## 正则化方法

正则化通过限制模型复杂度来缓解过拟合，是训练过程中最常用的技术之一。

| 方法 | 原理 | 适用场景 |
|------|------|----------|
| L1 正则化（Lasso） | 在损失函数中加入权重绝对值之和 | 特征选择（部分权重被压缩为 0） |
| L2 正则化（Ridge） | 在损失函数中加入权重的平方和 | 防止过拟合，保持所有特征参与 |
| Dropout | 训练时随机丢弃部分神经元 | 神经网络（尤其是深度网络） |
| Early Stopping | 验证集误差不再下降时提前停止训练 | 任何迭代训练过程 |
| 数据增强 | 通过变换生成更多训练样本 | 图像、文本等数据 |

实际使用中，L2 正则化是最常用的基线方法。对于深度神经网络，通常会同时使用 Dropout 和 Early Stopping。

## 超参数调优

模型训练中需要手动设定的参数称为超参数（Hyperparameter），常见的包括学习率、正则化强度、树的最大深度等。

| 调参方法 | 说明 | 优缺点 |
|----------|------|--------|
| 网格搜索 | 穷举所有参数组合 | 简单可靠，但计算成本高 |
| 随机搜索 | 在参数空间中随机采样 | 比网格搜索更高效，通常结果相近 |
| 贝叶斯优化 | 根据历史结果选择下一组参数 | 更高效但实现复杂 |

基本原则：先用少量数据做粗调，确定参数范围；再用全量数据做细调。不要一次调太多参数，优先调整对模型影响最大的参数（如学习率、正则化强度）。

## 交叉验证与深度学习评估进阶

### 用 PyTorch Lightning 实现 K 折交叉验证

交叉验证在深度学习中的实现比传统 ML 更复杂，因为训练成本高。PyTorch Lightning 提供了简洁的 API 来结合 sklearn 的 KFold 实现交叉验证：

```python
import pytorch_lightning as pl
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader, Subset

# 定义 Lightning 模型
class MyModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.layer = torch.nn.Linear(784, 10)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.layer(x.view(x.size(0), -1))
        loss = torch.nn.functional.cross_entropy(y_hat, y)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)

# K 折交叉验证
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
for fold, (train_idx, val_idx) in enumerate(kfold.split(dataset)):
    train_subset = Subset(dataset, train_idx)
    val_subset = Subset(dataset, val_idx)

    model = MyModel()
    trainer = pl.Trainer(max_epochs=10)
    trainer.fit(model, DataLoader(train_subset), DataLoader(val_subset))
    print(f"Fold {fold+1} 完成")
```

### 分层交叉验证（Stratified K-Fold）的重要性

对于类别不均衡的数据集，普通 K 折交叉验证可能导致某些折中完全缺失某一类别。分层 K 折（Stratified K-Fold）保证每折的类别比例与原始数据集一致，是处理不均衡数据的**默认选择**。

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
# y 是标签数组，必须传入以保持分层
for train_idx, val_idx in skf.split(X, y):
    # 每折的类别比例与原始数据一致
    ...
```

### 时间序列交叉验证

时间序列数据不能使用随机划分，因为未来数据不能出现在训练集中。正确的做法是使用**时间序列交叉验证**（也称为前向链验证）：

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(X):
    # 训练集永远是时间上更早的数据
    # 验证集是紧接训练集之后的数据
    ...
```

每次划分中，训练集逐渐增大，验证集始终是紧接训练集的固定长度窗口。这是金融预测、销量预测等时序任务的**标准做法**。

### 模型评估的常见误区

| 误区 | 说明 | 正确做法 |
|------|------|----------|
| 数据泄漏 | 在划分前做了全局标准化/特征选择 | 先划分，再在训练集上计算统计量，应用到验证集 |
| 反复使用测试集调参 | 测试集不再是客观评估 | 保留测试集直到最终评估，用验证集调参 |
| 只看平均分 | 忽略不同折之间的方差 | 同时报告均值和标准差，检查每折结果 |
| 忽略数据分布变化 | 训练集和真实场景分布不同 | 检查数据漂移，使用时间序列划分 |

### 生产环境评估要点

根据 2026 年的行业实践，模型上线前需要确认：

1. **离线 vs 在线一致性**：离线交叉验证分数高不等于在线效果好。上线前做 A/B 测试或影子部署。
2. **数据漂移监控**：训练数据分布会随时间变化。用统计检验（如 Kolmogorov-Smirnov 检验）监控特征分布变化。
3. **切片评估**：不只报告总体指标，还要按人群、地区、时间段等维度切片评估。一个模型可能在整体上表现良好，但在某个细分群体上完全失效。
4. **可复现性**：固定随机种子，记录数据版本和模型超参数，确保评估结果可复现。

### 参考来源

- DataExpertise — [Cross Validation: The Ultimate Power Guide to Reliable Model Evaluation](https://www.dataexpertise.in/cross-validation-reliable-model-evaluation/)
- Codegenes — [Mastering Cross-Validation with PyTorch Lightning](https://www.codegenes.net/blog/cross-validation-pytorch-lightning/)
- sklearn 官方文档 — [Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html)

---

## 延伸阅读

- [机器学习基础](../机器学习基础/)
- [数据与特征工程](../数据与特征工程/)
- [模型评估与基准](/进阶学习/模型评估与基准/)
- Machine Learning Mastery — [Overfitting and Underfitting With Machine Learning Algorithms](https://machinelearningmastery.com/overfitting-and-underfitting-with-machine-learning-algorithms/)
- Caltech CS156 — [Learning from Data](https://www.youtube.com/playlist?list=PLD63A284B7615313A)（经典机器学习入门课程）

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-26 09:04:58*
