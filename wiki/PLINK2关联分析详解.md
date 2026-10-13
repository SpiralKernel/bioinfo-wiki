# PLINK2关联分析详解

> 更新：2026-10-13；状态：可用；验证范围：公开小鼠数据的连续性状回归实测；二分类模板与扩展参数未执行。

PLINK 2的关联接口按性状拟合回归；正确读取性状、协变量、计数等位基因与错误码比记住一条命令更重要。

## 它在GWAS流程中承担什么

PLINK 2可用于样本与位点处理、频率摘要、PCA及关联。常规`--glm`对连续性状拟合线性回归，对二分类使用逻辑或Firth回归；它不是GRM混合模型。近亲样本的处理不能只靠增加PC，见[GWAS软件选择与比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E9%80%89%E6%8B%A9%E4%B8%8E%E6%AF%94%E8%BE%83)。

基础安装与版本见[PLINK2使用与版本管理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PLINK2%E4%BD%BF%E7%94%A8%E4%B8%8E%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86)。本页连续性状命令在PLINK v2.0.0-a.7.12LM中实测；二分类模板仅按官方接口核对。

## 输入准备

BED/BIM/FAM使用`--bfile`，PGEN/PVAR/PSAM使用`--pfile`。外部表型文件按FID/IID匹配，并用`--pheno-name`选择列；协变量用`--covar`及`--covar-name`明确指定。不要把缺失编码、分类变量或不同表型列留给软件猜测。

普通回归的样本应满足模型的独立性及其他假设。若剔除近亲，保留名单与理由；若保留家系个体，选择能够表示相关性的模型。PC调整和GRM处理的区别见[关联模型中的协变量与残差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%B3%E8%81%94%E6%A8%A1%E5%9E%8B%E4%B8%AD%E7%9A%84%E5%8D%8F%E5%8F%98%E9%87%8F%E4%B8%8E%E6%AE%8B%E5%B7%AE)。

## 已运行的数量性状命令

先完成[公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)的准备步骤，再在其输出目录`examples/output/gwas-real/`执行：

```bash
mkdir -p results
plink2 --bfile prepared/qc --chr-set 19 no-xy no-mt \
  --covar prepared/pca.eigenvec --covar-name PC1-PC3 \
  --glm hide-covar --threads 2 --out results/plink_pc3
```

本例FAM第六列是已经处理的连续CD8表型。`--chr-set 19`匹配本例小鼠常染色体设置，不能复制到鸡或其他物种。三个PC属于本案例比较设计，不是所有研究的固定数量。

用于对照的无PC普通回归写作`--glm allow-no-covars hide-covar`；此处是展示家系结构影响的诊断对照，不作为该家系数据的最终推荐分析。

## 二分类接口模板

以下需另准备独立设计与输入，尚未运行；默认常见1/2编码及缺失规则应按当前手册确认，0/1输入需核对`--1`等选项：

```bash
plink2 --pfile cohort --pheno phenotype.tsv --pheno-name case_status \
  --covar covariates.tsv --covar-name age,PC1-PC3 \
  --glm firth-fallback hide-covar --out results/binary
```

`firth-fallback`在常规逻辑回归失败时回退，不等于对所有位点强制Firth。极低MAC与明显不平衡仍需诊断；Firth不处理家系GRM，见[二分类性状OR与病例对照不平衡](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%8C%E5%88%86%E7%B1%BB%E6%80%A7%E7%8A%B6OR%E4%B8%8E%E7%97%85%E4%BE%8B%E5%AF%B9%E7%85%A7%E4%B8%8D%E5%B9%B3%E8%A1%A1)。

## 输出逐列怎样读

| 字段 | 应核对的信息 |
|---|---|
| ID、CHROM、POS | 是否与输入位点及参考版本一致 |
| REF、ALT、PROVISIONAL_REF? | BED来源的参考可能只是暂定，不能直接当作经FASTA核验 |
| A1、OMITTED、A1_FREQ | β计数哪种等位基因；频率属于什么样本集合 |
| TEST | 普通加性位点通常查看ADD；协变量行与其他检验分开 |
| OBS_CT、BETA、SE、P | 有效样本量、效应单位与不确定性 |
| ERRCODE | `.`以外的错误或失败需调查，不能当作正常不显著 |

本例rs3683945计数A，β≈−0.0718791、P≈0.0446981；GEMMA相同LM给出接近值。主信号不能只挑这一行，完整比较见[GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)。

## 参数与常见误用

`hide-covar`隐藏协变量结果行，不删除模型中的协变量。`omit-ref`可改变计数方向；`log10`会改变P列表示，后处理必须同步。剂量存在时，当前`--glm`会使用剂量，若要比较硬调用需明确转换，不能只换文件扩展名。

报错先查样本匹配、常数协变量、重复PC、共线及低MAC；不要直接提高容限后忽略模型问题。参数选择见[GWAS参数选择与敏感性分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E5%8F%82%E6%95%B0%E9%80%89%E6%8B%A9%E4%B8%8E%E6%95%8F%E6%84%9F%E6%80%A7%E5%88%86%E6%9E%90)，字段统一见[GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80)。

深入：[PLINK关联模型与错误码](https://www.cog-genomics.org/plink/2.0/assoc)、[文件格式](https://www.cog-genomics.org/plink/2.0/formats)、[输入与表型](https://www.cog-genomics.org/plink/2.0/input)。
