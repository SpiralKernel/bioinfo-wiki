# DESeq2安装对象与结果提取

> 更新：2026-10-15；状态：可用；验证范围：原生R与公开airway计数案例已执行；范围和结果见正文。

在匹配的R与Bioconductor环境中安装DESeq2，区分数据对象、模型拟合、对比和导出。

## 安装与载入

本轮用隔离Conda环境固定R4.4.3、DESeq2 1.46.0、airway1.26.0与apeglm1.28.0实际运行；这是复跑版本，不宣称最新。项目提供examples/environments/rnaseq.yml：

```bash
conda env create -f examples/environments/rnaseq.yml
conda run -n wiki-rnaseq Rscript examples/rnaseq_airway_demo.R
```

Linux本机安装已测，其他平台需核对渠道可用性。已有原生R可按[Bioconductor安装说明](https://bioconductor.org/install/)用BiocManager安装DESeq2、airway、apeglm，再安装jsonlite；R与Bioconductor版本应匹配，不把Linux环境锁直接用于所有系统。

## 对象与顺序

本例由整数计数和样本表建立DESeqDataSet，设计为`~ cell + dex`；DESeq估计尺度和离散度并拟合Wald模型。用results提取明确方向，再单独lfcShrink，保留完整dds和vsd供检查。

普通矩阵接口不接受把TPM四舍五入后的伪计数。转录本估计计数使用tximport等对应导入接口，见[Salmon定量与tximport基因汇总](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Salmon%E5%AE%9A%E9%87%8F%E4%B8%8Etximport%E5%9F%BA%E5%9B%A0%E6%B1%87%E6%80%BB)。

## 结果列与导出

baseMean为平均标准化计数，log2FoldChange/lfcSE对应当前检验结果，pvalue和padj分别是原始与校正显著性。本例额外列名明确标出apeglm后验SD、阈值检验P以及关闭独立过滤的padj，避免混用。

实际安装、结果和失败检查见[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)；软件API以[DESeq2手册](https://bioconductor.org/packages/release/bioc/manuals/DESeq2/man/DESeq2.pdf)及所用版本帮助为准。
