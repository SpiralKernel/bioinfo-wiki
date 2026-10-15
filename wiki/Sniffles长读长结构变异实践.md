# Sniffles长读长结构变异实践

> 更新：2026-10-15；状态：可用；验证范围：Sniffles2.8.1人工DEL/INS、SNF、force及格式兼容实测；真实物种/mosaic未测。

Sniffles相应模式从长读长比对发现SV，群体模式与已知位点分型需要不同输入。

## 输入与准备

按[Sniffles官方说明](https://github.com/fritzsedlazeck/Sniffles)固定版本和安装环境，确认`sniffles --help`。准备PacBio/ONT对应的比对BAM/CRAM及索引、样本信息和相同参考；注意长reads分裂/补充比对及原始比对设置。

本页模板按Sniffles2整理；本轮Sniffles2.8.1已在[人工长读长贯通SV调用与评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E9%95%BF%E8%AF%BB%E9%95%BF%E8%B4%AF%E9%80%9ASV%E8%B0%83%E7%94%A8%E4%B8%8E%E8%AF%84%E4%BC%B0)实际运行。真实物种、mosaic及其他复杂类型未测。软件、参考、覆盖和平台参数需跟随所选版本记录。

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

## 本版实测问题

人工小参考需--all-contigs；固定样本ID并在群体步骤传匹配参考。SNF群体调用的R01保留缺失，未强制填0/0。

本机2.8.1 force原生文件出现FORMAT键数及继承样本表头问题，案例保留raw与严格受限.compat副本，并记录已知版本、原名/新名和SHA。force的INFO支持可继承候选，读取当前样本FORMAT证据；GQ=0不作为可信阴性。完整操作只维护在[人工长读长贯通SV调用与评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E9%95%BF%E8%AF%BB%E9%95%BF%E8%B4%AF%E9%80%9ASV%E8%B0%83%E7%94%A8%E4%B8%8E%E8%AF%84%E4%BC%B0)。
