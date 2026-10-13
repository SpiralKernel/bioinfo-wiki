# 连锁不平衡与LD剪枝

> 更新：2026-10-13；验证范围：文档核对；操作需按所用环境验证。

连锁不平衡描述位点等位基因之间的非随机关联，LD 剪枝用于减少所选位点集合中的冗余。

## 位点为什么不能总被当成独立信息

两个相邻位点的等位基因可能经常一起出现。r² 是常见关联程度指标，但计算口径可以是已定相单倍型或未定相基因型剂量，需记录软件与选项。LD 随群体、频率及样本变化。

## 剪枝与clumping的区别

剪枝通常不使用表型关联强弱，得到适合 PCA 等用途的较低冗余子集；clumping 根据关联结果选择代表性信号并归组附近相关位点。两者都不等于精细定位或因果推断。

PLINK 2 的 `--indep-pairwise 50 5 0.2` 示例中，50 是位点数窗口，5 是移动的位点数，0.2 是 r² 阈值。加入 `kb` 时单位和版本要求会改变。输出的 `.prune.in` 需要再用 `--extract` 应用，不能以为生成名单后当前数据自动被剪枝。

参数是练习选择，实际应结合物种 LD 范围和目标比较。见[基因型质控与过滤](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E5%9E%8B%E8%B4%A8%E6%8E%A7%E4%B8%8E%E8%BF%87%E6%BB%A4)及 [PLINK 剪枝手册](https://www.cog-genomics.org/plink/2.0/ld)、[clumping 手册](https://www.cog-genomics.org/plink/2.0/postproc)。
