# VCF标准化多等位拆分与表示

> 更新：2026-10-14；状态：可用；验证范围：bcftools1.22与HTSlib1.22人工VCF/SAM案例已执行；真实检测性能及其他专业软件未实测。

先校验REF，再明确是否左对齐、拆多等位或原子化，记录和基因型必须一起更新。

## 可跟做的输入

先运行[人工VCF贯通变异分类与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5VCF%E8%B4%AF%E9%80%9A%E5%8F%98%E5%BC%82%E5%88%86%E7%B1%BB%E4%B8%8E%E6%8F%90%E5%8F%96)。本页所有跟做段均从项目根目录开始；进入能调用bcftools的同一环境，再进入案例输出目录。Conda安装者可先执行`conda activate variants`。

```bash
cd examples/output/variants
bcftools norm -f toy.fa -c e -m -any -Ov -o norm2.unsorted.vcf calls.vcf
bcftools sort -Oz -o norm2.vcf.gz norm2.unsorted.vcf
bcftools index norm2.vcf.gz
```

`-c e`遇REF不匹配即停止，不能把自动交换REF当作通用修复。输入参考必须和生成VCF的组装一致。左对齐可能改变位置/顺序，因此随后排序和重新索引。

## 三个不同操作

本例16条拆为17条，mixed的两种ALT分开；left_shift由200左移至179，但插入事件没有新增。S01原始mixed为1/2，拆后对G为1/0、对CA为0/1；原始ID可以重复，不再是唯一行键。

MNV保持一条，若确实需要原子化，可对序列解析集合另做：

```bash
bcftools norm -a --atom-overlaps . -f toy.fa -Ov -o atomized2.vcf sequence_resolved.vcf
```

本例序列集合9条变10条。原子化改变记录单位，不能把所得SNV自动看作独立突变；相位与原始单倍型关系也要保存。

## 一起核对哪些字段

GT按ALT索引重编码，Number=A/R/G字段涉及等位/基因型维度，不能只剪ALT字符串而保留原AD/PL。拆分时其他ALT变参考或缺失的策略应记录，复杂重叠尤其要检查。GVCF块、符号SV、BND与重复软件特有字段不能默认按同一小变异策略处理。

跨文件比较保留组装、CHROM/POS/REF/ALT及原始记录映射。操作实测范围为人工输入，依据另可查[bcftools规范化实现](https://github.com/samtools/bcftools/blob/1.22/vcfnorm.c)和[SNVIndelMNV与复杂变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SNVIndelMNV%E4%B8%8E%E5%A4%8D%E6%9D%82%E5%8F%98%E5%BC%82)。
