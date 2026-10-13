# GBLUP与rrBLUP原理及实现

> 更新：2026-10-13；状态：可用；验证范围：公式与原始方法核对；NumPy个体与标记两条路径已运行并通过等价性测试。

用同一套中心化、固定效应与方差缩放，连接个体GBLUP和标记岭回归。

## 从基因型构建关系矩阵

设训练集基因型矩阵M有n个个体、m个位点，每格为同一记录等位基因的0/1/2剂量。由训练集估计各位点频率p，得到中心化矩阵 $Z=M-2p$。一种常用缩放为：

$$s=\sum_j2p_j(1-p_j),\qquad K=ZZ^\mathsf T/s.$$

这里K表示基因组关系矩阵，其他文章常记为G。训练集单态位点应剔除；缺失值处理和等位基因顺序要固定。此处采用训练集基准；实际遗传评估可能采用另外定义的参考频率，需明确记录，不能每批候选自行重算后混用。

## 个体模型与标记模型

GBLUP设 $y=Xb+u+e$，$u\sim N(0,K\sigma_u^2)$，$e\sim N(0,I\sigma_e^2)$。设 $\lambda_G=\sigma_e^2/\sigma_u^2$，已知此比值时可写：

$$A=K+\lambda_GI,$$
$$\hat b=(X^\mathsf TA^{-1}X)^{-1}X^\mathsf TA^{-1}y,$$
$$\alpha=A^{-1}(y-X\hat b),\qquad \hat u_*=K_{*,t}\alpha.$$

星号表示候选个体，t表示训练集。教学代码只使用截距；多协变量时X必须列满秩，候选集还需提供对应固定效应才能预测完整表型。

RR-BLUP把遗传值写成 $u=Za$，假设标记效应独立且共享方差。与上述K匹配时，标记岭回归惩罚应为 $\lambda_a=s\lambda_G$：

$$\hat a=(Z^\mathsf TZ+s\lambda_GI)^{-1}Z^\mathsf T(y-X\hat b).$$

因此 $\hat u_*=Z_*\hat a$ 与GBLUP相同。等价性要求相同的中心化、标记权重、固定效应、样本和方差尺度。仅把两个软件的“lambda”填成同一个数，并不能保证相同模型。

## 收缩如何起作用

样本少、标记多时，无惩罚的标记效应不稳定。岭惩罚把每个标记效应向零收缩，以降低方差。较大lambda通常收缩更强；该参数可以由REML估计方差比，也可在训练集内部交叉验证选择。两者目标与数值可能不同。

## 实现要点与已验证内容

代码见[genomic_prediction_demo.py](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/genomic_prediction_demo.py)。实现用线性方程求解器，不显式求大矩阵逆；候选样本沿用训练中心、保留位点和标记顺序。程序实际比较了两条计算路径，最大预测差约 $1.0\times10^{-15}$，属于浮点误差范围。

此代码使用正lambda，未估计REML，也没有输出PEV。不要从等价性测试推断两个完整软件所有默认设置等价。数学与软件入口：[VanRaden方法](https://pubmed.ncbi.nlm.nih.gov/18946147/)、[rrBLUP预测实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/rrBLUP%E9%A2%84%E6%B5%8B%E5%AE%9E%E8%B7%B5)。验证设计见[GS训练验证与数据泄漏](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GS%E8%AE%AD%E7%BB%83%E9%AA%8C%E8%AF%81%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%B3%84%E6%BC%8F)。
