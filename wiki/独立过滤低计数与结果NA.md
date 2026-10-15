# 独立过滤低计数与结果NA

> 更新：2026-10-15；状态：可用；验证范围：原生R与公开airway计数案例已执行；范围和结果见正文。

预过滤、独立过滤和异常计数处理发生在不同环节，结果中的NA必须按原因解释。

## 三个位置

预过滤在拟合前移除指定基因。本例用总原始计数至少10，是固定练习选择，不是跨实验通用阈值；全零行已在这里移除。

独立过滤发生在结果整理阶段，通常根据平均标准化计数选择过滤范围，以改善给定alpha下的发现。一个基因可以有原始P却没有padj。若P本身为NA，还要查看全零、异常计数/Cook距离及具体软件处理，不能统称为低表达。

## 本例如何保留证据

输出result-status.csv，将“有P且有padj”“有P但padj为NA”“P为NA需继续检查”分开。关闭独立过滤另存对照结果；实际核对其padj与该次有效P上的BH校正相符。

关闭过滤是诊断对照，不应在看到哪个结果更好看后任意选择。alpha会参与默认过滤选择，若计划报告FDR0.05，应在提取时显式设置，而不是先用其他alpha再仅改变表的筛选数值。

相关API见[DESeq2结果手册](https://bioconductor.org/packages/release/bioc/manuals/DESeq2/man/DESeq2.pdf)。本轮具体计数见[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)；NA不会在图中擅自替换成0或1来冒充原始结果。
