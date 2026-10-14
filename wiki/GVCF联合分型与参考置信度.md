# GVCF联合分型与参考置信度

> 更新：2026-10-14；状态：可用；验证范围：官方文档与原始研究核对；专业检测命令为模板，未执行完整真实数据流程。

GVCF保留参考置信信息，合并中间文件与联合决定群体基因型是不同步骤。

## 为什么需要中间表示

单样本最终VCF常只记录发现的变异。某样本没有一条记录，可能是纯合参考，也可能是覆盖不足或没评估；不能填成0/0。GVCF通过参考块和相关信息帮助后续联合分型评估这些区别。

`<NON_REF>`是相应参考置信框架中的符号等位，不是发现了某种真实插入。GVCF参考块的END、分型置信及倍性也需要核对，不能当作普通SNP集合计数。

## 三类操作

| 操作 | 回答什么 | 不代表什么 |
|---|---|---|
| CombineGVCFs/导入GenomicsDB | 整理多个样本的中间证据 | 联合分型已经完成 |
| GenotypeGVCFs | 在对应模型下生成群体分型结果 | 所有质量过滤已经完成 |
| bcftools merge | 合并兼容记录与样本列 | 从缺失的测序证据重新推断了基因型 |

GATK GVCF与其他调用器的gVCF并不默认可互换；软件版本、头部、参考、倍性及模型均需核对。新增样本后的群体频率和过滤也应重审。

具体步骤见[GATK小变异检测与联合分型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GATK%E5%B0%8F%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E4%B8%8E%E8%81%94%E5%90%88%E5%88%86%E5%9E%8B)。依据：[GATK联合分型逻辑](https://gatk.broadinstitute.org/hc/en-us/articles/360035890431-The-logic-of-joint-calling-for-germline-short-variants)。
