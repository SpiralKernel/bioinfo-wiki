# 置换检验与Bootstrap实践

> 更新：2026-10-13；状态：可用；验证范围：人工独立样本BCa、9999次置换及20种精确分组已运行；复杂分层置换未运行。

Bootstrap近似估计量的抽样分布，置换构造零假设参考；两者必须尊重独立单位。

## 先决定重采样单位

独立个体可按个体重采样；配对数据按配对索引一起抽；层级数据可考虑供体、家系或其他合适的独立块。方法还依赖目标和抽样结构，不能把所有块bootstrap视为完全相同。

Bootstrap通常有放回抽观测并重新计算统计量；置换按零假设允许的交换规则重排数据。后者要求交换性，不能只因为两组均值相等就假定任何异方差数据都允许直接交换标签。

## 两个明确的Python接口

```python
from scipy import stats
import numpy as np

def difference(B, A, axis=0):
    return np.mean(B, axis=axis) - np.mean(A, axis=axis)

boot = stats.bootstrap((B, A), difference, paired=False,
                       method="BCa", n_resamples=4999, rng=20261015)
perm = stats.permutation_test((B, A), difference,
                             permutation_type="independent",
                             n_resamples=9999, rng=20261014)
```

这只是接口模板；B/A输入与置换条件必须先确定。完整实测中，Bootstrap用于独立异方差样本，置换另外生成满足零假设交换性的同方差位置模型数据，避免混用假设。

## 区间与P值的计算规则

百分位、basic和BCa区间不是同一种方法；小样本、离散数据或退化统计量可让Bootstrap失效。加大重采样次数只减少Monte Carlo误差，不能增加独立生物学样本。

Monte Carlo置换P值通常采用避免零值的修正；SciPy双侧值以两侧尾概率的规则计算。报告置换次数、精确或随机方式、统计量、单双侧与随机种子，不把没有观测到更极端结果写成P=0。

## 已运行结果

[合成数据贯通统计推断](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E7%BB%9F%E8%AE%A1%E6%8E%A8%E6%96%AD)中BCa均值差区间为[0.3035,1.6695]；另一组置换例子P=0.4194。六个固定数 `[1,2,3]` 与 `[4,5,6]` 的20种分组精确双侧P=0.1，说明小样本可达到的P值很离散。

配对处理、相关性或协变量调整需要相应置换设计，不能一律全局打乱。参考：[SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)、[permutation_test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html)。
