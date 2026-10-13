# 二分类性状OR与病例对照不平衡

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

二分类关联需要核对标签、病例与对照中的等位基因计数，以及模型是否能处理稀疏和相关样本。

## 逻辑回归的效应不是概率差

设病例概率为p，odds为`p/(1−p)`。逻辑回归对log-odds建模，某等位基因剂量系数β对应调整后的`OR = exp(β)`。OR=2表示odds翻倍，不能直接说患病概率翻倍；它也不是通常意义上的相对风险。

连续性状LMM的β以性状单位表达，即使把二分类0/1送进去，也不能自动将β取指数当成逻辑模型的OR。性状变换与模型决定效应尺度，见[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)。

## 标签和稀疏计数为什么关键

不同软件可能默认1/2或0/1编码，缺失也有不同约定。先列出标签、个数和定义，明确哪个是病例。100个病例与100000个对照的总样本数很大，但某低频变异在病例中仍可能只有0或1个携带者。

完全或近完全分离会让常规逻辑回归估计不稳定。Firth引入偏差校正；SPA改进部分得分统计量的尾部近似。它们解决的问题与GRM表示家系相关性不同：有Firth不代表已经校正亲缘，有GRM也不代表极低MAC统计量总可靠。

## 怎样选择与检查

独立样本的基础练习可查看[PLINK2关联分析详解](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PLINK2%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E8%AF%A6%E8%A7%A3)；相关样本和明显不平衡设计应详细审查[SAIGE单变异关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SAIGE%E5%8D%95%E5%8F%98%E5%BC%82%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)、[REGENIE两步关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/REGENIE%E4%B8%A4%E6%AD%A5%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)及[fastGWA与fastGWA-GLMM](https://github.com/SpiralKernel/bioinfo-wiki/wiki/fastGWA%E4%B8%8EfastGWA-GLMM)中的相应模块。[BOLT-LMM关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BOLT-LMM%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)的适用限制要单独阅读。

保存病例/对照数、各组等位基因计数、收敛或错误标记、检验方法、BETA或OR、SE与P。若只提供OR，需确认SE究竟属于OR还是log-OR；Meta分析通常需要一致的log-OR尺度。

## 最小练习

假设同一计数等位基因的log-OR为0.4，则OR约1.49；换成另一等位基因计数时，log-OR约−0.4、OR约0.67。这个方向变换不改变同一双侧检验的证据，但病例标签颠倒、编码不同或模型不同还需额外核对。

深入：[PLINK逻辑/Firth说明](https://www.cog-genomics.org/plink/2.0/assoc)、[SAIGE方法原文](https://doi.org/10.1038/s41588-018-0184-y)、[REGENIE二分类方法](https://rgcgithub.github.io/regenie/overview/)、[GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80)。
