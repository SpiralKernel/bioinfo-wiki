# CNVkit深度分段与拷贝数解释

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

CNVkit通过深度参考与校正估计相对剂量，再分段和进行相应拷贝数解释。

## 先选数据类型

WGS、捕获和扩增子不应共用未经核对的设置。需要排序BAM、匹配参考、目标/可访问区域以及适当正常参考；基线与性染色体/区域倍性需说明。[官方文档](https://cnvkit.readthedocs.io/en/stable/)给出各数据路径，本轮未执行。

示意WGS的正常参考模板，路径均需替换且正常样本需与研究设计匹配：

```bash
cnvkit.py batch sample.bam --normal normal.bam --method wgs   --fasta reference.fa --output-dir cnv-results
```

这不包含为具体研究选择的全部QC、纯度、倍性与最终call参数；捕获实验还需相应targets等信息，不能直接抄WGS模板。

## 从文件读到结论

理解coverage表、参考、校正后的cnr和分段cns各是什么。相对log2比值不自动等于整数CN；后续call要声明模型和阈值。查看GC/可比对性、异常bin、分段支持及样本与参考的兼容性。

仅有深度证据可能定位不到精确连接，也不能独立确认拷贝中性LOH。解释见[拷贝数基线非整倍体与LOH](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%8B%B7%E8%B4%9D%E6%95%B0%E5%9F%BA%E7%BA%BF%E9%9D%9E%E6%95%B4%E5%80%8D%E4%BD%93%E4%B8%8ELOH)；交叉核查见[CNV与PAV交叉验证及群体矩阵](https://github.com/SpiralKernel/bioinfo-wiki/wiki/CNV%E4%B8%8EPAV%E4%BA%A4%E5%8F%89%E9%AA%8C%E8%AF%81%E5%8F%8A%E7%BE%A4%E4%BD%93%E7%9F%A9%E9%98%B5)。
