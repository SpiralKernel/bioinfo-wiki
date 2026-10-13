# FarmCPU与BLINK原理

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

FarmCPU与BLINK通过迭代选择背景位点帮助检验其他位点，背景选择本身也是分析方法的一部分。

## 为什么引入多位点背景

单个位点检验会受到相关位点和背景结构影响；把很多相关位点一起作为固定效应又可能造成共线和计算问题。FarmCPU与BLINK尝试迭代选择一组代表背景的候选标记，再检验其他位点。

这里的pseudo-QTN是模型过程选出的背景代理位点，不是已经验证的因果变异。选择结果随样本、性状、参数及迭代过程改变，应与最终显著列表区分保存。

## 两种方法有什么区别

FarmCPU交替使用固定效应与随机效应部分，更新候选背景位点；其设计包含按基因组区间选取代表标记等步骤。BLINK利用LD信息减少冗余，并用BIC等准则选择背景规模，以改变候选选择与计算过程。

BIC是结合拟合与模型复杂度的准则，不能把它直接当作每个位点的P值。两种方法也不能仅概括成“更快的同一个MLM”。具体实现细节按原论文和所用软件版本核对。

## 软件怎样实现

[GAPIT多模型GWAS实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GAPIT%E5%A4%9A%E6%A8%A1%E5%9E%8BGWAS%E5%AE%9E%E8%B7%B5)提供FarmCPU与BLINK接口；[rMVP关联分析实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/rMVP%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E5%AE%9E%E8%B7%B5)包含FarmCPU，不能因此假定也实现了同样的BLINK调用。相同方法名在不同实现中还可能有不同默认值、停止条件和输出组织。

输入准备仍需要样本对齐、位点与染色体信息、性状及必要协变量。迭代方法不会自动修复错位样本、混杂、低质量分型或不合适的独立单位。

## 实践应该检查什么

先用所选软件官方数据运行一个模型，保存迭代日志、候选集合、收敛或停止原因。再与明确配置的GLM/MLM比较共同位点的效应与证据，并检查参数敏感性。

不能把显著位点更多当作方法更好。自适应选择、真实效应结构和假阳性控制需要通过合适模拟或独立证据评估；本文未在本机执行FarmCPU或BLINK。

深入：[FarmCPU原始研究](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1005767)、[BLINK原始研究](https://doi.org/10.1093/gigascience/giy154)、[GAPIT官方实现](https://github.com/jiabowang/GAPIT)。
