# DELLY结构变异与群体分型

> 更新：2026-10-14；状态：可用；验证范围：官方文档与原始研究核对；专业检测命令为模板，未执行完整真实数据流程。

DELLY按模式利用结构与深度证据，候选合并后仍需逐样本再分型。

## 接口先核对

本页按2026-10-14核对的[官方README](https://github.com/dellytools/delly)中`sr/lr/cnv`接口写模板，未安装/执行DELLY。旧版本接口可能不同，不保证以下命令适用于旧版；先看`delly --help`和具体模式帮助，保存版本。

输入为排序、索引及适当重复标记的BAM/CRAM和一致参考。短读长推荐使用匹配物种/组装的排除区间；不能把人类exclude map直接复制给其他物种。

## 短读长两样本结构变异模板

```bash
delly sr -g ref.fa -o S01.bcf S01.bam
delly sr -g ref.fa -o S02.bcf S02.bam
delly merge -g ref.fa -o sites.bcf S01.bcf S02.bcf
delly sr -g ref.fa -v sites.bcf -o S01.geno.bcf S01.bam
delly sr -g ref.fa -v sites.bcf -o S02.geno.bcf S02.bam
bcftools index S01.geno.bcf
bcftools index S02.geno.bcf
bcftools merge -m id -Ob -o cohort.geno.bcf S01.geno.bcf S02.geno.bcf
```

前三步发现并整理候选，后两次sr是对同一集合再分型，最后才整理样本列。这里没有自动执行适合实际设计的最终过滤；HWE、群体分组与家系应按任务决定。

## 模式与提取

长读长用对应lr模式并核对平台，深度CNV使用cnv；WGS深度模式不能默认用于外显子捕获。某些输出用CHR2描述远端连接，不是所有结果都以成对BND保存。

提取前核对SVTYPE、END、远端坐标和FORMAT定义；CNV可能使用RDCN等字段，不能自动用其他软件的CN字段脚本。继续[CNV检测与结果提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/CNV%E6%A3%80%E6%B5%8B%E4%B8%8E%E7%BB%93%E6%9E%9C%E6%8F%90%E5%8F%96)、[SV合并匹配与群体再分型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SV%E5%90%88%E5%B9%B6%E5%8C%B9%E9%85%8D%E4%B8%8E%E7%BE%A4%E4%BD%93%E5%86%8D%E5%88%86%E5%9E%8B)；原始研究：[DELLY](https://doi.org/10.1093/bioinformatics/bts378)。
