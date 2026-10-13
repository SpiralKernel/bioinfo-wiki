# REGENIE两步关联分析

> 更新：2026-10-13；状态：可用；验证范围：REGENIE v4.1.3.gz公开小鼠数量性状Step 1与Step 2实测；二分类、集合和生存分析未执行。

REGENIE先学习背景遗传预测，再结合按染色体留出的预测检验位点；两步文件、样本与性状必须保持对应。

## 为什么分成两步

Step 1在合适的建模位点上做分块岭回归与进一步组合，产生各性状的背景预测和LOCO预测。Step 2检验目标位点，并使用相应预测及协变量。它与直接输入一个稠密GRM的LMM接口不同，详见[LOCO与近端污染](https://github.com/SpiralKernel/bioinfo-wiki/wiki/LOCO%E4%B8%8E%E8%BF%91%E7%AB%AF%E6%B1%A1%E6%9F%93)。

实际大队列中，Step 1常用质量较好的常见基因分型位点；Step 2可扩展到更多填充或测序位点。本例用同一份8544位点硬调用数据验证接口，不代表这是所有项目应采用的建模集合。

## 输入与准备

基因型可按版本使用BED、PGEN或BGEN等格式。表型与协变量文件需要标题，起始列为FID、IID，并明确选择性状与协变量。类别型协变量应通过支持的接口或明确的指示编码处理。

Step 1的预测文件列表必须属于同一性状、基因型背景和样本配置，不能把另一批个体的`_pred.list`直接带进来。表型缺失和协变量缺失的处理要查看日志中的实际分析个体。

## 本轮已实测的数量性状命令

使用REGENIE v4.1.3.gz。准备见[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)，在`examples/output/gwas-real/`下执行：

```bash
mkdir -p regenie
regenie --step 1 --bed prepared/qc \
  --phenoFile prepared/regenie.pheno.txt --phenoCol CD8 \
  --covarFile prepared/regenie.covariates.txt --covarColList PC1,PC2,PC3 \
  --qt --bsize 200 --lowmem --threads 2 --out regenie/step1

regenie --step 2 --bed prepared/qc \
  --phenoFile prepared/regenie.pheno.txt --phenoCol CD8 \
  --covarFile prepared/regenie.covariates.txt --covarColList PC1,PC2,PC3 \
  --qt --bsize 200 --minMAC 20 --threads 2 \
  --pred regenie/step1_pred.list --out regenie/step2
```

`--bsize`控制处理块大小，不是显著性阈值；`--lowmem`通过中间文件降低部分内存需求，也会增加I/O。MAC20在本例只是明确的教学配置，应按性状和工具规则制定实际门槛。

## 二分类与其他模式

二分类使用`--bt`，并核对默认0/1编码与`--cc12`等选项。Step 2可配置Firth或SPA等处理，触发阈值和近似方法必须记录；本轮未实测这些二分类路径。

REGENIE还支持集合检验及版本相关的生存分析等功能，它们有自己的输入和假设。`--ignore-pred`会改变背景调整行为，不能在缺少Step 1文件时悄悄加上，再把结果称为原两步分析。

## 输出与检查

先检查Step 1交叉验证、实际使用样本与位点、LOCO输出列表；Step 2核对预测对应、每个性状的有效样本、检验失败与位点过滤。

本例结果含`ALLELE0 ALLELE1 A1FREQ N TEST BETA SE CHISQ LOG10P`。效应针对当前编码的ALLELE1；`LOG10P`是−log10(P)，不是P。导入绘图时直接将它再次取负对数会造成错误。

## 实测限制

本例用于学习接口及文件交接。小鼠家系数据中的诊断分布与GEMMA/GCTA不同，说明“程序完成”并不能证明某配置适合当前研究。不能把本例作为REGENIE在大型人类队列中的性能或校准评价。

深入：[REGENIE模型概览](https://rgcgithub.github.io/regenie/overview/)、[参数文档](https://rgcgithub.github.io/regenie/options/)、[大队列使用建议](https://rgcgithub.github.io/regenie/recommendations/)、[原始研究](https://doi.org/10.1038/s41588-021-00870-7)。
