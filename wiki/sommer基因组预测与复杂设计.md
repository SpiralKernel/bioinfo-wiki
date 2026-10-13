# sommer基因组预测与复杂设计

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

以当前mmes接口传入已知遗传协方差结构，再逐步扩展多随机效应和复杂设计。

## 什么时候使用

当模型需要多个随机效应、多性状或环境交互时，可以考虑sommer。复杂设计不能靠增加随机项名称自动解决，应先明确每个效应的观测层级与协方差。本机没有R，以下模板未运行。

当前官方定量遗传教程使用 `mmes`及`vsm`/`ism`；旧教程中的`mmer`/`vsr`有弃用或接口差异。保存包版本，避免混用跨版本参数。

## 共同输入

先运行[rrBLUP预测实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/rrBLUP%E9%A2%84%E6%B5%8B%E5%AE%9E%E8%B7%B5)中的基础R准备步骤，读取训练中心的K和包含NA候选的dat。

```r
install.packages("sommer")
library(sommer)
library(Matrix)
packageVersion("sommer")
inp <- readRDS("results/gs-input.rds")
dat <- inp$dat
K <- inp$K
dat$ID <- factor(dat$ID, levels = rownames(K))
stopifnot(!anyNA(dat$ID), identical(rownames(K), colnames(K)))
```

## 给mmes传入精度矩阵

参照当前官方教程的关系矩阵示例：

```r
delta <- 1e-4
Ki <- solve(K + diag(delta, nrow(K)))
Ki[lower.tri(Ki)] <- t(Ki)[lower.tri(Ki)]
Ki <- as(as(as(Ki, "dMatrix"), "generalMatrix"), "CsparseMatrix")
attr(Ki, "inverse") <- TRUE
fit <- mmes(trait ~ 1,
            random = ~ vsm(ism(ID), Gu = Ki),
            rcov = ~ units, data = dat, verbose = TRUE)
summary(fit)$varcomp
str(fit$u)
head(fit$u)
sessionInfo()
```

这里传入的是 `K + delta I` 的逆，属性名为小写 `inverse`。对角调整会改变所用协方差结构，不是所有项目必须照搬的固定参数。若使用其他接口或直接传协方差，必须重新核对手册，不能把G和G逆混用。

## 结果如何核对

官方当前示例从`fit$u`按个体名提取遗传效应。实际项目先查看结构、行名与效应列，确认训练和候选是否齐全，再按ID连接导出，禁止按行位置直接贴回原表。对多随机效应模型，需要分别标识加性、显性、共同环境及交互项，不能把任意BLUP列都称为GEBV。

检查方差组分、边界、收敛日志和预测基准。更多效应不保证更好：家系共同环境与遗传关系可能混淆，重复记录、环境连接和样本量决定可估计程度。

## 从基线扩展

先以单性状加性模型通过[GS训练验证与数据泄漏](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GS%E8%AE%AD%E7%BB%83%E9%AA%8C%E8%AF%81%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%B3%84%E6%BC%8F)，再增加环境、重复测量或多性状结构。每次扩展说明新增效应、矩阵维度、验证部署目标及独立预测表现。

官方教程示例数据现通过enhancer包读取；旧代码的数据来源和接口可能已经变化。参考：[sommer定量遗传官方教程](https://cran.r-project.org/web/packages/sommer/vignettes/sommer.qg.html)、[CRAN手册](https://cran.r-project.org/web/packages/sommer/sommer.pdf)。
