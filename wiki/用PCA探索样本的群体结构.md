# 用PCA探索样本的群体结构

> 更新：2026-10-13；验证范围：合成数据实测。

从经过质控的基因型出发，减少位点冗余、计算主成分，并结合样本信息检查结果。

## 输入和准备

需要 `qc.pgen/.pvar/.psam` 以及带唯一 ID 的样本表。先理解[群体结构是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E6%98%AF%E4%BB%80%E4%B9%88)、[PCA原理与实现](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PCA%E5%8E%9F%E7%90%86%E4%B8%8E%E5%AE%9E%E7%8E%B0)和[连锁不平衡与LD剪枝](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BF%9E%E9%94%81%E4%B8%8D%E5%B9%B3%E8%A1%A1%E4%B8%8ELD%E5%89%AA%E6%9E%9D)。下面命令在[合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)中已实测。

## 1. 生成并应用剪枝名单

```bash
plink2 --pfile qc --indep-pairwise 50 5 0.2 --out prune
plink2 --pfile qc --extract prune.prune.in --pca 5 --out pca
```

这是位点数窗口的教学选择。运行前记录质控口径和物种染色体设置。运行后检查名单不为空、位点 ID 唯一、实际进入 PCA 的位点数及样本数符合预期。

## 2. 按ID连接样本信息

`.eigenvec` 保存样本坐标，`.eigenval` 保存对应特征值。读取时核对标题行里的 FID/IID 规则，按实际 ID 列合并元数据，不能仅按行顺序贴上分组。重复或未匹配 ID 应先解决，见[样本表与数据审计实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%A0%B7%E6%9C%AC%E8%A1%A8%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%AE%A1%E8%AE%A1%E5%AE%9E%E8%B7%B5)。

## 3. 绘图和判断

先画 PC1 对 PC2，再看其他轴。分别按群体来源、批次、性别、缺失率与家系标记，比较是否出现技术因素或亲缘驱动的分离。查异常点时回看原始记录，不能只因“离群”就删除样本。

PCA 坐标轴正负号不影响相同轴上的相对关系；二维分离不能直接证明独立群体或祖源比例。若只计算五个特征值，不能简单用其和作为全部方差分母。

## 4. 交接到GWAS

保存位点名单、频率口径、样本 ID、工具版本、完整命令和图。选择 PC 协变量要结合设计和诊断，见[群体结构与GWAS有什么关系](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E4%B8%8EGWAS%E6%9C%89%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB)。

深入：[PLINK PCA 与投影说明](https://www.cog-genomics.org/plink/2.0/strat)、[PCA 实践方法论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC7750941/)。
