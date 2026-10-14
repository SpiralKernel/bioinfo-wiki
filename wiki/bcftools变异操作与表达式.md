# bcftools变异操作与表达式

> 更新：2026-10-14；状态：可用；验证范围：bcftools1.22与HTSlib1.22人工VCF/SAM案例已执行；真实检测性能及其他专业软件未实测。

bcftools处理VCF/BCF，安装环境、字段层级和表达式语义决定操作能否按预期执行。

## 环境与下载

先按[R与Python路径文件与项目组织](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E4%B8%8EPython%E8%B7%AF%E5%BE%84%E6%96%87%E4%BB%B6%E4%B8%8E%E9%A1%B9%E7%9B%AE%E7%BB%84%E7%BB%87)下载项目并进入根目录。这里的命令面向Linux或macOS；Windows可使用已配置的Linux环境/WSL，不能把Linux二进制直接当Windows Python包安装。

已有Conda时可在终端建立独立环境；还没有Conda时按[Miniforge官方安装](https://github.com/conda-forge/miniforge)选择系统/架构，再回到这里。安装步骤按官方资料整理，本轮实际用源码隔离编译，未实测所有系统的Conda安装。

```bash
conda create -n variants -c conda-forge -c bioconda bcftools=1.22 python=3.12
conda run -n variants bcftools --version
conda run -n variants bcftools +fill-tags -h
conda run -n variants python examples/variant_extraction_demo.py
```

`+fill-tags`是本例需要的插件。报“plugin not found”先核对插件是否与该bcftools环境匹配；源码安装可按官方说明设置BCFTOOLS_PLUGINS，不能拿另一版本插件混用。Python的.venv不会自动安装这个C工具。

## 常见子命令

view筛选/子集/格式转换，norm标准化，sort排序，index索引，query导出字段，filter标记或掩蔽，+fill-tags重算指定统计。merge合并不同样本，concat拼接兼容的相同样本记录片段；两者不代替重新分型。

`-Oz`输出BGZF压缩VCF，`-Ov`普通VCF，`-Ob`压缩BCF；普通gzip文件不自动具备随机区间索引。使用`-r/-R`前检查排序、压缩和索引。

## 表达式先看层级

INFO是记录级，FMT/FORMAT是样本级。`FMT/DP>=8 & FMT/GQ>=20`要求同一样本满足；`&&`可以让不同样本分别满足。两者不是可随意替换的写法，详见[变异位点过滤与基因型掩蔽](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E4%BD%8D%E7%82%B9%E8%BF%87%E6%BB%A4%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%8E%A9%E8%94%BD)。

本例工具版本为1.22，不称为最新版本。可执行案例和实际输出见[人工VCF贯通变异分类与提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5VCF%E8%B4%AF%E9%80%9A%E5%8F%98%E5%BC%82%E5%88%86%E7%B1%BB%E4%B8%8E%E6%8F%90%E5%8F%96)。依据：[安装](https://samtools.github.io/bcftools/howtos/install.html)、[Bioconda包](https://bioconda.github.io/recipes/bcftools/README.html)、[表达式教程](https://samtools.github.io/bcftools/howtos/filtering.html)。
