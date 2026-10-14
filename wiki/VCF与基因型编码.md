# VCF与基因型编码

> 更新：2026-10-14；状态：可用；验证范围：文档核对；操作需按所用环境验证。

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

## 记录、等位与事件

一个位置可能含多个ALT，拆分后ID可重复；一个结构事件也可能有两个BND记录。记录条数不直接等于位点数、替代等位数或事件数，见[SNVIndelMNV与复杂变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SNVIndelMNV%E4%B8%8E%E5%A4%8D%E6%9D%82%E5%8F%98%E5%BC%82)、[VCF中的SVTYPEEND与BND](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E4%B8%AD%E7%9A%84SVTYPEEND%E4%B8%8EBND)。

多等位拆分必须同步处理GT和等位维度字段，不能仅删ALT。样本子集和基因型掩蔽后，AC/AN/AF等统计要按实际来源重算或核对；外部人群频率与本队列频率分开记录。实际例子见[人工VCF贯通变异分类与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5VCF%E8%B4%AF%E9%80%9A%E5%8F%98%E5%BC%82%E5%88%86%E7%B1%BB%E4%B8%8E%E6%8F%90%E5%8F%96)。
