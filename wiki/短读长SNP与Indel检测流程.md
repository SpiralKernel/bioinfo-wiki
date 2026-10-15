# 短读长SNP与Indel检测流程

> 更新：2026-10-15；状态：可用；验证范围：官方文档与原始研究核对；专业检测命令为模板，未执行完整真实数据流程。

从有质量记录的读段和一致参考进入小变异发现、分型、过滤及交付。

## 输入及上游检查

先确认物种、倍性、文库、参考与样本表，保留FASTQ质控。比对后检查读组/样本名、排序和索引、覆盖、重复、比对质量及污染；CRAM还需可解码的参考。扩增子、WGS与捕获的重复/深度规则不同。

不要默认所有物种都能做同一套BQSR：需要合适的已知位点和工具假设。准备到analysis-ready BAM的操作由相应正式流程管理，见[基因组重测序与变异检测](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%87%8D%E6%B5%8B%E5%BA%8F%E4%B8%8E%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B)。

## 两个调用分支

GATK生殖系队列按[GATK小变异检测与联合分型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GATK%E5%B0%8F%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E4%B8%8E%E8%81%94%E5%90%88%E5%88%86%E5%9E%8B)走GVCF与联合分型。另一个短读长入口是bcftools的证据生成→调用。下面是已准备真实输入时的模板，不是项目自带BAM：

```bash
bcftools mpileup -f ref.fa -Ob -o cohort.pileup.bcf S01.bam S02.bam
bcftools call -m -v -Oz -o cohort.raw.vcf.gz cohort.pileup.bcf
```

两步分开保存中间结果以便初学检查。倍性、read过滤、最大深度、区域、似然注释及资源都需按当前版本和设计设置；默认值不是所有数据的推荐值。

## 交接与核查

原始调用不是过滤完成。核对样本数、参考、GT/DP/GQ等头部、缺失和等位分布，再做[VCF标准化多等位拆分与表示](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E6%A0%87%E5%87%86%E5%8C%96%E5%A4%9A%E7%AD%89%E4%BD%8D%E6%8B%86%E5%88%86%E4%B8%8E%E8%A1%A8%E7%A4%BA)及[变异位点过滤与基因型掩蔽](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E4%BD%8D%E7%82%B9%E8%BF%87%E6%BB%A4%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%8E%A9%E8%94%BD)。保存每步输入/输出条数与实际规则。

本轮只在人工SAM上执行mpileup/call并核对一个已知SNV；真实比对、队列调用与Indel性能没有实测。小案例见[人工VCF贯通变异分类与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5VCF%E8%B4%AF%E9%80%9A%E5%8F%98%E5%BC%82%E5%88%86%E7%B1%BB%E4%B8%8E%E6%8F%90%E5%8F%96)；原理与参数入口：[bcftools调用](https://samtools.github.io/bcftools/howtos/variant-calling.html)、[GATK生殖系流程](https://gatk.broadinstitute.org/hc/en-us/articles/360035535932-Germline-short-variant-discovery-SNPs-Indels)。

## 本轮整理入口

实际FreeBayes例见[FreeBayes小变异与倍性设置](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FreeBayes%E5%B0%8F%E5%8F%98%E5%BC%82%E4%B8%8E%E5%80%8D%E6%80%A7%E8%AE%BE%E7%BD%AE)；深度学习模型选型见[DeepVariant模型资源与运行边界](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DeepVariant%E6%A8%A1%E5%9E%8B%E8%B5%84%E6%BA%90%E4%B8%8E%E8%BF%90%E8%A1%8C%E8%BE%B9%E7%95%8C)。既有人工bcftools案例仍有其独立范围。
