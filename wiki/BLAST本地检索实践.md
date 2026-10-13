# BLAST本地检索实践

> 更新：2026-10-13；验证范围：文档核对；操作需按所用环境验证。

用本地数据库理解查询、数据库构建与结果字段，并将正式结论建立在覆盖率和统计解释上。

## 适用范围与准备

先读[BLAST原理与种子延伸](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLAST%E5%8E%9F%E7%90%86%E4%B8%8E%E7%A7%8D%E5%AD%90%E5%BB%B6%E4%BC%B8)和[FASTA与FASTQ](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FASTA%E4%B8%8EFASTQ)。这里介绍一般序列检索的软件接口；需要已安装 BLAST+、查询 FASTA 和来源明确的参考 FASTA，工具下载与完整手册在 [NCBI BLAST Help](https://blast.ncbi.nlm.nih.gov/doc/blast-help/)。

## 本地接口示例

```bash
blastn -version
mkdir -p results blastdb
makeblastdb -in reference.fa -dbtype nucl -out blastdb/reference
blastn -query query.fa -db blastdb/reference \
  -outfmt '6 qseqid sseqid pident length qstart qend sstart send evalue bitscore qcovs' \
  -out results/hits.tsv
```

命令按官方接口核对，尚未在本机安装 BLAST+ 运行。`reference.fa` 和 `query.fa` 是需替换的输入，不是已经提供的数据。若查询和数据库是蛋白，应选择对应程序与 `-dbtype prot`；详见手册的程序选择表。

## 输出与检查点

格式 6 的该示例没有标题行，列顺序由 outfmt 定义。保存列名说明、程序版本、查询校验值和数据库构建日期。检查覆盖率、方向及多个局部命中；空输出也可能是阈值、程序或数据库不匹配，需要查看日志与输入。

最佳命中不是自动的功能注释或一对一同源证明。统计解释见[比对相似性同源性与覆盖率](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%AF%94%E5%AF%B9%E7%9B%B8%E4%BC%BC%E6%80%A7%E5%90%8C%E6%BA%90%E6%80%A7%E4%B8%8E%E8%A6%86%E7%9B%96%E7%8E%87)，基因关系见[基因标识符与同源基因](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E6%A0%87%E8%AF%86%E7%AC%A6%E4%B8%8E%E5%90%8C%E6%BA%90%E5%9F%BA%E5%9B%A0)。

深入入口：[BLAST+ 应用手册](https://www.ncbi.nlm.nih.gov/books/NBK279690/)、[官方程序与文献索引](https://blast.ncbi.nlm.nih.gov/doc/blast-help/references.html)。
