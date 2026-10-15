# RNA-seq从FASTQ到基因计数

> 更新：2026-10-15；状态：可用；验证范围：官方资料与方法核对；本页上游或扩展软件流程未执行。

根据建库、reads布局和参考资源选择比对或定量路径，为差异分析提供来源明确的计数。

## 两条常见路径

基因组剪接比对→基因计数，例如[STAR剪接比对与RNA比对指标](https://github.com/SpiralKernel/bioinfo-wiki/wiki/STAR%E5%89%AA%E6%8E%A5%E6%AF%94%E5%AF%B9%E4%B8%8ERNA%E6%AF%94%E5%AF%B9%E6%8C%87%E6%A0%87)接[featureCounts基因计数与链方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/featureCounts%E5%9F%BA%E5%9B%A0%E8%AE%A1%E6%95%B0%E4%B8%8E%E9%93%BE%E6%96%B9%E5%90%91)；或转录本定量→基因汇总，例如[Salmon定量与tximport基因汇总](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Salmon%E5%AE%9A%E9%87%8F%E4%B8%8Etximport%E5%9F%BA%E5%9B%A0%E6%B1%87%E6%80%BB)。路径不同，计数与长度处理约定也不同，不应混合列拼成一个未经说明的矩阵。

## 每个阶段的检查点

| 阶段 | 核对内容 | 保存产物 |
|---|---|---|
| 实验与FASTQ | 生物学重复、单双端、链、UMI、样本ID | 样本表、数据来源与校验值 |
| 原始质控 | 碱基质量、接头、污染及文库特殊性 | QC报告、采用或不采用修剪的理由 |
| 比对/定量 | 参考和注释、索引、library type、多重比对 | 日志、命令、分配统计 |
| 汇总 | gene/transcript ID、单位、歧义规则 | 原始矩阵、映射表、未匹配清单 |
| 模型入口 | 样本对应、过滤、设计可估计性 | 已核对输入及分析计划 |

UMI文库是否需要分子去重、3′计数能否沿用常规全长假设，都要按实验技术判断。只凭重复率不能随意去除真实高表达信号。

本页为流程指南，未重跑真实FASTQ；原生R实测从airway已有计数开始。生产流程可参考[nf-core/rnaseq](https://nf-co.re/rnaseq/)，版本和参数应固定后再使用。继续到[RNA计数矩阵与样本表核对](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E4%B8%8E%E6%A0%B7%E6%9C%AC%E8%A1%A8%E6%A0%B8%E5%AF%B9)。
