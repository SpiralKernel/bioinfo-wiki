# PCA原理与实现

> 更新：2026-10-13；验证范围：文档核对；操作需按所用环境验证。

主成分分析寻找解释数据变化的正交方向；输入矩阵的定义和尺度直接影响结果。

## 从矩阵到坐标

设 X 的行为样本、列为特征。中心化后的矩阵做奇异值分解 X = UΣVᵀ；样本的主成分坐标为 UΣ，V 给出特征方向。是否按特征标准化，应根据数据类型决定。

基因型 PCA 常以位点频率进行中心化和方差尺度处理；普通表格直接做 PCA 不一定与 PLINK 的基因组 PCA 相同。稀有位点、LD 区域、家系、缺失和异常样本都可能主导某条轴。

## 不变量与易混淆点

特征向量符号可以整体翻转，所以两次图形左右颠倒不一定意味着结论改变。不同数据集单独计算的 PC1 也不是可直接拼接的同一坐标；投影需要保存训练集的频率、权重和处理规则。

只拿前五个特征值相除，不能准确宣称它们占“全部方差”的比例，除非掌握总方差或完整谱。

## 实践与深入

先用[合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)验证输入输出，再按[用PCA探索样本的群体结构](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%A8PCA%E6%8E%A2%E7%B4%A2%E6%A0%B7%E6%9C%AC%E7%9A%84%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84)检查真实数据。基因型处理依据见 [PLINK PCA 手册](https://www.cog-genomics.org/plink/2.0/strat)，一般 SVD 接口见 [NumPy 文档](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html)。
