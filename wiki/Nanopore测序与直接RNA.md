# Nanopore测序与直接RNA

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

Nanopore根据分子过孔电信号识别序列，原生DNA、cDNA和直接RNA是不同路线。

## 电信号到序列

核酸通过孔时产生与局部序列有关的电信号，basecaller将其转成碱基。孔、试剂、模型和处理决定结果，不能将早期准确率固定套到当前数据。

simplex和duplex涉及不同证据与处理。是否有足够双链信息、怎样组合依实际模型；duplex不表示所有read有双倍独立分子覆盖。

## RNA相关路线

直接RNA读取原始RNA相关信号；cDNA读取逆转录产物；PCR-cDNA还经过扩增。直接RNA流程可有辅助cDNA合成，但不能因此说被读出的分子是cDNA。

这些路线对转录本、端点、长度、输入和修饰有不同影响。直接RNA也不自动覆盖每条RNA全长或全部种类。

## 原始数据与交接

POD5保存原始读出，FASTQ只保留已识别序列与质量。重识别和某些修饰分析可能需要POD5和模型；修饰预测不是FASTQ直接存在的普通字母标签。

保存孔/化学、文库、basecaller/模型、长度/质量分布、拆分与原始信号策略。N50不代表组装正确，修饰还需相应验证。

来源：[ONT技术](https://nanoporetech.com/platform/technology/)、[Dorado](https://software-docs.nanoporetech.com/dorado/latest/)、[POD5](https://github.com/nanoporetech/pod5-file-format)。
