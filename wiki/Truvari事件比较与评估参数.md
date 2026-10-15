# Truvari事件比较与评估参数

> 更新：2026-10-15；状态：可用；验证范围：对应人工/官方微型案例已实际运行；具体范围见正文。

Truvari按明确的表示、区域和相似性规则比较SV集合，评估结果必须带着这些规则读取。

## 本轮实际版本与命令

使用Truvari5.5.0，输入VCF已排序、bgzip及索引，参考版本一致。人工案例实际参数：

```bash
truvari bench -b truth.vcf.gz -c V01.vcf.gz -o bench   -f reference.fa --includebed callable.bed --passonly   -s 50 -S 50 -r 100 -p 0.7 -P 0.7 --pick single
```

-b是真值侧，-c是候选侧；-r为参考距离容差，-p/-P分别控制序列和大小相似性。两边最小长度均显式设50；不要忽略软件可能有不同默认筛选。

## 读输出

summary.json包括TP-base、TP-comp、FP、FN与GT一致性相关指标；匹配和未匹配VCF用于逐事件核对。两个等位之间相似不等于已知因果或样本身份正确。

本例2个人工事件全部匹配且GT一致，只在给定区域和规则下核对这两条。没有运行真实GIAB大型基准、复杂BND或重复区域分层，不外推性能。

参数与新版本行为见[官方bench指南](https://github.com/ACEnglish/truvari/wiki/bench)。完整输入生成、调用和校验见[人工长读长贯通SV调用与评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E9%95%BF%E8%AF%BB%E9%95%BF%E8%B4%AF%E9%80%9ASV%E8%B0%83%E7%94%A8%E4%B8%8E%E8%AF%84%E4%BC%B0)，方法见[SV事件匹配与一对一评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SV%E4%BA%8B%E4%BB%B6%E5%8C%B9%E9%85%8D%E4%B8%8E%E4%B8%80%E5%AF%B9%E4%B8%80%E8%AF%84%E4%BC%B0)。
