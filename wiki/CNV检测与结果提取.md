# CNV检测与结果提取

> 更新：2026-10-15；状态：可用；验证范围：人工VCF的CN字段提取已执行；CNVkit及真实深度CNV检测未执行。

从可比深度生成分段与CN，再按字段含义导出，保留剂量和未知而非只留下事件标签。

## 先选测量场景

WGS、捕获与扩增子需采用支持该数据的深度方法，输入参考/靶区、正常基线及倍性必须一致。前置见[CNV深度校正分段与拷贝数估计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/CNV%E6%B7%B1%E5%BA%A6%E6%A0%A1%E6%AD%A3%E5%88%86%E6%AE%B5%E4%B8%8E%E6%8B%B7%E8%B4%9D%E6%95%B0%E4%BC%B0%E8%AE%A1)。

## CNVkit捕获模板

按[官方流程](https://cnvkit.readthedocs.io/en/stable/pipeline.html)安装并准备匹配的BAM/正常对照、靶区与参考。以下仅演示输入衔接，未运行；不是所有群体数据都适用该对照设计：

```bash
cnvkit.py batch sample.bam --normal normal.bam --targets targets.bed \
  --fasta ref.fa --output-reference baseline.cnn --output-dir cnvkit-out
cnvkit.py call cnvkit-out/sample.cns -o cnvkit-out/sample.call.cns
cnvkit.py export bed cnvkit-out/sample.call.cns --show all -o cnvkit-out/sample.all.bed
```

`.cnr`是相对信号，`.cns`是分段，call输出新增相应CN估计。示例不代替检查肿瘤纯度、性染色体或非二倍体设置。export默认可只输出非基线段，示例`--show all`用于保留所有段；坐标与CN解释见[官方导出说明](https://cnvkit.readthedocs.io/en/stable/importexport.html)。

## 人工VCF的实际导出

先完成[人工VCF贯通变异分类与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5VCF%E8%B4%AF%E9%80%9A%E5%8F%98%E5%BC%82%E5%88%86%E7%B1%BB%E4%B8%8E%E6%8F%90%E5%8F%96)，每页从根目录开始，进入`examples/output/variants`并使用bcftools环境：

```bash
bcftools query -i 'INFO/SVTYPE="CNV"' \
  -f '%CHROM\t%POS\t%INFO/END[\t%SAMPLE=%CN]\n' normalized.vcf.gz
```

得到chrToy、800、900、S01=2、S02=1、S03=3。这是1-based POS/END的查询表，不能改名BED就声称已转换坐标。人工CN来自输入头部定义，不是本轮用深度估计得到的CN。

## 交付检查

真实工具可能使用CN、RDCN等不同字段；先读头部再改query模板。保存bin/分段信号、CN/质量、基线与样本对应；多个样本边界不同，要定义统一区域再比较，不能按结果第几行拼接。缺失CN保留未知，CN=1与CN=0不合并成同一“缺失基因”。

## 本轮整理入口

[CNVkit深度分段与拷贝数解释](https://github.com/SpiralKernel/bioinfo-wiki/wiki/CNVkit%E6%B7%B1%E5%BA%A6%E5%88%86%E6%AE%B5%E4%B8%8E%E6%8B%B7%E8%B4%9D%E6%95%B0%E8%A7%A3%E9%87%8A)细分输入/输出；[拷贝数基线非整倍体与LOH](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%8B%B7%E8%B4%9D%E6%95%B0%E5%9F%BA%E7%BA%BF%E9%9D%9E%E6%95%B4%E5%80%8D%E4%BD%93%E4%B8%8ELOH)与[CNV与PAV交叉验证及群体矩阵](https://github.com/SpiralKernel/bioinfo-wiki/wiki/CNV%E4%B8%8EPAV%E4%BA%A4%E5%8F%89%E9%AA%8C%E8%AF%81%E5%8F%8A%E7%BE%A4%E4%BD%93%E7%9F%A9%E9%98%B5)说明剂量、基线及unknown。真实CNV调用仍未实测。
