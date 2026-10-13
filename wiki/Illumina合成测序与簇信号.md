# Illumina合成测序与簇信号

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

Illumina通过簇上合成与循环信号读出序列，化学和簇生成方式因产品而异。

## 从文库到簇

文库带有适合平台的结构，形成可读簇以提供足够信号。桥式扩增是经典解释；某些patterned flow cell有不同簇生成机制，不能将所有型号写成相同桥式流程。

文库PCR与仪器相关簇生成不是同一阶段。PCR-free建库不表示后续完全没有信号放大，也不表示没有样本偏差。

## 合成测序

SBS在逐轮合成中识别加入的碱基。光学通道和化学变化，因此“四种碱基永远对应四种独立颜色”并非普遍定律。basecaller由循环信号估计序列和质量。

分子失去同步会影响后续信号，phasing/prephasing描述相应问题；实际质量还受文库多样性、化学和模型影响。

## 单双端和索引

R1、index read和R2各有布局。索引用于拆分样本，不是应保留进常规目标比对的序列；R1/R2角色也依文库确认。见[文库接头索引与条形码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%96%87%E5%BA%93%E6%8E%A5%E5%A4%B4%E7%B4%A2%E5%BC%95%E4%B8%8E%E6%9D%A1%E5%BD%A2%E7%A0%81)、[单端双端读长与插入片段](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8D%95%E7%AB%AF%E5%8F%8C%E7%AB%AF%E8%AF%BB%E9%95%BF%E4%B8%8E%E6%8F%92%E5%85%A5%E7%89%87%E6%AE%B5)。

仪器数据经识别、拆分后形成常见FASTQ。记录运行/试剂、布局、样本表、软件与质量，Q30比例不能代替全部检查。

来源：[SBS官方说明](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology.html)、[索引说明](https://support-docs.illumina.com/SHARE/IndexedSeq/Content/SHARE/IndexedSequencing/IndexedSeqIntro.htm)。
