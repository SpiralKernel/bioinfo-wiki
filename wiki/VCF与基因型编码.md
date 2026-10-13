# VCF与基因型编码

> 更新：2026-10-13；验证范围：文档核对；操作需按所用环境验证。

VCF 以位点为记录，保存参考与替代等位基因，以及每个样本的基因型和其他字段。

## 先读哪些列

前八列是 CHROM、POS、ID、REF、ALT、QUAL、FILTER、INFO。包含样本时，FORMAT 定义后续样本单元格里的字段顺序。例如 `FORMAT=GT:DP` 的 `0/1:28` 表示对应基因型及深度。

```text
#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT sample1
1 100 v1 A G . PASS . GT:DP 0/1:28
```

此段以空格展示列，实际 VCF 使用制表符且需要元信息头。

## 常见误读

GT 的 0 是 REF、1 是第一个 ALT、2 是第二个 ALT，不是“携带两份 ALT”。对于二等位二倍体记录，`1/1` 才是两份第一 ALT；`.` 表示缺失。`0|1` 的相位顺序不自动给出父母来源。

REF 不保证常见，ALT 也不保证有害或是效应等位基因。QUAL 是位点级信息，GQ 是基因型级质量，DP 的含义需看其位置和头部定义。

## 交接检查

记录参考组装、倍性、多等位拆分及归一化策略；跨文件匹配优先使用组装、染色体、位置、REF、ALT 的组合，而不仅是可能重复的 ID。见[SNP与基因型是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SNP%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%98%AF%E4%BB%80%E4%B9%88)和[参考基因组与注释版本](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%82%E8%80%83%E5%9F%BA%E5%9B%A0%E7%BB%84%E4%B8%8E%E6%B3%A8%E9%87%8A%E7%89%88%E6%9C%AC)。

字段的权威定义在 [VCF 4.5 规范](https://samtools.github.io/hts-specs/VCFv4.5.pdf)。
