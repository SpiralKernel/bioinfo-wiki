# STAR剪接比对与RNA比对指标

> 更新：2026-10-15；状态：可用；验证范围：官方资料与方法核对；本页上游或扩展软件流程未执行。

RNA跨外显子连接的reads需要剪接感知比对；参考、注释、链和比对统计一起核对。

## 为什么不能照搬DNA比对例子

成熟RNA可能跨越很长的基因组内含子，普通连续DNA比对假设不适用。STAR是剪接比对工具之一，索引构建需匹配基因组和注释，并考虑reads长度及所用版本。[官方仓库与手册](https://github.com/alexdobin/STAR)提供完整命令。

本轮未安装或执行STAR。上一轮人工minimap2短读长DNA案例不验证RNA剪接，也不能当本页实测。

## 应保存的指标

记录输入reads/read pairs、唯一与多重比对、未比对原因、剪接连接和错配等。不同工具分母和类别不同，不能仅比较一个“mapping rate”。多重比对在重复基因家族中可能影响基因计数；跨剪接支持还要结合注释与比对质量。

airway包的原始处理说明采用STAR、GRCh37与Ensembl75，本轮只读取其计数对象，没有重跑这些比对，见[airway来源说明](https://bioconductor.org/packages/release/data/experiment/vignettes/airway/inst/doc/airway.html)。

下游计数必须与同一参考注释配套，读[GFF3GTF与基因转录本外显子](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GFF3GTF%E4%B8%8E%E5%9F%BA%E5%9B%A0%E8%BD%AC%E5%BD%95%E6%9C%AC%E5%A4%96%E6%98%BE%E5%AD%90)及[featureCounts基因计数与链方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/featureCounts%E5%9F%BA%E5%9B%A0%E8%AE%A1%E6%95%B0%E4%B8%8E%E9%93%BE%E6%96%B9%E5%90%91)。
