# GWAS软件结果比较与一致性检查

> 更新：2026-10-13；状态：可用；验证范围：公开小鼠七种配置及chr17对照实测；不是跨场景性能、功效或错误控制基准。

先用同一模型检查软件交接，再解释不同模型的结果；单一数据集的显著数量不构成软件排名。

## 固定什么才能开始比较

固定分析个体、基因型/剂量、性状与变换、位点集合、协变量、计数方向以及检验类型。记录GRM或背景预测的构建规则与缺失处理。对不同模型的比较，明确哪些因素本来就不同。

本轮数据与运行方式见[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)；全部主要配置用1410个个体与8544个共同位点，PC调整配置使用同一组三个PC。

## 第一关：相同普通LM能否对齐

PLINK PC3与GEMMA LM经过[GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80)后，效应与P值接近到输出精度。52个位点翻转计数方向后才可直接比较。若这一关不通过，先检查样本顺序、协变量截距、表型列与编码，不急于解释软件优劣。

![QQ诊断与普通LM一致性](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/gwas-round2/qq-and-lm-check.png)

图：左侧为本例七种配置的QQ分布；右侧为同模型、同计数方向的β。PLINK PC3与GEMMA LM曲线接近重合。λ仅为诊断指标，不是校准或功效排名。

## 第二关：不同背景如何改变结果

| 本例配置 | λGC约值 | Bonferroni阈值下位点数 |
|---|---:|---:|
| PLINK无PC | 22.47 | 2633 |
| PLINK PC3 | 6.57 | 681 |
| GEMMA LM PC3 | 6.57 | 681 |
| GEMMA LMM PC3 | 0.78 | 20 |
| GCTA MLMA PC3 | 0.77 | 19 |
| GCTA fastGWA PC3 | 1.09 | 32 |
| REGENIE PC3两步 | 2.02 | 69 |

门槛为0.05/8544≈5.85×10⁻⁶。这里计的是位点，不是独立区域或因果机制。家系、LD、真实信号、背景近似和近端污染都会影响分布；不能凭“最接近1”或“显著最多”给方法排名。

尤其是REGENIE完成本例运行不代表已验证其适合小样本育种家系，也不代表它在大规模人类队列中表现如此。

## 第三关：检查背景排除对照

![第17号染色体背景对照](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/gwas-round2/chr17-loco.png)

仅对第17号染色体做GEMMA对照：用其余染色体建立K，再检验同一条染色体的288个位点。rs6249614的P从全基因组GRM时约6.73×10⁻¹⁵变为约1.31×10⁻²⁸，同时SE发生变化。

这说明背景定义会影响检验，符合检查[LOCO与近端污染](https://github.com/SpiralKernel/bioinfo-wiki/wiki/LOCO%E4%B8%8E%E8%BF%91%E7%AB%AF%E6%B1%A1%E6%9F%93)的目的；它不独立证明哪一种结果是真实机制，也不是全基因组LOCO实测。

## 最后应交付什么

保留共同位点表、对齐规则、失败与排除列表、版本和命令、效应散点、QQ与局部区域解释。若做严谨方法评估，还需合适的无效与有效模拟、独立数据或预定验证设计；本例不提供这种全面基准。

原始方法与参数见[GEMMA线性混合模型实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GEMMA%E7%BA%BF%E6%80%A7%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B%E5%AE%9E%E8%B7%B5)、[GCTA与MLMA关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GCTA%E4%B8%8EMLMA%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)、[REGENIE两步关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/REGENIE%E4%B8%A4%E6%AD%A5%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)。统计边界见[GWAS曼哈顿图QQ图与膨胀因子](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E6%9B%BC%E5%93%88%E9%A1%BF%E5%9B%BEQQ%E5%9B%BE%E4%B8%8E%E8%86%A8%E8%83%80%E5%9B%A0%E5%AD%90)。
