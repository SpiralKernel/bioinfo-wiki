# SVIMasm与dipcall组装变异选型

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

组装调用需要区分单倍型状态、比对可调用范围和工具所表达的变异类型。

## SVIM-asm

输入是组装对参考的相应BAM及参考，单倍体和二倍体模式不同。以下为未实测的二倍体模板，需要真实的两套单倍型比对与索引：

```bash
svim-asm diploid output h1.sorted.bam h2.sorted.bam reference.fa
```

按[SVIM-asm官方说明](https://github.com/eldariont/svim-asm)核对比对参数、主/补充记录和输出类别，不能把reads BAM当组装BAM直接复用。

## dipcall

[dipcall](https://github.com/lh3/dipcall)面向一对相位单倍型组装相对参考的调用，输出VCF和相应可调用区域。缺少一套单倍型、组装塌陷或低质量区域会影响解释；不能把可调用区域外“没有记录”当真阴性。

两者与SyRI的共线性/重排组织有不同任务。先按[组装比较共线性与变异方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E8%A3%85%E6%AF%94%E8%BE%83%E5%85%B1%E7%BA%BF%E6%80%A7%E4%B8%8E%E5%8F%98%E5%BC%82%E6%96%B9%E5%90%91)建立输入假设，再选择工具，保留原生输出和表示映射。本轮三者均未实际执行。
