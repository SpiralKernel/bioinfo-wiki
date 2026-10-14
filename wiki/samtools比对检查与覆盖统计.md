# samtools比对检查与覆盖统计

> 更新：2026-10-14；状态：可用；验证范围：人工基因案例与实际工具输出核对；具体已测范围见正文。

先确认比对文件可读、标记合理及覆盖符合实验设计，再解释调用结果。

## 三层检查

1. 文件层：头部、EOF、排序和索引是否正常。
2. 比对层：primary/secondary/supplementary、配对、重复和MAPQ的统计定义。
3. 研究层：目标区间覆盖、可调用碱基和样本间一致性。

本机实际samtools1.22、HTSlib1.22；本地文件功能已运行，编译未启用远程libcurl访问。不能据此声称云文件功能也验证过。

## 实际使用的命令

```bash
samtools sort -o sorted.bam aligned.sam
samtools quickcheck -v sorted.bam
samtools index sorted.bam
samtools flagstat -O json sorted.bam > flagstat.json
samtools coverage sorted.bam > coverage.tsv
```

`quickcheck`主要检查头和文件结尾，不遍历全部中间内容；它通过不代表内部无损。[官方quickcheck说明](https://www.htslib.org/doc/samtools-quickcheck.html)明确这一边界。本轮额外移除人工BAM末尾28字节，确实触发EOF检查失败。

人工40条reads全部primary mapped，但只覆盖1600bp参考中的169bp，覆盖比例10.5625%。因此[flagstat](https://www.htslib.org/doc/samtools-flagstat.html)的比对率不能替代全参考或目标区间覆盖。

重复标记、覆盖过滤、MAPQ阈值和paired-end重叠策略会改变统计。记录命令及分母，再比较样本。实例见[从FASTQ到比对检查与变异调用](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BB%8EFASTQ%E5%88%B0%E6%AF%94%E5%AF%B9%E6%A3%80%E6%9F%A5%E4%B8%8E%E5%8F%98%E5%BC%82%E8%B0%83%E7%94%A8)、[SAM与BAM及CRAM](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SAM%E4%B8%8EBAM%E5%8F%8ACRAM)。
