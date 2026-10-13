# PacBioSMRT与HiFi测序

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

PacBio记录单分子实时合成，HiFi利用同一环状模板多次通过形成高准确共识。

## 单分子实时合成

SMRT观察聚合酶相关合成信号。SMRTbell将插入片段置于环状结构，使同一分子可多次通过；subread、polymerase read和最终CCS/HiFi read不是同一计数单位。

HiFi由重复观测形成共识。多次pass通常来自同一原始分子，不能当多个独立样本或独立覆盖分子。

## 长度与准确性

片段、模板、运行与处理影响读长、pass和可用产量。单次原始经过的错误率不能代表最终HiFi，也不能把历史CLR与HiFi混成一种数据。

“长读长都低准确”过度概括；记录read类型、过滤、质量模型和化学版本，不能给所有项目统一准确率保证。

## 修饰和文件

原生DNA动力学可用于特定修饰分析，依赖模型、覆盖与建库；扩增/转换后的模板不自动保留同样信息。按任务保存HiFi序列、BAM相关标签/动力学、SMRT Link/CCS版本和处理记录。RNA还要区分Iso-Seq/cDNA来源。

来源：[HiFi官方原理](https://www.pacb.com/technology/hifi-sequencing/how-it-works/)、[Wenger等原始研究](https://www.nature.com/articles/s41587-019-0217-9)。下游见[长读长测序分析入门](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%95%BF%E8%AF%BB%E9%95%BF%E6%B5%8B%E5%BA%8F%E5%88%86%E6%9E%90%E5%85%A5%E9%97%A8)。
