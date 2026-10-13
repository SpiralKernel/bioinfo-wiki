# RNA测序建库选择与偏倚

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

富集、去除、逆转录、链特异和read布局决定可观察RNA及计数方式。

## 建库改变测量对象

| 路线/维度 | 主要影响 |
|---|---|
| poly(A)相关富集 | 更偏向相应有尾RNA，不覆盖所有类型 |
| rRNA去除 | 保留范围依试剂和样本 |
| 3′/5′端计数 | 端部信号不自动恢复完整异构体 |
| 小RNA | 特定长度和连接对象选择 |
| 链特异 | 来源方向与软件规则匹配 |
| cDNA与直接RNA | 复制步骤、原生信息和偏差不同 |

逆转录、片段选择和连接影响观测比例，低完整性样本可能有端部偏差。全长方案也需检查实际完整读段比例，不能按名称推定全部全长。

## 下游匹配

差异表达明确计数单位、参考和独立重复；剪接/异构体需连接证据；非编码、小RNA和修饰不默认同一建库。

见[链特异性与RNA测序方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%93%BE%E7%89%B9%E5%BC%82%E6%80%A7%E4%B8%8ERNA%E6%B5%8B%E5%BA%8F%E6%96%B9%E5%90%91)、[PacBioSMRT与HiFi测序](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PacBioSMRT%E4%B8%8EHiFi%E6%B5%8B%E5%BA%8F)、[Nanopore测序与直接RNA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Nanopore%E6%B5%8B%E5%BA%8F%E4%B8%8E%E7%9B%B4%E6%8E%A5RNA)。组别和建库批次不宜完全混杂，平台并非唯一偏差来源。

本页未执行建库。分析见[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)、[小RNA分析入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B0%8FRNA%E5%88%86%E6%9E%90%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)；验证见[转录组差异与qPCR验证设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BD%95%E7%BB%84%E5%B7%AE%E5%BC%82%E4%B8%8EqPCR%E9%AA%8C%E8%AF%81%E8%AE%BE%E8%AE%A1)。流程参考：[nf-core/rnaseq](https://nf-co.re/rnaseq/latest/docs/usage/)。
