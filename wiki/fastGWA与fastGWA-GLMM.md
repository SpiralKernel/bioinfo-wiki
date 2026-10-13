# fastGWA与fastGWA-GLMM

> 更新：2026-10-13；状态：可用；验证范围：GCTA v1.94.1稀疏GRM及fastGWA数量性状实测；fastGWA-GLMM二分类未执行。

fastGWA利用稀疏关系和快速检验提高可扩展性；数量性状与二分类模块需要分别配置和核验。

## 它与MLMA有什么区别

fastGWA是GCTA中的快速关联模块，常用稀疏GRM表示较强的个体相关性，并结合相应近似进行数量性状检验。fastGWA-GLMM针对二分类，包含逻辑混合模型及SPA等处理。它们不只是给[GCTA与MLMA关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GCTA%E4%B8%8EMLMA%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)增加线程。

稀疏化会改变背景表示，因此不应要求与稠密GRM方法每个位点完全相同；也不能把一个稀疏阈值当作所有人群或育种群体的通用参数。

## 稀疏GRM怎样准备

本例先由同一批质控样本生成稠密GRM，再用阈值构建稀疏形式。较大数据还可按官方说明分块或直接建立稀疏输出；矩阵分块方式、索引和合并顺序必须遵循工具约定。

工作目录为`examples/output/gwas-real/`，前置步骤见[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)：

```bash
gcta64 --grm gcta/full --make-bK-sparse 0.05 --out gcta/sparse

gcta64 --bfile prepared/qc --autosome-num 19 \
  --grm-sparse gcta/sparse --fastGWA-mlm \
  --pheno prepared/gcta.pheno.txt --qcovar prepared/gcta.qcovar.txt \
  --seed 20261013 --thread-num 2 --out gcta/fastgwa_pc3
```

这两条在v1.94.1中实测。0.05为本轮展示设置，随机种子用于复现抽样调参过程；应保留日志中的估计与收敛信息。

## 二分类接口与验证范围

fastGWA-GLMM对应`--fastGWA-mlm-binary`等接口；需准备正确标签、病例/对照数及合适的GRM、协变量与质量控制。按所选版本的二分类官方示例确认编码和输出效应尺度，不直接将上述连续CD8表型改个参数就运行。

本轮没有运行二分类模块，不能把数量性状的成功和图形当作不平衡病例对照验证。前置概念见[二分类性状OR与病例对照不平衡](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%8C%E5%88%86%E7%B1%BB%E6%80%A7%E7%8A%B6OR%E4%B8%8E%E7%97%85%E4%BE%8B%E5%AF%B9%E7%85%A7%E4%B8%8D%E5%B9%B3%E8%A1%A1)及[MAF与MAC及稀有变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/MAF%E4%B8%8EMAC%E5%8F%8A%E7%A8%80%E6%9C%89%E5%8F%98%E5%BC%82)。

## 怎样检查是否运行了想要的模型

检查实际是否读入稀疏GRM、保留多少相关关系、分析个体数、方差估计、Gamma调参及测试位点数。按官方说明，缺失相关矩阵时某些fastGWA用法会转为普通回归；因此不能仅根据命令或文件名中出现fastGWA就称为混合模型。

本例数量性状`.fastGWA`标题含`CHR SNP POS A1 A2 N AF1 BETA SE P`，逐项读计数方向、样本数与标准误。二分类的详细字段按该模块说明读取，不套用定量模板。

## 实测结果怎样使用

本轮1410个体、8544位点的数量性状流程完整运行。fastGWA与稠密GRM输出存在差别，是检查背景、近似与数据结构的起点。小鼠家系案例不能建立人类大队列的速度、功效或校准排名。

图形比较见[GWAS曼哈顿图QQ图与膨胀因子](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E6%9B%BC%E5%93%88%E9%A1%BF%E5%9B%BEQQ%E5%9B%BE%E4%B8%8E%E8%86%A8%E8%83%80%E5%9B%A0%E5%AD%90)。深入：[官方fastGWA与GLMM说明](https://yanglab.westlake.edu.cn/software/gcta)、[fastGWA原始论文](https://doi.org/10.1038/s41588-019-0530-8)、[fastGWA-GLMM原始论文](https://www.nature.com/articles/s41588-021-00954-4)。
