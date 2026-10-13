# PLINK2使用与版本管理

> 更新：2026-10-13；状态：可用；验证范围：文档核对；操作需按所用环境验证。

PLINK 2 用于基因型处理、PCA 和关联等任务；参数与默认行为需要绑定具体版本。

## 安装与记录

从 [PLINK 官方下载页](https://www.cog-genomics.org/plink/2.0/)按操作系统和 CPU 选择构建，解压到自己的工具目录。首先执行 `plink2 --version` 并记录完整输出。不要把 PLINK 1.9 和 PLINK 2 的同名参数默认视为完全相同。

本项目示例实测版本为 v2.0.0-a.7.12LM 64-bit Intel（12 Oct 2026）。实际下载的新版本可能不同，应保留版本和对应手册日期。

## 最小输入检查

```bash
plink2 --version
plink2 --pfile cohort --missing --freq --out results/input_check
```

第二条假设 `cohort.pgen/.pvar/.psam` 已存在；输出目录需预先建立。PGEN 系统以 `--pfile` 读取，BED/BIM/FAM 系统以 `--bfile` 读取。

非人类染色体设置、性染色体、倍性和额外 contig 必须核对研究物种与手册，不能用默认人类配置解释所有数据。

## 结果检查与深入

每次保留 `.log`，检查最终样本/位点数、警告与输出列。格式详见 [PLINK 文件参考](https://www.cog-genomics.org/plink/2.0/formats)。从[合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)开始练习，再进入真实数据。
