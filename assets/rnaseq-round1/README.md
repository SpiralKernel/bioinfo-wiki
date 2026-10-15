# 公开airway真实计数案例结果

本目录为原生R4.4.3、DESeq2 1.46.0、airway1.26.0、apeglm1.28.0实际执行后的汇总、top50预览、样本/设计/QC/PCA表与诊断图。数据为公开计数对象，不是本轮从FASTQ重新生成。未验证原论文的所有生物学结论。

完整计数、模型RDS、标准化矩阵与全部差异表保留于忽略的examples/output，读者用脚本从固定airway包重建。provenance记录实际RData、导出输入和完整结果SHA；top50不是完整检验集合或富集背景。公开sample_id均为原公开数据的运行编号。

session-info仅将本机R环境绝对路径替换为<R_ENV>，保留版本和BLAS等信息。linux-conda-packages/explicit记录本机精确构建；读者常规安装使用examples/environments/rnaseq.yml，精确Linux记录不保证其他系统可用。

诊断图PCA使用VST、高变异基因，标签是SRR10395后的尾号，形状对应cell、颜色对应dex。MA边界三角表示超出图示范围，完整数值仍在结果中；火山图横轴原始LFC、纵轴原始Wald P，显著颜色由padj定义。基础R表格脚本也已在同一原生R实际运行。

见[维护记录](../../maintenance/rnaseq-round1-2026-10-15.md)。
