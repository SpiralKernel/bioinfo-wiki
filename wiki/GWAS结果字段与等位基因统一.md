# GWAS结果字段与等位基因统一

> 更新：2026-10-13；状态：可用；验证范围：公开小鼠七种配置结果字段、52个位点方向翻转与同模型一致性实测。

跨软件结果表先统一位点、效应方向、性状尺度和P值表示，再比较统计量。

## 建议保留的统一字段

至少包括研究/性状、软件与模型、检验类型、组装、染色体、位置、ID、效应等位基因EA、另一等位基因OA、效应频率EAF、BETA、SE、样本信息、P或−log10(P)、质量与失败标记。保留原始表，统一表不能抹去来源。

本轮脚本只转换固定案例的几种输出，并严格拒绝样本、位置或等位基因不匹配；它不是适用于任意研究的自动Meta分析清洗器。

## 常见输出映射

| 输出 | 效应与频率 | 证据与样本 |
|---|---|---|
| PLINK 2 | A1、OMITTED、A1_FREQ、BETA、SE | P、TEST、OBS_CT、ERRCODE；特殊log10选项需另处理 |
| GEMMA | allele1、allele0、af、beta、se | p_wald/p_lrt/p_score按所选模式；观测/缺失列随模式不同 |
| GCTA MLMA | A1、A2、Freq、b、se | p；N需结合实际分析与缺失记录 |
| fastGWA数量性状 | A1、A2、AF1、BETA、SE | P、N |
| REGENIE本例 | ALLELE1、ALLELE0、A1FREQ、BETA、SE | LOG10P为−log10(P)，另保留TEST与N |

其他工具先读对应详细页与版本手册。没有等位基因的结果表，应回到输入映射补齐，而不是根据次要频率猜字符。

## 翻转方向时怎样变换

双等位加性模型中，若只把计数从A换为G，且样本和模型相同：β变号，EAF变为1−EAF，SE及同一双侧检验的P不变。逻辑模型还对应OR取倒数，但SE通常应在log-OR尺度处理。

例如A方向β=0.2、EAF=0.3，G方向应为β=−0.2、EAF=0.7。不能只交换EA/OA字符而不改β与频率。

## 不能自动解决的情况

A/T与C/G回文位点在链方向不明时，仅凭字符无法消歧；其他链互补也需要参考、频率与原始编码证据。坐标组装不同、多等位拆分、性状标准化不同或病例标签颠倒，均不是一个简单翻转就能修复。

等位基因频率的输出精度也可能不同。本例GEMMA的af显示精度低于PLINK，轻微差别不一定来自个体集合变化。参考身份在BED来源中可能只是暂定，需要额外核验。

## 本例为何需要这一步

在8544个共同位点中，GEMMA、GCTA与REGENIE各有52个输出方向与PLINK当前A1相反。统一后，PLINK PC3与GEMMA LM的最大绝对β差约5×10⁻⁷，−log10(P)最大差约2.16×10⁻⁶，符合打印精度。

相同模型的一致性是交接检查；换成LMM或其他方法后的P值差异，应回到背景、估计和检验解释，不继续“修正”到相同结果。

代码：[规范化与比较脚本](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/plot_gwas_comparison.py)。前置：[SNP与基因型是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SNP%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%98%AF%E4%BB%80%E4%B9%88)、[二分类性状OR与病例对照不平衡](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%8C%E5%88%86%E7%B1%BB%E6%80%A7%E7%8A%B6OR%E4%B8%8E%E7%97%85%E4%BE%8B%E5%AF%B9%E7%85%A7%E4%B8%8D%E5%B9%B3%E8%A1%A1)。深入：[PLINK关联输出](https://www.cog-genomics.org/plink/2.0/assoc)、[REGENIE文档](https://rgcgithub.github.io/regenie/options/)。
