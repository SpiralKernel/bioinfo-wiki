# LOCO与近端污染

> 更新：2026-10-13；状态：可用；验证范围：文档核对；公开小鼠第17号染色体的GEMMA背景排除对照实测，未做完整全基因组LOCO。

LOCO在检验某条染色体时把它排除出背景遗传表示，以减少局部信号被背景模型吸收。

## 同一信号为什么可能被调整掉

若待检验位点及其LD邻域同时参与构建GRM或背景预测，部分局部信号可能先被随机效应或预测部分吸收，再用于当前位点检验。这种近端污染可能降低检验效能，程度与模型、位点选择和遗传结构有关。

LOCO的做法是：检验第c条染色体时，背景矩阵或预测只用其他染色体；逐条染色体更换对应背景。它是减少局部信号进入背景的一种设计，并不自动解决所有群体结构和模型失配。

## 不同软件怎样表达

GCTA有MLMA-LOCO模块；REGENIE在两步流程中产生按染色体区分的LOCO预测；SAIGE某些配置使用LOCO，但稀疏GRM拟合的配置并不与完整GRM模式完全相同。具体行为应绑定版本与模型，不能认为任何软件中出现LOCO参数就执行了一模一样的过程。

它与leave-one-out交叉验证（LOOCV）不同：后者通常按观测样本留出；这里留出的是染色体上的遗传信息。REGENIE建模中的交叉验证与LOCO也分别承担不同职责。

## 已运行的单条染色体对照

在[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)中，我们另外使用第17号染色体之外的位点建立GEMMA标准化GRM，再只检验第17号染色体。样本、表型、PC和待检验位点保持对应，用于观察背景定义变化的影响。

这个练习只验证一条染色体的对照，不是已经完成全基因组LOCO。单条染色体的P值分布也不能直接作为全基因组QQ校准评价。实际数值与图见[GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)。

## 需要保留什么

记录测试染色体、建模位点名单、样本顺序、GRM或预测文件对应。用单一“排除17”的矩阵检验其他所有染色体，不构成完整LOCO。若按染色体分任务，命令、矩阵和输出命名应能直接追溯。

深入：[REGENIE LOCO方法说明](https://rgcgithub.github.io/regenie/overview/)、[GCTA官方手册](https://yanglab.westlake.edu.cn/software/gcta)、[SAIGE两步配置](https://saigegit.github.io/SAIGE-doc/docs/single_step1.html)。
