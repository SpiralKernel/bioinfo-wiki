# DNA甲基化分析入门

> 更新：2026-10-14；状态：可用；验证范围：文档核对；完整流程未在本机运行。

甲基化分析需要匹配测量技术，以覆盖和重复信息估计位点或区域差异。

## 先区分平台

亚硫酸氢盐测序、其他转换测序和甲基化芯片的原始数据、偏倚与模型不同。不能把芯片的信号处理步骤直接套到测序计数。

对于转换测序，常见路线是读段质量检查、适配的比对、位点甲基化证据提取、覆盖与转换相关检查、位点或区域差异分析。记录背景序列类型、正反链处理、过滤和参考版本。

## 如何理解比例

10 个读段中 8 个支持甲基化和 100 个读段中 80 个支持甲基化，比例都是 0.8，但观测精度不同。保留甲基化与总覆盖计数，不只交付比例矩阵。多个相邻位点组成的区域还涉及相关性和区域定义。

## 第一轮实践

按 [nf-core/methylseq 官方说明](https://nf-co.re/methylseq/latest/docs/usage/)的 test profile 做环境和小数据练习。固定发布版本，确认该配置使用哪一种测量与参考。输出检查覆盖分布、位点上下文及甲基化计数；差异区域需另外使用适合实验设计的统计方法分析，并核对区域定义与重复。不要把基础流程测试成功当作差异分析或生物学验证完成。

完整流程尚未在本机运行。阈值与模型应结合[生物学重复与技术重复](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%9F%E7%89%A9%E5%AD%A6%E9%87%8D%E5%A4%8D%E4%B8%8E%E6%8A%80%E6%9C%AF%E9%87%8D%E5%A4%8D)和[P值效应量与多重检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/P%E5%80%BC%E6%95%88%E5%BA%94%E9%87%8F%E4%B8%8E%E5%A4%9A%E9%87%8D%E6%A3%80%E9%AA%8C)，转换平台特有指标需继续查官方文档。


## 统计基础与验证入口

[表观组峰与调控证据验证](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%A1%A8%E8%A7%82%E7%BB%84%E5%B3%B0%E4%B8%8E%E8%B0%83%E6%8E%A7%E8%AF%81%E6%8D%AE%E9%AA%8C%E8%AF%81)补充本任务所需的统计或验证判断。分析前先确认[统计方法选择与分析计划](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%9F%E8%AE%A1%E6%96%B9%E6%B3%95%E9%80%89%E6%8B%A9%E4%B8%8E%E5%88%86%E6%9E%90%E8%AE%A1%E5%88%92)，结果解释时区分[组学验证的层级与证据](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E9%AA%8C%E8%AF%81%E7%9A%84%E5%B1%82%E7%BA%A7%E4%B8%8E%E8%AF%81%E6%8D%AE)。

## 对应方法与深入

[差异峰与差异甲基化方法](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B7%AE%E5%BC%82%E5%B3%B0%E4%B8%8E%E5%B7%AE%E5%BC%82%E7%94%B2%E5%9F%BA%E5%8C%96%E6%96%B9%E6%B3%95)解释输入条件和适用边界；软件运行步骤与方法假设一起核对。
