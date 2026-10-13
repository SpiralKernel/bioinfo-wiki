# 转录组差异与qPCR验证设计

> 更新：2026-10-13；状态：可用；验证范围：原始研究与官方规范核对；实验设计说明，未执行湿实验或真实组学验证。

分别验证差异表达统计、表达测量与生物学重复，避免把qPCR当作自动证明功能。

## 先检查RNA-seq证据

确认独立生物学重复、配对/批次设计、原始计数、归一化、效应方向与FDR。低表达、样本组成和离群可能改变候选排序；候选规则应综合效应、区间和生物学问题，而不是只拿最小P值的几个基因。

完整流程见[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)。差异表达不等于蛋白变化，也不直接证明通路活性改变。

## qPCR验证的是哪一层

同一RNA做RT-qPCR主要提供测量方法间的技术确认；新独立个体才增加独立生物学重复证据。需要记录组织、采样时点、目标转录本、参考基因稳定性、检测特异性、扩增效率和对照。没有单个参考基因适合所有组织与处理。

本页提供设计和解释，不给固定实验参数；具体实施与质量报告应结合[MIQE 2.0指南](https://pubmed.ncbi.nlm.nih.gov/40272429/)（DOI：10.1093/clinchem/hvaf043）。

## ΔCt与ΔΔCt如何解释

常见定义为ΔCt=Ct目标−Ct参考，ΔΔCt=ΔCt处理−ΔCt对照；在相应效率假设下相对倍数为 $2^{-\Delta\Delta Ct}$。倍数增加与ΔCt减少方向相反，应在图和统计表中说明。

技术孔先按预定质量规则汇总到生物学单位，再按配对或独立设计分析合适的ΔCt/模型尺度。不能把每个技术孔当独立个体，或只在不对称的倍数值上不加判断做普通t检验。效率不相容时需要相应校正，不能坚持用简化公式。

## 验证表与阴性结果

保留候选选择理由、RNA-seq效应/区间/FDR、qPCR检测对象、独立样本数、ΔCt方向、效应/区间及失败原因。候选中的部分未复现应报告，不用不断替换基因直到全部成功。

进一步功能解释还需相应干预、蛋白或表型证据，见[组学验证的层级与证据](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E9%AA%8C%E8%AF%81%E7%9A%84%E5%B1%82%E7%BA%A7%E4%B8%8E%E8%AF%81%E6%8D%AE)。公式来源：[Livak与Schmittgen相对定量原始方法](https://doi.org/10.1006/meth.2001.1262)。


## 测序技术与上游输入

名称区别见[RT-PCR实时PCR与数字PCR的区别](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RT-PCR%E5%AE%9E%E6%97%B6PCR%E4%B8%8E%E6%95%B0%E5%AD%97PCR%E7%9A%84%E5%8C%BA%E5%88%AB)；曲线、分区和质量判读见[qPCR与数字PCR结果判读](https://github.com/SpiralKernel/bioinfo-wiki/wiki/qPCR%E4%B8%8E%E6%95%B0%E5%AD%97PCR%E7%BB%93%E6%9E%9C%E5%88%A4%E8%AF%BB)；引物和检测对象见[引物扩增子与特异性](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%BC%95%E7%89%A9%E6%89%A9%E5%A2%9E%E5%AD%90%E4%B8%8E%E7%89%B9%E5%BC%82%E6%80%A7)。
