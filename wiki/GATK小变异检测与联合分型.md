# GATK小变异检测与联合分型

> 更新：2026-10-14；状态：可用；验证范围：官方文档与原始研究核对；专业检测命令为模板，未执行完整真实数据流程。

用HaplotypeCaller生成样本参考置信证据，再用相应联合分型步骤得到群体小变异。

## 前提与用途

这里是GATK4生殖系SNV/Indel模板，未执行。准备同一参考下的analysis-ready BAM及索引、读组与样本名，参考FASTA的fai和sequence dictionary。原始处理见[短读长SNP与Indel检测流程](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%9F%AD%E8%AF%BB%E9%95%BFSNP%E4%B8%8EIndel%E6%A3%80%E6%B5%8B%E6%B5%81%E7%A8%8B)。

GATK安装/Java环境、版本和资源先按[官方仓库](https://github.com/broadinstitute/gatk)核对。下面文件名为待准备输入，不是项目自带数据。倍性2仅示例，需要按染色体与实验设计修改。

## 两个样本的小规模模板

```bash
gatk HaplotypeCaller -R ref.fa -I S01.bam -O S01.g.vcf.gz -ERC GVCF --sample-ploidy 2
gatk HaplotypeCaller -R ref.fa -I S02.bam -O S02.g.vcf.gz -ERC GVCF --sample-ploidy 2
gatk CombineGVCFs -R ref.fa -V S01.g.vcf.gz -V S02.g.vcf.gz -O cohort.g.vcf.gz
gatk GenotypeGVCFs -R ref.fa -V cohort.g.vcf.gz -O cohort.raw.vcf.gz
```

前两步是样本证据，第三步是小规模中间合并，第四步才是联合分型。大队列通常改用匹配版本的GenomicsDBImport设计；不能简单换成cat多个VCF。

## 分型之后

保留原始结果；检查样本、倍性、注释分布、缺失和参考一致性；根据数据与可信资源选择VQSR或有依据的硬过滤。非模式物种/小样本不应盲套人类训练资源和固定阈值。

标准化、过滤与提取是后续步骤，见[VCF标准化多等位拆分与表示](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E6%A0%87%E5%87%86%E5%8C%96%E5%A4%9A%E7%AD%89%E4%BD%8D%E6%8B%86%E5%88%86%E4%B8%8E%E8%A1%A8%E7%A4%BA)和[变异位点过滤与基因型掩蔽](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E4%BD%8D%E7%82%B9%E8%BF%87%E6%BB%A4%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%8E%A9%E8%94%BD)。小样本运行完命令不意味着已验证准确度。

依据：[HaplotypeCaller](https://gatk.broadinstitute.org/hc/en-us/articles/360037225632-HaplotypeCaller)、[生殖系群体流程](https://gatk.broadinstitute.org/hc/en-us/articles/360035535932-Germline-short-variant-discovery-SNPs-Indels)、[GVCF联合分型与参考置信度](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GVCF%E8%81%94%E5%90%88%E5%88%86%E5%9E%8B%E4%B8%8E%E5%8F%82%E8%80%83%E7%BD%AE%E4%BF%A1%E5%BA%A6)。
