# t检验配对设计与Welch检验

> 更新：2026-10-13；状态：可用；验证范围：NIST与SciPy接口核对；Welch公式、区间及配对反例已在人工数据运行。

连续数值的均值比较先区分独立与配对，再确定方差和参考分布假设。

## 三种常见设计

单样本t检验比较均值与指定值；配对t检验对每对差值做单样本检验；独立两样本t检验比较两组均值。配对通常来自同一个体前后或事先匹配，不能根据两组长度相同就判定配对。

经典t参考分布的精确性依赖相应正态误差条件；较大样本可能使用近似，但独立性、离群值和重尾仍需检查。配对设计关注差值分布，不要求把两组原始值分别做正态筛选后才使用。

## Welch怎样计算

设目标为B组均值减A组均值：

$$SE=\sqrt{s_A^2/n_A+s_B^2/n_B},\qquad t=(\bar y_B-\bar y_A)/SE.$$

Welch采用近似自由度，不要求两组总体方差相等。等方差Student版本使用合并方差，是另一假设设置。没有充分理由时，不必先做方差齐性检验再机械切换两种t检验。

## 最小代码

```python
from scipy import stats
independent = stats.ttest_ind(B, A, equal_var=False, alternative="two-sided")
paired = stats.ttest_rel(after, before, alternative="two-sided")
```

A、B和前后数组需由自己的设计明确；这段是接口说明。完整已运行输入见[合成数据贯通统计推断](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E7%BB%9F%E8%AE%A1%E6%8E%A8%E6%96%AD)：Welch效应0.9911，95%区间[0.2749,1.7074]，P=0.00761；配对数据中保留配对得到P=0.00191，忽略配对得到P=0.677。不同P来自不同的误差结构，并不表示“选择更显著的方法”。

## 不适用的直接套用

原始RNA-seq计数、严重依赖的数据和多因素设计不应不加判断地逐列套t检验；可进入[广义线性模型与逻辑回归](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B9%BF%E4%B9%89%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E9%80%BB%E8%BE%91%E5%9B%9E%E5%BD%92)或[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)。小样本极端值明显时先检查数据和稳健方法，不把非参数检验当万能替代。

公式与条件见[NIST两样本t检验](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm)、[SciPy官方接口](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)。
