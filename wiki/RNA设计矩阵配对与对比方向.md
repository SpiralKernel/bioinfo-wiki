# RNA设计矩阵配对与对比方向

> 更新：2026-10-15；状态：可用；验证范围：原生R与公开airway计数案例已执行；范围和结果见正文。

设计矩阵把样本信息变成模型列，对比定义了究竟要比较哪两个状态。

## 配对不是把八个样本当八个独立重复

airway有4条细胞系，每条各含untrt和trt。模型`~ cell + dex`用cell表示配对单位差异，用dex表示处理差异。它假设这里估计共同的处理效应，没有估计每条细胞系各自独立的处理效应。

本例8行设计矩阵有5个独立列，剩余自由度3。若每个处理只出现于一个批次，加入batch和condition不能凭空分离效应；设计不满秩就应停止并检查实验，而不是任意删除某列后解释成已校正。

## 对比方向必须写明

`contrast=c("dex","trt","untrt")`表示trt相对untrt。正log2FC表示该方向上的增加；交换分子分母后log2FC变号，双侧零效应检验的P应保持一致。本轮实际核对了这一性质。

“参考组是什么”和“输出列名是什么”都需确认。`resultsNames(dds)`列出可提取系数；复杂交互的主效应依赖参考水平，不能只看名称中有condition就当全体平均效应。

本项目[R输入检查](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/rnaseq_input_checks.R)会检查样本对应、满秩和剩余自由度。继续读[RNA交互作用与LRT比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E4%BA%A4%E4%BA%92%E4%BD%9C%E7%94%A8%E4%B8%8ELRT%E6%AF%94%E8%BE%83)、[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)。
