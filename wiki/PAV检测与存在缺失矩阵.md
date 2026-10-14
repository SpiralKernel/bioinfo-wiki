# PAV检测与存在缺失矩阵

> 更新：2026-10-14；状态：可用；验证范围：人工已判定PAV证据的矩阵整理已运行；组装比较、同源推断和真实PAV检测未运行。

先获得目标特征的存在、缺失或未知证据，再构建矩阵，不能把没注释或没覆盖直接记为0。

## 定义目标与单位

目标可以是序列片段、基因或其他统一特征，单位可以是单倍型组装或个体。首先定义何谓同一特征、至少几份算存在、可检测与缺失需要什么证据。杂合缺失不自动等于整个个体没有该基因。

## 组装证据分支

准备可比质量的组装、参考与注释，核对方向和染色体关系；进行全基因组比较，再结合共线性/同源和独立覆盖证据判定。下列为[SyRI官方示例](https://schneebergerlab.github.io/syri/example.html)对应的模板，未执行：

```bash
minimap2 -ax asm5 --eqx ref.fa query.fa > assemblies.sam
syri -c assemblies.sam -r ref.fa -q query.fa -F S
```

asm5是否适合实际序列差异需另判断。SyRI结构结果不是直接完成基因PAV矩阵；还需统一基因边界、同源关系、缺口与可检测证据。reads分支同样不能把局部低深度单独当作确定缺失。

## 可运行的矩阵整理例子

项目根目录执行，只需Python标准库：

```bash
python3 examples/pav_matrix_demo.py
```

输入`examples/data/variants/pav_evidence.tsv`是已经人工指定状态的示例证据，行故意乱序。脚本按特征和样本匹配，检查重复，输出`examples/output/pav-matrix/matrix.tsv`：

| 特征 | S01 | S02 | S03 |
|---|---:|---:|---:|
| toyGene1 | 1 | 0 | NA |
| toyGene2 | 1 | 1 | 1 |
| toyGene3 | 0 | 1 | NA |

1表示本例已判定存在，0表示已判定缺失，NA表示未知。3×3共5个1、2个0、2个NA；缺少一个证据组合时也保留NA。重复运行覆盖输出同名文件。

脚本只实测矩阵整理，不发现PAV、不做正交同源推断。原始证据来源与可检测状态应一直保留；不能用RNA不表达证明DNA不存在。概念见[结构变异CNV与PAV](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%93%E6%9E%84%E5%8F%98%E5%BC%82CNV%E4%B8%8EPAV)，源码：[PAV矩阵示例](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/pav_matrix_demo.py)。
