# STR重复扩增与移动元件插入

> 更新：2026-10-14；状态：可用；验证范围：官方文档与原始研究核对；专业检测命令为模板，未执行完整真实数据流程。

串联重复长度变化与移动元件插入具有不同的证据和输出，不能一律当普通Indel。

## 串联重复

STR是短串联重复；更广义串联重复的单元可更长。重复等位可用重复次数、长度和组成描述。CAG重复10次为30 bp，但真实区域可包含中断或多个motif，不能一律用总长度除以一个单元长度。

reads若没有跨越重复及唯一侧翼，定位和长度就有不确定性。短读长模型可利用跨越、侧翼或重复内reads；长读长仍需足够支持、平台质量和正确目录。

## 移动元件

转座子/移动元件插入可由两侧连接、家族序列与靶位点重复等证据支持。参考中已有的元件与非参考插入不是同一检测目标；参考TE注释不等于样本间插入多态性。

某软件的`CN`可能是重复次数字符串，另一软件的CN是拷贝数；必须读FORMAT定义。类似地，`<STRn>`、完整等位序列或自定义TE家族字段依赖调用器。

继续[STR与重复扩增检测及提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/STR%E4%B8%8E%E9%87%8D%E5%A4%8D%E6%89%A9%E5%A2%9E%E6%A3%80%E6%B5%8B%E5%8F%8A%E6%8F%90%E5%8F%96)、[转座子插入检测与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BA%A7%E5%AD%90%E6%8F%92%E5%85%A5%E6%A3%80%E6%B5%8B%E4%B8%8E%E6%8F%90%E5%8F%96)。依据：[ExpansionHunter简介](https://github.com/Illumina/ExpansionHunter/blob/master/docs/01_Introduction.md)、[TRGT原始研究](https://doi.org/10.1038/s41587-023-02057-3)、[ngs_te_mapper2研究](https://doi.org/10.1093/genetics/iyab113)。
