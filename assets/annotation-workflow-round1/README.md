# 人工注释与工作流结果副本

来自examples/data/annotation固定人工输入，无实际物种与个体数据。annotation-summary中仅省略本机绝对路径日志行，计数、版本和校验值保留。workflow-validation的最终summary SHA对应其原始独立运行报告，不对应经过路径删减的annotation-summary副本；两者执行目录与用途不同。

consequences.tsv为每条记录-ALT-转录本的后果长表；selected-high.tsv按ALT筛选。两张公开表以.表示缺失文本字段，脚本原始输出对应为空字段；列与行关系不变。overlaps与closest文件为bedtools无表头原始TSV：前6列A BED、随后6列B BED，boundary/closest末列分别为重叠长度/距离。无命中采用工具的占位字段。行数不是不同变异数。

gene-models图由examples/plot_annotation.py读取固定基因模型与实际summary生成，柱状图单位是注释行。source-downloads保存实际下载归档的URL、SHA与大小，源码包与工具二进制不提交。

详见[维护记录](../../maintenance/annotation-workflow-round1-2026-10-14.md)。
