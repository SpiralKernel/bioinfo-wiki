# 官方TRGT小数据贯通重复分型

> 更新：2026-10-15；状态：可用；验证范围：对应人工/官方微型案例已实际运行；具体范围见正文。

下载固定提交的PacBio官方微型输入，核对SHA后实际运行TRGT并解析长度与motif计数。

## 安装与下载

以下按已测Linux x86_64整理，Windows需适用Linux环境；其他平台未实测。先按[人工长读长贯通SV调用与评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E9%95%BF%E8%AF%BB%E9%95%BF%E8%B4%AF%E9%80%9ASV%E8%B0%83%E7%94%A8%E4%B8%8E%E8%AF%84%E4%BC%B0)建立variant-calling Python环境，再按[TRGT重复分型与目录字段](https://github.com/SpiralKernel/bioinfo-wiki/wiki/TRGT%E9%87%8D%E5%A4%8D%E5%88%86%E5%9E%8B%E4%B8%8E%E7%9B%AE%E5%BD%95%E5%AD%97%E6%AE%B5)取得官方TRGT5.1.0二进制，将TRGT_BIN设为其绝对路径。在项目根目录执行：

```bash
export TRGT_BIN="/你的实际绝对路径/trgt"
conda run -n wiki-variant-calling python examples/trgt_official_demo.py
```

程序从固定commit b21c6217eeaef9a080205932fe29f730dc00e31f下载5个官方输入，共342,835字节，并逐个检查SHA。[资源清单](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/data/variant-detection/trgt-inputs.json)保留来源和许可，不把原始BAM另行重授权发布。已有同一fixture可用--input-dir，仍核对SHA。

## 输出与核对

默认examples/output/trgt-official，非空目录拒绝覆盖；可用--output换新目录。产生原生calls.vcf.gz、索引、spanning BAM、日志与summary。实际TRGT5.1.0-ec66463得到TR1、GT=1/1、AL=33/33bp、MC字符串11/11，支持SD=15/14。

固定catalog为chrA [10001,10061)，对应1起始10002–10061；VCF POS=10001是padding锚点。参考重复60bp、等位33bp，AL不含padding；GT是等位索引，不是次数。ALLR为原生等位长度范围，不作为所有工具共有的同一统计区间定义。

## 适用范围

这是官方提供的chrA微型示例，不是人类真实样本的诊断或准确率基准，也不验证ONT、复杂多motif、中断或超长重复。保留AL/MC/MS、支持、范围与失败状态，学习如何核对单位与来源。

源码[trgt_official_demo.py](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/trgt_official_demo.py)，详细操作与字段见[官方教程](https://github.com/PacificBiosciences/trgt/blob/main/docs/tutorial.md)。下一步回到[STR与重复扩增检测及提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/STR%E4%B8%8E%E9%87%8D%E5%A4%8D%E6%89%A9%E5%A2%9E%E6%A3%80%E6%B5%8B%E5%8F%8A%E6%8F%90%E5%8F%96)和[串联重复STRVNTR与中断](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%B8%B2%E8%81%94%E9%87%8D%E5%A4%8DSTRVNTR%E4%B8%8E%E4%B8%AD%E6%96%AD)。

## 原生字段怎么读

正文“33/33”等只简写两项结果，原生AL/MC等字段通常用逗号分隔，不是相位符号。GT使用斜杠，表示本例未分相的等位索引。具体样本行以原生VCF为准。

| 字段 | 本例原生值 | 含义 |
|---|---|---|
| GT | 1/1 | 两份等位索引 |
| AL | 33,33 | 每个等位的重复区长度，bp，不含padding |
| MC | 11,11 | 本例纯CAG的motif计数，VCF类型为字符串 |
| SD | 15,14 | 分配到各等位的跨越read支持 |
| ALLR | 30-39,33-33 | 原生等位长度范围 |

复杂或分相输出应按该版本等位排序/字段约定关联，不能普遍凭GT左右位置猜MC/MS等字段顺序；本例两长度相同也不能验证所有顺序场景。
