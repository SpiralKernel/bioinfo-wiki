# BLAST原理与种子延伸

> 更新：2026-10-13；验证范围：合成数据实测。

BLAST 是序列局部相似性检索的启发式方法族；理解种子、延伸和统计评估比只记命令更重要。

## 搜索为什么可以更快

先把查询分成短词，查找可能的种子命中，再向周围延伸高分区域，最后整理和统计评估候选比对。蛋白检索可依据替换矩阵生成相近词，不限于完全相同的片段。不同 BLAST 程序、任务与历史版本并非一套完全相同的实现。

X-drop 延伸在当前得分落后于已见最佳得分超过给定幅度时停止；应保存最佳端点，而非停止位置。种子长度和筛选影响速度与敏感性，不能认为启发式结果总与[Smith-Waterman局部比对](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Smith-Waterman%E5%B1%80%E9%83%A8%E6%AF%94%E5%AF%B9)一致。

## 教学实现的范围

[教学代码](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/alignment_demo.py)实现完全匹配短词索引、无空位双向延伸、X-drop 和重复区间去重。人工字符串 `ABCD` 对 `XXABCDYY` 找到得分 8；`ABCD` 对 `AXCY` 没有长度 2 的精确种子，却能由动态规划得到正分局部比对。这一反例展示漏检来源。

代码没有实现蛋白邻近词、双命中触发、仿射空位、低复杂度处理、反向互补、数据库并行和 E-value 统计。因此它是理解一个搜索思路的可运行练习，不能代替 BLAST+ 或用于正式注释结论。

## 怎样读检索结果

E-value 是在相应模型、评分及搜索空间下，期望出现的达到该得分的随机匹配数量；它不是同源关系为假的概率。结合 identity、覆盖率、比对长度和数据库版本读结果，见[比对相似性同源性与覆盖率](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%AF%94%E5%AF%B9%E7%9B%B8%E4%BC%BC%E6%80%A7%E5%90%8C%E6%BA%90%E6%80%A7%E4%B8%8E%E8%A6%86%E7%9B%96%E7%8E%87)。

实际工具使用见[BLAST本地检索实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLAST%E6%9C%AC%E5%9C%B0%E6%A3%80%E7%B4%A2%E5%AE%9E%E8%B7%B5)。深入：[1990 年 BLAST 论文](https://doi.org/10.1016/S0022-2836(05)80360-2)、[1997 年 Gapped BLAST 论文](https://doi.org/10.1093/nar/25.17.3389)、[NCBI 得分统计教程](https://www.ncbi.nlm.nih.gov/BLAST/tutorial/Altschul-1.html)。
