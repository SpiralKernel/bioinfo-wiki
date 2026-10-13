# Ensembl参考与注释查询

> 更新：2026-10-13；状态：可用；验证范围：官方文档核对；检索与批量下载练习未在本机执行。

Ensembl把参考组装、基因模型、变异与同源信息联系起来，查询结果必须携带物种和发布版本。

## 查询前确定四件事

物种是什么、参考组装是哪版、需要基因还是转录本层级、所用ID是哪套。一个基因可以有多个转录本和蛋白产物；基因名、稳定ID和坐标也不是可无条件互换的字段。基础见[参考基因组与注释版本](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%82%E8%80%83%E5%9F%BA%E5%9B%A0%E7%BB%84%E4%B8%8E%E6%B3%A8%E9%87%8A%E7%89%88%E6%9C%AC)和[基因标识符与同源基因](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E6%A0%87%E8%AF%86%E7%AC%A6%E4%B8%8E%E5%90%8C%E6%BA%90%E5%9F%BA%E5%9B%A0)。

## 单个基因查询练习

按[Ensembl官方教程](https://www.ensembl.org/info/website/tutorials/index.html)选择一个示例基因。记录物种、组装、基因ID、位置、链方向和转录本列表；导出一个转录本序列时说明取的是cDNA、CDS还是蛋白，不能统称为“基因序列”。再查看同源关系及其证据，说明是直系还是旁系。

导出区间时核对[基因组坐标与区间](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E5%9D%90%E6%A0%87%E4%B8%8E%E5%8C%BA%E9%97%B4)。在负链上“上游”与数值更小的坐标并非始终同义，应根据基因方向和工具约定定义范围。

## 多个ID怎样批量查询

使用BioMart或官方API时先选数据集、过滤条件和输出字段，用少数已知ID测试，再处理全部列表。保存未匹配及一对多映射，不应让内连接悄悄丢失基因，也不应因重复映射放大[富集分析与GSEA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8EGSEA)的计数。

记录release或归档站点；本页没有运行批量API查询。变异后果分析见[变异注释与候选证据整理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%B3%A8%E9%87%8A%E4%B8%8E%E5%80%99%E9%80%89%E8%AF%81%E6%8D%AE%E6%95%B4%E7%90%86)，实际检索页面可能随站点更新变化，应以官方教程对应版本为准。

深入：[稳定ID说明](https://www.ensembl.org/info/genome/stable_ids/index.html)、[BioMart文档](https://www.ensembl.org/info/data/biomart/index.html)、[公共数据库与数据获取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%85%B1%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8E%E6%95%B0%E6%8D%AE%E8%8E%B7%E5%8F%96)。
