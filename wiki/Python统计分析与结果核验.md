# Python统计分析与结果核验

> 更新：2026-10-13；状态：可用；验证范围：两个Python教学程序已运行；Welch与BH经独立实现核对，其他接口按各页说明。

用明确的数组、方向和参数调用SciPy，并通过手算关系与独立实现检查输出。

## 环境与入口

教学依赖建议Python 3.10+、SciPy 1.15+（使用rng接口），可在项目运行`python -m pip install -r requirements-teaching.txt`。本轮实测Python 3.14、NumPy 2.5.4、SciPy 1.18.1、Matplotlib 3.11.2。官方网页显示的版本可能与安装版本不同，保留实际环境记录；不要靠默认值记忆方法。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install numpy scipy matplotlib
.venv/bin/python examples/statistics_demo.py
.venv/bin/python examples/basic_algorithms_demo.py
```

在项目根目录运行；安装当前版本不保证将来与本轮逐位一致。教学输出写入 `examples/output/statistics/` 和 `examples/output/basic-algorithms/`，重复运行覆盖同名文件。

## 常用接口与需写明的选项

| 问题 | SciPy入口 | 不能省略的解释 |
|---|---|---|
| 独立均值差 | `stats.ttest_ind` | `equal_var=False`表示Welch，参数顺序决定方向 |
| 配对均值差 | `stats.ttest_rel` | 数组必须按同一配对ID排序 |
| 秩和/符号秩 | `mannwhitneyu` / `wilcoxon` | 独立或配对、并列、精确/渐近方式 |
| 分类计数 | `fisher_exact` / `chi2_contingency` | 行列含义、单双侧、校正和期望计数 |
| 区间重采样 | `bootstrap` | 方法、配对规则、次数与随机数 |
| 置换 | `permutation_test` | 交换规则、统计量、精确/随机 |
| BH/BY | `false_discovery_control` | 有效P值、检验家族与依赖条件 |

表内列出的接口不代表本项目全部执行过。实测范围见[合成数据贯通统计推断](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E7%BB%9F%E8%AE%A1%E6%8E%A8%E6%96%AD)，其他方法的具体假设在对应概念页。

## 最低限度的核验

核对有限值、缺失、样本长度和ID；检查默认axis是否把预期的样本维度当成特征维度。对均值差统一写为B−A；统计量符号、区间和绘图必须一致。

本项目独立实现Welch效应/自由度/区间与BH排序校正，再与SciPy核对；梯度下降与NumPy `lstsq`比较。数值一致验证实现与目标关系，不能证明真实数据满足假设。

输出保留效应、SE或区间、P、调整值、独立样本数、对比、版本与种子。不要静默`nan_policy="omit"`后丢掉每个基因实际样本数，也不要将下溢P=0当作无限证据。

依据：[SciPy统计模块](https://docs.scipy.org/doc/scipy/reference/stats.html)。真实R/Bioconductor流程继续使用各工具官方接口；本轮没有安装R。
