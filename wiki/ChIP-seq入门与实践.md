# ChIP-seq入门与实践

> 更新：2026-10-13；状态：可用；验证范围：文档核对；完整流程未在本机运行。

ChIP-seq 分析目标富集相对背景的信号分布，必须区分对照、抗体目标与信号宽度。

## 输入与流程

需要 IP 样本、对应背景对照、重复信息、抗体目标和参考资源。对照类型及对应关系是分析输入，不能从文件名猜测。

先做质量与比对检查，再评估重复和背景、调用适合目标的峰、检查重复一致性、构建共同区域计数及模型。转录因子窄峰和部分组蛋白修饰宽信号的调用设置可能不同，不宜统一合并所有抗体的峰集。

## 实践练习

使用 [nf-core/chipseq 的官方样本表与测试配置](https://nf-co.re/chipseq/latest/docs/usage/)。先核对所选版本的列名，再填写目标、重复和 control 对应关系；文档不同版本的字段可能变化，样本表必须绑定版本。

练习应保存 IP/对照的质量报告、轨迹、峰表和重复比较。任选一个区域查看目标相对背景是否有一致信号；只有某个样本出现的峰需要结合测序量和背景进一步审查。

本机未运行完整流程。峰差异不直接证明基因表达变化或功能改变，见[峰与FRiP及TSS富集](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B3%B0%E4%B8%8EFRiP%E5%8F%8ATSS%E5%AF%8C%E9%9B%86)及[富集分析与GSEA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8EGSEA)。

深入：[ENCODE ChIP-seq 标准入口](https://www.encodeproject.org/chip-seq/)、[nf-core/chipseq 输出说明](https://nf-co.re/chipseq/latest/docs/output/)。
