# R与Python安装环境与编辑器

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

语言解释器负责执行，编辑器帮助写代码；先确认运行的是哪个环境。

## 四个角色

Python/R是语言及其运行环境；VS Code/RStudio是可选编辑器；系统终端执行命令；Python/R控制台执行对应语言。安装编辑器不等于已经有正确解释器。

Windows/macOS从官方说明选择安装程序，Linux按发行版或项目环境管理；本页没有在各操作系统实测安装，不给跨系统通用的一条安装命令。

## 先验证

以下在系统终端执行，而非R/Python控制台：

```bash
python --version
Rscript --version
```

有的系统使用`python3`，按实际命令选择。若找不到Rscript，先确认R已安装及可执行文件路径；使用RStudio也可在R控制台执行`R.version.string`确认语言版本。

Python练习可建立虚拟环境，使用其中的解释器运行。Windows常见`.venv\Scripts\python.exe`，macOS/Linux常见`.venv/bin/python`。VS Code应选择该解释器；RStudio项目工作目录应对应项目根目录。

先运行[同一份样本表贯通R与Python](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%8C%E4%B8%80%E4%BB%BD%E6%A0%B7%E6%9C%AC%E8%A1%A8%E8%B4%AF%E9%80%9AR%E4%B8%8EPython)，无需为了第一张表安装大量包。不要把WebR内部验证当作本机已安装原生R。

官方入口：[Python安装/使用](https://docs.python.org/3/using/index.html)、[R下载](https://cran.r-project.org/)、[Posit RStudio](https://posit.co/download/rstudio-desktop/)、[VS Code Python](https://code.visualstudio.com/docs/python/python-tutorial)。
