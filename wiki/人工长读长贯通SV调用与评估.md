# 人工长读长贯通SV调用与评估

> 更新：2026-10-15；状态：可用；验证范围：对应人工/官方微型案例已实际运行；具体范围见正文。

实际从人工DNA reads比对到Sniffles调用、群体输出和Truvari两事件核对，并保留发现的格式问题。

## 环境与运行

[下载项目ZIP](https://github.com/SpiralKernel/bioinfo-wiki/archive/refs/heads/main.zip)并解压，在含README.md与examples的项目根目录运行。已有Conda时：

```bash
conda env create -f examples/environments/variant-calling.yml
conda run -n wiki-variant-calling python examples/variant_calling_demo.py
```

以下按Linux x86_64终端整理；Windows需适用Linux环境，其他系统未逐一实测。环境YAML按本机实际成功安装的同一组Conda软件约束整理，未另在各系统重建。环境包含Python/pysam、minimap2、samtools、Sniffles、Truvari及FreeBayes；实际Linux版本见[维护记录](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/maintenance/variant-detection-round2-2026-10-15.md)。非PATH工具可设对应的MINIMAP2_BIN、SAMTOOLS_BIN、SNIFFLES_BIN、TRUVARI_BIN等绝对路径。

默认输出examples/output/calling-sv，非空目录拒绝覆盖。另练习用`--output examples/output/calling-sv-practice2`指定新目录；只运行小变异例用`--case small`，见[FreeBayes小变异与倍性设置](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FreeBayes%E5%B0%8F%E5%8F%98%E5%BC%82%E4%B8%8E%E5%80%8D%E6%80%A7%E8%AE%BE%E7%BD%AE)。

## 输入与实际链路

固定种子20261015生成100kb人工参考，V01为含500bp DEL和300bp INS的人工杂合样本，R01为参考对照；每个样本160条完美16kb DNA reads。minimap2用map-hifi仅为教学配置，不模拟真实HiFi错误。

先读[变异发现联合分型与缺失状态](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E5%8F%91%E7%8E%B0%E8%81%94%E5%90%88%E5%88%86%E5%9E%8B%E4%B8%8E%E7%BC%BA%E5%A4%B1%E7%8A%B6%E6%80%81)：候选发现→中间证据→群体调用→在已知事件重新分型。具体为排序/索引BAM→单样本Sniffles VCF+SNF→SNF群体调用；另以V01候选在R01 BAM执行force。Truvari只评估V01相对两个已知人工事件，限定BED[10000,90000)、距离100、序列与大小相似度0.7、PASS及单匹配。

小参考显式使用`--all-contigs`，该参数不是实际物种自动推荐。群体步骤同时传参考并核对序列锚点。源码[variant_calling_demo.py](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/variant_calling_demo.py)。

## 实际结果与重要反例

| 检查 | 实际结果 |
|---|---|
| V01单样本发现 | DEL/INS各1，GT均0/1 |
| R01单样本发现 | 0条候选，不自动当全参考分型 |
| SNF群体VCF | 2事件；V01为0/1，R01保留./. |
| Truvari事件与GT | TP-base=TP-comp=2、FP/FN=0；匹配GT一致2 |
| R01 force原生文件 | FORMAT键数不一致，样本名继承候选，未直接作为合法结果使用 |
| 受限派生兼容副本 | 两事件GT为0/0，但GQ均0；保留DR/DV和修正记录 |

Truvari得分只针对两个易例，不代表真实SV准确率、复杂类型或全基因组性能。R01 force的低GQ也不应表述成高置信参考。

## 格式问题如何处理

本机Sniffles2.8.1 force输出FORMAT为GT:GQ:DR:DV，样本有第5个PS占位；原生头部样本名继承V01。程序保留raw，检查genotypeSource确为已验证的Sniffles2.8.1、已声明PS、单样本且精确符合已知4键/5值末尾点的模式后，在独立.compat副本补PS。经BAM RG确认实际样本R01后另记表头改名，保存原名/新名和两文件SHA；不改GT/GQ/DR/DV或INFO。

未知格式异常拒绝兼容处理，不能把这段逻辑当通用VCF修复器。DR/DV按本次头部分别为参考/替代支持read数，GQ为分型质量，PS为相位块字段；兼容副本未提升这些质量。force的INFO SUPPORT/VAF/COVERAGE可来自候选记录，当前样本证据读FORMAT，不能把继承INFO当R01支持。

公开汇总、图和原始/派生核对记录在[结果目录](https://github.com/SpiralKernel/bioinfo-wiki/tree/main/assets/variant-detection-round2)。真实SV调用、其他平台、INV/DUP/BND及低频/多倍体性能未在本例验证。

## 去哪里核对产物

| 文件 | 用途与本例检查 |
|---|---|
| V01.vcf / R01.vcf | 分别有2条/0条候选 |
| cohort.vcf | 两个样本列，R01仍为./. |
| bench/summary.json | TP-base/TP-comp、FP/FN及GT一致性 |
| R01.force.vcf | 原生输出，保留格式异常供审计 |
| R01.force.compat.vcf | 受限格式/样本表头兼容副本，GQ=0仍非可信阴性 |
| summary.json / commands.json | 汇总及实际命令记录 |

成功运行会打印汇总。在项目根目录可用`conda run -n wiki-variant-calling python -m json.tool examples/output/calling-sv/summary.json`查看；再次运行请换新输出目录。

## 配图

配图另需Matplotlib；例如`conda install -n wiki-variant-calling -c conda-forge matplotlib`后，在项目根目录运行`conda run -n wiki-variant-calling python examples/plot_variant_calling.py`。需先完成SV和TRGT两个案例，默认读取其summary，图保存examples/output/variant-calling-plots。

![人工SV与官方重复分型单位核对](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/variant-detection-round2/calling-and-repeat.png)
