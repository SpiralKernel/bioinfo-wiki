# GFF3GTF与基因转录本外显子

> 更新：2026-10-14；状态：可用；验证范围：官方文档与方法来源核对；本页专业软件模板未单独执行。

理解基因注释文件中的层级和区间，才能把变异正确映射到转录本。

## 从基因到CDS

基因是一个注释单位；同一基因可有多条转录本。外显子是成熟转录本保留的片段，可能包含非翻译区UTR；CDS是参与编码的片段。不能把所有exon当作CDS，也不能把每一行注释当成不同基因。

GFF3常用第九列的`ID`与`Parent`连接gene→mRNA/transcript→exon/CDS。GTF常以`gene_id`和`transcript_id`记录归属。两者通常都是九列、1起始闭区间；属性语法不同，不能仅改扩展名完成转换。[GFF3规范](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md)和[NCBI注释说明](https://www.ncbi.nlm.nih.gov/genbank/genomes_gff/)给出了格式与具体约定。

## 一个容易重复计数的例子

人工基因gPlus有txPlus1与txPlus2，两者共享101–160外显子。一个变异与两条exon行重叠，会产生两对命中，但仍可能只是一个基因、一个VCF记录。应分别统计记录数、ALT数、转录本数与重叠对数。

读取时先检查染色体名、边界、链、Parent是否存在、转录本归属与CDS phase。注释可能允许跨行共享ID等合法形式，应遵守来源规范，不能用教学脚本充当通用GFF验证器。

继续读[CDS阅读框密码子与剪接位点](https://github.com/SpiralKernel/bioinfo-wiki/wiki/CDS%E9%98%85%E8%AF%BB%E6%A1%86%E5%AF%86%E7%A0%81%E5%AD%90%E4%B8%8E%E5%89%AA%E6%8E%A5%E4%BD%8D%E7%82%B9)、[GFFGTF版本核查与注释准备](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GFFGTF%E7%89%88%E6%9C%AC%E6%A0%B8%E6%9F%A5%E4%B8%8E%E6%B3%A8%E9%87%8A%E5%87%86%E5%A4%87)。
