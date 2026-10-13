# FASTA与FASTQ

> 更新：2026-10-13；状态：可用；验证范围：文档核对；操作需按所用环境验证。

FASTA 保存序列及标题，FASTQ 还保存逐碱基质量信息，二者服务于不同分析阶段。

## 怎样识别

FASTA 的记录以 `>` 标题行开始，后接一行或多行序列。FASTQ 的常见形式以 `@` 标题行开始，随后是序列、`+` 分隔和质量字符串。不要只凭扩展名判定内容。

FASTQ 中序列长度应与质量字符串长度对应。双端数据的两个文件还要检查读段标识和记录顺序。真实解析器需要处理格式边界；简单把总行数除以四，只适用于已经确认的四行记录格式。

## 使用场景

测序读段通常从 FASTQ 开始；参考序列、蛋白序列和数据库检索输入常用 FASTA。FASTA 不保留原始逐碱基质量，不能转换回原始 FASTQ 的测量信息。

质量解释见[测序深度覆盖度与质量分数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E6%B7%B1%E5%BA%A6%E8%A6%86%E7%9B%96%E5%BA%A6%E4%B8%8E%E8%B4%A8%E9%87%8F%E5%88%86%E6%95%B0)；检索实践见[BLAST本地检索实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLAST%E6%9C%AC%E5%9C%B0%E6%A3%80%E7%B4%A2%E5%AE%9E%E8%B7%B5)。格式细节参考 [NCBI FASTA 说明](https://www.ncbi.nlm.nih.gov/genbank/fastaformat/)和 [SAMtools FASTQ 文档](https://www.htslib.org/doc/samtools-fasta.html)。
