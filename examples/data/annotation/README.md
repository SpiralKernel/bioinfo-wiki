# 人工基因、变异与reads

全部数据用于教学，参考名chrToy不是实际物种。参考长度1600bp，背景采用固定种子20261014构造，编码区另按已知CDS设置。当前文件及运行报告中的SHA256固定实际输入，不依赖重新随机生成来复现。

- genome.fa：人工参考序列。
- genes.gff3：gPlus（+）含txPlus1/txPlus2，gMinus（−）含txMinus。三条完整CDS各120bp，使用标准密码表，每段60bp、phase0，无UTR。
- cds.fa、protein.fa：独立提供的转录本序列核对文件；负链CDS按转录方向存储。蛋白包含对应模型的终止标记。
- variants.vcf：12条记录、13个ALT。含多ALT、同义/错义、终止、移码、剪接和内含子位置；预期用于后果检查，不是从reads全部调用出来的集合。
- boundaries.bed：7个半开区间，用于基因边界和并列最近距离检查。
- reads.fastq：40条单端150bp人工reads，20条参考和20条105 C>T替代状态。仅覆盖参考的一小段，用于实际mapper/BAM/caller链；不模拟测序错误或真实复杂度。

两个案例使用同一人工参考，但用途不同：annotation_demo.py注释固定VCF，genome_alignment_demo.py从FASTQ调用预设SNV。不能把前者12条VCF记录说成后者全部检出。

运行脚本把必要输入复制到独立输出。修改练习请先复制整套输入，用--input-dir和新的--output指向副本；报告含固定结果断言，不是生产通用包装器。

查看[注释案例](https://github.com/SpiralKernel/bioinfo-wiki/wiki/人工基因贯通区间注释与后果提取)、[比对案例](https://github.com/SpiralKernel/bioinfo-wiki/wiki/从FASTQ到比对检查与变异调用)。
