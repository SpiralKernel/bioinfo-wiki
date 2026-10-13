# SNP与基因型是什么

> 更新：2026-10-13；验证范围：文档核对；操作需按所用环境验证。

SNP 描述单碱基位点的变异，基因型描述某个体在该位点携带的等位基因组合。

## SNP、SNV与等位基因

单核苷酸变异（single nucleotide variant，SNV）是单个碱基位置的序列差异。SNP 的历史用法常强调群体中的多态性；实际文献和数据库用法并不完全一致。频率必须说明参考群体，不能只凭名称认定 MAF 大于某个阈值。入门定义可对照 [NHGRI 的 SNP 解释](https://www.genome.gov/genetics-glossary/Single-Nucleotide-Polymorphisms-SNPs)。

假设某位点出现 A、G，它们是两种等位基因。对于这里讨论的二倍体常染色体，一个个体可能为 A/A、A/G 或 G/G，分别是两种纯合和一种杂合。单倍体、性染色体及多倍体需要另行考虑倍性。

## 三组名称需要分开

| 名称 | 根据什么定义 | 重要边界 |
|---|---|---|
| REF / ALT | 参考序列与文件记录 | REF 不一定是群体中的主要等位基因 |
| major / minor | 指定群体内的频率 | 换群体后主次关系可能改变 |
| effect / other allele | 模型或结果表的计数方向 | 效应等位基因既可能是 REF，也可能是 ALT |

A1、A2 的含义要查看软件版本和具体文件；不能直接当成“主要/次要”。[PLINK 输入说明](https://www.cog-genomics.org/plink/2.0/input)专门说明了这些约定。

## 0、1、2编码与剂量

若模型计数 G 的拷贝数，A/A、A/G、G/G 对应 0、1、2。改为计数 A 时对应 2、1、0，回归系数的方向也可能反转。填充剂量是期望拷贝数，可以是 0.7 等小数；它不同于已经确定的硬基因型。

缺失应按文件和软件约定表示，不能默认所有地方的 `0`、`-9` 都代表缺失，也不能未经说明就均值填补。

## 相位和文件表示

VCF 中 `0` 指 REF，`1` 指第一个 ALT；`0/1` 表示未定相，`0|1` 表示等位基因顺序有相位信息，但不自动说明哪个来自父亲。更多例子见[VCF与基因型编码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E7%BC%96%E7%A0%81)和 [VCF 规范](https://samtools.github.io/hts-specs/VCFv4.5.pdf)。

PLINK 的 PED/MAP、BED/BIM/FAM 和 PGEN/PVAR/PSAM 是不同的存储系统。BED 是二进制基因型数据，BIM 记位点，FAM 记样本；不要把PLINK的BED与[基因组坐标与区间](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E5%9D%90%E6%A0%87%E4%B8%8E%E5%8C%BA%E9%97%B4)中的BED混为一谈。

## 具体例子与下一步

在[合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)中，我们给 G 剂量设置正效应；实际结果的 A1 是 A，BETA 为负。解读时必须同时读 A1 和 BETA。

下一步读[连锁不平衡与LD剪枝](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BF%9E%E9%94%81%E4%B8%8D%E5%B9%B3%E8%A1%A1%E4%B8%8ELD%E5%89%AA%E6%9E%9D)及[群体结构是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E6%98%AF%E4%BB%80%E4%B9%88)。
