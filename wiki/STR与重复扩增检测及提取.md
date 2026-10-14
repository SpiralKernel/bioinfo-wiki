# STR与重复扩增检测及提取

> 更新：2026-10-14；状态：可用；验证范围：人工VCF重复字段提取已执行；ExpansionHunter与TRGT未执行。

把重复目录、等位长度或次数、支持与区间一起保存，不能只导出GT就完成重复分析。

## 输入准备

确认平台、参考、repeat catalog及工具版本。目录只定义被分析的目标，不是“全基因组所有重复均已检出”。短读长与HiFi的输入、模型和输出格式不同。

## 两类专业模板

ExpansionHunter需适合的短读长WGS和JSON目录；TRGT对应HiFi和重复BED定义。以下文件需另准备，两种工具均未运行：

```bash
ExpansionHunter --reads sample.bam --reference ref.fa \
  --variant-catalog repeats.json --output-prefix sample.eh
trgt genotype --genome ref.fa --repeats repeats.bed \
  --reads sample.hifi.bam --output-prefix sample.trgt
```

先用各自官方小数据确认安装、catalog与输出，再替换自己的数据。TRGT相应输出可能需另排序索引；不要把一种目录改后缀给另一种工具。

## 按实际格式提取

ExpansionHunter相应格式的FORMAT/CN是重复次数表示，可连同RU导出；TRGT使用AL（bp）、ALLR、MC等字段，且当前格式的等位级字段顺序不能直接由带相位GT的左右位置推断：

```bash
bcftools query -f '%CHROM\t%POS\t%INFO/RU[\t%SAMPLE=%CN]\n' sample.eh.vcf
bcftools query -f '%CHROM\t%POS\t%INFO/TRID[\t%SAMPLE\t%GT\t%AL\t%ALLR\t%MC]\n' sample.trgt.vcf.gz
```

这两条专业结果提取是文档模板，需核对所用版本头部。不要把EH的CN和CNV工具的拷贝数CN拼成同一语义列。

## 本轮实际案例

人工VCF给自定义REPCN而非上述软件原生字段，案例query输出CAG、S01=10/12、S02=10/10、S03=未知。它验证字段导出，未从reads估计重复次数。真实解释还应检查长度区间、motif中断、单倍型、支持及目录缺失。

依据：[EH使用](https://github.com/Illumina/ExpansionHunter/blob/master/docs/03_Usage.md)、[EH输出](https://github.com/Illumina/ExpansionHunter/blob/master/docs/06_OutputVcfFiles.md)、[TRGT教程](https://github.com/PacificBiosciences/trgt/blob/main/docs/tutorial.md)、[TRGT字段说明](https://github.com/PacificBiosciences/trgt/blob/main/docs/vcf_files.md)。
