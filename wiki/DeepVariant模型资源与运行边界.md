# DeepVariant模型资源与运行边界

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

DeepVariant的小变异调用依赖模型、候选生成和输入参考；固定运行环境也要固定模型来源。

## 输入与输出

准备排序索引BAM/CRAM、参考及索引、样本名和资源预算。模型应匹配WGS/WES或相应长读长平台等实际支持范围，核对版本对应的model type，不能将某平台名称直接当所有测序版本都适配。

通常得到VCF及可选gVCF。gVCF用于相应后续联合分型链路，不是普通VCF补一个文件后缀。保存容器tag/digest、模型、参考和运行命令。

## 如何开始

先使用[官方quick start](https://github.com/google/deepvariant)所用版本的小范围示例，确认CPU/GPU、内存、区域参数和各阶段产物，再换自己的输入。完整路径与版本占位符必须落到实际资源；本轮没有下载模型或运行DeepVariant，不提供伪装成实测的性能数值。

它与[Sniffles长读长结构变异实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Sniffles%E9%95%BF%E8%AF%BB%E9%95%BF%E7%BB%93%E6%9E%84%E5%8F%98%E5%BC%82%E5%AE%9E%E8%B7%B5)承担的小变异/SV任务不同；联合分析和倍性支持也需按具体实现核对。读[长读长小变异检测与模型选择](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%95%BF%E8%AF%BB%E9%95%BF%E5%B0%8F%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E4%B8%8E%E6%A8%A1%E5%9E%8B%E9%80%89%E6%8B%A9)、[变异检测输入准备与样本清单](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E8%BE%93%E5%85%A5%E5%87%86%E5%A4%87%E4%B8%8E%E6%A0%B7%E6%9C%AC%E6%B8%85%E5%8D%95)。
