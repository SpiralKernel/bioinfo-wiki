# SV事件匹配与一对一评估

> 更新：2026-10-15；状态：可用；验证范围：对应人工/官方微型案例已实际运行；具体范围见正文。

先规定区域、类型、断点和序列相似性，再进行匹配与计数。

## 匹配规则先于分数

SV可能用不同锚点、序列或符号表达。相同POS不能保证相同事件；近断点也不能替代插入序列相似性、长度和方向。一个真值被多个候选命中时，需要声明一对一还是多重匹配策略。

TP-base与TP-comp分别从真值侧和候选侧计数，不能在复杂表示下假定永远相等。存在匹配、GT一致、断点与等位序列准确性分开评价；范围外或不可调用事件单独处理。

## 本轮实际例子

[人工长读长贯通SV调用与评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E9%95%BF%E8%AF%BB%E9%95%BF%E8%B4%AF%E9%80%9ASV%E8%B0%83%E7%94%A8%E4%B8%8E%E8%AF%84%E4%BC%B0)使用2个人工DEL/INS，BED限定[10000,90000)，固定refdist100、序列和长度相似度0.7、单匹配和PASS筛选。实际TP-base=TP-comp=2、FP/FN=0，匹配GT一致2。此结果只证明这两个简单事件的链路，不是该软件对所有SV的准确率。

修改容差时应同时比较匹配对和被排除集合，不能只挑最高分参数。具体参数见[Truvari事件比较与评估参数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Truvari%E4%BA%8B%E4%BB%B6%E6%AF%94%E8%BE%83%E4%B8%8E%E8%AF%84%E4%BC%B0%E5%8F%82%E6%95%B0)及[官方bench说明](https://github.com/ACEnglish/truvari/wiki/bench)。
