# 公开airway数据贯通DESeq2

> 更新：2026-10-15；状态：可用；验证范围：原生R与公开airway计数案例已执行；范围和结果见正文。

用公开真实计数在原生R完成配对模型、效应收缩、阈值检验和诊断，并核对关键结果性质。

## 数据来自哪里

使用Bioconductor airway包的`airway`整数计数对象，原研究GSE52778；4条人气道平滑肌细胞系，每条有处理trt和对照untrt，共8个样本。[包内来源说明](https://bioconductor.org/packages/release/data/experiment/vignettes/airway/inst/doc/airway.html)记录STAR、GRCh37/Ensembl75和summarizeOverlaps处理。本轮没有下载原FASTQ或重跑计数，也没有复现原论文所有分析。

## 下载、安装与第一次运行

[下载项目ZIP](https://github.com/SpiralKernel/bioinfo-wiki/archive/refs/heads/main.zip)，解压并进入含README.md和examples的根目录。按[DESeq2安装对象与结果提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DESeq2%E5%AE%89%E8%A3%85%E5%AF%B9%E8%B1%A1%E4%B8%8E%E7%BB%93%E6%9E%9C%E6%8F%90%E5%8F%96)创建环境，在Linux/macOS或WSL终端执行：

```bash
conda env create -f examples/environments/rnaseq.yml
conda run -n wiki-rnaseq Rscript examples/test_rnaseq_inputs.R
conda run -n wiki-rnaseq Rscript examples/rnaseq_airway_demo.R
```

Windows原生R需先按Bioconductor安装所需包，再在系统终端执行Rscript；本轮仅实测Linux。安装、载入和运行是不同步骤，首次安装需要联网。分析本身只用已安装数据包，不额外联网查询基因名。

输出在examples/output/rnaseq-airway。为保护已有结果，非空目录会拒绝运行；再练习可传一个新的目录，例如`Rscript examples/rnaseq_airway_demo.R examples/output/rnaseq-practice2`。不允许覆盖既有输出的规则只针对本案例。

## 实际操作

故意打乱样本表后按ID重排，检查4×2配对结构；原始总计数至少10预过滤；拟合`~ cell + dex`，提取trt对untrt、alpha0.05；apeglm单独收缩；另做|log2FC|>1阈值检验及关闭独立过滤的诊断对照；使用VST作PCA、样本距离、MA与火山图。

固定环境和本次具体数值记录在[summary.json](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/rnaseq-round1/summary.json)，详细范围在[维护记录](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/maintenance/rnaseq-round1-2026-10-15.md)。

| 本次固定设置 | 实际结果 |
|---|---|
| 原始基因数→总计数≥10保留 | 63,677→22,369 |
| 普通Wald padj<0.05 | 4,030：上调2,208、下调1,822 |
| 有P但因独立过滤无padj | 5,204 |
| 保留集合内P为NA | 0；不表示所有数据都不会有异常P |
| 关闭独立过滤的诊断对照 | 3,820个显著 |
| 绝对log2FC>1的专门检验 | 243个显著 |

以上是本次包版本、过滤和设计下的结果，不是原论文发现数或跨版本必须逐位相同的真值。

## 核对产物与反例

counts.csv和samples.csv可核对输入；design-matrix.csv可核对满秩；differential-expression.csv保存完整结果，top50.csv仅用于查看，不作为富集的默认背景；result-status.csv保留NA分类，sample-qc.csv保存尺度与文库量。

实际检查：反向对比只翻转LFC而保留双侧P/padj；关闭独立过滤的padj与BH一致；apeglm结果保留原Wald P/padj。基础输入检查会拒绝分数计数、缺样本和混杂设计。

![airway配对DESeq2诊断](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/rnaseq-round1/diagnostics.png)

图上PCA样本标签为SRR10395后的尾号，形状区分细胞系、颜色区分处理；MA图和火山图颜色用原Wald padj<0.05，火山图纵轴为原始P。MA图边界三角表示超出当前纵轴显示范围，原表数值未截断。本轮只运行VST，未运行rlog。

修改图形可在已有输出上执行`Rscript examples/plot_rnaseq_airway.R`，只重画diagnostics.png，不重新拟合模型；可传已有输出目录。

源码[rnaseq_airway_demo.R](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/rnaseq_airway_demo.R)。别用“显著基因数相同”作为唯一复跑标准；包版本、过滤及数值精度可能改变边界，先核对完整参数和输入。
