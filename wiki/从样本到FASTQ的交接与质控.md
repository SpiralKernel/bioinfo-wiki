# 从样本到FASTQ的交接与质控

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

按样本、文库、运行与数据阶段交接，文件和质量报告需要相互追溯。

## 最少交接四类记录

样本表写来源、个体、组别、批次和重复；文库表写建库、索引、UMI和read布局；运行表写平台/化学、识别与拆分版本；文件表写路径、大小、记录数、压缩和校验值。

样本、文库、文件名称可能不同，保留映射。重复上机或重做文库不等于新独立样本。

## 检查顺序

1. 核对文件、样本、校验值和读段名称。
2. 确认阶段：信号、循环识别、拆分后FASTQ或BAM。
3. 检查单双端对应、序列与质量长度。
4. 读长度、质量、接头、GC、重复和未分配比例。
5. 按任务检查比对、覆盖、污染和捕获，不只看Q30。
6. 保存处理前后数量与排除原因，再交给下游。

## 文库差异

扩增子、单细胞、UMI、小RNA和长读长结构不同。统一剪切可能删掉标签，统一去重可能误删真实分子。异常QC有时来自设计，应调查而非机械判失败。

本页没有执行真实文件交接或外部QC。工具见[测序质控工具选择与报告阅读](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E8%B4%A8%E6%8E%A7%E5%B7%A5%E5%85%B7%E9%80%89%E6%8B%A9%E4%B8%8E%E6%8A%A5%E5%91%8A%E9%98%85%E8%AF%BB)，格式见[测序数据格式与原始信号](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E4%B8%8E%E5%8E%9F%E5%A7%8B%E4%BF%A1%E5%8F%B7)及[FASTA与FASTQ](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FASTA%E4%B8%8EFASTQ)。参考：[FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)、[MultiQC](https://docs.seqera.io/multiqc)。
