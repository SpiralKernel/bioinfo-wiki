# FreeBayes小变异与倍性设置

> 更新：2026-10-15；状态：可用；验证范围：对应人工/官方微型案例已实际运行；具体范围见正文。

FreeBayes使用局部单倍型与概率模型调用小变异；倍性和混样假设需按样本声明。

## 输入与操作

需要同参考排序BAM及索引、参考FASTA与读组。基本模板：

```bash
freebayes -f reference.fa -p 2 sample.bam > sample.vcf
```

输出可能有SNP、Indel、MNP和局部复杂单倍型。过滤、标准化与多等位拆分需要另做并保留原表示，见[VCF标准化多等位拆分与表示](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E6%A0%87%E5%87%86%E5%8C%96%E5%A4%9A%E7%AD%89%E4%BD%8D%E6%8B%86%E5%88%86%E4%B8%8E%E8%A1%A8%E7%A4%BA)。

## 倍性选项不等于所有特殊场景已解决

-p控制相应模型倍性；不同区域、池化样本和拷贝变化还有其他约定，按[官方README](https://github.com/freebayes/freebayes)及所用版本帮助核对。四倍体剂量、混池频率与二倍体GT不是同一种量，不能只改-p后就宣称真实多倍体性能已验证。

## 本轮实际运行

安装[人工长读长贯通SV调用与评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E9%95%BF%E8%AF%BB%E9%95%BF%E8%B4%AF%E9%80%9ASV%E8%B0%83%E7%94%A8%E4%B8%8E%E8%AF%84%E4%BC%B0)的variant-calling环境后，在项目根目录执行`conda run -n wiki-variant-calling python examples/variant_calling_demo.py --case small`。

FreeBayes1.3.10在40条人工短reads上调用chrToy:105 C>T、GT=0/1；输出examples/output/calling-small，非空目录拒绝覆盖。输入沿用人工注释参考，不是真实物种检测基准。原生INFO/TYPE为小变异类型，不要求头部必须定义SVTYPE；解析器已据此纠错。
