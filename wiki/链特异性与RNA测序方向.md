# 链特异性与RNA测序方向

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

链特异性保存RNA来源方向，R1/R2与原始RNA的关系由建库布局决定。

## 保存什么方向

链特异性使读段保留原始RNA来源链的信息，有助区分重叠与反义转录。不意味着所有R1都与原始RNA同向。

forward/reverse、first-strand/second-strand等命名在工具与试剂间可能采用不同约定，应把建库说明、read布局与软件参数对应，而非凭名称猜。

## 如何核对

先取实验记录，再利用已注释、不重叠区域的比对方向检查。信息不足、污染和复杂转录会影响推断。错误参数可能减少有效计数或混淆反义信号。

单端/双端、链特异/非特异、端部/全长是不同维度；双端并不自动链特异。样本表保存策略、试剂、布局及软件设置，上游丢失的方向证据不能靠后续差异分析恢复。

来源：[nf-core/rnaseq](https://nf-co.re/rnaseq/latest/docs/usage/)、[RSeQC infer_experiment](https://rseqc.sourceforge.net/#infer-experiment-py)。应用见[RNA测序建库选择与偏倚](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%B5%8B%E5%BA%8F%E5%BB%BA%E5%BA%93%E9%80%89%E6%8B%A9%E4%B8%8E%E5%81%8F%E5%80%9A)。
