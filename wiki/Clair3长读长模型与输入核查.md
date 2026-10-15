# Clair3长读长模型与输入核查

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

Clair3结合pileup与完整比对信息进行长读长小变异调用，模型选择是输入准备的一部分。

## 先固定平台信息

记录HiFi或ONT、化学/碱基识别模型、reads处理与比对参数，再选该release支持的模型。覆盖和训练域不匹配可能改变调用，不能以“都叫长读长”替代这些记录。

输入一般为排序索引比对、参考、模型与输出目录；工具内部阶段与线程/内存使用需要按[官方说明](https://github.com/HKU-BAL/Clair3)核对。容器和模型分别固定，测试小区域时也保留区域外限制。

## 结果如何接入

先检查样本、contig、REF、过滤和GT字段，再进入标准化与评估。与其他工具比较时统一参考、可调用范围和变异表示，不能只比较VCF行数。

本轮未执行Clair3或真实长读长SNV/Indel模型。人工FreeBayes例与Sniffles例不验证本工具。方法入口[小变异检测的似然与局部组装](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B0%8F%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E7%9A%84%E4%BC%BC%E7%84%B6%E4%B8%8E%E5%B1%80%E9%83%A8%E7%BB%84%E8%A3%85)、[长读长小变异检测与模型选择](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%95%BF%E8%AF%BB%E9%95%BF%E5%B0%8F%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E4%B8%8E%E6%A8%A1%E5%9E%8B%E9%80%89%E6%8B%A9)。
