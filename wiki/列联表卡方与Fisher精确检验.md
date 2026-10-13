# 列联表卡方与Fisher精确检验

> 更新：2026-10-13；状态：可用；验证范围：SciPy接口核对；两个列联表人工算例已运行；配对二分类仅方法说明。

分类数据用计数表组织；独立、配对和抽样设计决定参考分布与效应解释。

## 先构造计数而不是百分比

2×2表可以表示组别×是否检出。保留四个格子的计数、行列标签和分母；只给百分比通常不足以计算不确定性。一个独立单位应按设计贡献信息，重复测量不能当新的独立人次。

## 卡方与Fisher

Pearson卡方独立性检验使用观测与期望计数的偏离，期望计数按行总计×列总计/总数计算；近似是否合理要看期望计数和表结构，不能只看总样本量。Fisher在相应条件下使用精确参考分布，常用于小样本2×2表；其条件化方式与抽样假设也应说明。

```python
from scipy import stats
result = stats.fisher_exact([[8, 2], [1, 9]], alternative="two-sided")
chi = stats.chi2_contingency([[20, 15, 10], [10, 20, 15]], correction=False)
```

这两项已在[合成数据贯通统计推断](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E7%BB%9F%E8%AE%A1%E6%8E%A8%E6%96%AD)运行：第一项OR=36、P=0.00548；第二项最小期望计数12.5、P=0.0802。OR的方向取决于行列摆放；零格会影响点估计和区间。不要只报P而省略效应和表格。

## 配对和单比例是不同问题

同一对象前后是否阳性形成配对二分类表，常用McNemar等相应方法，重点是两种不一致对，而非普通独立组Fisher检验。一次成功次数与已知概率比较可用二项检验，n是独立试验数。

富集分析也可能用超几何或Fisher框架，但必须定义背景集合、入选规则和多重检验；见[富集分析与GSEA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8EGSEA)。细胞类型比例还存在供体与组成结构，不能把所有细胞合为巨大独立列联表。

依据：[SciPy Fisher](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html)、[卡方](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html)、[二项检验](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html)。
