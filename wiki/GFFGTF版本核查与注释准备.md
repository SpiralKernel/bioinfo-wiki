# GFFGTF版本核查与注释准备

> 更新：2026-10-14；状态：可用；验证范围：人工基因案例与实际工具输出核对；具体已测范围见正文。

注释前先确认序列、坐标和基因模型属于同一套参考，避免得到表面完整却对应错误版本的后果。

## 准备清单

保存物种、组装accession及版本、下载日期、注释release、FASTA/GFF/GTF/CDS/蛋白来源与SHA256。染色体名相同不代表组装相同；加减chr前缀只是命名修改，不是版本转换。

列出序列名与长度，检查GFF边界、链和父子关系；将注释seqid与FASTA名称逐项比较。核、细胞器、未定位contig是否纳入要明确。CDS和蛋白ID的版本后缀不能随意删去，先建立可追溯映射。

## 验证模型

按转录方向重建CDS，检查phase和遗传密码表，并与来源CDS、蛋白核对。来源可能包含部分模型、特殊翻译等，应该按来源约定处理并记录例外；不要把所有警告强行消掉。

人工例子只有完整、标准密码、phase0的三条转录本。SnpEff实际3条CDS和3条蛋白检查均零错误，并不代表教学解析器已支持所有GFF合法形式。

## 失败时先停在哪里

REF不匹配先查FASTA版本和表示；大量序列缺失先查命名与下载范围；蛋白普遍错误先查链、phase、密码表与版本配对。不能先忽略错误，再在后果表中补解释。

输出应有资源清单、检查报告、ID映射、数据库版本与未解决问题。下一步[SnpEff自建数据库与后果解析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SnpEff%E8%87%AA%E5%BB%BA%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8E%E5%90%8E%E6%9E%9C%E8%A7%A3%E6%9E%90)或[VEP缓存离线注释与CSQ](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VEP%E7%BC%93%E5%AD%98%E7%A6%BB%E7%BA%BF%E6%B3%A8%E9%87%8A%E4%B8%8ECSQ)；规范见[NCBI GFF说明](https://www.ncbi.nlm.nih.gov/genbank/genomes_gff/)。
