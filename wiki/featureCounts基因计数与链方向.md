# featureCounts基因计数与链方向

> 更新：2026-10-15；状态：可用；验证范围：官方资料与方法核对；本页上游或扩展软件流程未执行。

featureCounts按注释和分配规则把比对记录汇总为特征计数；计数单位和歧义处理必须记录。

## 提前明确规则

常见基因层面计数以exon为特征、gene_id汇总；共享外显子、多重比对、多特征重叠和链方向都会改变分配。计数值不同不一定是后续差异软件造成。

以下为双端BAM的命令模板，需按本机版本帮助核对参数，本轮未安装或运行featureCounts：

```bash
featureCounts -T 4 -p --countReadPairs -s 0   -t exon -g gene_id -a matched.gtf -o gene-counts.txt   sample1.sorted.bam sample2.sorted.bam
```

`-p`和是否按read pair计数的选项不能只凭旧教程推断，必须确认实际版本行为。`-s 0`表示此模板按非链特异处理，不是对所有RNA文库的推荐。来源：[官方featureCounts说明](https://subread.sourceforge.net/featureCounts.html)。

## 检查输出而非只取数字列

查看Assigned与各类Unassigned状态；低分配可能源于注释版本、链设置、比对质量或特征歧义。summary中的类别需结合命令解释，不能都归因于“低质量”。

生成矩阵时保留gene ID，识别Chr/Start/End/Strand/Length等注释列与实际样本列，按明确ID映射样本名。不要按列位置盲切，也不要把Length列当样本。继续读[RNA计数矩阵与样本表核对](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E4%B8%8E%E6%A0%B7%E6%9C%AC%E8%A1%A8%E6%A0%B8%E5%AF%B9)、[链特异性与RNA测序方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%93%BE%E7%89%B9%E5%BC%82%E6%80%A7%E4%B8%8ERNA%E6%B5%8B%E5%BA%8F%E6%96%B9%E5%90%91)。
