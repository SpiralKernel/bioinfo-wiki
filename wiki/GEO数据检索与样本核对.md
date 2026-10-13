# GEO数据检索与样本核对

> 更新：2026-10-13；状态：可用；验证范围：官方文档核对；检索与批量下载练习未在本机执行。

GEO连接研究、样本与处理数据，选择数据前先确认实验设计和矩阵数值含义。

## 三类常见编号

GSE是研究系列，GSM是提交的样本记录，GPL是平台记录。一个GSE可以有多个GSM，平台信息帮助理解测量方法；这些编号不能直接当作三个独立生物学重复。原始测序读段可能另链接到SRA，见[SRA与ENA读段检索](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SRA%E4%B8%8EENA%E8%AF%BB%E6%AE%B5%E6%A3%80%E7%B4%A2)。

## 一次检索的顺序

按研究问题、物种和测量类型搜索 → 阅读研究说明与原论文 → 逐个核对GSM中的来源、处理和重复 → 下载所需元数据与文件清单 → 明确从原始读段还是处理矩阵开始。用[样本表与数据审计实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%A0%B7%E6%9C%AC%E8%A1%A8%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%AE%A1%E8%AE%A1%E5%AE%9E%E8%B7%B5)记录组别、个体、批次与文件对应。

下载Series Matrix或补充表时，要查VALUE列含义、标准化说明、基因标识与缺失编码。文件名含counts也应核对原始处理方法；不能把所有矩阵都送入同一种差异检验。

## 初学练习与完成标准

在[GEO官方数据集说明](https://www.ncbi.nlm.nih.gov/geo/info/datasets.html)中选择一个示例研究，先不下载大文件，整理GSE、GSM、GPL、分组和原始/处理数据入口。完成后应能说清有多少独立样本、是否配对、哪个文件适合下一步分析，哪些元数据仍缺失。

本页提供检索与审计练习，未下载并重新分析指定研究。若目标是RNA-seq差异表达，可先跑[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)的airway小数据，再研究真实GEO项目。

深入：[GEO下载格式与接口](https://www.ncbi.nlm.nih.gov/geo/info/download.html)、[GEO程序访问](https://www.ncbi.nlm.nih.gov/geo/info/geo_paccess.html)、[公共数据库与数据获取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%85%B1%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8E%E6%95%B0%E6%8D%AE%E8%8E%B7%E5%8F%96)。
