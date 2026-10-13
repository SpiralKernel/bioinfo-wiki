# GWAS软件选择与比较

> 更新：2026-10-13；状态：可用；验证范围：选型资料核对；贯穿案例实测PLINK、GEMMA、GCTA及REGENIE，其他软件未执行。

先根据性状、样本相关性、物种和数据规模选择模型，再选择能够实现并验证它的软件。

## 先分清软件、模型与分析任务

PLINK、GEMMA和GCTA是软件；普通回归、线性混合模型和逻辑混合模型是模型类别；FarmCPU与BLINK是可在不同工具中实现的方法。软件名字相同不代表运行了同一模型，模型简称相同也不代表默认设置相同。GAPIT与TASSEL中的GLM通常指general linear model；PLINK的`--glm`按性状调用线性、逻辑或Firth等回归。

这个专题覆盖个体水平的单变异关联主线，并说明多位点和基因集合分析的接口。汇总统计Meta分析、精细定位和基因组预测有不同输入与目标，不应与一次普通GWAS混为一谈。

## 写下五个选型条件

1. 性状是连续值、病例对照、计数，还是生存时间？能否使用当前模型的分布假设？
2. 样本是否包含家系、近亲、群体分层或重复测量？PC与GRM各解决什么？
3. 研究物种、倍性和染色体编码是什么？软件是否对该设计有依据？
4. 建模位点与待检验位点分别有多少？输入是硬基因型还是剂量？
5. 是否需要多个性状、罕见变异集合检验或大规模分批计算？

先读[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)、[二分类性状OR与病例对照不平衡](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%8C%E5%88%86%E7%B1%BB%E6%80%A7%E7%8A%B6OR%E4%B8%8E%E7%97%85%E4%BE%8B%E5%AF%B9%E7%85%A7%E4%B8%8D%E5%B9%B3%E8%A1%A1)和[MAF与MAC及稀有变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/MAF%E4%B8%8EMAC%E5%8F%8A%E7%A8%80%E6%9C%89%E5%8F%98%E5%BC%82)。连续性状也要审查量纲、离群、变换和[关联模型中的协变量与残差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%B3%E8%81%94%E6%A8%A1%E5%9E%8B%E4%B8%AD%E7%9A%84%E5%8D%8F%E5%8F%98%E9%87%8F%E4%B8%8E%E6%AE%8B%E5%B7%AE)。

## 软件与场景对照

| 软件或模块 | 主要思路与常见入口 | 选择时必须核对 | 详细说明 |
|---|---|---|---|
| PLINK 2 | 每个位点的线性或逻辑/Firth回归；同时负责大量质控任务 | 常规`--glm`不建模家系GRM | [PLINK2关联分析详解](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PLINK2%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E8%AF%A6%E8%A7%A3) |
| GEMMA | 稠密亲缘矩阵的LM/LMM；另有多性状与BSLMM任务 | 矩阵定义、样本顺序、截距与检验类型 | [GEMMA线性混合模型实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GEMMA%E7%BA%BF%E6%80%A7%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B%E5%AE%9E%E8%B7%B5) |
| GCTA MLMA | 以稠密GRM做混合模型关联；另有LOCO模块 | GRM与关联样本、PC、方差组分与LOCO设置 | [GCTA与MLMA关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GCTA%E4%B8%8EMLMA%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90) |
| GCTA fastGWA | 稀疏GRM与快速近似；GLMM模块用于二分类 | 稀疏化依据、模块差别、是否真正使用GRM | [fastGWA与fastGWA-GLMM](https://github.com/SpiralKernel/bioinfo-wiki/wiki/fastGWA%E4%B8%8EfastGWA-GLMM) |
| REGENIE | 两步全基因组回归与LOCO预测，再做关联 | 两步文件对应；性状、校正、建模位点质量 | [REGENIE两步关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/REGENIE%E4%B8%A4%E6%AD%A5%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90) |
| SAIGE | 零混合模型与单变异得分检验；二分类使用SPA | 病例对照计数、MAC、收敛与方差比；集合检验另有流程 | [SAIGE单变异关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SAIGE%E5%8D%95%E5%8F%98%E5%BC%82%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90) |
| BOLT-LMM | 面向较大人类队列的高效混合模型关联 | 官方样本规模与物种适用说明、LD资源及病例对照平衡 | [BOLT-LMM关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BOLT-LMM%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90) |
| EMMAX | 在零模型估计方差后快速检验位点 | 旧格式、显式截距、顺序、编码与版本 | [EMMAX关联分析与旧流程兼容](https://github.com/SpiralKernel/bioinfo-wiki/wiki/EMMAX%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E4%B8%8E%E6%97%A7%E6%B5%81%E7%A8%8B%E5%85%BC%E5%AE%B9) |
| GAPIT | R中的多模型接口，包括MLM、FarmCPU、BLINK等 | 具体模型、参数、数据对齐与选择过程 | [GAPIT多模型GWAS实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GAPIT%E5%A4%9A%E6%A8%A1%E5%9E%8BGWAS%E5%AE%9E%E8%B7%B5) |
| TASSEL | GUI与命令行中的GLM/MLM及遗传数据处理 | taxa交集、群体结构协变量、亲缘矩阵及输出检验 | [TASSEL关联分析实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/TASSEL%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E5%AE%9E%E8%B7%B5) |
| rMVP | 内存映射与并行的GLM/MLM/FarmCPU | 转换后的样本顺序、协变量顺序、外存文件完整性 | [rMVP关联分析实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/rMVP%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E5%AE%9E%E8%B7%B5) |

GCTA在表中按模块分行，其余也不是“一套软件只做一种模型”。这些工具没有跨场景通用的名次，不能以显著位点最多或QQ图最贴线来决定胜负。

## 给入门学生的三条路径

**理解输入输出**：先做[合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)，再读PLINK详细页。

**学习家系与数量性状**：做[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)，在同一样本上比较普通回归、PC调整及GRM模型。GEMMA与GCTA适合在本案例中学习；REGENIE的小数据运行只验证接口，不推导出它适合所有育种家系。

**研究大队列或不平衡二分类**：阅读SAIGE、REGENIE、fastGWA-GLMM及BOLT的适用范围，先跑所选版本的官方测试，再在自己的设计中诊断。不能因有二分类标签就把任意LMM输出当作OR。

## 怎样公平比较

固定研究问题、分析个体、位点、性状变换、协变量和计数方向；再比较相同检验或明确解释模型差别。详细步骤见[GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)，交接见[GWAS软件输入转换与样本对齐](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E8%BE%93%E5%85%A5%E8%BD%AC%E6%8D%A2%E4%B8%8E%E6%A0%B7%E6%9C%AC%E5%AF%B9%E9%BD%90)及[GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80)。

本专题对PLINK、GEMMA、GCTA（MLMA及fastGWA数量性状）和REGENIE有公开数据实测。SAIGE、BOLT、EMMAX和R/Java工具按官方资料编写，未在本机执行；每页标明范围。

深入入口：[PLINK关联文档](https://www.cog-genomics.org/plink/2.0/assoc)、[GCTA官方手册](https://yanglab.westlake.edu.cn/software/gcta)、[REGENIE概览](https://rgcgithub.github.io/regenie/overview/)、[SAIGE官方文档](https://saigegit.github.io/SAIGE-doc/)。
