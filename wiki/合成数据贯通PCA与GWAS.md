# 合成数据贯通PCA与GWAS

> 更新：2026-10-13；验证范围：合成数据实测。

用固定随机种子的人工数据练习文件交接、质控、PCA 与数量性状关联，不需要下载真实个体数据。

## 环境与输入

需要 Python 3.9+ 和 PLINK 2。本次实测使用 Python 3.14.8、PLINK v2.0.0-a.7.12LM（12 Oct 2026），Linux x86_64。官方安装入口见[PLINK2使用与版本管理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PLINK2%E4%BD%BF%E7%94%A8%E4%B8%8E%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86)。

在本项目根目录运行：

```bash
python3 examples/generate_population_data.py
bash examples/run_population_demo.sh
```

如果工具不在 PATH，可使用 `PLINK2_BIN=/完整路径/plink2 bash examples/run_population_demo.sh`。输出写到 `examples/output/population/`；重复运行会覆盖该目录中的同名输出。

生成器用固定种子 20261013，产生 120 个二倍体样本、600 个独立模拟位点和一个数量表型。表型包含 v1 的 G 剂量效应及随机噪声。它不模拟家系、真实 LD、批次或复杂群体历史。

## 实测检查点

| 阶段 | 文件 | 本次结果 |
|---|---|---|
| 输入 | toy.vcf、phenotype.tsv | 120 样本，600 位点 |
| 质控 | qc.pgen/pvar/psam | 120 样本、600 位点保留 |
| 剪枝 | prune.prune.in | 600 位点保留，因本例独立模拟 |
| PCA | pca.eigenvec | 120 行样本，5 个 PC |
| 回归 | gwas.trait.glm.linear | v1 的 ADD 检验 P≈1.95×10⁻²⁵ |

v1 的 A1 为 A，BETA≈−1.84。生成器对 G 赋正效应，计数 A 时负方向是相容的；不能只看 BETA 符号就判断模拟失败。

## 自己检查而不只看成功退出

确认样本与协变量匹配，检查 TEST、OBS_CT 和 ERRCODE；核对 v1 的效应等位基因与生成逻辑。改变噪声或样本数量，观察效应估计与证据强度的变化。

示例阈值只是演示，不是通用研究标准。真实工作流分别见[基因型质控与过滤](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E5%9E%8B%E8%B4%A8%E6%8E%A7%E4%B8%8E%E8%BF%87%E6%BB%A4)、[用PCA探索样本的群体结构](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%A8PCA%E6%8E%A2%E7%B4%A2%E6%A0%B7%E6%9C%AC%E7%9A%84%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84)和[GWAS从数据准备到结果解释](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E4%BB%8E%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87%E5%88%B0%E7%BB%93%E6%9E%9C%E8%A7%A3%E9%87%8A)。

代码：[数据生成器](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/generate_population_data.py)、[运行脚本](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/run_population_demo.sh)。模型选项参照 [PLINK --glm](https://www.cog-genomics.org/plink/2.0/assoc)。
