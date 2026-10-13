# rMVP关联分析实践

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

rMVP通过外存矩阵和并行运行关联分析，转换后的样本顺序及协变量对应是最重要的检查点。

## 功能与模型

rMVP提供GLM、MLM和FarmCPU等关联接口，并组织转换、亲缘估计、PC和绘图。它是软件实现，不等于一个新的统一模型；方法区别见[FarmCPU与BLINK原理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FarmCPU%E4%B8%8EBLINK%E5%8E%9F%E7%90%86)及[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)。

本页按官方README核对，未在本机安装运行。R包、原生库、数值库与输出设置都应记录版本。

## 从输入到外存文件

用`MVP.Data`及对应格式接口转换基因型，按同一流程处理表型与map。外存矩阵通常包含描述文件和背后的数据文件，不能只保留`.desc`而丢失数据本体。

若转换同时传入了表型，应读取转换后生成的`.phe`等结果，核对共同个体和顺序，而不是继续使用未重新排列的原表型。map中的标记顺序也必须对应矩阵的标记维度。

## 关联模板

下面需要已经生成并审计过`mvp`前缀的数据，未在本机执行：

```r
library(rMVP)
genotype <- bigmemory::attach.big.matrix("mvp.geno.desc")
phenotype <- read.table("mvp.phe", header=TRUE, check.names=FALSE)
map <- read.table("mvp.geno.map", header=TRUE, check.names=FALSE)
stopifnot(!anyDuplicated(phenotype[[1]]))
fit <- MVP(phe=phenotype[, c(1, 2)], geno=genotype, map=map,
           nPC.GLM=3, nPC.MLM=3, nPC.FarmCPU=3,
           ncpus=2, method=c("GLM", "MLM", "FarmCPU"),
           file.output=c("pmap", "pmap.signal", "plot", "log"))
sessionInfo()
```

先核对转换后的矩阵行列语义、个体与标记数量，再运行模板。此处三个PC仅展示接口；没有额外环境协变量，也不能自动代表你的实验设计。

## 自备K和协变量时

可通过`K`和相应`CV.GLM`、`CV.MLM`、`CV.FarmCPU`传入对象。官方明确说明协变量不会自动替你重新排列个体，因此必须先按最终基因型顺序对齐；仅维度相同不够。

已经在CV矩阵中添加PC时，不再重复设置对应的nPC参数。不要因为函数调用成功就假定自动生成的PC、外部PC和环境变量没有重复或共线，见[关联模型中的协变量与残差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%B3%E8%81%94%E6%A8%A1%E5%9E%8B%E4%B8%AD%E7%9A%84%E5%8D%8F%E5%8F%98%E9%87%8F%E4%B8%8E%E6%AE%8B%E5%B7%AE)。

## 资源、输出与常见误读

内存映射有助于管理大矩阵，但并行线程、矩阵运算与文件读取仍需资源。明确`ncpus`与任务限制，不无意使用共享服务器全部CPU；`maxLine`等块处理参数按该版本文档选择。

保存完整关联表、显著表、图和日志，并核对实际阈值含义。绘图函数能接收其他软件结果，不代表那些结果已在模型、效应方向和样本上统一。置换也要尊重家系或实验设计，不能任意打乱个体标签来制造阈值。

深入：[rMVP官方说明](https://github.com/xiaolei-lab/rMVP)、[CRAN参考手册](https://cran.r-project.org/web/packages/rMVP/rMVP.pdf)、[原始软件论文](https://doi.org/10.1016/j.gpb.2020.10.007)、[GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)。
