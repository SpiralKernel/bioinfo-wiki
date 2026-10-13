# 从DNA到RNA和蛋白质

> 更新：2026-10-13；状态：可用；验证范围：文档核对；纸面例子核算；外部分析未在本机执行。

区分基因、转录本和蛋白质层级，是理解不同组学测量对象和标识符的起点。

## 一个基因为什么不只对应一行

基因是与功能产物相关的基因组区域；产物可以是RNA，也可能经翻译产生蛋白质。转录把DNA信息用于生成RNA；翻译根据编码序列生成蛋白质。并非所有基因都编码蛋白，也不是测到RNA增加就能保证蛋白同比增加。

真核转录本可经剪接形成不同形式。外显子是保留在相应成熟转录本中的部分，内含子是其中被剪除的部分；外显子并不全部编码蛋白，还可能包含非翻译区域。CDS是编码序列，不能与整个转录本序列等同。

## 三个分析层级

同一个基因可以有多个转录本，不同转录本可能产生不同蛋白异构体。基因层面的计数合并了部分转录本信息；转录本层面的变化也可能在基因总量中不明显。参考注释中的模型是当前资源对结构的表示，版本变化会影响定量和映射。

DNA变异、RNA表达和蛋白丰度测量不同对象。[组学分析总览与选型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E5%88%86%E6%9E%90%E6%80%BB%E8%A7%88%E4%B8%8E%E9%80%89%E5%9E%8B)帮助选择测量层级；[基因标识符与同源基因](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E6%A0%87%E8%AF%86%E7%AC%A6%E4%B8%8E%E5%90%8C%E6%BA%90%E5%9F%BA%E5%9B%A0)解释如何在层级之间映射。

## 最小练习

按[Ensembl参考与注释查询](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Ensembl%E5%8F%82%E8%80%83%E4%B8%8E%E6%B3%A8%E9%87%8A%E6%9F%A5%E8%AF%A2)查看一个有多个转录本的基因，找出基因ID、一个转录本ID和一个蛋白ID；对照转录本全长与CDS，说明为什么长度不必相等。再解释基因计数表的一行为什么不总对应一个唯一蛋白。

深入：[NHGRI基因定义](https://www.genome.gov/genetics-glossary/Gene)、[NHGRI转录解释](https://www.genome.gov/genetics-glossary/Transcription)、[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)。
