# R包Python包与可复现环境

> 更新：2026-10-15；状态：可用；验证范围：官方语言文档核对；基础样本表经WebR及原生R验证；airway/DESeq2/apeglm已在隔离Conda环境运行；安装与第三方包按页说明。

包安装到环境，先确认解释器、库位置和版本来源。

## Python：统一使用项目环境

先按[R与Python路径文件与项目组织](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E8%B7%AF%E5%BE%84%E6%96%87%E4%BB%B6%E4%B8%8E%E9%A1%B9%E7%9B%AE%E7%BB%84%E7%BB%87)进入项目根目录。基础样本表不依赖第三方包；要画图或跑群体案例时，建议Python 3.10+，建立`.venv`并安装教学依赖。

macOS/Linux系统终端：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-teaching.txt
.venv/bin/python examples/programming_basics.py --plot
```

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-teaching.txt
.\.venv\Scripts\python.exe examples/programming_basics.py --plot
```

Windows若只有`py`，把创建环境那行的`python`换成`py`，之后继续用环境里的完整解释器路径。这样无需激活环境，也不会把包误装到另一个Python。VS Code选择`.venv`中的解释器；`sys.executable`可核对运行位置。requirements记录版本要求，精确重现还需保存实际版本/锁文件和系统信息。

## R：安装与载入分开

第一轮样本表只用base R，无需安装tidyverse或DESeq2。CRAN包通常用`install.packages()`；Bioconductor包通过BiocManager选择匹配R的发布系列。准备进入RNA官方练习时，在**R控制台**运行：

```r
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}
BiocManager::install(c("airway", "DESeq2"))
BiocManager::valid()
sessionInfo()
```

安装通常对同一环境做一次，每次新会话仍需`library(airway)`和`library(DESeq2)`载入。不要随意指定另一个发布系列覆盖现有环境；根据官方提示处理R/包版本不匹配。报错时保存完整错误、`sessionInfo()`及`.libPaths()`，见[R与Python报错调试与求助](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E6%8A%A5%E9%94%99%E8%B0%83%E8%AF%95%E4%B8%8E%E6%B1%82%E5%8A%A9)。

renv可管理项目依赖，不能代替系统库或外部软件。R安装片段按[Bioconductor官方说明](https://www.bioconductor.org/install/)整理，本轮另在隔离Conda环境安装原生R4.4.3、airway、DESeq2、apeglm和jsonlite，见[DESeq2安装对象与结果提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DESeq2%E5%AE%89%E8%A3%85%E5%AF%B9%E8%B1%A1%E4%B8%8E%E7%BB%93%E6%9E%9C%E6%8F%90%E5%8F%96)；上方BiocManager安装路径未单独执行。基础R脚本已用原生R复跑。

来源：[Python venv](https://docs.python.org/3/library/venv.html)、[pip指南](https://pip.pypa.io/en/stable/user_guide/)、[renv](https://rstudio.github.io/renv/)。
