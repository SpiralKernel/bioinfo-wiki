# rrBLUP预测实践

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

从可检查的输入矩阵开始，用rrBLUP建立单性状GBLUP基线并理解方差、GEBV与PEV。

## 使用范围与安装

rrBLUP提供标记岭回归和关系矩阵BLUP；`mixed.solve`面向一个遗传随机方差组分加残差的模型。它适合入门基线，复杂的多随机效应设计应考虑其他接口。核对的CRAN版本为4.6.3。本机没有R，以下R代码为未运行模板。

```r
install.packages("rrBLUP")
packageVersion("rrBLUP")
sessionInfo()
```

## 先生成共同输入

先按[合成家系数据贯通GS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E5%AE%B6%E7%B3%BB%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9AGS)生成 `examples/output/gs/genotypes.tsv` 和 `phenotypes.tsv`。在项目根目录启动R，运行下面的基础R准备步骤；其他GS软件R教程也可以读取它保存的RDS。

```r
raw <- read.delim("examples/output/gs/genotypes.tsv", check.names = FALSE)
dat <- read.delim("examples/output/gs/phenotypes.tsv", na.strings = "NA")
stopifnot(!anyDuplicated(raw$ID), !anyDuplicated(dat$ID))
M <- as.matrix(raw[, -1, drop = FALSE])
storage.mode(M) <- "double"
rownames(M) <- raw$ID
stopifnot(all(dat$ID %in% rownames(M)))
M <- M[match(dat$ID, rownames(M)), , drop = FALSE]
stopifnot(identical(rownames(M), as.character(dat$ID)),
          all(is.finite(M)), all(M %in% c(0, 1, 2)))
tr <- !is.na(dat$trait)
means <- colMeans(M[tr, , drop = FALSE])
keep <- apply(M[tr, , drop = FALSE], 2, var) > 0
stopifnot(any(keep))
Z <- sweep(M[, keep, drop = FALSE], 2, means[keep], "-")
p <- means[keep] / 2
K <- tcrossprod(Z) / sum(2 * p * (1 - p))
dimnames(K) <- list(as.character(dat$ID), as.character(dat$ID))
dir.create("results", showWarnings = FALSE)
saveRDS(list(dat = dat, Z = Z, K = K, means = means, keep = keep),
        "results/gs-input.rds")
```

该模板针对没有基因型缺失的人工数据，不包含真实数据填充。K包含训练和候选个体，但中心只由有表型训练个体计算。交叉验证时必须在每个训练折重新准备，而非直接拿此完整训练K和表型调参。

## 拟合并提取GEBV

```r
library(rrBLUP)
inp <- readRDS("results/gs-input.rds")
dat <- inp$dat
fit <- kin.blup(data = dat, geno = "ID", pheno = "trait",
                K = inp$K, PEV = TRUE)
str(fit)
stopifnot(all(dat$ID %in% names(fit$g)))
out <- data.frame(ID = dat$ID,
                  GEBV = unname(fit$g[as.character(dat$ID)]))
write.table(out[is.na(dat$trait), ], "results/rrblup-candidates.tsv",
            sep = "\t", row.names = FALSE, quote = FALSE)
fit$Vg
fit$Ve
```

`kin.blup`按ID连接关系矩阵，缺失表型不作为观测；K中保留候选可让其获得预测。`g`表示遗传效应，`pred`表示相应预测，不要根据名称猜测是否包括固定均值；结合手册和模型检查。若加入性别或环境，分类变量用`fixed`，连续协变量用`covariate`并明确候选取值。

## A.mat与mixed.solve的接口差异

`A.mat`要求标记编码−1/0/1，不能把0/1/2原样传进去。对当前M可以考虑 `A.mat(M - 1)`，但其默认频率基准和缺失处理与上面训练限定的手工K可能不同。不要只改函数名就声称相同数据处理。

`mixed.solve(y = ..., Z = ..., method = "REML")`可估计标记效应；若改用个体K，需明确随机效应设计及候选映射。两种模型的方差尺度不同，见[GBLUP与rrBLUP原理及实现](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GBLUP%E4%B8%8ErrBLUP%E5%8E%9F%E7%90%86%E5%8F%8A%E5%AE%9E%E7%8E%B0)。

## 检查与失败排查

核对K行列名和dat ID、方差是否落边界、候选是否全有输出、模型均值及遗传基准。PEV可用于模型下的可靠度计算，但不替代独立验证。重复ID、无多态标记、错误编码、缺失协变量和固定效应不满秩都应先解决。

本模板由REML估计方差，教学Python用内层CV选择lambda，结果不要求逐数相等。完整验证仍按[GS训练验证与数据泄漏](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GS%E8%AE%AD%E7%BB%83%E9%AA%8C%E8%AF%81%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%B3%84%E6%BC%8F)进行。参考：[官方手册](https://cran.r-project.org/web/packages/rrBLUP/rrBLUP.pdf)、[原始软件论文](https://doi.org/10.3835/plantgenome2011.08.0024)。
