# EMMAX关联分析与旧流程兼容

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

EMMAX是混合模型关联的经典实现，理解旧文件编码与顺序是复现已有分析的关键。

## 什么情况下需要读这页

已有项目或论文使用EMMAX时，需要还原其基因型转换、亲缘估计、性状与协变量设置。EMMAX借助零模型估计和相应近似提高大量位点检验效率，不能仅根据名称把它与GEMMA或SAIGE视为完全同一流程。

新分析的选择还应看性状、亲缘、物种、规模与软件验证范围，见[GWAS软件选择与比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E9%80%89%E6%8B%A9%E4%B8%8E%E6%AF%94%E8%BE%83)。本机没有运行EMMAX。

## 文件与顺序

传统接口使用数值编码的TPED/TFAM。表型通常为FID、IID、数值三列，按TFAM顺序排列；协变量也带FID/IID，并需要显式截距列1。K是同一个体顺序的数值矩阵。

TPED中的数字1/2是转换后的等位基因编码，不是VCF的REF/ALT索引。旧软件和说明中对效应编码的表述可能不一致，复现必须保存原始等位基因到数值的映射，并用已知位点或人工例子核对方向，不能只根据“1通常是什么”猜β含义。

## 旧版接口结构

以下按官方传统说明整理，未执行；`plink`指相容的旧版接口，不能直接用PLINK 2替换程序名：

```bash
plink --bfile cohort --recode12 --output-missing-genotype 0 \
  --transpose --out emmax_input
emmax-kin-intel64 -v -d 10 emmax_input
emmax -v -d 10 -t emmax_input -p phenotype.txt \
  -k emmax_input.aBN.kinf -c covariates.txt -o results/emmax
```

二进制名称、BN/IBS矩阵选项与输出后缀依发行包核对；先创建`results/`并按官方教程的小数据检验。转换时另保留等位基因映射、样本顺序与过滤记录。

## 输出与判断

传统`.ps`表包含位点、效应、SE与P，未必自带等位基因和坐标；需要按保留的映射表补齐。`.reml`记录零模型相关估计；其伪遗传率不能无说明与其他工具的SNP遗传率直接比较。

亲缘矩阵出现NaN时先查单态位点、频率与输入编码。矩阵维度正确但样本顺序错误，可能照样产生结果，必须在运行前检查而非只看退出状态。

## 二分类与扩展限制

经典EMMAX以线性模型思路处理性状。二分类标签送入LMM后，β不自动成为log-OR；明显不平衡与稀疏计数需要另审查适合的方法。VCF或集合检验可能涉及EPACTS等其他封装，不应声称传统命令已经覆盖全部输入与任务。

深入：[EMMAX官方说明](https://genome.sph.umich.edu/wiki/EMMAX)、[原始方法](https://doi.org/10.1038/ng.548)、[GWAS软件输入转换与样本对齐](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E8%BE%93%E5%85%A5%E8%BD%AC%E6%8D%A2%E4%B8%8E%E6%A0%B7%E6%9C%AC%E5%AF%B9%E9%BD%90)、[GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80)。
