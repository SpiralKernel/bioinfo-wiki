# SAM与BAM及CRAM

> 更新：2026-10-13；验证范围：文档核对；操作需按所用环境验证。

SAM、BAM 和 CRAM 表达序列比对记录，坐标排序、索引和参考资源决定很多下游操作能否正确进行。

## 三种格式

SAM 是可读文本；BAM 是二进制存储；CRAM 使用压缩方案，读取时可能需要匹配的参考序列。它们与原始[FASTA与FASTQ](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FASTA%E4%B8%8EFASTQ)不同：同一读段可有主比对、次级或补充比对记录。

记录中的 FLAG、CIGAR、MAPQ 和坐标解释需要参考规范。MAPQ 通常描述放置位置的不确定性，不等于每个碱基的测序质量。索引也不是排序的替代品。

## 实践检查

```bash
samtools quickcheck -v sample.bam
samtools flagstat sample.bam
samtools view -H sample.bam
```

这些是需在安装 SAMtools 后运行的检查命令，尚未在本机执行。`quickcheck` 不完整解码全部记录，安静退出不能证明数据没有所有内部问题。检查参考名称、长度、排序说明和读组，并确认索引对应当前文件。

详细查看 [SAM/BAM/CRAM 规范](https://samtools.github.io/hts-specs/)和 [samtools quickcheck 的范围](https://www.htslib.org/doc/samtools-quickcheck.html)。应用见[基因组重测序与变异检测](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%87%8D%E6%B5%8B%E5%BA%8F%E4%B8%8E%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B)。
