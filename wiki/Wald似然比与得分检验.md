# Wald似然比与得分检验

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

不同检验从参数、似然改善或零模型局部变化评估证据，软件输出的P值必须注明检验类型。

## 三种思路

Wald检验看效应估计距离零有多少个标准误，单参数时常用β/SE或其平方。似然比检验比较零模型与备择模型的拟合似然。得分检验从零模型处的变化趋势与信息量判断加入位点是否有帮助。

在适用的大样本条件下，它们可能接近；有限样本、极低MAC、边界、分离或不同近似下可以有差别。模型相同不表示三种P值必然逐位相等。

## 软件参数怎样读

GEMMA的`-lm 1`与`-lmm 1`指定Wald，2指定似然比，3指定得分，4同时输出三者；LM与LMM的背景模型仍不同。GCTA和其他软件的输出要查本模块说明，不能只根据列名`P`推定检验。

PLINK数量性状输出含T_STAT；REGENIE的`LOG10P`是−log10(P)，不是原始P。涉及Firth、SPA或其他校正时，还要记录使用了哪种校正及触发条件。

## 怎样比较与检查

先统一[GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80)，明确分析样本、协变量、模型、自由度与检验方法，再解释剩余差别。若P来自似然比检验，未必能由报告的β/SE精确重建；不能因此直接断定软件算错。

诊断某个位点时同时查看效应、SE、观测数、MAC、收敛和错误码。看起来很小的P值若来自失败或不可估计模型，不应作为正常信号保留。

深入：[GEMMA手册](https://github.com/genetics-statistics/GEMMA/blob/v0.98.5/doc/manual.pdf)、[PLINK关联输出与错误码](https://www.cog-genomics.org/plink/2.0/assoc)、[REGENIE方法说明](https://rgcgithub.github.io/regenie/overview/)。
