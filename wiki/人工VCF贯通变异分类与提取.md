# 人工VCF贯通变异分类与提取

> 更新：2026-10-14；状态：可用；验证范围：bcftools1.22与HTSlib1.22人工VCF/SAM案例已执行；真实检测性能及其他专业软件未实测。

用固定人工输入实际运行小变异调用、VCF标准化、类型/区域/样本提取与质量处理。

## 下载与第一次运行

从[项目仓库](https://github.com/SpiralKernel/bioinfo-wiki) Code → Download ZIP，或[直接下载ZIP](https://github.com/SpiralKernel/bioinfo-wiki/archive/refs/heads/main.zip)，解压到同时含README.md、examples和scripts的根目录。进入目录的方法见[R与Python路径文件与项目组织](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E8%B7%AF%E5%BE%84%E6%96%87%E4%BB%B6%E4%B8%8E%E9%A1%B9%E7%9B%AE%E7%BB%84%E7%BB%87)。

先按[bcftools变异操作与表达式](https://github.com/SpiralKernel/bioinfo-wiki/wiki/bcftools%E5%8F%98%E5%BC%82%E6%93%8D%E4%BD%9C%E4%B8%8E%E8%A1%A8%E8%BE%BE%E5%BC%8F)安装独立variants环境。在项目根目录的系统终端执行：

```bash
conda run -n variants python examples/variant_extraction_demo.py
```

已有能运行的bcftools及Python时也可直接`python3 examples/variant_extraction_demo.py`；非PATH工具用`--bcftools "/你的实际路径/bcftools"`。脚本需+fill-tags插件，基础代码只用Python标准库。

## 输入、输出与运行范围

`examples/data/variants/`保存固定人工参考及fai、calls.vcf、regions.bed、samples.txt、toy.sam。VCF有16条记录、3个样本；SAM有40条已人工构造的比对。脚本复制到输出目录后运行，原始输入不被改写。

输出在`examples/output/variants/`：标准化VCF及索引、各类提取VCF、掩蔽/重算结果、variants/cnv/str表、toy_called.vcf、summary.json和commands.json。重复运行覆盖输出同名文件。`--input-dir`与`--output`分别指定输入副本与独立输出，不能把输入目录当输出。

本机Linux、Python3.14.8、bcftools1.22/HTSlib1.22实际运行。Conda安装及所有操作系统未逐一实测；专业调用器未运行。人工SAM没有经过真实read mapper，不能当完整重测序基准。

## 核对结果

| 操作 | 本例实际结果 |
|---|---|
| 多等位拆分/标准化 | 16→17条；插入200左移至179 |
| 序列类型提取 | SNV5、Indel3、MNV1 |
| 符号/标记集合 | DEL/INV/DUP/CNV/STR/TE各1，BND2条对应1事件 |
| 接受FILTER | 仅PASS15；PASS或未评估16 |
| 目标位置302 | 按记录跨度1条；仅POS命中0条 |
| 选择S01后再筛ALT携带 | 15条，排除该样本缺失与纯合参考记录 |
| 同一样本与跨样本质量表达式 | 16条与17条 |
| 人工SAM调用 | chrToy:100 G→A，GT=0/1 |

这些筛选不是连续过滤的漏斗，而是从同一个输入回答不同问题。类型表按本例构造的分类统计；CNV、TE或STR在生物学上可与SV交叉，不能把本例分组当通用互斥分类法。

本例SNV选S01后AC/AN为1/2，旧AF仍可能为0.833333，重算后0.5。低质量样本掩蔽后仍保留记录。CN示例2/1/3与重复次数10/12等均为人工指定输入，不是从reads检测所得。

## 配图和继续练习

配图另需Matplotlib。按[R包Python包与可复现环境](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E5%8C%85Python%E5%8C%85%E4%B8%8E%E5%8F%AF%E5%A4%8D%E7%8E%B0%E7%8E%AF%E5%A2%83)建立.venv、安装教学依赖，然后在项目根目录执行`.venv/bin/python examples/plot_variant_extraction.py`。这里面向Linux/macOS或WSL；只运行基础案例不需要安装绘图库。

![人工变异记录分类](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/variants-round1/variant-records.png)

先复制输入目录到独立练习目录，再用`--input-dir`指向副本；把SNV的REF改成错误碱基，程序应停止，而不是自动修复。改samples.txt后需同步调整演示的固定结果断言；这是有预期真值的教学程序，不是任意生产VCF的通用包装器。

PAV状态整理另运行`python3 examples/pav_matrix_demo.py`，见[PAV检测与存在缺失矩阵](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PAV%E6%A3%80%E6%B5%8B%E4%B8%8E%E5%AD%98%E5%9C%A8%E7%BC%BA%E5%A4%B1%E7%9F%A9%E9%98%B5)。详细操作由[变异检测分型与提取学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E5%88%86%E5%9E%8B%E4%B8%8E%E6%8F%90%E5%8F%96%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)连接。[VCF案例源码](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/variant_extraction_demo.py)，[固定输入](https://github.com/SpiralKernel/bioinfo-wiki/tree/main/examples/data/variants)。
