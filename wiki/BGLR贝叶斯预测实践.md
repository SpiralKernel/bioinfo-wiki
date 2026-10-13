# BGLR贝叶斯预测实践

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

用共同输入建立BRR基线，再比较BayesA/B/C、BL与RKHS，同时检查采样和预测量定义。

## 准备输入与环境

本机未安装R，代码未运行。先完成[rrBLUP预测实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/rrBLUP%E9%A2%84%E6%B5%8B%E5%AE%9E%E8%B7%B5)中的基础R准备步骤，得到 `results/gs-input.rds`；该准备步骤不依赖rrBLUP拟合。输入有300个个体，60个候选的表型为NA，基因型Z采用训练集中心。

```r
install.packages("BGLR")
library(BGLR)
packageVersion("BGLR")
inp <- readRDS("results/gs-input.rds")
dat <- inp$dat
Z <- inp$Z
stopifnot(nrow(Z) == nrow(dat),
          identical(rownames(Z), as.character(dat$ID)))
dir.create("results/bglr", recursive = TRUE, showWarnings = FALSE)
```

## 从BRR开始

```r
set.seed(20261013)
fit <- BGLR(y = dat$trait,
            ETA = list(list(X = Z, model = "BRR")),
            nIter = 12000, burnIn = 2000, thin = 5,
            saveAt = "results/bglr/brr_", verbose = TRUE)
str(fit$ETA[[1]])
genetic <- drop(Z %*% fit$ETA[[1]]$b)
out <- data.frame(ID = dat$ID, GEBV = genetic,
                  predicted_y = fit$yHat)
write.table(out[is.na(dat$trait), ], "results/bglr/candidates.tsv",
            sep = "\t", quote = FALSE, row.names = FALSE)
sessionInfo()
```

BGLR允许目标y缺失；NA候选不贡献观测表型。默认包含截距，`yHat`是模型下的表型预测；在这一个标记随机项的模型里，`Z %*% b`对应遗传预测部分。增加其他随机项后应分别提取，不能把所有贡献都称为GEBV。

这些迭代数仅用于展示接口，不代表已经收敛。`saveAt`使用独立前缀，以免不同链或模型覆盖日志与样本。

## 替换模型时记录什么

BRR可以替换为BayesA、BayesB、BayesC或BL，但需要记录各模型先验和相关超参数。模型解释见[贝叶斯回归与核方法用于GS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%B4%9D%E5%8F%B6%E6%96%AF%E5%9B%9E%E5%BD%92%E4%B8%8E%E6%A0%B8%E6%96%B9%E6%B3%95%E7%94%A8%E4%BA%8EGS)。若使用线性关系核，可将ETA随机项写为 `list(K = inp$K, model = "RKHS")`；带宽或其他核构建仍需训练限定。

输入参数 `R2`用于先验设定，不是完成训练后得到的独立预测R²。不同先验的模型不能只凭训练拟合值排序。

## 采样与验证

查看方差和超参数轨迹，估计有效样本量，使用不同种子的独立链检查一致性；需要时增加迭代或调整先验。不能只丢弃固定比例预热后就宣布收敛。

外层测试y在拟合中设NA，保留一份独立的评价标签。全部预处理、位点筛选和调参只使用训练折。候选NA与外层验证NA的用途不同：后者有封存标签供评价，最终候选通常没有目标观测。

本项目仅核对接口，没有MCMC实测指标。参考：[BGLR官方手册](https://cran.r-project.org/web/packages/BGLR/BGLR.pdf)、[软件原始论文](https://doi.org/10.1534/genetics.114.164442)。
