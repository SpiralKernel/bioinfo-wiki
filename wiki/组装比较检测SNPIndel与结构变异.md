# 组装比较检测SNPIndel与结构变异

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

从成套组装及参考出发，保留共线性、单倍型和不可判定区域，再整理各类变异。

本页是选型与检查指南，尚非本项目可直接复跑案例。可从[SyRI官方酵母工作示例](https://schneebergerlab.github.io/syri/pipeline.html)查看匹配参考、query和示范命令；本轮未执行。

## 准备与比对

固定reference/query方向、组装版本、物种、单倍型状态与原始reads来源。检查完整性、污染、重复塌陷和明显缺口；相互比对前确认染色体命名不是按名称硬配。

选择匹配组装差异程度的比对配置，保留主/次/补充关系和唯一映射信息。大倒位/重排可能打断共线性，不能先强行删掉所有非共线片段再宣称没有SV。

## 选择调用与组织方式

[SVIMasm与dipcall组装变异选型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SVIMasm%E4%B8%8Edipcall%E7%BB%84%E8%A3%85%E5%8F%98%E5%BC%82%E9%80%89%E5%9E%8B)连接不同组装模型；SyRI可组织共线性与重排范围。工具输出的小变异、结构事件和未比对区域分别保存，并保留来源ID。

参考/查询互换会改变INS/DEL描述。单倍型缺失或未组装区域不自动等于个体PAV=0。针对候选回查reads、另一单倍型与覆盖，见[CNV与PAV交叉验证及群体矩阵](https://github.com/SpiralKernel/bioinfo-wiki/wiki/CNV%E4%B8%8EPAV%E4%BA%A4%E5%8F%89%E9%AA%8C%E8%AF%81%E5%8F%8A%E7%BE%A4%E4%BD%93%E7%9F%A9%E9%98%B5)。

## 交付

输出原生结果、映射后的VCF/BED、可调用与不可判定区间、每类事件数量以及证据限制。小变异与SV分别采用适合的匹配标准，不按行号直接对照。

本轮未运行组装检测软件。依据[SyRI](https://github.com/schneebergerlab/syri)、[SVIM-asm](https://github.com/eldariont/svim-asm)、[dipcall](https://github.com/lh3/dipcall)；概念见[组装比较共线性与变异方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E8%A3%85%E6%AF%94%E8%BE%83%E5%85%B1%E7%BA%BF%E6%80%A7%E4%B8%8E%E5%8F%98%E5%BC%82%E6%96%B9%E5%90%91)。
