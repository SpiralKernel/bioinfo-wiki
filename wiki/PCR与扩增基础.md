# PCR与扩增基础

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

PCR利用引物和聚合酶扩增目标区域，扩增拷贝不等于新增独立信息。

## 解决什么问题

PCR使少量目标DNA区域产生更多拷贝，便于检测或测序。RNA通常先逆转录为cDNA，见[RT-PCR实时PCR与数字PCR的区别](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RT-PCR%E5%AE%9E%E6%97%B6PCR%E4%B8%8E%E6%95%B0%E5%AD%97PCR%E7%9A%84%E5%8C%BA%E5%88%AB)。

基本组成有模板、引物、聚合酶和核苷酸。分链、引物结合与延伸的循环让目标拷贝增加；具体实验条件依所选试剂和验证设计，本页解释原理。

## 拷贝增加与信息

理想指数模型为 $N_c=N_0(1+E)^c$，E为每轮相对扩增效率。实际效率不一定恒定，后期可进入平台阶段，因此终点产量不能直接精确反推起始模板数。

同一原始分子的扩增拷贝相关，不能当新独立样本。早期错误、不同目标效率和等位基因脱落会影响序列与定量。

## 与测序连接

扩增子测序先用PCR选目标；一些文库进行扩增；一些平台另有簇形成或信号放大。原生单分子测序不要求所有模板先PCR，PCR-free必须说明指哪个阶段。

需要区分目标身份、特异性、对照、污染和抑制。产物大小或终点信号不单独证明目标正确，也不代表完成定量。

下一步见[引物扩增子与特异性](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%BC%95%E7%89%A9%E6%89%A9%E5%A2%9E%E5%AD%90%E4%B8%8E%E7%89%B9%E5%BC%82%E6%80%A7)、[扩增子测序与靶向测序设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%89%A9%E5%A2%9E%E5%AD%90%E6%B5%8B%E5%BA%8F%E4%B8%8E%E9%9D%B6%E5%90%91%E6%B5%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1)。来源：[NHGRI PCR](https://www.genome.gov/about-genomics/fact-sheets/Polymerase-Chain-Reaction-Fact-Sheet)、[MIQE 2.0](https://pubmed.ncbi.nlm.nih.gov/40272429/)。
