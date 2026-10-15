# cuteSV长读长结构变异与支持提取

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

cuteSV从长读长比对中提取和聚类SV信号，平台与过滤参数要随版本记录。

## 输入和模板

准备排序索引长读长BAM和一致参考，先运行cuteSV --help。下方为需替换输入的单样本模板，本轮未安装或执行：

```bash
mkdir -p cuteSV-work
cuteSV sample.bam reference.fa sample.sv.vcf cuteSV-work --threads 4 --genotype
```

不同平台的推荐聚类参数应读[官方README](https://github.com/tjiangHIT/cuteSV)，不能把另一平台的参数直接作为默认答案。本模板显式加--genotype；仅发现而未开启该选项时不能期待已估计GT。

## 提取前的检查

核对SVTYPE、SVLEN、END和插入序列是否真实给出，支持reads和GT/GQ的定义以原生头部为准。支持数不同不一定意味着候选更可信；覆盖、分裂比对和聚类都会影响计数。

与Sniffles做交并集时先进行[SV事件匹配与一对一评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SV%E4%BA%8B%E4%BB%B6%E5%8C%B9%E9%85%8D%E4%B8%8E%E4%B8%80%E5%AF%B9%E4%B8%80%E8%AF%84%E4%BC%B0)，不能只按POS连接表。人工Sniffles案例没有实测cuteSV，也不构成二者排名。
