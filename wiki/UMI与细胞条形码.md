# UMI与细胞条形码

> 更新：2026-10-13；状态：可用；验证范围：文档核对；完整流程未在本机运行。

细胞条形码帮助区分测量单元，UMI 用于识别分子标签；二者不是同一类标识符。

同一个细胞条形码下可有许多不同 UMI，同一 UMI 字符串也可能在不同细胞或基因上下文出现。分子去重需要结合具体实验与处理算法，而不是把全表相同 UMI 一律合并。

UMI 计数与 read 数不同，均不自动等于样本中全部 RNA 分子的真实数量。双细胞、空液滴、环境 RNA 和捕获效率都会影响解释。

实践见[单细胞转录组入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8D%95%E7%BB%86%E8%83%9E%E8%BD%AC%E5%BD%95%E7%BB%84%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)。深入阅读 [10x 基因表达处理说明](https://www.10xgenomics.com/support/software/cell-ranger/latest/algorithms-overview/cr-gex-algorithm)和 [Scanpy 官方教程](https://scanpy.readthedocs.io/en/stable/tutorials/basics/clustering.html)。
