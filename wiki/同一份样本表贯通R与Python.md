# 同一份样本表贯通R与Python

> 更新：2026-10-15；状态：可用；验证范围：Python实际运行；base R完整脚本经WebR R4.6.0执行，输出语义交叉核验；本轮原生R4.4.3复跑基础案例；第三方R包仅验证另页DESeq2案例。

用两张故意顺序不同的小表练习按ID合并，保留缺失并核对两种语言的描述结果。

## 输入与运行

通过[项目仓库](https://github.com/SpiralKernel/bioinfo-wiki)中的 Code → Download ZIP，也可[直接下载ZIP](https://github.com/SpiralKernel/bioinfo-wiki/archive/refs/heads/main.zip)并解压。先按[R与Python路径文件与项目组织](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E8%B7%AF%E5%BE%84%E6%96%87%E4%BB%B6%E4%B8%8E%E9%A1%B9%E7%9B%AE%E7%BB%84%E7%BB%87)把终端或RStudio当前目录设为根目录。`examples/data/programming_measurements.csv`有8个样本、1个NA；`programming_metadata.csv`行顺序不同，包含条件A/B与批次。数据为人工数字，不用于生物学推断。

macOS/Linux终端：

```bash
python3 examples/programming_basics.py
Rscript examples/programming_basics.R
```

Windows PowerShell：

```powershell
python examples/programming_basics.py
Rscript examples/programming_basics.R
```

先确认安装页中的命令能找到解释器；Windows若只有`py`命令，可将第一行的`python`换为`py`。Rscript不在PATH时，不必先修改系统设置：在已打开正确项目的RStudio **R控制台**执行`source("examples/programming_basics.R")`。

Python基本表格脚本只需标准库；可选`--plot`需Matplotlib。R脚本只需base R，建议先通过[R与Python安装环境与编辑器](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E5%AE%89%E8%A3%85%E7%8E%AF%E5%A2%83%E4%B8%8E%E7%BC%96%E8%BE%91%E5%99%A8)确认命令可用。

## 已运行与边界

Python 3.14.8已实际运行。R脚本在WebR的R 4.6.0 WebAssembly运行时执行，包含CSV读取、merge、缺失检查、均值、lm和base R PDF图；本轮另在原生R4.4.3执行该完整脚本，仍得到8行、1缺失、A均值2/B均值5.5和条件系数3.5。DESeq2/apeglm验证另见[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)，不代表全部R包或各操作系统已测。

两种语言均得到8行、1个缺失，A组有效n=3、均值2，B组有效n=4、均值5.5。R参考A的模型截距2、B系数3.5；只是人工算术，不提供因果或组学统计结论。

## 检查输出

Python输出`examples/output/programming/python/joined.csv`、`summary.json`，加`--plot`可生成values.png。R输出`examples/output/programming/r/joined.csv`、`summary.csv`、`session-info.txt`和`values.pdf`。重复运行覆盖同名文件。

检查ID仍按原测量表对应，S04缺失保留，不因均值计算而整行消失。CSV字节格式可能不同，比较数据含义而不是要求完全相同文件。

## 练习

复制**整个解压项目**为新的练习文件夹，在副本根目录运行副本脚本。把副本测量表S02的ID改为S01，Python应报`Empty or duplicate sample ID`；从干净ZIP恢复该表，再把元数据S01改为S99，Python应报`Sample ID sets do not match`。R的`stopifnot`也应停止。最后恢复输入，只改变元数据行顺序，均值应保持。

Python的`--output`只改输出路径，不改输入；改原项目以外的一张CSV不会影响该脚本。本例明确只把空值和`NA`视为缺失；`NaN`、`Infinity`等非有限文本应报错，不能计入有效n。ID保留字符串，包括`001`的前导零。

后续读[Python读取清理与合并样本表](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Python%E8%AF%BB%E5%8F%96%E6%B8%85%E7%90%86%E4%B8%8E%E5%90%88%E5%B9%B6%E6%A0%B7%E6%9C%AC%E8%A1%A8)、[R读取清理与合并样本表](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E8%AF%BB%E5%8F%96%E6%B8%85%E7%90%86%E4%B8%8E%E5%90%88%E5%B9%B6%E6%A0%B7%E6%9C%AC%E8%A1%A8)和[R与Python绘图和统计入门](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E7%BB%98%E5%9B%BE%E5%92%8C%E7%BB%9F%E8%AE%A1%E5%85%A5%E9%97%A8)。[Python源码](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/programming_basics.py)、[R源码](https://github.com/SpiralKernel/bioinfo-wiki/blob/main/examples/programming_basics.R)。
