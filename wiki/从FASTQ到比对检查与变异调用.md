# 从FASTQ到比对检查与变异调用

> 更新：2026-10-14；状态：可用；验证范围：人工基因案例与实际工具输出核对；具体已测范围见正文。

从人工reads开始实际连接minimap2、samtools和bcftools，补上人工SAM案例之前的比对步骤。

## 安装与运行

需要Python3和可执行的minimap2、samtools、bcftools。已有Conda可新建独立环境，例如`conda create -n alignment-demo -c conda-forge -c bioconda python minimap2 samtools bcftools`；此安装命令是环境模板，实际工具来自官方源码本地编译。

[下载项目](https://github.com/SpiralKernel/bioinfo-wiki/archive/refs/heads/main.zip)并在项目根目录运行：

```bash
conda run -n alignment-demo python examples/genome_alignment_demo.py
```

已有PATH工具时直接`python3 examples/genome_alignment_demo.py`。非PATH位置分别用MINIMAP2_BIN、SAMTOOLS_BIN、BCFTOOLS_BIN环境变量。输出默认`examples/output/alignment-chain/`，重复执行覆盖同名结果；使用`--output`指定独立目录。

## 本例做了什么

复制固定人工FASTA和40条单端150bp FASTQ；minimap2 `-ax sr`并写入读组；samtools排序、quickcheck、索引、flagstat及coverage；bcftools mpileup/call检测小变异。源码[genome_alignment_demo.py](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/genome_alignment_demo.py)保存实际命令。

本机minimap2 2.30-r1287、samtools1.22/HTSlib1.22、bcftools1.22。实际检出预设`chrToy:105 C>T`、GT=0/1；40条primary reads全部比对，但仅覆盖参考的169/1600bp（10.5625%）。高比对率不等于全参考可调用。

## 边界

这些短而规则的人工reads没有模拟真实重复、污染、测序错误、双端结构和群体复杂性。脚本不构成正式重测序最佳流程，也没有运行BWA、重复标记、BQSR、联合分型或专业SV检测。

查看[minimap2BWA与比对器选择](https://github.com/SpiralKernel/bioinfo-wiki/wiki/minimap2BWA%E4%B8%8E%E6%AF%94%E5%AF%B9%E5%99%A8%E9%80%89%E6%8B%A9)和[samtools比对检查与覆盖统计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/samtools%E6%AF%94%E5%AF%B9%E6%A3%80%E6%9F%A5%E4%B8%8E%E8%A6%86%E7%9B%96%E7%BB%9F%E8%AE%A1)理解指标；正式数据还要落实样本表、质控、参考版本、可调用范围和适合的调用策略，见[基因组重测序与变异检测](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%87%8D%E6%B5%8B%E5%BA%8F%E4%B8%8E%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B)。
