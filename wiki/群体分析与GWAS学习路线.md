# 群体分析与GWAS学习路线

> 更新：2026-10-14；状态：可用；验证范围：文档核对；操作需按所用环境验证。

从基因型编码和样本审计出发，依次完成群体探索、关联分析和证据解释。

## 建议顺序

1. [SNP与基因型是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SNP%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%98%AF%E4%BB%80%E4%B9%88)、[VCF与基因型编码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E7%BC%96%E7%A0%81)：确认位点、倍性、缺失和计数等位基因。
2. [样本表与数据审计实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%A0%B7%E6%9C%AC%E8%A1%A8%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%AE%A1%E8%AE%A1%E5%AE%9E%E8%B7%B5)、[基因型质控与过滤](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E5%9E%8B%E8%B4%A8%E6%8E%A7%E4%B8%8E%E8%BF%87%E6%BB%A4)：核对个体身份、缺失率、频率和筛选记录。
3. [连锁不平衡与LD剪枝](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BF%9E%E9%94%81%E4%B8%8D%E5%B9%B3%E8%A1%A1%E4%B8%8ELD%E5%89%AA%E6%9E%9D)、[亲缘关系与遗传关系矩阵](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%B2%E7%BC%98%E5%85%B3%E7%B3%BB%E4%B8%8E%E9%81%97%E4%BC%A0%E5%85%B3%E7%B3%BB%E7%9F%A9%E9%98%B5)：理解位点冗余和样本相关性。
4. [群体结构是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E6%98%AF%E4%BB%80%E4%B9%88)、[用PCA探索样本的群体结构](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%A8PCA%E6%8E%A2%E7%B4%A2%E6%A0%B7%E6%9C%AC%E7%9A%84%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84)：检查整体差异与技术因素。
5. [群体结构与GWAS有什么关系](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E4%B8%8EGWAS%E6%9C%89%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB)、[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)：确定表型和协变量所对应的模型。
6. [GWAS软件选择与比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E9%80%89%E6%8B%A9%E4%B8%8E%E6%AF%94%E8%BE%83)：按性状、家系、物种与规模选择软件及模块。
7. [GWAS从数据准备到结果解释](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E4%BB%8E%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87%E5%88%B0%E7%BB%93%E6%9E%9C%E8%A7%A3%E9%87%8A)与[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)：运行并核对结果。
8. [GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)、[GWAS曼哈顿图QQ图与膨胀因子](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E6%9B%BC%E5%93%88%E9%A1%BF%E5%9B%BEQQ%E5%9B%BE%E4%B8%8E%E8%86%A8%E8%83%80%E5%9B%A0%E5%AD%90)：先对齐相同模型，再解释背景差别。

## 第一个可运行练习

运行[合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)。它只依赖 Python 和 PLINK 2，用人工生成的数据熟悉文件之间的连接。随后替换为自己的数据时，重新审查染色体设置、倍性、亲缘关系、表型类型及阈值，不能直接继承练习里的选择。

## 深入实践与排错

[GWAS软件输入转换与样本对齐](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E8%BE%93%E5%85%A5%E8%BD%AC%E6%8D%A2%E4%B8%8E%E6%A0%B7%E6%9C%AC%E5%AF%B9%E9%BD%90) → [GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80) → [GWAS参数选择与敏感性分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E5%8F%82%E6%95%B0%E9%80%89%E6%8B%A9%E4%B8%8E%E6%95%8F%E6%84%9F%E6%80%A7%E5%88%86%E6%9E%90)。报错时查[GWAS常见报错与排查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E5%B8%B8%E8%A7%81%E6%8A%A5%E9%94%99%E4%B8%8E%E6%8E%92%E6%9F%A5)；模型前置查[零模型与方差组分](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%9B%B6%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BB%84%E5%88%86)、[LOCO与近端污染](https://github.com/SpiralKernel/bioinfo-wiki/wiki/LOCO%E4%B8%8E%E8%BF%91%E7%AB%AF%E6%B1%A1%E6%9F%93)和[二分类性状OR与病例对照不平衡](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%8C%E5%88%86%E7%B1%BB%E6%80%A7%E7%8A%B6OR%E4%B8%8E%E7%97%85%E4%BE%8B%E5%AF%B9%E7%85%A7%E4%B8%8D%E5%B9%B3%E8%A1%A1)。

## 学完后的自检

能否追溯每个效应值计数哪种等位基因？PCA 用了哪些位点？表型和协变量如何与样本对齐？一个显著位点与因果变异之间还缺少什么证据？

深入查看 [PLINK 2 输入说明](https://www.cog-genomics.org/plink/2.0/input)、[关联模型文档](https://www.cog-genomics.org/plink/2.0/assoc)和 [GEMMA 原始论文](https://doi.org/10.1038/ng.2310)。

## 从关联分析走向预测

若下一步是预测候选个体的遗传价值，进入[GS算法软件与实践路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GS%E7%AE%97%E6%B3%95%E8%BD%AF%E4%BB%B6%E4%B8%8E%E5%AE%9E%E8%B7%B5%E8%B7%AF%E7%BA%BF)。先区分[基因组选择与GWAS的区别](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%80%89%E6%8B%A9%E4%B8%8EGWAS%E7%9A%84%E5%8C%BA%E5%88%AB)，再做符合实际候选群体的验证；GWAS显著性不替代预测表现。

## 遗传变异模式与过程

本路线以性状关联为主。若问题是多样性、群体分化、近交、选择或历史，转入[群体遗传学分析学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E9%81%97%E4%BC%A0%E5%AD%A6%E5%88%86%E6%9E%90%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)。两类任务的样本、频率筛选及LD处理目的不同，不应复用同一套过滤结果而不审查。

## 如果还没有基因型

已有VCF/PLINK输入可继续本路线；只有FASTQ/BAM时，先按[变异检测分型与提取学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E5%88%86%E5%9E%8B%E4%B8%8E%E6%8F%90%E5%8F%96%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)生成并核查对应变异。不同类型的分型/剂量、缺失和样本对齐不能一律视为二倍体SNP矩阵。
