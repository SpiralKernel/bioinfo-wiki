# ATAC-seq入门与实践

> 更新：2026-10-13；状态：可用；验证范围：文档核对；完整流程未在本机运行。

从可及性测序读段得到区域信号与差异分析，重点检查信号质量、重复一致性和共同计数区域。

## 输入与主要步骤

输入为 FASTQ、样本表、匹配参考及注释。ATAC-seq 反映可及性相关信号，不直接测量基因表达或某个特定蛋白的结合。

| 阶段 | 产物 | 检查点 |
|---|---|---|
| 读段质量与比对 | BAM、质控报告 | 接头、比对、参考和片段分布 |
| 过滤与信号处理 | 可用片段、信号轨迹 | 重复、线粒体、黑名单及处理口径 |
| 区域识别 | 峰集合 | TSS 富集、FRiP、重复一致性 |
| 共同区域计数 | 区域×样本矩阵 | 区域定义、样本对应、计数单位 |
| 差异与注释 | 差异区域及注释 | 重复、模型、FDR、基因连接依据 |

定义见[峰与FRiP及TSS富集](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B3%B0%E4%B8%8EFRiP%E5%8F%8ATSS%E5%AF%8C%E9%9B%86)。最近基因注释只是一种关联规则，远端峰不能仅凭邻近位置就断言调控某个基因。

## 第一轮实践

从 [nf-core/atacseq 使用说明](https://nf-co.re/atacseq/latest/docs/usage/)选择官方测试配置，固定版本后运行其 test profile；记录实际启用的参考和参数。先解释一份质量报告、一组重复的信号轨迹和一个峰记录，再扩展到差异分析。

流程尚未在本机运行。自有物种的染色体、线粒体名称、黑名单、TSS 注释与峰调用设置应单独核对，不能复制人类资源。

深入标准见 [ENCODE ATAC 数据标准](https://www.encodeproject.org/data-standards/atac-seq/atac-encode4/)。衔接[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)与[多组学整合入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%A4%9A%E7%BB%84%E5%AD%A6%E6%95%B4%E5%90%88%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)。


## 统计基础与验证入口

[表观组峰与调控证据验证](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%A1%A8%E8%A7%82%E7%BB%84%E5%B3%B0%E4%B8%8E%E8%B0%83%E6%8E%A7%E8%AF%81%E6%8D%AE%E9%AA%8C%E8%AF%81)补充本任务所需的统计或验证判断。分析前先确认[统计方法选择与分析计划](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%9F%E8%AE%A1%E6%96%B9%E6%B3%95%E9%80%89%E6%8B%A9%E4%B8%8E%E5%88%86%E6%9E%90%E8%AE%A1%E5%88%92)，结果解释时区分[组学验证的层级与证据](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E9%AA%8C%E8%AF%81%E7%9A%84%E5%B1%82%E7%BA%A7%E4%B8%8E%E8%AF%81%E6%8D%AE)。
