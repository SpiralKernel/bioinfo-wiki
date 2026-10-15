# McClintock与xTea转座子检测选型

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

TE检测需同时固定参考、家族资源、平台与目标，不能仅把一段插入序列归类就结束。

## McClintock

[McClintock](https://github.com/bergmanlab/mcclintock)整合多个TE插入方法；需要对应参考、TE资源与reads及各模块依赖。运行整套流程前先核对所选模块的支持平台、输入和输出；方法共享相同上游资源时也可能共享偏差。

## xTea与其他实现

[xTea官方入口](https://github.com/parklab/xTea)包含不同数据类型和模式。短读长、长读长或特定家族的支持必须按具体版本/路径核对，不能推广成“所有TE、所有物种、所有平台”。现有[重复序列与转座子变异软件](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%87%8D%E5%A4%8D%E5%BA%8F%E5%88%97%E4%B8%8E%E8%BD%AC%E5%BA%A7%E5%AD%90%E5%8F%98%E5%BC%82%E8%BD%AF%E4%BB%B6)还连接ngs_te_mapper2等工具。

## 统一结果表

至少保留位点、方向、家族、参考或非参考状态、插入序列/长度、两侧支持、目标位点重复等证据及原生ID。聚合多个工具前要明确定义事件匹配规则和分型状态，不能简单取坐标交集就当真值。

本轮未执行TE专业调用器。流程分为[转座子插入检测与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BA%A7%E5%AD%90%E6%8F%92%E5%85%A5%E6%A3%80%E6%B5%8B%E4%B8%8E%E6%8F%90%E5%8F%96)和[长读长TE插入证据整理流程](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%95%BF%E8%AF%BB%E9%95%BFTE%E6%8F%92%E5%85%A5%E8%AF%81%E6%8D%AE%E6%95%B4%E7%90%86%E6%B5%81%E7%A8%8B)；物种家族库、嵌套插入与可比对性是必要输入假设。
