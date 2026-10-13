# GWAS软件输入转换与样本对齐

> 更新：2026-10-13；状态：可用；验证范围：公开小鼠PLINK/GEMMA/GCTA/REGENIE输入转换与ID核对实测；其余约定按官方文档核对。

转换必须保持样本身份、位点身份、等位基因编码和性状含义；格式可以读入不代表转换正确。

## 先建立共同样本清单

从基因型、表型、协变量和必要关系矩阵分别导出ID，检查唯一性与交集。FID/IID组合、仅IID和taxa是不同约定；若IID不是全局唯一，需要建立无碰撞的稳定映射。列出各来源独有与缺失个体，再决定排除，而不是默默内连接后继续。

保存原始文件、转换脚本、共同个体名单与转换后的顺序。不要依赖两个文件当前恰好同序，也不要用会改变样本数的过滤后结果配旧矩阵。

## 各工具常用约定

| 工具 | 表型或协变量的关键特点 | 特别检查 |
|---|---|---|
| PLINK 2 | 外部表格按FID/IID匹配，明确列名；内部FAM/PSAM也能存表型 | 表型编码与类型、有效交集 |
| GEMMA | 本例表型在FAM；外部纯数值协变量按行对应 | `-c`显式截距，不带ID/标题；K同序 |
| GCTA | 表型与协变量带FID/IID，常用无标题格式 | 定量`--qcovar`与分类`--covar`分开 |
| REGENIE | 表型与协变量带FID/IID和标题 | 两步性状名、样本、预测文件一致 |
| SAIGE | 表型表指定样本ID列，输入与索引分阶段 | 指定ID需唯一；稀疏矩阵附ID表 |
| BOLT-LMM | 外部表型与协变量带标题，通过列名选择 | 分类与定量列接口、交集与缺失 |
| EMMAX | 传统表型、协变量按TFAM顺序 | 显式截距、1/2编码与原始等位基因映射 |
| GAPIT/TASSEL/rMVP | taxa或转换后的个体对象 | 自动交集后的样本；rMVP外部CV按最终顺序 |

这是本专题涉及的常用入口，具体格式以该版本详细页为准，不构成所有输入选项的完整清单。

## 位点与编码的交接

同一位点应同时记录组装、染色体、位置、REF/ALT或实际两种等位基因及稳定ID。BED的第一/第二等位基因未必经过参考序列核验；转成PGEN不会自动使它们成为可信REF/ALT。

硬调用与剂量不能无说明互换。数值0/1/2必须指明计数哪种等位基因；旧TPED的数字1/2含义又不同。多等位位点拆分、链方向和缺失转换应留下规则，见[VCF与基因型编码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E7%BC%96%E7%A0%81)及[定相与基因型填充](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AE%9A%E7%9B%B8%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E5%A1%AB%E5%85%85)。

## 本轮实际遇到的转换问题

GEMMA官方小鼠FAM含六列表型扩展，直接当作所有软件的普通六列FAM并不稳妥。脚本先核对扩展表型与独立矩阵一致，再制作六列教学副本：保留FID/IID与性别，选择第一性状；父母列置0，仅用于本流程的基因型处理，亲缘由GRM表示。原始文件保留。

本例1940个体中1410个有第一性状，后续质控与协变量都用这一集合。GEMMA协变量按最终FAM顺序生成，第一列是1；GCTA和REGENIE使用各自需要的ID与标题形式。

## 转换后的验收

检查样本与位点数、重复ID、缺失分布、等位基因频率和少数位点的逐样本编码；矩阵还核对维度、顺序、对称性及来源名单。通过一个同样本、同协变量的普通LM对照，能帮助发现方向或顺序错误，但不能代替全部格式审计。

代码见[多软件教学脚本](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/gwas_software_demo.py)，结果统一见[GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80)。深入：[PLINK格式文档](https://www.cog-genomics.org/plink/2.0/formats)、[GEMMA手册](https://github.com/genetics-statistics/GEMMA/blob/v0.98.5/doc/manual.pdf)、[REGENIE输入选项](https://rgcgithub.github.io/regenie/options/)。
