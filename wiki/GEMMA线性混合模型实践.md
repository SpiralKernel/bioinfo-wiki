# GEMMA线性混合模型实践

> 更新：2026-10-13；状态：可用；验证范围：GEMMA 0.98.5公开小鼠GRM、LM、LMM及chr17背景排除对照实测；其他模块未执行。

GEMMA以显式亲缘矩阵拟合关联模型，适合学习固定效应、背景相关性和检验方法的连接。

## 模型与适用任务

GEMMA可做普通线性模型、单性状LMM、多性状LMM及BSLMM等任务；本页实测只包含数量性状LM/LMM与GRM，不涵盖全部模块。LMM把个体相关性放入K代表的随机效应，见[零模型与方差组分](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%9B%B6%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BB%84%E5%88%86)。

选择它时应评估稠密矩阵的内存和特征分解成本。n×n的double矩阵仅一份就约需8n²字节，实际程序还需其他数组；这个估算不是峰值内存承诺。

## 输入与最容易出错的顺序

本例用BED/BIM/FAM，表型在FAM第六列。GEMMA也支持BIMBAM等接口，但不同格式的表型、剂量与缺失约定不能混用。

`-c`指定的是按基因型个体顺序排列的纯数值协变量矩阵，不能直接放FID、IID或标题行。提供`-c`时需要显式包含截距列1；未提供时程序默认处理截距。本例为“1、PC1、PC2、PC3”四列。

外部K也必须与个体顺序一致；维度正确不代表身份正确。数据对齐见[GWAS软件输入转换与样本对齐](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E8%BE%93%E5%85%A5%E8%BD%AC%E6%8D%A2%E4%B8%8E%E6%A0%B7%E6%9C%AC%E5%AF%B9%E9%BD%90)。

## 已实测的三步命令

先按[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)准备输入。工作目录是`examples/output/gwas-real/`：

```bash
mkdir -p gemma
export OPENBLAS_NUM_THREADS=2
gemma -bfile prepared/qc -c prepared/gemma.covariates.txt \
  -maf 0.05 -miss 0.05 -gk 2 -outdir gemma -o grm

gemma -bfile prepared/qc -c prepared/gemma.covariates.txt \
  -maf 0.05 -miss 0.05 -lm 1 -outdir gemma -o lm_pc3

gemma -bfile prepared/qc -c prepared/gemma.covariates.txt \
  -maf 0.05 -miss 0.05 -k gemma/grm.sXX.txt \
  -lmm 1 -outdir gemma -o lmm_pc3
```

实测GEMMA 0.98.5。`-gk 2`生成标准化矩阵`sXX`；`-gk 1`生成中心化矩阵`cXX`，不能把后缀或权重定义随意互换。这里显式写出MAF和缺失设置，避免跨软件隐藏的默认筛选造成比较错位。

## 检验与输出

`-lm`和`-lmm`区分背景模型，后面的1为Wald检验，2为似然比，3为得分，4输出三者。详见[Wald似然比与得分检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Wald%E4%BC%BC%E7%84%B6%E6%AF%94%E4%B8%8E%E5%BE%97%E5%88%86%E6%A3%80%E9%AA%8C)。

`.assoc.txt`中的`allele1/allele0`、`af`、`beta`、`se`和具体P列要一起读。不同模式或版本的观测数、缺失数与额外列可能不同；读取标题而非固定第几列。本例LM含`n_obs`，LMM含`n_miss`，不能直接用一套硬编码列位置。

效应方向以实际输入编码和输出等位基因为准，不根据“minor”字样推断。旧版本方向曾有变化；BED来自其他软件时第一等位基因也未必是当前样本中的次要等位基因。

## 结果检查与范围

检查分析个体、SNP数、特征分解、方差估计与警告。本例1410个体、8544位点；rs6249614的全基因组GRM LMM得到β≈−0.4467002、P≈6.73×10⁻¹⁵。这些数值仅用于本例校验，不是正式生物学新发现。

本例另做第17号染色体背景排除对照，见[LOCO与近端污染](https://github.com/SpiralKernel/bioinfo-wiki/wiki/LOCO%E4%B8%8E%E8%BF%91%E7%AB%AF%E6%B1%A1%E6%9F%93)；完整全基因组LOCO未在此执行。二分类不能把此LMM系数当成log-OR，多性状与BSLMM也有各自输入和目标。

深入：[GEMMA官方仓库](https://github.com/genetics-statistics/GEMMA)、[0.98.5手册](https://github.com/genetics-statistics/GEMMA/blob/v0.98.5/doc/manual.pdf)、[GEMMA原始方法](https://doi.org/10.1038/ng.2310)。
