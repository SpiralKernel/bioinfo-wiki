# R与Python生信编程入门路线

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

先用同一份小表学会运行、索引、清理、合并和绘图，再进入具体生信包。

## 从哪里开始

不要求先会Linux或Git。先从[项目仓库](https://github.com/SpiralKernel/bioinfo-wiki)中的 Code → Download ZIP，也可[直接下载ZIP](https://github.com/SpiralKernel/bioinfo-wiki/archive/refs/heads/main.zip)并解压，找到README.md、examples、scripts和wiki。解压后的文件夹可能叫bioinfo-wiki-main。所有练习命令从项目根目录运行；看不懂“根目录”时先读[R与Python路径文件与项目组织](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E8%B7%AF%E5%BE%84%E6%96%87%E4%BB%B6%E4%B8%8E%E9%A1%B9%E7%9B%AE%E7%BB%84%E7%BB%87)。

R和Python都可以做表格、统计与图；项目可优先学习一种，再学习另一种的差异。不需要一开始同时记住所有包。

## 推荐顺序

1. [R与Python安装环境与编辑器](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E5%AE%89%E8%A3%85%E7%8E%AF%E5%A2%83%E4%B8%8E%E7%BC%96%E8%BE%91%E5%99%A8)：区分解释器、编辑器、终端和控制台。
2. [Notebook脚本与命令行运行](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Notebook%E8%84%9A%E6%9C%AC%E4%B8%8E%E5%91%BD%E4%BB%A4%E8%A1%8C%E8%BF%90%E8%A1%8C)：保存并完整运行一个文件。
3. [Python变量容器循环与函数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Python%E5%8F%98%E9%87%8F%E5%AE%B9%E5%99%A8%E5%BE%AA%E7%8E%AF%E4%B8%8E%E5%87%BD%E6%95%B0)或[R向量数据框索引与函数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E6%A1%86%E7%B4%A2%E5%BC%95%E4%B8%8E%E5%87%BD%E6%95%B0)。
4. [Python读取清理与合并样本表](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Python%E8%AF%BB%E5%8F%96%E6%B8%85%E7%90%86%E4%B8%8E%E5%90%88%E5%B9%B6%E6%A0%B7%E6%9C%AC%E8%A1%A8)或[R读取清理与合并样本表](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E8%AF%BB%E5%8F%96%E6%B8%85%E7%90%86%E4%B8%8E%E5%90%88%E5%B9%B6%E6%A0%B7%E6%9C%AC%E8%A1%A8)。
5. [同一份样本表贯通R与Python](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%8C%E4%B8%80%E4%BB%BD%E6%A0%B7%E6%9C%AC%E8%A1%A8%E8%B4%AF%E9%80%9AR%E4%B8%8EPython)：先完成不依赖第三方包的读取与核对。
6. [R包Python包与可复现环境](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E5%8C%85Python%E5%8C%85%E4%B8%8E%E5%8F%AF%E5%A4%8D%E7%8E%B0%E7%8E%AF%E5%A2%83)、[R与Python绘图和统计入门](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E7%BB%98%E5%9B%BE%E5%92%8C%E7%BB%9F%E8%AE%A1%E5%85%A5%E9%97%A8)：再添加可选依赖。
7. [R与Python报错调试与求助](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E6%8A%A5%E9%94%99%E8%B0%83%E8%AF%95%E4%B8%8E%E6%B1%82%E5%8A%A9)：保存错误、环境和最小复现。

## 完成标准

能解释变量、缺失与样本ID；按ID而非行号合并；知道Python从0、R从1索引；能找到输出、读报错、保存环境信息并从干净会话重跑。

本机Python案例已运行。基础R脚本通过WebR的R 4.6.0 WebAssembly运行时验证，本机没有原生Rscript，也未验证所有CRAN/Bioconductor包或IDE安装。代码使用普通base R，学生在原生R中运行方式仍按教程。

后续进入[组学分析方法学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E5%88%86%E6%9E%90%E6%96%B9%E6%B3%95%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)或[群体遗传学分析学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E9%81%97%E4%BC%A0%E5%AD%A6%E5%88%86%E6%9E%90%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)。语言来源：[Python官方教程](https://docs.python.org/3/tutorial/)、[An Introduction to R](https://cran.r-project.org/doc/manuals/r-release/R-intro.html)。
