# ExpansionHunter位点定义与重复估计

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

ExpansionHunter按目标位点的序列结构估计重复，位点定义与证据范围决定可解释性。

## 最小catalog结构

[官方格式](https://github.com/Illumina/ExpansionHunter/blob/master/docs/04_VariantCatalogFiles.md)使用JSON数组。以下只演示一个人工定义，没有配套BAM，不是可直接运行的数据集：

```json
[
  {
    "LocusId": "toyRepeat",
    "LocusStructure": "(CAG)*",
    "ReferenceRegion": "chrToy:100-130",
    "VariantType": "Repeat"
  }
]
```

ReferenceRegion使用0起始半开坐标；LocusStructure表达位点结构。它与TRGT BED不是同一格式，不能仅改扩展名。

## 输入与模板

准备匹配的短读长比对、参考、catalog和适用样本信息；本轮未安装或执行：

```bash
ExpansionHunter --reads sample.bam --reference reference.fa   --variant-catalog repeats.json --output-prefix sample.repeat
```

跨越、侧翼和重复内部reads能提供不同信息，短reads/片段长度可能限制估计；特殊RareRepeat设置需要相应依据，不能把所有目标都改成该类型来追求更长数值。输出重复次数、区间和失败状态按头部与版本核对。

阅读[串联重复STRVNTR与中断](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%B8%B2%E8%81%94%E9%87%8D%E5%A4%8DSTRVNTR%E4%B8%8E%E4%B8%AD%E6%96%AD)、[STR与重复扩增检测及提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/STR%E4%B8%8E%E9%87%8D%E5%A4%8D%E6%89%A9%E5%A2%9E%E6%A3%80%E6%B5%8B%E5%8F%8A%E6%8F%90%E5%8F%96)；工具与许可以[官方仓库](https://github.com/Illumina/ExpansionHunter)为准。
