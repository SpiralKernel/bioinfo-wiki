# Salmon定量与tximport基因汇总

> 更新：2026-10-15；状态：可用；验证范围：官方资料与方法核对；本页上游或扩展软件流程未执行。

转录本定量、基因汇总及长度校正相互衔接，必须使用同版本转录本到基因映射。

## 输入和输出

Salmon针对参考转录本资源估计丰度，索引及可选decoy配置决定可比对资源。保存转录本FASTA、注释、索引构建命令、版本和library type；自动推断也应检查推断结果。[Salmon官方文档](https://salmon.readthedocs.io/en/latest/salmon.html)给出具体流程。

quant.sf包含转录本ID、长度、有效长度、TPM和估计计数等信息。TPM与NumReads用途不同，不能直接选TPM列当DESeq2原始矩阵。

## tximport如何衔接

提供每个样本quant.sf路径和匹配的tx2gene映射，tximport进行相应汇总；再用DESeqDataSetFromTximport等接口导入。不同countsFromAbundance设置对应不同的长度处理约定，应按[tximport官方指南](https://bioconductor.org/packages/release/bioc/vignettes/tximport/inst/doc/tximport.html)配套使用，避免重复长度校正。

先检查转录本ID匹配比例、版本后缀和一对多关系。不认识的ID应报告，不静默丢弃；只删版本号可能误合并，需要来源依据。

本轮未执行Salmon或tximport，airway案例使用包内已有整数基因计数，而非其中另一个Salmon导入对象。继续读[RNA-seq从FASTQ到基因计数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8EFASTQ%E5%88%B0%E5%9F%BA%E5%9B%A0%E8%AE%A1%E6%95%B0)、[计数丰度与标准化](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%AE%A1%E6%95%B0%E4%B8%B0%E5%BA%A6%E4%B8%8E%E6%A0%87%E5%87%86%E5%8C%96)。
