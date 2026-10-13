# UniProt蛋白条目与证据

> 更新：2026-10-13；状态：可用；验证范围：官方文档核对；检索与批量下载练习未在本机执行。

蛋白数据库条目同时包含序列和注释证据，人工审阅状态不等于每项功能都已实验验证。

## 从什么字段开始读

先核对accession、物种、蛋白名称和序列版本，再看功能、亚细胞定位、结构域、交叉引用及证据。UniProtKB包含经过人工审阅的Swiss-Prot部分与尚未完整人工审阅的TrEMBL部分；审阅状态和蛋白存在证据是不同概念。

同一个基因可能有多个异构体；数据库中的canonical序列是代表形式，并不自动代表每个组织的主要形式。下载FASTA时明确是否包含异构体，以及使用的是全库还是特定物种的proteome。

## 一次条目阅读练习

在[UniProtKB入口](https://www.uniprot.org/entry)按已知基因和物种查一个条目，记录ID、审阅状态、序列长度和一项功能注释。展开其证据或引用，说明该信息来自实验、人工综合还是计算推断。再查看交叉引用，核对与Ensembl基因或转录本的对应。

本页尚未批量调用API。正式下载应记录数据库release、查询条件、是否包含异构体、校验值和映射失败记录；[条目历史](https://www.uniprot.org/help/entry_history)可以追溯序列与注释更新。

## 在分析中怎样使用

[蛋白质组入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%9B%8B%E7%99%BD%E8%B4%A8%E7%BB%84%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)需要明确参考蛋白库和共享肽段导致的protein group。[BLAST本地检索实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLAST%E6%9C%AC%E5%9C%B0%E6%A3%80%E7%B4%A2%E5%AE%9E%E8%B7%B5)使用蛋白参考时，也要说明库的范围与版本；一个最佳命中不能取代证据阅读。

深入：[UniProt proteome说明](https://www.uniprot.org/help/proteome)、[官方查询接口说明](https://www.uniprot.org/help/api_queries)、[基因标识符与同源基因](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E6%A0%87%E8%AF%86%E7%AC%A6%E4%B8%8E%E5%90%8C%E6%BA%90%E5%9F%BA%E5%9B%A0)。
