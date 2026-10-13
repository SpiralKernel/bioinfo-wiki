# Smith-Waterman局部比对

> 更新：2026-10-13；验证范围：合成数据实测。

Smith–Waterman 用动态规划找到给定打分规则下的最优局部比对，适合理解序列比对的精确基线。

## 状态与递推

H(i,j) 表示以两个序列的第 i、j 个字符结束的最佳局部得分。使用线性空位罚分 g > 0 时：

```text
H(i,j) = max(0,
             H(i-1,j-1) + s(query[i-1], subject[j-1]),
             H(i-1,j) - g,
             H(i,j-1) - g)
```

0 允许从当前位置重新开始。记录最优得分的格子，沿来源回溯到 0，得到局部区间；这与必须覆盖整个序列的全局比对不同。若采用仿射空位罚分，需要增加相应状态，不能只把 g 改成一个常数就声称完成。

## 实现与检查

[本项目教学代码](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/alignment_demo.py)使用人工字符串和匹配 +2、错配 −1、空位 −2，返回得分、对齐字符与区间；区间使用 0 基、右开形式。

```bash
python3 examples/alignment_demo.py
```

实测 `ABCD` 对 `XXABCDYY` 得分 8；完全不同字符得分 0；`ABCDE` 对 `ABXCDE` 得分 8，包含一个空位。代码是教学实现，采用完整矩阵，时间与空间量级均为 O(mn)。

## 为什么还需要BLAST

数据库有大量序列时，逐条完整动态规划成本很高。[BLAST原理与种子延伸](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLAST%E5%8E%9F%E7%90%86%E4%B8%8E%E7%A7%8D%E5%AD%90%E5%BB%B6%E4%BC%B8)用启发式缩小搜索范围，但可能漏掉没有合适种子的局部匹配。

原始方法见 [Smith & Waterman, 1981](https://doi.org/10.1016/0022-2836(81)90087-5)。
