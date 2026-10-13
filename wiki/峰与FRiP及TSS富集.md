# 峰与FRiP及TSS富集

> 更新：2026-10-13；验证范围：文档核对；完整流程未在本机运行。

峰是相对背景具有信号富集的区域，FRiP 和 TSS 富集用于从不同角度评价部分染色质测量。

峰的边界取决于数据、背景和调用方法，不等于真实调控元件边界。窄峰与宽峰适用的信号结构不同。

FRiP 是按特定统计口径落在峰区中的读段或片段比例；应记录分母、峰集、是否去重及过滤规则。TSS 富集衡量转录起始区域附近的信噪特征，受参考注释与算法影响。

比较两个项目的数字前，先核对口径。某个项目的推荐阈值只适用于相应测量与标准，不自动成为所有物种或实验的合格线。

实践见[ATAC-seq入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/ATAC-seq%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)和[ChIP-seq入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/ChIP-seq%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)。定义与标准见 [ENCODE 术语表](https://www.encodeproject.org/data-standards/terms/)和[ATAC 标准](https://www.encodeproject.org/data-standards/atac-seq/atac-encode4/)。
