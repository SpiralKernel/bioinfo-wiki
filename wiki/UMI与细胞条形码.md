# UMI与细胞条形码

> 更新：2026-10-13；状态：可用；验证范围：文档核对；完整流程未在本机运行。

细胞条形码帮助区分测量单元，UMI 用于识别分子标签；二者不是同一类标识符。

同一个细胞条形码下可有许多不同 UMI，同一 UMI 字符串也可能在不同细胞或基因上下文出现。分子去重需要结合具体实验与处理算法，而不是把全表相同 UMI 一律合并。

UMI 计数与 read 数不同，均不自动等于样本中全部 RNA 分子的真实数量。双细胞、空液滴、环境 RNA 和捕获效率都会影响解释。

实践见[单细胞转录组入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8D%95%E7%BB%86%E8%83%9E%E8%BD%AC%E5%BD%95%E7%BB%84%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)。深入阅读 [10x 基因表达处理说明](https://www.10xgenomics.com/support/software/cell-ranger/latest/algorithms-overview/cr-gex-algorithm)和 [Scanpy 官方教程](https://scanpy.readthedocs.io/en/stable/tutorials/basics/clustering.html)。


## 与建库索引和重复的区别

样本索引用于拆分样本，细胞条形码标记相应测量单元，UMI用于分子标签，见[文库接头索引与条形码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%96%87%E5%BA%93%E6%8E%A5%E5%A4%B4%E7%B4%A2%E5%BC%95%E4%B8%8E%E6%9D%A1%E5%BD%A2%E7%A0%81)。UMI有限长度可能发生碰撞，标签也可能识别错误；同字符串不自动等于同一原始分子。具体去重依上下文和算法。

扩增子同起点不自动是PCR重复，原生分子数量也不能由read数直接恢复，见[测序错误重复偏差与嵌合体](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E9%94%99%E8%AF%AF%E9%87%8D%E5%A4%8D%E5%81%8F%E5%B7%AE%E4%B8%8E%E5%B5%8C%E5%90%88%E4%BD%93)。
