# GS中的REML混合模型方程与求解

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

区分方差组分估计、给定参数的BLUP求解和大规模关系矩阵近似。

## 三件不同的工作

GS软件经常同时完成估计方差、求育种值和计算不确定性。应分清：REML估计方差参数；混合模型方程在给定参数下求固定与随机效应；数值求解方法负责高效稳定地完成这些计算。

## REML解决什么

设 $y=Xb+Zu+e$，$u\sim N(0,G\sigma_u^2)$，$e\sim N(0,R\sigma_e^2)$。REML利用消除固定效应影响的残差信息估计方差组分。AI-REML等算法用不同的更新策略，结果还受边界约束、收敛阈值及初值影响。

某个方差估计接近零可能对应信息不足、冗余随机效应或边界最优。日志写“收敛”并不保证生物学解释正确。应看方差估计、标准误、梯度、约束状态，以及模型是否可识别。

## 混合模型方程

若G、R可逆，令 $\lambda=\sigma_e^2/\sigma_u^2$，则一种尺度下的方程为：

$$\begin{bmatrix}X^\mathsf TR^{-1}X&X^\mathsf TR^{-1}Z\\Z^\mathsf TR^{-1}X&Z^\mathsf TR^{-1}Z+\lambda G^{-1}\end{bmatrix}\begin{bmatrix}\hat b\\\hat u\end{bmatrix}=\begin{bmatrix}X^\mathsf TR^{-1}y\\Z^\mathsf TR^{-1}y\end{bmatrix}.$$

这里R表示残差的相对协方差结构，不能同时把绝对残差方差再重复乘进公式。半正定G或含约束的模型需要软件相应处理，不能盲目求逆。

## 怎样理解求解器

Cholesky等直接分解适用于相应正定系统；PCG通过迭代求解，需检查残差与停止条件。选择PCG不等于改变统计模型，但停止过早会影响数值结果。APY是基因组逆矩阵近似的思路，核心个体选择等设置会影响近似，不能把它仅理解为另一种完全相同的精确求解器。

工程上优先求解线性方程，而非显式存储不必要的大矩阵逆。样本量、标记量、稀疏结构和随机效应数量共同决定内存与时间，不能仅按“GWAS能跑多少样本”估计GS需求。

## 本项目教学实现的边界

[合成家系数据贯通GS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E5%AE%B6%E7%B3%BB%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9AGS)用内层交叉验证选择lambda，并直接求解线性方程，没有REML优化和大规模迭代求解器。专业软件可能默认REML，因此不应要求它们与教学脚本使用不同lambda时给出逐位一致结果。

接口例子见[rrBLUP手册](https://cran.r-project.org/web/packages/rrBLUP/rrBLUP.pdf)、[HIBLUP教程](https://www.hiblup.com/tutorials)、[BLUPF90说明](https://nce.ads.uga.edu/wiki/doku.php?id=readme.blupf90)。
