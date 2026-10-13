# 中文生信 Wiki

面向入门学生，从群体分析、GWAS和GS出发，连接术语解释、算法、组学工作流和实践。

**阅读入口：[GitHub Wiki](https://github.com/SpiralKernel/bioinfo-wiki/wiki)** · **[关键词索引](https://github.com/SpiralKernel/bioinfo-wiki/wiki/关键词索引)**

## 从哪里开始

- [统计学与组学验证学习路线](wiki/统计学与组学验证学习路线.md)：概率、估计、基础检验及各组学验证。
- [生信基础算法学习路线](wiki/生信基础算法学习路线.md)：数据结构、查找、图、动态规划、聚类与优化。
- [组学验证的层级与证据](wiki/组学验证的层级与证据.md)：计算、统计、技术、独立样本和功能证据。

- [中文生信学习地图](wiki/中文生信学习地图.md)：前置知识与阅读入口。
- [群体分析与GWAS学习路线](wiki/群体分析与GWAS学习路线.md)：质控、PCA、模型与关联解释。
- [GWAS软件选择与比较](wiki/GWAS软件选择与比较.md)：PLINK、GEMMA、GCTA、REGENIE、SAIGE、BOLT及育种常用工具。
- [公开小鼠数据贯通多软件GWAS](wiki/公开小鼠数据贯通多软件GWAS.md)：真实公开数据、四个软件、七种配置及结果诊断图。
- [GS算法软件与实践路线](wiki/GS算法软件与实践路线.md)：算法、六种软件、验证设计与候选预测。
- [合成家系数据贯通GS](wiki/合成家系数据贯通GS.md)：300个人工个体、GBLUP与岭回归等价、嵌套验证和60个候选预测。
- [组学分析总览与选型](wiki/组学分析总览与选型.md)：按研究问题选择测量与流程。
- [合成数据贯通PCA与GWAS](wiki/合成数据贯通PCA与GWAS.md)：本项目实际运行的练习。
- [BLAST原理与种子延伸](wiki/BLAST原理与种子延伸.md)：人工字符串教学实现。

各篇标明更新时间与验证范围。组学实践包含官方数据、检查点和详细教程入口；本机没有运行的流程已明确标注。

## 运行教学例子

Python 3.9+ 可运行序列比对教学例子；它不依赖第三方包，不是完整BLAST实现：

```bash
python3 examples/alignment_demo.py
```

群体练习另需[PLINK 2](https://www.cog-genomics.org/plink/2.0/)，使用固定种子生成120个人工样本和600个位点：

```bash
bash examples/run_population_demo.sh
# 若不在PATH：
PLINK2_BIN=/完整路径/plink2 bash examples/run_population_demo.sh
```

输出在 `examples/output/population/`，重复运行覆盖其中同名结果。详见[实测记录](maintenance/validation-2026-10-13.md)。二进制、练习输出和原稿私有备份不提交。

完整公开小鼠案例的工具依赖、运行方式与验证范围见[第二轮GWAS记录](maintenance/gwas-round2-2026-10-13.md)。代码为 `examples/gwas_software_demo.py` 和 `examples/plot_gwas_comparison.py`；公开配图与汇总指标在 `assets/gwas-round2/`，个体数据仍不纳入仓库。

GS教学例子依赖NumPy，配图另需Matplotlib：

```bash
python3 -m pip install numpy matplotlib
python3 examples/genomic_prediction_demo.py
python3 examples/plot_genomic_prediction.py
```

输出在 `examples/output/gs/`，重复运行覆盖同名文件；建议使用项目虚拟环境。实际结果和验证范围见[GS第一轮记录](maintenance/gs-round1-2026-10-13.md)。专业GS软件的模板尚未运行，教学实现不包含REML、MCMC或ssGBLUP。

统计与基础算法练习建议Python 3.10+，依赖NumPy、SciPy 1.15+（rng接口）和Matplotlib：

```bash
python3 -m pip install -r requirements-teaching.txt
python3 examples/statistics_demo.py
python3 examples/basic_algorithms_demo.py
```

[统计案例](wiki/合成数据贯通统计推断.md)实际运行了均值、配对、分类表、区间、置换、多重校正与供体层级反例；[算法练习](wiki/基础算法可复现练习.md)包含六类小型实现。两者均为人工数据，原始输出分别在 `examples/output/statistics/` 和 `examples/output/basic-algorithms/`，重复运行覆盖同名文件。版本与边界见[本轮维护记录](maintenance/statistics-round1-2026-10-13.md)。分组学验证页提供设计指南，未执行湿实验。

## 在Obsidian编写并发布

原稿在 Obsidian 的 `知识库/中文生信Wiki`；本仓库 `wiki/` 是生成的发布版。写作属性和维护规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。

```bash
python3 scripts/export_wiki.py --source '/你的Obsidian库/知识库/中文生信Wiki' --refresh-index
python3 -m pip install -r requirements-teaching.txt
python3 -m unittest discover -s tests -v
bash scripts/publish_wiki.sh
```

导出只读取六类目录：学习路线、术语与概念、方法与算法、工具、数据库、分析工作流。草稿和待编写页面默认不导出；正文属性会转换为公开的状态、更新时间及验证说明，首页、侧边栏和关键词索引自动生成。默认不修改原稿；`--refresh-index` 只刷新原稿中的自动索引。模板、写作入口、私有备份和其他Obsidian笔记不导出。

内部链接支持标题、相对笔记路径、Wiki根路径和无歧义别名；代码块与行内代码中的双括号保持原样。断链、重名、缺少必要属性、未闭合代码块会停止导出。Obsidian嵌入和标题锚点暂不支持；附件不自动复制，添加图片前需自行安排公开资源及检查标准Markdown路径。

发布脚本使用Git与已登录的GitHub CLI，在旁边的独立 `bioinfo-wiki.wiki` 仓库拉取、校验、同步并推送。仅同步清单中的文件；删除或改名只清理此前受管理的旧页，保留其他页面。若受管理页面曾在网页上修改，发布会停止，需先把差异合回Obsidian原稿。首次从旧版升级也会核对旧文件校验值。初次启用GitHub Wiki时需要先在网页创建第一页，本项目已完成。

## 项目结构

```text
examples/                  人工数据与算法教学代码
scripts/export_wiki.py     校验链接、导出文章、生成导航和索引
scripts/sync_wiki_files.py  校验清单并保护远程人工修改
scripts/publish_wiki.sh     发布到Wiki独立仓库
tests/                     导出与同步行为检查
maintenance/               验证记录（私有备份目录除外）
wiki/                      可检查和提交的发布文件
```
