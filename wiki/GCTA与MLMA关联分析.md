# GCTA与MLMA关联分析

> 更新：2026-10-13；状态：可用；验证范围：GCTA v1.94.1公开小鼠稠密GRM及MLMA实测；GREML、COJO和完整MLMA-LOCO未执行。

GCTA包含多种遗传统计任务；MLMA使用稠密GRM做关联，不能与GREML或fastGWA模块混称。

## 先选模块再写命令

GCTA的GRM模块构建关系矩阵，GREML估计方差组分，MLMA检验关联，COJO使用汇总统计做条件与联合分析。它们输入和研究目标不同。运行过GCTA不等于已经完成GWAS，输出遗传率也不是位点P值表。

本页实测稠密GRM和数量性状MLMA；快速稀疏矩阵方法另见[fastGWA与fastGWA-GLMM](https://github.com/SpiralKernel/bioinfo-wiki/wiki/fastGWA%E4%B8%8EfastGWA-GLMM)。模型前置见[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)及[零模型与方差组分](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%9B%B6%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BB%84%E5%88%86)。

## 输入约定

使用BED/BIM/FAM前缀与明确的样本集合。表型文件通常为无标题的FID、IID、性状值；`--mpheno`选择多列表型中的相应列。定量协变量用`--qcovar`，分类协变量用`--covar`，不要用一种接口承接所有编码。

稠密GRM通常由`.grm.bin`、`.grm.N.bin`和`.grm.id`共同组成，`--grm`后给前缀。二进制矩阵与样本ID文件是一套；只有复制矩阵而换掉ID表会破坏对应关系。

## 已运行的命令

工作目录为[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)的`examples/output/gwas-real/`：

```bash
mkdir -p gcta
gcta64 --bfile prepared/qc --autosome-num 19 \
  --make-grm --thread-num 2 --out gcta/full

gcta64 --bfile prepared/qc --autosome-num 19 \
  --grm gcta/full --mlma --pheno prepared/gcta.pheno.txt \
  --qcovar prepared/gcta.qcovar.txt --thread-num 2 --out gcta/mlma_pc3
```

实测版本v1.94.1，启动横幅记录构建信息。与本例小鼠对应的常染色体数为19；其他物种需要重新设置。表型和三个PC与PLINK/GEMMA案例来自同一批样本。

## 如何阅读结果

本例`.mlma`标题为`Chr SNP bp A1 A2 Freq b se p`。A1对应效应计数，b是性状单位的效应；Freq及参考身份都要按输入与输出说明核对。文件没有逐位点N列时，应另保留分析个体与缺失信息，不凭完整数据总数填充所有研究结果。

本例rs3683945的A1为A，b≈−0.0671868、P≈0.263012。结果与普通LM不同，不能因此认定哪一软件出错；本例含家系结构，背景模型已改变。

## GRM与LOCO的选择

构建GRM的位点质量、权重、频率与样本会影响模型。PCA使用的LD剪枝集合与GRM集合可以不同，但每个名单都要保留理由。不能只因PCA剪枝就自动对所有关联与GRM阶段使用同一组位点。

GCTA还提供`--mlma-loco`，其目标是按测试染色体排除背景信息；本轮未执行该完整模块。已有的GEMMA单染色体对照用于理解[LOCO与近端污染](https://github.com/SpiralKernel/bioinfo-wiki/wiki/LOCO%E4%B8%8E%E8%BF%91%E7%AB%AF%E6%B1%A1%E6%9F%93)，不应标记成GCTA-LOCO实测。

## 排错与深入

先查看实际纳入的样本、GRM维度、方差组分收敛和关联SNP数。出现不可逆、边界或少量有效个体时，检查输入与模型，不直接忽略警告或强行继续。稠密矩阵规模随n²增长，需要资源评估。

深入：[GCTA官方手册](https://yanglab.westlake.edu.cn/software/gcta)、[GCTA官方源代码](https://github.com/JianYang-Lab/GCTA)、[GCTA原始论文](https://doi.org/10.1016/j.ajhg.2010.11.011)、[GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)。
