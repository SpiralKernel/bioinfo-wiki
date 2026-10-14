# Sniffles长读长结构变异实践

> 更新：2026-10-14；状态：可用；验证范围：官方文档与原始研究核对；专业检测命令为模板，未执行完整真实数据流程。

Sniffles相应模式从长读长比对发现SV，群体模式与已知位点分型需要不同输入。

## 输入与准备

按[Sniffles官方说明](https://github.com/fritzsedlazeck/Sniffles)固定版本和安装环境，确认`sniffles --help`。准备PacBio/ONT对应的比对BAM/CRAM及索引、样本信息和相同参考；注意长reads分裂/补充比对及原始比对设置。

本页按核对时Sniffles2接口整理模板，未运行该软件。软件、参考、覆盖和平台参数需跟随所选版本记录。

## 单样本与群体模板

```bash
sniffles --input S01.bam --reference ref.fa --vcf S01.sv.vcf --snf S01.snf
sniffles --input S02.bam --reference ref.fa --vcf S02.sv.vcf --snf S02.snf
sniffles --input S01.snf S02.snf --vcf cohort.sv.vcf
```

SNF包含群体模式需要的中间信息，不是VCF文件改后缀。参考有助于相应序列输出；群体结果仍需核对样本、缺失、类型和分型质量。

## 已知位点的再分型

```bash
sniffles --input S01.bam --genotype-vcf known.sv.vcf --vcf S01.regenotyped.vcf
```

这里评估已知集合，不等于无偏发现全部新事件。输出事件可能以符号或序列表示，先读头部，再按[按类型提取SNPIndel与结构变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%8C%89%E7%B1%BB%E5%9E%8B%E6%8F%90%E5%8F%96SNPIndel%E4%B8%8E%E7%BB%93%E6%9E%84%E5%8F%98%E5%BC%82)操作；缺失不填参考。

## 检查点

分类型和大小看支持与质量，回查复杂区域和候选reads，按[变异评估真值集合与可检测区域](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E8%AF%84%E4%BC%B0%E7%9C%9F%E5%80%BC%E9%9B%86%E5%90%88%E4%B8%8E%E5%8F%AF%E6%A3%80%E6%B5%8B%E5%8C%BA%E5%9F%9F)评估。非生殖系模式是另外的假设，不能凭低频就套用默认二倍体解释。原理见[结构变异检测的读对分裂读段与组装](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%93%E6%9E%84%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E7%9A%84%E8%AF%BB%E5%AF%B9%E5%88%86%E8%A3%82%E8%AF%BB%E6%AE%B5%E4%B8%8E%E7%BB%84%E8%A3%85)，原始论文：[Sniffles2](https://doi.org/10.1038/s41587-023-02024-y)。
