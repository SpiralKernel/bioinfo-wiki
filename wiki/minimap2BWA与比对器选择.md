# minimap2BWA与比对器选择

> 更新：2026-10-14；状态：可用；验证范围：人工基因案例与实际工具输出核对；具体已测范围见正文。

按reads类型、参考结构和分析目的选择比对器，再核对输出标记与下游兼容性。

## 先说任务

短读长DNA、长读长DNA、剪接RNA、组装对组装并不是相同任务。preset包含多项假设，不能只因某软件能读FASTQ就采用默认参数。BWA系常用于短读长DNA；minimap2有短读长、长读长和剪接等不同模式，需核对对应版本和任务。[minimap2官方README](https://github.com/lh3/minimap2)列出模式与使用方式。

本轮实际minimap2 2.30-r1287，使用`-ax sr`将40条人工单端150bp DNA reads比对到1600bp人工参考。没有运行BWA，也没有比较两者真实性能。

## 读组与输出

本例使用`-R '@RG\tID:toy\tSM:toySample'`写入读组，再交给samtools排序和索引。SM等字段关系到下游样本识别，不能把所有样本不加区分地合并。

检查primary、secondary和supplementary记录的用途、MAPQ、剪切和未比对比例。高比对率可能来自重复区域或偏好参考等位，不能自动证明结果可靠。比对器参数改变后需重新检查调用和覆盖，不能只看运行是否结束。

实际命令由[从FASTQ到比对检查与变异调用](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BB%8EFASTQ%E5%88%B0%E6%AF%94%E5%AF%B9%E6%A3%80%E6%9F%A5%E4%B8%8E%E5%8F%98%E5%BC%82%E8%B0%83%E7%94%A8)的脚本记录；理解输出先读[SAM与BAM及CRAM](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SAM%E4%B8%8EBAM%E5%8F%8ACRAM)。专业真实物种的短读长/长读长比较仍在后续维护范围。
