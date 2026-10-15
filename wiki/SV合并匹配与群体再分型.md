# SV合并匹配与群体再分型

> 更新：2026-10-15；状态：可用；验证范围：官方文档与原始研究核对；专业检测命令为模板，未执行完整真实数据流程。

跨样本整理SV需要定义事件相似性，再分型与缺失处理决定群体矩阵是否可信。

## 匹配不只看坐标

同一事件可能有偏移断点或不同序列表示，附近两个独立事件也可能距离很近。匹配通常综合类型、断点距离、大小相似性、区间重叠、方向与可用序列；插入/BND不能机械套缺失区间重叠规则。

对低复杂区，适当归一化与序列相似性尤其重要。容差太大会把不同等位塌为一条，太小会保留重复候选；参数应做敏感性检查。见[Truvari工具与论文入口](https://github.com/ACEnglish/truvari)。

## 三个不同步骤

1. 合并候选位点/事件集合，保存来源及匹配关系。
2. 用调用器支持的接口重新评估各样本在该集合中的分型。
3. 整理兼容分型输出为群体VCF，并重新检查缺失、倍性、质量和频率。

bcftools merge本身不是第三方SV调用器的再分型算法。把无记录填0/0会把没有证据当作不存在；用于PAV也有同样问题。

[DELLY结构变异与群体分型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DELLY%E7%BB%93%E6%9E%84%E5%8F%98%E5%BC%82%E4%B8%8E%E7%BE%A4%E4%BD%93%E5%88%86%E5%9E%8B)展示位点列表→逐样本分型→合并的模板；[Sniffles长读长结构变异实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Sniffles%E9%95%BF%E8%AF%BB%E9%95%BF%E7%BB%93%E6%9E%84%E5%8F%98%E5%BC%82%E5%AE%9E%E8%B7%B5)展示SNF群体模式。不要把SV事件匹配、VCF标准化或GVCF联合分型互相替代。

## 本轮整理入口

本轮[人工长读长贯通SV调用与评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E9%95%BF%E8%AF%BB%E9%95%BF%E8%B4%AF%E9%80%9ASV%E8%B0%83%E7%94%A8%E4%B8%8E%E8%AF%84%E4%BC%B0)分别运行SNF群体与BAM force，保留两者不同状态；匹配规则见[SV事件匹配与一对一评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SV%E4%BA%8B%E4%BB%B6%E5%8C%B9%E9%85%8D%E4%B8%8E%E4%B8%80%E5%AF%B9%E4%B8%80%E8%AF%84%E4%BC%B0)、[Truvari事件比较与评估参数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Truvari%E4%BA%8B%E4%BB%B6%E6%AF%94%E8%BE%83%E4%B8%8E%E8%AF%84%E4%BC%B0%E5%8F%82%E6%95%B0)。
