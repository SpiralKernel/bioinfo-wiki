# 小RNA分析入门与实践

> 更新：2026-10-13；状态：可用；验证范围：文档核对；操作示例未在本机运行。

小RNA测序关注短RNA群体，接头处理、长度选择和注释分配直接影响计数。

## 与常规RNA-seq有什么不同

小RNA建库选择的分子长度和接头结构不同，常见目标包括miRNA等短RNA。因为插入片段短，读段经常读入接头；是否正确识别接头会明显改变有效序列。不能直接照搬常规mRNA的全部预处理和定量规则。

## 从读段到计数

准备样本表和实验接头信息 → 原始质控 → 接头去除与长度检查 → 按注释及任务比对或定量 → 查看RNA类别组成和多重匹配 → 汇总计数 → 使用符合设计的差异模型。某些研究需要区分成熟miRNA、前体和序列变体，必须说明计数归属规则。

短序列更容易匹配多个位置；注释版本及类别竞争会改变分配。记录物种、组装、miRNA数据库版本、接头序列来源、长度门槛和多重匹配处理。未知RNA占比高时回查文库和注释，不应只删除后报告剩余部分。

## 官方实践入口

按[nf-core/smrnaseq用法](https://nf-co.re/smrnaseq/latest/docs/usage/)选择固定release，先读取该版本样本表结构和支持的参考配置，再运行官方测试。本机尚未执行此流程；实际运行需保存命令、容器、软件版本和测试日志。

完成后检查每个样本的有效读段数、长度分布、miRNA比例、计数矩阵和样本对应关系。差异分析仍以[生物学重复与技术重复](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%9F%E7%89%A9%E5%AD%A6%E9%87%8D%E5%A4%8D%E4%B8%8E%E6%8A%80%E6%9C%AF%E9%87%8D%E5%A4%8D)为基础；定量方法与[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)可有相通之处，但输入和注释假设应单独核对。

## 可以支持什么结论

丰度变化首先说明测量到的小RNA水平差异；计算预测的靶基因不是已证实调控关系。靶基因富集需要明确候选来源、背景及多重检验，见[富集分析与GSEA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8EGSEA)。

深入：[nf-core/smrnaseq项目与输出文档入口](https://nf-co.re/smrnaseq/)、[FASTA与FASTQ](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FASTA%E4%B8%8EFASTQ)、[计数丰度与标准化](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%AE%A1%E6%95%B0%E4%B8%B0%E5%BA%A6%E4%B8%8E%E6%A0%87%E5%87%86%E5%8C%96)。


## 测序技术与上游输入

[RNA测序建库选择与偏倚](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%B5%8B%E5%BA%8F%E5%BB%BA%E5%BA%93%E9%80%89%E6%8B%A9%E4%B8%8E%E5%81%8F%E5%80%9A)说明长度、连接和富集的影响；用[从样本到FASTQ的交接与质控](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BB%8E%E6%A0%B7%E6%9C%AC%E5%88%B0FASTQ%E7%9A%84%E4%BA%A4%E6%8E%A5%E4%B8%8E%E8%B4%A8%E6%8E%A7)核对接头和布局，避免套用普通WGS剪切。
