# R与Python路径文件与项目组织

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

项目根目录和当前工作目录决定相对路径，从找得到输入和输出开始组织代码。

## 找到并进入根目录

根目录是同时包含README.md、examples、scripts和wiki的文件夹，解压后可能叫bioinfo-wiki-main。可直接在这一层打开终端；若终端在别处，用`cd`进入。下面引号中的路径是**示意路径，必须替换成你的实际解压路径**。

macOS/Linux系统终端：

```bash
cd "/实际解压位置/bioinfo-wiki-main"
pwd
ls
```

Windows PowerShell：

```powershell
cd "C:\实际解压位置\bioinfo-wiki-main"
Get-Location
Get-ChildItem
```

检查列表里是否能看到README.md和examples；若只看到一个bioinfo-wiki-main文件夹，还需进入一层。然后在同一终端运行[同一份样本表贯通R与Python](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%8C%E4%B8%80%E4%BB%BD%E6%A0%B7%E6%9C%AC%E8%A1%A8%E8%B4%AF%E9%80%9AR%E4%B8%8EPython)的命令。

## RStudio中设置项目

打开 File → New Project → Existing Directory，选择上述根目录，创建并打开该项目。下次打开生成的`.Rproj`文件即可回到此目录。先在**R控制台**检查：

```r
getwd()
file.exists("examples/data/programming_measurements.csv")
```

第二行应为`TRUE`。若为`FALSE`，重新检查项目选中了哪一层；也可临时执行`setwd("C:/你的实际路径/bioinfo-wiki-main")`，随后再次验证。R里的Windows路径可用正斜杠，不能原样粘贴包含未转义反斜杠的路径。

Python控制台也可检查：

```python
from pathlib import Path
print(Path.cwd())
print(Path("examples/data/programming_measurements.csv").exists())
```

第二行布尔结果应为`True`。相对路径从当前目录解释，绝对路径从系统根或盘符解释。

## 组织规则

原始输入单独保存，代码放脚本，输出与日志单独目录。用路径函数组合路径，避免公开代码硬编码个人桌面目录。R脚本要求从项目根目录启动；Python脚本通过自身位置确定项目目录，Notebook仍需另确认当前目录。

这里的目录操作按官方界面与文档整理，未在Windows/macOS分别实测安装。基础目录实践见[Linux与项目目录实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Linux%E4%B8%8E%E9%A1%B9%E7%9B%AE%E7%9B%AE%E5%BD%95%E5%AE%9E%E8%B7%B5)，第一轮不要求先学Linux。来源：[Python pathlib](https://docs.python.org/3/library/pathlib.html)、[R工作目录](https://stat.ethz.ch/R-manual/R-devel/library/base/html/getwd.html)。
