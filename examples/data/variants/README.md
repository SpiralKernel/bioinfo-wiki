# 人工变异输入

本目录数据完全人工构造，不对应真实物种、基因或样本。

- `toy.fa`与`toy.fa.fai`：chrToy 1400 bp、chrOther 400 bp；重复区用于左对齐与STR字段教学。
- `calls.vcf`：16条记录、3个样本。包括混合多等位、MNV、小Indel、符号SV、BND、CNV、STR和TE标记，质量和缺失有意设置为反例。
- `regions.bed`：0-based半开区间chrToy:[301,302)，对应VCF位置302；小缺失POS为300。
- `samples.txt`：选择S01。
- `toy.sam`：40条人工已比对记录；chrToy:100有20条REF、20条ALT证据，不是实际比对器输出。
- `pav_evidence.tsv`：已经人工指定的present/absent/unknown状态，用于格式整理，不发现PAV。

VCF的TEFAMILY与REPCN是本项目自定义教学字段。CN列为预先指定的人工拷贝数，不是专业深度估计结果；STR列也不是检测所得。不能把这些字段当成所有调用器的标准输出。

从项目根目录运行`examples/variant_extraction_demo.py`与`examples/pav_matrix_demo.py`。VCF案例需要bcftools及+fill-tags插件；PAV整理仅需Python标准库。输出另存，修改实验应复制输入并通过`--input-dir`或`--input`明确指向副本。教学断言固定为原输入预期，改变输入后需要同步调整。
