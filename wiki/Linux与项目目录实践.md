# Linux与项目目录实践

> 更新：2026-10-13；验证范围：文档核对；操作需按所用环境验证。

先学会识别路径、检查文本和保存日志，就能建立可追溯的最小分析项目。

## 在项目根目录组织输入输出

建议使用 `data/raw/` 保存原始输入，`data/processed/` 保存派生数据，`scripts/` 保存代码，`results/` 保存结果，`logs/` 保存日志。原始输入以独立校验值记录，派生文件使用不同路径。

```bash
pwd
mkdir -p data/raw data/processed scripts results logs
head -n 5 samples.tsv
wc -l samples.tsv
sha256sum samples.tsv
```

命令需要在你自己的项目目录运行。`wc -l` 统计换行，不直接等于样本数，标题行和特殊格式均需考虑。文件名含空格时加引号。

## 保存一次运行的上下文

```bash
python3 --version > logs/environment.txt
python3 scripts/analysis.py > logs/analysis.log 2>&1
```

第二条是结构示例，需要已有 analysis.py；重定向会覆盖同名日志，可使用带日期的文件名。查看退出码和日志，也检查输出内容，而不只看文件是否存在。

更完整的依赖管理见[可复现分析与工作流管理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%AF%E5%A4%8D%E7%8E%B0%E5%88%86%E6%9E%90%E4%B8%8E%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%AE%A1%E7%90%86)。命令语义深入看 [GNU Coreutils 手册](https://www.gnu.org/software/coreutils/manual/coreutils.html)和 [Bash 重定向说明](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)。
