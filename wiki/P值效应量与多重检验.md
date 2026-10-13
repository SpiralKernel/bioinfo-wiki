# P值效应量与多重检验

> 更新：2026-10-13；状态：可用；验证范围：定义与原始研究核对；2000人工特征校正已运行，BH与SciPy独立核验。

P值衡量指定零假设下的数据相容性，效应量描述方向与大小；大量检验需要额外控制错误。

## P值不是哪种概率

在零假设及其他检验条件成立时，P值是获得至少与观测同样极端的统计量的概率。“极端”由预定检验定义。它不是零假设为真的概率、结果为假概率或复现概率。

P值还受样本量和误差影响。相同效应可以因样本量不同出现不同P；未显著不等于等价。报告差值、BETA、OR或log2 fold change的方向、单位和区间，见[假设检验与双侧单侧选择](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8E%E5%8F%8C%E4%BE%A7%E5%8D%95%E4%BE%A7%E9%80%89%E6%8B%A9)。

## 单次错误与多重错误

检验1000个完全无效条目，各项检验有效且单次α=0.05时，误报数期望约50；不要求每次恰好50，也不要求条目独立才能计算这个期望。若进一步假设独立，至少一个误报的概率为 $1-(1-0.05)^{1000}$。

家族错误率FWER是至少一次一类错误的概率。Bonferroni以α/m作为单项门槛，在有效P值条件下不要求独立性；代价可能是较保守。检验家族m和过滤规则必须明示，不能只对筛过最小P的集合重新缩小m。

## FDR和BH

实现假发现比例FDP为 $V/\max(R,1)$，V是假发现数、R是全部发现数；FDR是其期望。它不表示每个入选条目有相同的错误概率，也不保证每一次研究FDP均低于目标。

BH将m个有效P值排序，找满足 $p_{(i)}\le iq/m$ 的最大i，拒绝之前的条目。调整值通过从末尾向前取 $\min_{j\ge i}(mp_{(j)}/j)$ 并截到1，再还原原顺序。BH的标准保证有独立或相应正依赖条件；任意依赖下可考虑BY等方法，仍需确认P值本身有效。

## 调整后P值与区间

调整后P值与原始95%置信区间不必对应同一多重控制规则。逐项原始CI不等于同时区间。`padj=NA`也可能来自过滤、缺失或异常，不能默认为无效应。

[合成数据贯通统计推断](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E7%BB%9F%E8%AE%A1%E6%8E%A8%E6%96%AD)的2000个独立人工特征中，原始P规则选194个，BH选62个、其中3个为模拟假发现。单次FDP为3/62，不能代替对FDR方法性质的说明。教学BH实现已与SciPy核对。

保留原始P、调整值、方法、效应/区间、每特征样本量、检验家族和过滤规则。应用见[GWAS从数据准备到结果解释](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E4%BB%8E%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87%E5%88%B0%E7%BB%93%E6%9E%9C%E8%A7%A3%E9%87%8A)、[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)。

依据：[BH原始论文](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x)、[R p.adjust](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html)、[SciPy FDR说明](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.false_discovery_control.html)。
