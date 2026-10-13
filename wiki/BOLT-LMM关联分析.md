# BOLT-LMM关联分析

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

BOLT-LMM面向较大队列的混合模型关联，模型模式、样本适用性、参考资源与输出列需要同时核对。

## 先确认是否适合你的数据

本页核对的是官方v2.5手册。作者建议在超过5000个样本的人类数据中使用，近似方法的验证范围主要为人类；小样本建议考虑GCTA或GEMMA。提供非人类染色体参数，不等于已经在任意物种与育种设计中完成验证。

因此本轮的小鼠家系例子没有强行运行BOLT。对病例对照明显不平衡的性状，官方另建议考虑SAIGE、REGENIE等路线；BOLT的线性混合模型效应不能直接当作逻辑模型log-OR。

## 两种任务与关联模式

BOLT-LMM做关联，BOLT-REML估计方差组分和遗传相关等；`--reml`输出不能当作GWAS位点结果。关联的`--lmm`包含相应混合先验模式，`--lmmInfOnly`仅做无限小模型统计；模式不同可能产生不同输出列。

需要区分建模位点和更多待检验位点。输入可使用PLINK硬调用建模，并按支持的接口检验填充数据；填充剂量、样本文件与参考身份要保持对应。

## 官方接口模板

以下未在本机执行，文件与目录均需自行准备；适用于已确认合适的人类数量性状设计：

```bash
mkdir -p results
bolt --bfile=cohort_model \
  --phenoFile=phenotypes.tsv --phenoCol=trait \
  --covarFile=covariates.tsv --qCovarCol=age \
  --qCovarCol=PC1 --qCovarCol=PC2 --qCovarCol=PC3 \
  --lmm --LDscoresFile=matching_LD_scores.tab.gz \
  --numThreads=2 --statsFile=results/bolt.stats
```

`--qCovarCol`为定量协变量，分类变量使用相应`--covarCol`接口。LD score表需要与所用模式、群体及坐标资源兼容；不能把手册中的欧洲人群表无条件用于其他群体。遗传图谱与扩展BGEN输入等要求应按固定版本教程补全。

## 读输出时保留什么

核对SNP、染色体、位置、ALLELE1/ALLELE0、A1FREQ、BETA、SE和具体统计量列。PLINK建模输入中第一等位基因通常对应效应方向，但它不一定是生物学REF；BGEN等格式及版本选项还需另核对。

不同版本中INFO字段含义可能变化；v2.5手册明确调整了其与缺失比例的关系。因此不能只凭同名列就与其他工具的INFO直接互换。

## 诊断与复现

检查样本交集、缺失处理、建模位点、校准资源、拟合警告和实际使用的模型。软件自动过滤不等于完整研究质控，应另保存MAF、MAC、HWE等检查与决定。

先运行发行包提供的例子，再用于目标数据。记录版本、原始命令、资源校验与具体P值列；解释参考[GWAS曼哈顿图QQ图与膨胀因子](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E6%9B%BC%E5%93%88%E9%A1%BF%E5%9B%BEQQ%E5%9B%BE%E4%B8%8E%E8%86%A8%E8%83%80%E5%9B%A0%E5%AD%90)，对比参考[GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)。

深入：[BOLT-LMM v2.5官方手册](https://alkesgroup.broadinstitute.org/BOLT-LMM/BOLT-LMM_manual.html)、[BOLT-LMM原始研究](https://doi.org/10.1038/ng.3190)、[生物样本库规模应用](https://doi.org/10.1038/s41588-018-0144-6)。
