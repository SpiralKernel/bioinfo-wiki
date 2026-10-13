# ASReml基因组预测接口

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

用已知关系矩阵定义遗传随机效应，核对矩阵属性、缺失表型与预测量的区别。

## 使用前提

ASReml-R是需要相应授权的软件。本页适合已经使用它的项目；本机未安装，模板未运行。安装和版本应按官方发行说明执行，并记录R、ASReml及授权环境。

先完成[rrBLUP预测实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/rrBLUP%E9%A2%84%E6%B5%8B%E5%AE%9E%E8%B7%B5)中的基础R输入准备，得到K和包含NA候选的dat。以下展示加性遗传关系接口；更复杂的试验、重复测量和多性状模型需另作设计。

## 传入协方差矩阵

```r
library(asreml)
inp <- readRDS("results/gs-input.rds")
dat <- inp$dat
K <- inp$K
stopifnot(identical(rownames(K), colnames(K)))
dat$ID <- factor(dat$ID, levels = rownames(K))
stopifnot(!anyNA(dat$ID))
fit <- asreml(fixed = trait ~ 1,
              random = ~ vm(ID, K, singG = "PSD"),
              residual = ~ idv(units), data = dat,
              na.action = na.method(y = "include", x = "fail"))
summary(fit)$varcomp
str(coef(fit)$random)
sessionInfo()
```

K在这里是已知协方差的相对关系结构，有正确dimnames。`singG="PSD"`用于相应半正定情形的接口处理，不能替代检查矩阵来源、对称性及ID映射。查看模型收敛和约束状态，必要时按官方方法更新拟合。

## 逆矩阵属性不要混用

`vm`也可以使用适当格式的逆矩阵，官方接口通过 `INVERSE` 属性等识别，注意这里是大写。sommer示例中的小写`inverse`不能直接移植过来。如果准备的是G逆却被当成G，模型中的关系结构就会改变。

不是所有矩阵都可以直接`solve`；基因组矩阵常可能半正定。若加入对角调整或混合，记录具体处理和统计含义。

## 提取GEBV与预测表型

`coef(fit)$random`可用于检查随机效应解，但应核对名称中的模型项与个体ID，再只提取加性遗传项。`predict(fit, classify="ID")`得到的预测表可能包含均值或其他模型贡献，不能自动命名为GEBV。

对NA候选，检查ID水平是否保留、是否有预测、固定效应是否可估计。模型下的标准误或PEV与实际部署预测能力不同，仍需按[GS训练验证与数据泄漏](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GS%E8%AE%AD%E7%BB%83%E9%AA%8C%E8%AF%81%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%B3%84%E6%BC%8F)做外层验证。

## 排错顺序

先核对数据ID与矩阵行列名，再核对协方差或逆矩阵身份、固定效应列满秩、NA处理与候选类别。之后检查方差边界、残差结构和模型连接性。输出有数值不代表每个预测都可估计或可跨环境比较。

参考：[ASReml已知方差结构官方说明](https://asreml.kb.vsni.co.uk/knowledge-base/knownstruc/)、[ASRgenomics官方手册](https://asreml.kb.vsni.co.uk/wp-content/uploads/sites/3/ASRgenomics_Manual.pdf)。
