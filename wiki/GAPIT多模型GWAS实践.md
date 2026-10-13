# GAPIT多模型GWAS实践

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

GAPIT把多种关联与预测方法组织在R接口中；每次应明确模型、样本交集及输出，而不是把一键运行当成模型选择。

## 软件与方法分开理解

GAPIT支持GLM、MLM、CMLM、MLMM、FarmCPU、BLINK等方法及其他任务。它们不共享完全相同的假设与背景调整；FarmCPU和BLINK的迭代选择见[FarmCPU与BLINK原理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FarmCPU%E4%B8%8EBLINK%E5%8E%9F%E7%90%86)。GAPIT中的GLM语境通常是general linear model，不能直接等同于其他软件的广义模型接口。

截至本次核对，官方仓库已提供Version IV说明；旧教程可能基于GAPIT3或其他源码。安装包、函数脚本、方法实现和示例数据都应固定版本或提交。

## 三类主要数据

表型Y通常第一列为Taxa，后面为性状；数值基因型GD通常第一列为Taxa，后续为标记；标记信息GM至少明确标记、染色体与位置。HapMap等其他入口按该版本手册处理，不能只改扩展名。

先核对Taxa唯一、共同个体、数值编码、缺失处理和标记顺序。自动取交集并不意味着所有原始个体都被分析，也不代表重复ID会被正确处理。

## 基于官方输入结构的R模板

本机无GAPIT环境，以下未运行；请先从[官方仓库](https://github.com/jiabowang/GAPIT)获取匹配版本的教程数据，保存为这些文件名，并在独立输出目录运行：

```r
library(GAPIT)
Y <- read.table("traits.txt", header=TRUE, check.names=FALSE)
GD <- read.table("genotypes_numeric.txt", header=TRUE, check.names=FALSE)
GM <- read.table("marker_map.txt", header=TRUE, check.names=FALSE)
stopifnot(!anyDuplicated(Y[[1]]), !anyDuplicated(GD[[1]]))
fit <- GAPIT(Y=Y[, c(1, 2)], GD=GD, GM=GM,
             model=c("GLM", "MLM", "FarmCPU", "Blink"),
             PCA.total=3, file.output=TRUE)
sessionInfo()
```

模型字符串按当前官方示例使用`Blink`；不同版本的大小写与方法调用需再次核对。这里的三个PC是模板设置，不是育种群体通用推荐。若要公平比较，应先固定共同个体、位点与固定效应配置。

## 输出和模型过程

分别保存每个模型的关联表、实际分析个体、参数和日志。阅读效应或P列前核对该模型的字段定义、单位及计数编码；不要把不同模型的输出直接拼成一列无来源P值。

对FarmCPU/BLINK还应查看候选背景位点、迭代及停止条件。候选代理标记不是已经验证的因果QTN；显著数更多也不自动代表更好的错误控制。

## 常见问题

Taxa交集变小先查命名和缺失，而不是继续画图。输入太大时评估R矩阵与多次复制的内存开销；从网上直接加载不断更新的源码，不足以保证可复现。若输入分类或计数性状，要核对所选方法是否适用。

深入：[GAPIT官方说明与手册入口](https://github.com/jiabowang/GAPIT)、[GAPIT4原始研究](https://doi.org/10.1093/molbev/msag107)、[FarmCPU原始研究](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1005767)、[GWAS参数选择与敏感性分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E5%8F%82%E6%95%B0%E9%80%89%E6%8B%A9%E4%B8%8E%E6%95%8F%E6%84%9F%E6%80%A7%E5%88%86%E6%9E%90)。
