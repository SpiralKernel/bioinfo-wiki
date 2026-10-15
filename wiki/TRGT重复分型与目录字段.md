# TRGT重复分型与目录字段

> 更新：2026-10-15；状态：可用；验证范围：对应人工/官方微型案例已实际运行；具体范围见正文。

TRGT从相应HiFi比对对目标串联重复分型；catalog、长度和motif字段应按原生定义读取。

## 环境和输入

本轮实际使用官方TRGT5.1.0-ec66463及PacBio提供的微型例。本轮为Linux x86_64，使用trgt-v5.1.0-x86_64-unknown-linux-gnu.tar.gz；Windows可在适用Linux环境操作，其他平台须按官方release支持核对，未实测。下载[官方release](https://github.com/PacificBiosciences/trgt/releases/tag/v5.1.0)中适合本机的平台文件，核对版本，将TRGT_BIN设为解压后trgt的绝对路径。软件许可和适用数据见[官方协议](https://github.com/PacificBiosciences/trgt/blob/main/LICENSE.md)；本案例只运行PacBio提供的输入，原始fixture通过固定URL下载，不改标为本项目许可。

需要参考FASTA/fai、排序索引HiFi BAM与目标位点BED。catalog指位点定义文件，不是文件夹。本轮固定行是：

```text
chrA    10001    10061    ID=TR1;MOTIFS=CAG;STRUC=<TR>
```

实际文件使用制表符。BED为[10001,10061)，对应1起始重复区10002–10061，共60bp；VCF POS=10001是前一碱基的padding锚点。

## 调用和原生输出

下面是已有输入的接口模板，在包含inputs子目录的工作目录运行；第一次跟做优先执行下方链接的Python包装脚本。设置TRGT_BIN后可用`"$TRGT_BIN" --version`核对，单设变量不会将trgt加入PATH。

```bash
"$TRGT_BIN" genotype --genome inputs/reference.fasta --reads inputs/sample.bam   --repeats inputs/repeat.bed --output-prefix calls --threads 1
```

本轮得到TR1、GT=1/1、AL=33/33bp、MC=11/11。GT是等位索引；AL不含padding，MC在此VCF中为字符串计数。复杂motif时不能统一用AL÷motif长替代原生组成。

参考跨度60bp与两等位33bp说明本例不是“检测到扩增”就必然长度增加。完整操作见[官方TRGT小数据贯通重复分型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AE%98%E6%96%B9TRGT%E5%B0%8F%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E9%87%8D%E5%A4%8D%E5%88%86%E5%9E%8B)；[字段教程](https://github.com/PacificBiosciences/trgt/blob/main/docs/tutorial.md)。
