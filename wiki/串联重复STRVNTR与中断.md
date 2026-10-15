# 串联重复STRVNTR与中断

> 更新：2026-10-15；状态：可用；验证范围：对应人工/官方微型案例已实际运行；具体范围见正文。

串联重复需要同时描述单元、总长度、次数与组成，不能只用一个长度标签概括。

## 用同一个小例子分清单位

`CAGCAGCAG`含3个CAG单元，总长9bp。若中间插入其他序列，或者同一位点有多个motif，等位总长除以某个motif长度不能自动得到该motif次数。

STR常用于较短单元的串联重复，VNTR常涉及更长重复单元或相应历史命名，具体边界因文献/工具而异。两者均不同于散在TE家族的插入；也不能只因名字含repeat就认为所有工具支持。

## 输出读什么

保留位点ID、参考区间、motif/结构、每个等位长度、次数或组成、支持与区间、相位及失败状态。TRGT的AL以bp表示，MC可按字符串表达各motif计数；不要把VCF里的GT=1理解为重复一次。

本轮官方例AL=33/33、MC=11/11，是简单纯CAG例。参考catalog跨度60bp，输出VCF锚点不等于重复的第一个碱基。详见[TRGT重复分型与目录字段](https://github.com/SpiralKernel/bioinfo-wiki/wiki/TRGT%E9%87%8D%E5%A4%8D%E5%88%86%E5%9E%8B%E4%B8%8E%E7%9B%AE%E5%BD%95%E5%AD%97%E6%AE%B5)、[官方TRGT小数据贯通重复分型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AE%98%E6%96%B9TRGT%E5%B0%8F%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E9%87%8D%E5%A4%8D%E5%88%86%E5%9E%8B)；[官方教程](https://github.com/PacificBiosciences/trgt/blob/main/docs/tutorial.md)。

## 一个中断例子

`CAG CAG CAA CAG`总长12bp，含3个CAG单元及1个CAA中断单元。12÷3=4不能解释成4个CAG。该例只说明单位，本轮TRGT仍只实测纯CAG示例。
