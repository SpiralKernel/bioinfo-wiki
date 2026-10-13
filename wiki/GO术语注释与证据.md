# GO术语注释与证据

> 更新：2026-10-13；验证范围：官方文档核对；检索与批量下载练习未在本机执行。

GO用结构化术语描述基因产物相关功能，术语、注释关系和证据类型需要分开阅读。

## 三个方面

GO包括生物过程BP、分子功能MF和细胞组分CC。它们分别从过程、活动与位置等角度描述知识；不是三个可直接互换的通路名称。GO术语通过不同关系连接，不能把整个结构理解成一棵只有一种父子关系的分类树。

注释将基因产物联系到术语，并携带证据代码、来源等信息。术语的定义与某个基因是否被注释到该术语是两件事。没有注释可能因为研究不足或资源覆盖，不直接说明没有相应功能。

## 怎样核对一条注释

用[GO官方概览](https://www.geneontology.org/docs/ontology-documentation/)选择一个术语，记录GO ID、名称、定义与所属方面；查看相关注释时再记录基因产物ID、物种、关系、证据及参考文献。依据[证据代码说明](https://www.geneontology.org/docs/guide-go-evidence-codes/)区分实验和不同计算来源，不将所有注释视为同等实验结论。

本页未运行大批量注释查询。做批量映射时记录ontology和annotation版本、ID转换规则、未匹配条目和是否处理过时术语。

## 与富集结果的关系

[富集分析与GSEA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8EGSEA)比较的是指定背景与基因集合下的统计模式。相似或重叠GO术语可能来自共享基因和术语关系；显著术语数量不等于独立机制数量。解释时查看驱动基因和效应方向，并回到原始注释证据。

深入：[GO注释入门](https://www.geneontology.org/docs/introduction-to-go-annotations/)、[GO富集说明](https://www.geneontology.org/docs/go-enrichment-analysis/)、[公共数据库与数据获取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%85%B1%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8E%E6%95%B0%E6%8D%AE%E8%8E%B7%E5%8F%96)。
