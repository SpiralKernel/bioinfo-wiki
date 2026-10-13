# GS算法软件与实践路线

> 更新：2026-10-13；状态：可用；验证范围：路线与官方资料核对；NumPy教学案例已运行；六种专业软件尚未在本机运行。

从育种值和验证设计出发，连接GBLUP、贝叶斯模型、单步法与六种软件指南。

## 先明确预测对象

GS（genomic selection，基因组选择）利用基因组信息预测遗传价值，再服务于选择决策。本文主要讨论数量性状的加性遗传预测。生产上还要考虑多性状目标、近交、成本与配种设计；预测一列分数并不等于完成育种决策。

先读[基因组选择与GWAS的区别](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%80%89%E6%8B%A9%E4%B8%8EGWAS%E7%9A%84%E5%8C%BA%E5%88%AB)和[育种值GEBV准确度与可靠度](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%82%B2%E7%A7%8D%E5%80%BCGEBV%E5%87%86%E7%A1%AE%E5%BA%A6%E4%B8%8E%E5%8F%AF%E9%9D%A0%E5%BA%A6)。已有GWAS经验的人尤其要调整检查重点：从显著位点和P值，转向候选个体、预测能力、偏差及部署时能够获得的信息。

## 推荐学习顺序

1. 理解[亲缘关系与遗传关系矩阵](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%B2%E7%BC%98%E5%85%B3%E7%B3%BB%E4%B8%8E%E9%81%97%E4%BC%A0%E5%85%B3%E7%B3%BB%E7%9F%A9%E9%98%B5)，能够区分基因型矩阵、系谱矩阵A与基因组关系矩阵G。
2. 学习[GBLUP与rrBLUP原理及实现](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GBLUP%E4%B8%8ErrBLUP%E5%8E%9F%E7%90%86%E5%8F%8A%E5%AE%9E%E7%8E%B0)，知道个体效应与标记效应为什么可以给出相同预测。
3. 阅读[GS训练验证与数据泄漏](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GS%E8%AE%AD%E7%BB%83%E9%AA%8C%E8%AF%81%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%B3%84%E6%BC%8F)，先定义要预测同家系后代、新家系还是下一世代。
4. 运行[合成家系数据贯通GS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E5%AE%B6%E7%B3%BB%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9AGS)，从数据对齐、嵌套验证走到60个候选个体的预测。
5. 选择软件复现基线，再学习[贝叶斯回归与核方法用于GS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%B4%9D%E5%8F%B6%E6%96%AF%E5%9B%9E%E5%BD%92%E4%B8%8E%E6%A0%B8%E6%96%B9%E6%B3%95%E7%94%A8%E4%BA%8EGS)或[系谱BLUP与单步ssGBLUP](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%B3%BB%E8%B0%B1BLUP%E4%B8%8E%E5%8D%95%E6%AD%A5ssGBLUP)。
6. 需要解释方差估计和大矩阵求解时，读[GS中的REML混合模型方程与求解](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GS%E4%B8%AD%E7%9A%84REML%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B%E6%96%B9%E7%A8%8B%E4%B8%8E%E6%B1%82%E8%A7%A3)。

## 软件怎样选择

| 软件与指南 | 适合学习或分析的问题 | 需要额外关注什么 | 本项目验证 |
|---|---|---|---|
| [rrBLUP预测实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/rrBLUP%E9%A2%84%E6%B5%8B%E5%AE%9E%E8%B7%B5) | 单个遗传随机效应、RR-BLUP/GBLUP基线 | 编码、关系矩阵与REML结果 | 文档与R模板，未运行R |
| [BGLR贝叶斯预测实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BGLR%E8%B4%9D%E5%8F%B6%E6%96%AF%E9%A2%84%E6%B5%8B%E5%AE%9E%E8%B7%B5) | 不同标记先验、多核预测 | MCMC收敛、先验和链间一致性 | 文档与R模板，未运行R |
| [sommer基因组预测与复杂设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/sommer%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%A2%84%E6%B5%8B%E4%B8%8E%E5%A4%8D%E6%9D%82%E8%AE%BE%E8%AE%A1) | 多随机效应、多性状和试验设计 | 版本接口、方差可识别性 | 文档与R模板，未运行R |
| [HIBLUP基因组预测实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/HIBLUP%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%A2%84%E6%B5%8B%E5%AE%9E%E8%B7%B5) | 命令行的基因组与系谱遗传评估 | 输入格式、缺失基因型、方差参数 | 官方命令模板，未运行 |
| [BLUPF90单步遗传评估流程](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLUPF90%E5%8D%95%E6%AD%A5%E9%81%97%E4%BC%A0%E8%AF%84%E4%BC%B0%E6%B5%81%E7%A8%8B) | 结合系谱、基因型及未分型亲属的ssGBLUP | 编号转换、A/G兼容和参数文件 | 官方流程，未运行 |
| [ASReml基因组预测接口](https://github.com/SpiralKernel/bioinfo-wiki/wiki/ASReml%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%A2%84%E6%B5%8B%E6%8E%A5%E5%8F%A3) | 已采用ASReml的复杂混合模型项目 | 授权、已知协方差和预测量定义 | 官方接口模板，未运行 |

软件选择依据模型和数据设计，不依据软件名称的流行程度。单性状线性基线、贝叶斯模型、单步评估解决的问题存在交集，也各有额外假设。各软件应在同一外层划分、同一表型定义与同一指标下比较。

## 已经提供的操作路径

[GS数据准备与候选个体预测](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GS%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87%E4%B8%8E%E5%80%99%E9%80%89%E4%B8%AA%E4%BD%93%E9%A2%84%E6%B5%8B)说明真实项目应准备什么；[合成家系数据贯通GS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E5%AE%B6%E7%B3%BB%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9AGS)提供本项目实际运行的NumPy教学实现和图。教学代码验证GBLUP与标记岭回归的等价性，并比较随机个体划分与家系留出。它没有实现REML、MCMC或ssGBLUP，不能替代生产软件。

## 维护方式

术语解释在概念页维护，软件页只补充接口差异。每增加一种模型，至少补齐输入、训练方式、超参数、验证设计、输出定义和失败检查。软件更新后优先复查接口、缺失值处理及矩阵缩放；未运行的命令保持明确标记。

原始方法入口：[Meuwissen等的基因组选择论文](https://research.wur.nl/en/publications/prediction-of-total-genetic-value-using-genome-wide-dense-marker-/)、[VanRaden的基因组关系矩阵方法](https://pubmed.ncbi.nlm.nih.gov/18946147/)。


## 统计基础与验证入口

[统计学与组学验证学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%9F%E8%AE%A1%E5%AD%A6%E4%B8%8E%E7%BB%84%E5%AD%A6%E9%AA%8C%E8%AF%81%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)补充本任务所需的统计或验证判断。分析前先确认[统计方法选择与分析计划](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%9F%E8%AE%A1%E6%96%B9%E6%B3%95%E9%80%89%E6%8B%A9%E4%B8%8E%E5%88%86%E6%9E%90%E8%AE%A1%E5%88%92)，结果解释时区分[组学验证的层级与证据](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E9%AA%8C%E8%AF%81%E7%9A%84%E5%B1%82%E7%BA%A7%E4%B8%8E%E8%AF%81%E6%8D%AE)。
