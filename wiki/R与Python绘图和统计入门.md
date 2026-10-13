# R与Python绘图和统计入门

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

先画独立观测和缺失，再计算明确目标；图形、模型和生物学结论分别检查。

## 同一份表的图

先完成[同一份样本表贯通R与Python](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%8C%E4%B8%80%E4%BB%BD%E6%A0%B7%E6%9C%AC%E8%A1%A8%E8%B4%AF%E9%80%9AR%E4%B8%8EPython)。Python可选绘图需Matplotlib，按[R包Python包与可复现环境](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E5%8C%85Python%E5%8C%85%E4%B8%8E%E5%8F%AF%E5%A4%8D%E7%8E%B0%E7%8E%AF%E5%A2%83)安装到`.venv`后，在项目根目录的终端执行：

macOS/Linux：

```bash
.venv/bin/python examples/programming_basics.py --plot
```

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe examples/programming_basics.py --plot
```

R绘图无需第三方包，在正确项目的**R控制台**执行：

```r
source("examples/programming_basics.R")
```

Python生成散点图PNG，R生成箱线图加观测点PDF。两种样式不同，应对应A组3个、B组4个有效观测；缺失样本S04保留在输出表但不画成0。

![Python人工观测](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/programming-round1/python-values.png)

![R人工观测](https://raw.githubusercontent.com/SpiralKernel/bioinfo-wiki/main/assets/programming-round1/r-values.png)

## 从描述到模型

上面的R脚本已生成`joined`和`fit`。在同一R会话执行`coef(fit)`，预期截距约2、`conditionB`约3.5。公式`value ~ condition`左边是响应值，右边是分组；脚本把A指定为参考。A的预测值为2，B为2+3.5=5.5，正好对应原始组均值。这是人工数字的算术关系，没有生物学或因果证据。

模型输入、缺失规则与独立单位先明确。散点相关、组均值和P值回答不同问题；真实推断读[统计方法选择与分析计划](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%9F%E8%AE%A1%E6%96%B9%E6%B3%95%E9%80%89%E6%8B%A9%E4%B8%8E%E5%88%86%E6%9E%90%E8%AE%A1%E5%88%92)、[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)。轴注明单位，误差线注明SD/SE/CI，保留观测点。

Python图已运行，R脚本及PDF经WebR执行；预览PNG由PDF渲染。本机没有原生Rscript，也未实测各系统安装。依据：[Matplotlib教程](https://matplotlib.org/stable/tutorials/pyplot.html)、[R绘图入门](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Graphical-procedures)。
