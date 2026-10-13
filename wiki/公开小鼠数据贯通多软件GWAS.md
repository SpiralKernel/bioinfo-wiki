# 公开小鼠数据贯通多软件GWAS

> 更新：2026-10-13；状态：可用；验证范围：四个软件与七种主要配置端到端实测；附加chr17对照与MAF计数实测，完整全基因组LOCO未执行。

用固定版本的公开小鼠数据完成质控、PCA、多软件关联、等位基因统一和诊断图，学习每一步的交接与判断。

## 研究问题与数据来历

目标是学习家系相关样本的数量性状关联，以及软件输入和结果如何比较。使用[GEMMA v0.98.5官方示例](https://github.com/genetics-statistics/GEMMA/tree/v0.98.5/example)，原始来源与预处理见[该版本手册](https://github.com/genetics-statistics/GEMMA/blob/v0.98.5/doc/manual.pdf)。

下载文件实际包含1940个体、12226个常染色体标记，85个FID组；第一表型CD8有1410个有效观测，分析副本包含72个FID组。来源手册文字与文件个体数存在不一致，本文按下载文件与运行日志记录，不仅根据文件名或手册数字猜测。

表型已经由来源流程校正若干因素并做分位数正态化；基因型也经过来源处理。本例从发布的基因型与处理表型开始，不复现原始测序、分型或全部研究质控。β不以原始细胞百分比解释。

参考组装未在当前练习中确定，坐标只沿用示例；不直接用于现代组装注释或新功能结论。

## 软件与代码

本轮环境为Linux x86_64、Python 3.14.8，实测PLINK v2.0.0-a.7.12LM、GEMMA 0.98.5、GCTA v1.94.1、REGENIE v4.1.3.gz。源码与安装入口在各软件详细页，先确认本机版本与可执行文件位置。

[运行脚本](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/gwas_software_demo.py)只依赖Python标准库并调用上述二进制；自动下载约6.6MB的固定版本输入，并核对四个文件的SHA256。工具本体需要先自行安装，脚本不会代替安装。

## 在项目根目录运行

```bash
python3 examples/gwas_software_demo.py \
  --plink2 plink2 --gemma gemma --gcta gcta64 --regenie regenie \
  --fastgwa --loco-chr17 --threads 2
```

工具不在PATH时，把程序名换成完整路径。GCTA与REGENIE是可选参数；最小运行可仅提供PLINK和GEMMA。`--fastgwa`需要GCTA；`--loco-chr17`只追加一条染色体的对照。

输出写入`examples/output/gwas-real/`；重复运行会覆盖同名派生文件与日志，原始下载文件先校验再复用。需要保留多次实验时使用不同`--output`目录。

## 分阶段检查点

| 阶段 | 本次检查结果 | 主要产物 |
|---|---|---|
| 输入审计 | 1940个体、12226位点、1410个有效第一性状 | 四个源文件与校验记录 |
| 转换 | 六列教学FAM；父母ID未用于此分析副本，原件保留 | prepared/cohort与complete.keep |
| 教学质控 | 1410个体、8544位点 | qc.bed/bim/fam |
| LD剪枝与PCA | 649位点用于PCA，计算5轴，关联使用前3轴 | prune名单与pca.eigenvec |
| 普通回归与混合模型 | 每个主要配置测试8544共同位点 | 各软件结果与日志 |
| 结果统一 | 52个位点需要相对PLINK翻转方向 | harmonized-results.tsv |
| 附加chr17对照 | 288个测试位点；K来自其他染色体 | loco目录 |

阈值0.05、三个PC与稀疏阈值0.05均是本例设定，不是通用方案。命令JSON、各阶段日志和run-metadata.json提供实际交接记录。

## 绘图与核对

绘图环境另外需要NumPy、SciPy、Matplotlib；使用独立环境安装并记录版本，然后在项目根目录运行：

```bash
python3 examples/plot_gwas_comparison.py
```

脚本检查共同位点与样本、统一等位基因，并验证PLINK PC3与GEMMA LM接近输出精度；生成质控/PCA、曼哈顿、QQ及chr17对照图，保存summary.json。实际图见下方及[GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)。

![输入规模、MAF与PCA](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/gwas-round2/data-and-pca.png)

图：关联与PCA使用不同位点集合；PCA按四个最大的已记录FID组着色，其他组为灰色。图中的分团不能直接被命名为确定祖源，家系结构也是重要来源。

## 怎样判断练习完成

能够解释530个体为何没有进入本性状分析、PCA为何用649位点而关联用8544位点、各软件如何读取截距与ID、52个方向翻转怎样处理，以及普通回归与GRM方法为何不能要求结果完全一致。

本例不提供正式软件功效排名，不验证不平衡二分类、稀有变异、多倍体、全基因组LOCO或真实候选机制。继续阅读[GWAS参数选择与敏感性分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E5%8F%82%E6%95%B0%E9%80%89%E6%8B%A9%E4%B8%8E%E6%95%8F%E6%84%9F%E6%80%A7%E5%88%86%E6%9E%90)、[GWAS常见报错与排查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E5%B8%B8%E8%A7%81%E6%8A%A5%E9%94%99%E4%B8%8E%E6%8E%92%E6%9F%A5)及[变异注释与候选证据整理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%B3%A8%E9%87%8A%E4%B8%8E%E5%80%99%E9%80%89%E8%AF%81%E6%8D%AE%E6%95%B4%E7%90%86)。
