# 变异检测第二轮结果

SV和FreeBayes输入完全人工构造；TRGT使用固定提交的PacBio提供微型输入。公开汇总、真值匹配、受限格式兼容审计和环境信息，不发布工具、原始BAM或FASTQ。TRGT下载清单保留其来源与协议，不给原始fixture另行重授权。

force-format-audit只列原生/派生表头、FORMAT和样本值；原生VCF保留于可复跑输出。派生副本只补PS键并修正经BAM确认的样本表头，GT/GQ/DR/DV及INFO不变。0/0且GQ=0不是高置信参考；SNF群体R01仍保留缺失。

Truvari只在指定区域和参数下匹配两个易例，分别保存TP-base/TP-comp及GT一致性。TRGT的AL以bp、MC本例以字符串次数表示，VCF锚点不计入AL。图的上下两部分是不同案例和单位，不能用于平台/算法性能排名。

环境记录同时保存Conda构建和实际Python包，包括回归/配图另加的SciPy与Matplotlib；读者基本调用环境使用examples/environments/variant-calling.yml即可。详见[维护与双代理纠错记录](../../maintenance/variant-detection-round2-2026-10-15.md)。
