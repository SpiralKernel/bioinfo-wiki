# SRA与ENA读段检索

> 更新：2026-10-13；验证范围：官方文档核对；检索与批量下载练习未在本机执行。

读段归档中的study、sample、experiment与run有不同层级，下载与合并必须保留这些关系。

## 层级怎样理解

Study组织一项研究；Sample描述生物材料；Experiment记录文库与测序方案；Run关联一次运行的数据文件。一个样本可以有多个文库或run，因此十个run不一定是十个独立生物学重复。

SRA与ENA提供相关归档数据的访问入口，具体文件形式与可用字段按所选资源核对。双端测序、重复测序和技术拆分都要回到元数据判断，不能仅凭文件名后缀决定合并。

## 下载前先导出清单

从研究编号查询run表，保留研究、样本、实验、run、物种、平台、文库策略、单双端、大小、文件链接和校验值。再把run与论文中的组别、个体和批次对应。无法对应时先解决元数据，避免下载后给数据贴错标签。

确认存储容量、可用访问方式和是否受限；按官方接口下载并验证校验值。压缩文件大小不等于后续比对空间，资源评估见[服务器资源与批量任务](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%9C%8D%E5%8A%A1%E5%99%A8%E8%B5%84%E6%BA%90%E4%B8%8E%E6%89%B9%E9%87%8F%E4%BB%BB%E5%8A%A1)。

## 一个可检查的练习

使用[ENA检索下载指南](https://ena-docs.readthedocs.io/en/latest/retrieval/general-guide.html)选择其公开示例，只导出run及文件信息。找到一个存在多个run的样本，解释它们是独立个体还是同一样本的技术记录。完成下载后再按[FASTA与FASTQ](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FASTA%E4%B8%8EFASTQ)检查格式、读段配对与样本对应。

本页尚未实际下载归档读段。合并方案、下载命令和参考资源需与具体研究及所用工具版本一起记录。

深入：[ENA对象关系说明](https://ena-docs.readthedocs.io/en/latest/submit/reads/programmatic.html)、[NCBI SRA入口](https://www.ncbi.nlm.nih.gov/sra)、[结果报告与数据共享](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%93%E6%9E%9C%E6%8A%A5%E5%91%8A%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%85%B1%E4%BA%AB)。
