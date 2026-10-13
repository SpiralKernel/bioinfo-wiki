# RT-PCR实时PCR与数字PCR的区别

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

逆转录、实时检测和数字分区描述不同环节，RT不能默认解释为实时。

## 先把名称拆开

| 名称 | 主要含义 | 常见输出 |
|---|---|---|
| 常规PCR | 扩增DNA，常在终点观察产物 | 产物及检测结果 |
| RT-PCR | 先逆转录RNA为cDNA，再PCR | RNA来源目标的扩增结果 |
| qPCR / real-time PCR | 随循环监测荧光相关信号 | 扩增曲线、Cq/Ct等 |
| RT-qPCR | 逆转录与实时定量结合 | RNA目标的相应定量 |
| dPCR | 分区后依据终点阳性/阴性推断含量 | 分区计数与浓度估计 |
| ddPCR | 液滴分区的一类dPCR | 液滴分类与相应估计 |

RT通常指reverse transcription，不是“实时”的通用缩写。数字PCR也可接入逆转录，液滴只是分区形式之一。

## 定量假设

Cq/Ct来自阈值及算法，受效率、背景与输入影响。dPCR不是简单把阳性分区数当分子数：一个分区可能含多个目标，需要统计校正和体积定义。

“绝对定量”不表示没有测量误差。回收、抑制、分区分类、有效体积和参考材料均影响结果。

判读见[qPCR与数字PCR结果判读](https://github.com/SpiralKernel/bioinfo-wiki/wiki/qPCR%E4%B8%8E%E6%95%B0%E5%AD%97PCR%E7%BB%93%E6%9E%9C%E5%88%A4%E8%AF%BB)；转录组用途见[转录组差异与qPCR验证设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BD%95%E7%BB%84%E5%B7%AE%E5%BC%82%E4%B8%8EqPCR%E9%AA%8C%E8%AF%81%E8%AE%BE%E8%AE%A1)。依据：[MIQE 2.0](https://pubmed.ncbi.nlm.nih.gov/40272429/)、[dMIQE 2020](https://pubmed.ncbi.nlm.nih.gov/32746458/)。
