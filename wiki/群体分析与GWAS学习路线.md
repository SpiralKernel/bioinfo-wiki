# 群体分析与GWAS学习路线

> 更新：2026-10-13；状态：可用；验证范围：文档核对；操作需按所用环境验证。

从基因型编码和样本审计出发，依次完成群体探索、关联分析和证据解释。

## 建议顺序

1. [SNP与基因型是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SNP%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%98%AF%E4%BB%80%E4%B9%88)、[VCF与基因型编码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E7%BC%96%E7%A0%81)：确认位点、倍性、缺失和计数等位基因。
2. [样本表与数据审计实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%A0%B7%E6%9C%AC%E8%A1%A8%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%AE%A1%E8%AE%A1%E5%AE%9E%E8%B7%B5)、[基因型质控与过滤](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E5%9E%8B%E8%B4%A8%E6%8E%A7%E4%B8%8E%E8%BF%87%E6%BB%A4)：核对个体身份、缺失率、频率和筛选记录。
3. [连锁不平衡与LD剪枝](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BF%9E%E9%94%81%E4%B8%8D%E5%B9%B3%E8%A1%A1%E4%B8%8ELD%E5%89%AA%E6%9E%9D)、[亲缘关系与遗传关系矩阵](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%B2%E7%BC%98%E5%85%B3%E7%B3%BB%E4%B8%8E%E9%81%97%E4%BC%A0%E5%85%B3%E7%B3%BB%E7%9F%A9%E9%98%B5)：理解位点冗余和样本相关性。
4. [群体结构是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E6%98%AF%E4%BB%80%E4%B9%88)、[用PCA探索样本的群体结构](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%A8PCA%E6%8E%A2%E7%B4%A2%E6%A0%B7%E6%9C%AC%E7%9A%84%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84)：检查整体差异与技术因素。
5. [群体结构与GWAS有什么关系](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E4%B8%8EGWAS%E6%9C%89%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB)、[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)：确定表型和协变量所对应的模型。
6. [GWAS从数据准备到结果解释](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E4%BB%8E%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87%E5%88%B0%E7%BB%93%E6%9E%9C%E8%A7%A3%E9%87%8A)：检查结果表、效应方向、多重检验及候选区域。

## 第一个可运行练习

运行[合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)。它只依赖 Python 和 PLINK 2，用人工生成的数据熟悉文件之间的连接。随后替换为自己的数据时，重新审查染色体设置、倍性、亲缘关系、表型类型及阈值，不能直接继承练习里的选择。

## 学完后的自检

能否追溯每个效应值计数哪种等位基因？PCA 用了哪些位点？表型和协变量如何与样本对齐？一个显著位点与因果变异之间还缺少什么证据？

深入查看 [PLINK 2 输入说明](https://www.cog-genomics.org/plink/2.0/input)、[关联模型文档](https://www.cog-genomics.org/plink/2.0/assoc)和 [GEMMA 原始论文](https://doi.org/10.1038/ng.2310)。
