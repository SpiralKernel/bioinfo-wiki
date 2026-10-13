# Notebook脚本与命令行运行

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

交互适合探索，完整脚本和从头运行帮助暴露隐藏状态并保存可复现步骤。

## 三个输入位置

系统终端执行`python ...`或`Rscript ...`；Windows PowerShell块对应Windows终端；Python控制台执行Python语句；R控制台执行R语句。教程代码块标注bash/python/r，先看标签再粘贴。

`.py`和`.R`是代码文件，不是输出目录。先按[R与Python路径文件与项目组织](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E8%B7%AF%E5%BE%84%E6%96%87%E4%BB%B6%E4%B8%8E%E9%A1%B9%E7%9B%AE%E7%BB%84%E7%BB%87)设置当前目录，再保存文件并从终端完整运行；RStudio也可在正确项目目录中`source("examples/programming_basics.R")`。

## Notebook隐藏状态

单元格可以乱序执行，变量可能来自已删除或未展示的单元。交付前重启内核，从上到下全部运行，确认路径、输入和依赖均明确；显示结果不证明当前代码可以重新生成它。

脚本同样需要从干净会话运行，不应依赖工作区里旧对象。重复执行会覆盖哪些输出要写明，本项目例子只覆盖指定output目录的同名文件。

## 选择

初学先跑通提供的小脚本，再用Notebook探索；不是所有任务都必须使用Notebook。长流程和批处理保存参数、日志与退出状态，见[可复现分析与工作流管理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%AF%E5%A4%8D%E7%8E%B0%E5%88%86%E6%9E%90%E4%B8%8E%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%AE%A1%E7%90%86)。

来源：[Python脚本解释器](https://docs.python.org/3/tutorial/interpreter.html)、[JupyterLab文档](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html)、[Rscript说明](https://stat.ethz.ch/R-manual/R-devel/library/utils/html/Rscript.html)。
