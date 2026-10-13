# GWAS从数据准备到结果解释

> 更新：2026-10-13；验证范围：合成数据实测。

将基因型、表型和设计信息连接到合适的关联模型，并审查效应方向与证据边界。

## 输入与研究问题

需要经过[基因型质控与过滤](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E5%9E%8B%E8%B4%A8%E6%8E%A7%E4%B8%8E%E8%BF%87%E6%BB%A4)的数据、表型定义、样本表、协变量以及必要的亲缘信息。先明确数量性状还是二分类、独立单位、测量单位、缺失值和排除标准。

## 1. 样本对齐与模型选择

按 ID 对齐表型和协变量，检查合并后的组别、缺失与共线性。有家系或相关样本时评估混合模型，而不是把所有分析都称作普通线性回归。见[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)。

## 2. 运行数量性状教学例

```bash
plink2 --pfile qc --pheno phenotype.tsv --pheno-name trait \
  --covar pca.eigenvec --covar-name PC1-PC5 \
  --glm hide-covar --out gwas
```

本命令已在独立生成的合成样本上运行，使用普通数量性状回归，不是 GRM 混合模型。所用五个 PC 是教学演示，不是对真实数据的通用建议。

## 3. 阅读结果表

检查 ID、位置、REF、ALT、A1、TEST、OBS_CT、BETA、SE、P 和 ERRCODE。主效应通常查看对应 ADD 行，其他检验要按模型说明解释。不能将错误码或缺失 P 当作正常不显著结果。

本例 v1 的 A1=A，BETA≈−1.84，P≈1.95×10⁻²⁵，与对 G 赋正效应的生成逻辑相容。详见[合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)。

## 4. 统计与生物学解释

预先说明检验集合与[P值效应量与多重检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/P%E5%80%BC%E6%95%88%E5%BA%94%E9%87%8F%E4%B8%8E%E5%A4%9A%E9%87%8D%E6%A3%80%E9%AA%8C)方法。Manhattan 图定位信号，QQ 图辅助诊断；二者不独立证明模型可靠。结合样本量、频率、效应、局部 LD、分层和重复验证审查结果。

关联位点未必是因果变异，最近基因未必是作用基因。候选解释还需要注释、精细定位、功能与独立证据，见[变异注释与候选证据整理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%B3%A8%E9%87%8A%E4%B8%8E%E5%80%99%E9%80%89%E8%AF%81%E6%8D%AE%E6%95%B4%E7%90%86)、[基因标识符与同源基因](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E6%A0%87%E8%AF%86%E7%AC%A6%E4%B8%8E%E5%90%8C%E6%BA%90%E5%9F%BA%E5%9B%A0)及[富集分析与GSEA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8EGSEA)。

参数接口见 [PLINK 关联手册](https://www.cog-genomics.org/plink/2.0/assoc)；混合模型详见 [GEMMA](https://doi.org/10.1038/ng.2310)。
