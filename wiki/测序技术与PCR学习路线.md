# 测序技术与PCR学习路线

> 更新：2026-10-14；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

从PCR、文库和信号读出理解测序，再按目标选择技术、数据和质量检查。

## 先建立整条脉络

PCR扩增特定区域，建库让分子适合测序，仪器将分子相关信号转为数据，生信再做碱基识别、比对和推断。这些环节可以关联，但PCR不是所有测序共有的必经步骤。

一、二、三代是常用教学分类，并非严格统一标准，也不表示后出现的一代在所有任务上都更好。

## 一、二、三代怎样对应

| 常用分类 | 代表路线 | 理解重点 |
|---|---|---|
| 一代 | Sanger链终止 | 有限目标片段与峰图判读 |
| 二代 | Illumina、DNBSEQ、半导体等大规模并行路线 | 高通量、模板放大与短读长信息 |
| 三代 | 常以PacBio、Nanopore单分子路线为代表 | 长分子、实时读出及平台特定共识/信号模型 |

长读长与单分子描述不同属性；准确性应区分原始读出和最终共识，不能简化成“代数越高越准确”或“长读长必然不准确”。

## 推荐顺序

1. [PCR与扩增基础](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PCR%E4%B8%8E%E6%89%A9%E5%A2%9E%E5%9F%BA%E7%A1%80) → [引物扩增子与特异性](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%BC%95%E7%89%A9%E6%89%A9%E5%A2%9E%E5%AD%90%E4%B8%8E%E7%89%B9%E5%BC%82%E6%80%A7) → [RT-PCR实时PCR与数字PCR的区别](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RT-PCR%E5%AE%9E%E6%97%B6PCR%E4%B8%8E%E6%95%B0%E5%AD%97PCR%E7%9A%84%E5%8C%BA%E5%88%AB)。
2. [DNA与RNA样本质量及建库偏差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DNA%E4%B8%8ERNA%E6%A0%B7%E6%9C%AC%E8%B4%A8%E9%87%8F%E5%8F%8A%E5%BB%BA%E5%BA%93%E5%81%8F%E5%B7%AE) → [文库接头索引与条形码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%96%87%E5%BA%93%E6%8E%A5%E5%A4%B4%E7%B4%A2%E5%BC%95%E4%B8%8E%E6%9D%A1%E5%BD%A2%E7%A0%81) → [单端双端读长与插入片段](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8D%95%E7%AB%AF%E5%8F%8C%E7%AB%AF%E8%AF%BB%E9%95%BF%E4%B8%8E%E6%8F%92%E5%85%A5%E7%89%87%E6%AE%B5)。
3. [Sanger测序原理与峰图判读](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Sanger%E6%B5%8B%E5%BA%8F%E5%8E%9F%E7%90%86%E4%B8%8E%E5%B3%B0%E5%9B%BE%E5%88%A4%E8%AF%BB) → [第二代测序原理与平台比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%AC%AC%E4%BA%8C%E4%BB%A3%E6%B5%8B%E5%BA%8F%E5%8E%9F%E7%90%86%E4%B8%8E%E5%B9%B3%E5%8F%B0%E6%AF%94%E8%BE%83)。
4. [Illumina合成测序与簇信号](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Illumina%E5%90%88%E6%88%90%E6%B5%8B%E5%BA%8F%E4%B8%8E%E7%B0%87%E4%BF%A1%E5%8F%B7)、[DNBSEQ测序与滚环扩增](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DNBSEQ%E6%B5%8B%E5%BA%8F%E4%B8%8E%E6%BB%9A%E7%8E%AF%E6%89%A9%E5%A2%9E)、[半导体测序与同聚物信号](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8D%8A%E5%AF%BC%E4%BD%93%E6%B5%8B%E5%BA%8F%E4%B8%8E%E5%90%8C%E8%81%9A%E7%89%A9%E4%BF%A1%E5%8F%B7)。
5. [PacBioSMRT与HiFi测序](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PacBioSMRT%E4%B8%8EHiFi%E6%B5%8B%E5%BA%8F)、[Nanopore测序与直接RNA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Nanopore%E6%B5%8B%E5%BA%8F%E4%B8%8E%E7%9B%B4%E6%8E%A5RNA)。
6. [碱基识别质量值与一致性序列](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%A2%B1%E5%9F%BA%E8%AF%86%E5%88%AB%E8%B4%A8%E9%87%8F%E5%80%BC%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E5%BA%8F%E5%88%97) → [测序错误重复偏差与嵌合体](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E9%94%99%E8%AF%AF%E9%87%8D%E5%A4%8D%E5%81%8F%E5%B7%AE%E4%B8%8E%E5%B5%8C%E5%90%88%E4%BD%93) → [测序深度覆盖度与质量分数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E6%B7%B1%E5%BA%A6%E8%A6%86%E7%9B%96%E5%BA%A6%E4%B8%8E%E8%B4%A8%E9%87%8F%E5%88%86%E6%95%B0)。
7. [测序方案选型与实验设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E6%96%B9%E6%A1%88%E9%80%89%E5%9E%8B%E4%B8%8E%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1) → [从样本到FASTQ的交接与质控](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BB%8E%E6%A0%B7%E6%9C%AC%E5%88%B0FASTQ%E7%9A%84%E4%BA%A4%E6%8E%A5%E4%B8%8E%E8%B4%A8%E6%8E%A7)。

## 按任务继续

靶区域查[扩增子测序与靶向测序设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%89%A9%E5%A2%9E%E5%AD%90%E6%B5%8B%E5%BA%8F%E4%B8%8E%E9%9D%B6%E5%90%91%E6%B5%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1)；RNA查[RNA测序建库选择与偏倚](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%B5%8B%E5%BA%8F%E5%BB%BA%E5%BA%93%E9%80%89%E6%8B%A9%E4%B8%8E%E5%81%8F%E5%80%9A)与[链特异性与RNA测序方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%93%BE%E7%89%B9%E5%BC%82%E6%80%A7%E4%B8%8ERNA%E6%B5%8B%E5%BA%8F%E6%96%B9%E5%90%91)；组装查[混合测序组装与结果评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B7%B7%E5%90%88%E6%B5%8B%E5%BA%8F%E7%BB%84%E8%A3%85%E4%B8%8E%E7%BB%93%E6%9E%9C%E8%AF%84%E4%BC%B0)及[N50组装连续性与完整性](https://github.com/SpiralKernel/bioinfo-wiki/wiki/N50%E7%BB%84%E8%A3%85%E8%BF%9E%E7%BB%AD%E6%80%A7%E4%B8%8E%E5%AE%8C%E6%95%B4%E6%80%A7)。

定量查[qPCR与数字PCR结果判读](https://github.com/SpiralKernel/bioinfo-wiki/wiki/qPCR%E4%B8%8E%E6%95%B0%E5%AD%97PCR%E7%BB%93%E6%9E%9C%E5%88%A4%E8%AF%BB)；文件查[测序数据格式与原始信号](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E4%B8%8E%E5%8E%9F%E5%A7%8B%E4%BF%A1%E5%8F%B7)；报告查[测序质控工具选择与报告阅读](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E8%B4%A8%E6%8E%A7%E5%B7%A5%E5%85%B7%E9%80%89%E6%8B%A9%E4%B8%8E%E6%8A%A5%E5%91%8A%E9%98%85%E8%AF%BB)。数量口径见[测序产量有效数据与成本口径](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E4%BA%A7%E9%87%8F%E6%9C%89%E6%95%88%E6%95%B0%E6%8D%AE%E4%B8%8E%E6%88%90%E6%9C%AC%E5%8F%A3%E5%BE%84)，计算见[人工区间贯通测序指标](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E5%8C%BA%E9%97%B4%E8%B4%AF%E9%80%9A%E6%B5%8B%E5%BA%8F%E6%8C%87%E6%A0%87)。

## 学完应能判断什么

能区分模板分子、扩增拷贝与读段，知道PE150不是连续300碱基读段，知道高平均深度不能保证所有区域可靠；能核对平台、建库、模型、数据阶段和参考版本。

本轮为原理、设计与判读指南，没有执行PCR、建库或测序仪。人工计算只能核对指标定义，不能替代真实平台验证。

来源：[NHGRI PCR](https://www.genome.gov/about-genomics/fact-sheets/Polymerase-Chain-Reaction-Fact-Sheet)、[Illumina单双端](https://www.illumina.com/science/technology/next-generation-sequencing/plan-experiments/paired-end-vs-single-read.html)、[PacBio HiFi](https://www.pacb.com/technology/hifi-sequencing/how-it-works/)、[Nanopore原理](https://nanoporetech.com/platform/technology/)。

## DNA测序之后

变异目标与平台条件由[变异检测分型与提取学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E5%88%86%E5%9E%8B%E4%B8%8E%E6%8F%90%E5%8F%96%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)衔接，区分长短读长小变异、SV、CNV/PAV和重复相关任务。测序产量或读长本身不能证明所有类型已经准确检出。
