# 按类型提取SNPIndel与结构变异

> 更新：2026-10-14；状态：可用；验证范围：bcftools1.22与HTSlib1.22人工VCF/SAM案例已执行；真实检测性能及其他专业软件未实测。

先拆清混合ALT与表示，再按定义筛选；序列类型、结构注释和长度门槛是不同条件。

## 跟做：本例的序列变异

先运行[人工VCF贯通变异分类与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5VCF%E8%B4%AF%E9%80%9A%E5%8F%98%E5%BC%82%E5%88%86%E7%B1%BB%E4%B8%8E%E6%8F%90%E5%8F%96)，从项目根目录进入`examples/output/variants`，并确保终端使用已安装bcftools的环境。以下以本例不带SVTYPE的受控序列集合演示：

```bash
bcftools view -i 'INFO/SVTYPE="."' -v snps -Ov -o selected.snps.vcf normalized.vcf.gz
bcftools view -i 'INFO/SVTYPE="."' -v indels -Ov -o selected.indels.vcf normalized.vcf.gz
bcftools view -i 'INFO/SVTYPE="."' -v mnps -Ov -o selected.mnps.vcf normalized.vcf.gz
```

本例分别5、3、1条。mixed先拆开，分别进入SNP和Indel集合。若没拆，`-v`按记录中相应类型ALT命中，不能保证输出每个ALT都属于目标类型。

## 跟做：结构与特定注释

```bash
bcftools view -i 'INFO/SVTYPE="DEL"' -Ov -o selected.del.vcf normalized.vcf.gz
bcftools view -i 'INFO/SVTYPE="BND"' -Ov -o selected.bnd.vcf normalized.vcf.gz
bcftools view -i 'INFO/SVTYPE="CNV"' -Ov -o selected.cnv.vcf normalized.vcf.gz
```

本例DEL1、BND2、CNV1条；INV/DUP可同样按其SVTYPE筛选。BND两条是一对人工事件，需要保留MATEID/EVENT关系。

## 迁移到真实数据

没有SVTYPE不等于一定是小变异，有SVTYPE也不能保证所有工具类别相同。序列解析的大插入/缺失可能没有相同标签，符号SV又不能用ALT字符串长度计算长度。先根据调用器定义整理类型、长度、方向和来源，再制定集合；不要仅靠grep尖括号。

按FILTER、样本或基因型筛选是另外的条件。STR/TE可用特有字段，但字段缺失不证明目标不存在，见[STR与重复扩增检测及提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/STR%E4%B8%8E%E9%87%8D%E5%A4%8D%E6%89%A9%E5%A2%9E%E6%A3%80%E6%B5%8B%E5%8F%8A%E6%8F%90%E5%8F%96)、[转座子插入检测与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BA%A7%E5%AD%90%E6%8F%92%E5%85%A5%E6%A3%80%E6%B5%8B%E4%B8%8E%E6%8F%90%E5%8F%96)。实际类型实现可对照[bcftools view源码](https://github.com/samtools/bcftools/blob/1.22/vcfview.c)，字段定义见[VCF中的SVTYPEEND与BND](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E4%B8%AD%E7%9A%84SVTYPEEND%E4%B8%8EBND)。
