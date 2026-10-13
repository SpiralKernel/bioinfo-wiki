# SAIGE单变异关联分析

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

SAIGE先拟合零混合模型，再做单变异检验；二分类的SPA处理与样本相关性建模需要共同核对。

## 用来解决什么问题

SAIGE可对数量或二分类性状拟合相应的零混合模型，并进行关联检验。二分类单变异流程使用SPA等方法处理病例对照不平衡带来的尾部近似问题；同时还要考虑低MAC、效应估计、收敛和相关性。

SPA、Firth与GRM各有作用，不能互相替代，见[二分类性状OR与病例对照不平衡](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%8C%E5%88%86%E7%B1%BB%E6%80%A7%E7%8A%B6OR%E4%B8%8E%E7%97%85%E4%BE%8B%E5%AF%B9%E7%85%A7%E4%B8%8D%E5%B9%B3%E8%A1%A1)。SAIGE-GENE/集合检验有单独的数据准备与调用，不是把单变异结果改个文件名。

## 运行前准备

固定SAIGE版本、R依赖或容器及官方示例。零模型阶段可使用PLINK基因型或适用的稀疏GRM配置；表型表有标题，包含唯一的样本ID、目标性状与协变量。若只使用IID，先确认它在整个研究中唯一，不能忽略重复FID/IID组合的区别。

待检验数据可为版本支持的VCF/BCF、BGEN、PLINK或SAV等。索引、样本ID、GT/DS字段和等位基因顺序需分别确认；BGEN的sample信息不能随意替换。

## 二分类流程模板

以下只是按官方接口整理的结构，本机未安装运行SAIGE。需把文件名、样本ID列和性状列替换为实际输入，并先运行固定版本的官方测试：

```bash
mkdir -p results
Rscript step1_fitNULLGLMM.R \
  --plinkFile=cohort --phenoFile=phenotypes.tsv \
  --phenoCol=case_status --sampleIDColinphenoFile=IID \
  --covarColList=age,PC1,PC2,PC3 --traitType=binary \
  --nThreads=2 --outputPrefix=results/saige_null

Rscript step2_SPAtests.R \
  --vcfFile=chr1.dosage.vcf.gz --vcfField=DS --chrom=1 \
  --GMMATmodelFile=results/saige_null.rda \
  --varianceRatioFile=results/saige_null.varianceRatio.txt \
  --minMAC=20 --LOCO=TRUE \
  --SAIGEOutputFile=results/saige_chr1.tsv
```

Step 1模型文件和方差比文件来自同一轮拟合；Step 2的染色体与LOCO预测必须对应。VCF索引要求及废弃参数随版本变化，应按[当前Step 2文档](https://saigegit.github.io/SAIGE-doc/docs/single_step2.html)核对，不能照抄老教程中的索引选项。

## 完整与稀疏配置的区别

零模型使用完整GRM还是稀疏GRM，会影响输入、计算、LOCO行为以及后续快速检验设置。官方稀疏拟合示例不等于完整模式仅换一个路径；其Step 2可能还需要对应稀疏矩阵与样本ID文件。

数量性状接口使用`--traitType=quantitative`等设置；官方示例包含逆正态变换选项。是否变换与效应尺度必须记录，不能把变换后的β与原始量纲β直接比较。分类协变量接口的命名也应按手册确认，不凭参数中的字母猜测含义。

## 检查什么才算跑通

先核对病例/对照数、有效样本、收敛及方差比估计，再核对Step 2的实际位点数量、MAC、缺失处理、SPA或其他校正记录。输出中效应对应的等位基因与频率字段需要一起读；有更多细节输出时，可检查病例/对照携带情况。

必要时按官方选项估计Firth校正效应，但并非所有P值都能由一个β/SE重建。空输出、不可估计和极端稀疏记录应单独整理，而非替换为P=1。

深入：[SAIGE官网](https://saigegit.github.io/SAIGE-doc/)、[Step 1](https://saigegit.github.io/SAIGE-doc/docs/single_step1.html)、[Step 2](https://saigegit.github.io/SAIGE-doc/docs/single_step2.html)、[原始方法](https://doi.org/10.1038/s41588-018-0184-y)。
