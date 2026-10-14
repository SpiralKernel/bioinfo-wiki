# VEP缓存离线注释与CSQ

> 更新：2026-10-14；状态：可用；验证范围：官方文档与方法来源核对；本页专业软件模板未单独执行。

VEP可使用本地缓存和参考FASTA完成后果注释；缓存、物种、组装与程序版本必须匹配。

## 安装与资源不是一回事

VEP程序、物种缓存、FASTA和插件资源分别管理。固定物种、assembly、release、缓存路径和参考校验值；离线模式不等于资源自动齐全。[Ensembl VEP官方仓库](https://github.com/Ensembl/ensembl-vep/blob/release/115/README.md)提供安装入口，本页未安装或执行VEP。

下面是待按实际release核对的命令模板，缓存需提前安装；路径和assembly都必须替换：

```bash
vep --input_file normalized.vcf --output_file annotated.vcf   --vcf --cache --offline --dir_cache /你的缓存目录   --species YOUR_SPECIES --assembly YOUR_ASSEMBLY   --fasta /你的参考.fa
```

运行前用该版本`vep --help`核对支持选项，先做少量变异的REF和预期后果检查。非模式物种若缺合适缓存，需评估自定义GFF/GTF等方式或SnpEff自建库，不能借用近缘物种坐标直接注释。

## CSQ要从头部读格式

CSQ用`|`分列、`,`分记录，字段顺序以本次VCF头的Format为准。不能从别人的教程复制一个固定列号。ANN与CSQ也不是同一格式。

可用[bcftools +split-vep文档](https://samtools.github.io/bcftools/howtos/plugin.split-vep.html)了解结构化拆分；本轮未实测VEP及该插件的CSQ流程。特别检查等位最小表示、多ALT关联和转录本选择，避免字符串包含HIGH就选中全部ALT。

继续读[转录本选择与代表注释](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BD%95%E6%9C%AC%E9%80%89%E6%8B%A9%E4%B8%8E%E4%BB%A3%E8%A1%A8%E6%B3%A8%E9%87%8A)、[参考版本转换与REF复核](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%82%E8%80%83%E7%89%88%E6%9C%AC%E8%BD%AC%E6%8D%A2%E4%B8%8EREF%E5%A4%8D%E6%A0%B8)。
