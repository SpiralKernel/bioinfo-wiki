# 组学方法、群体遗传与R/Python首轮记录 · 2026-10-14

## 内容与保存

新增35篇完整正文：23篇组学/群体遗传、12篇R/Python。覆盖RNA计数、批次整合、单细胞表示与供体比较、表观组、蛋白、代谢、微生物与多组学；群体部分覆盖多样性、FST、祖源、近交/ROH、LD、选择与历史。编程部分从安装和运行入口进入变量、索引、缺失、ID合并、绘图、路径、环境与调试。

更新19篇原有正文，另更新Obsidian开始写作入口与自动关键词索引。总地图、组学总览、旧群体/GWAS路线和各组学流程均接入新方法页。保存前核对原稿基线SHA-256，修改前备份；本轮56个Markdown文件写入Obsidian，随后逐文件确认与暂存审阅版一致。

导出216篇正文及首页、侧边栏、关键词索引，共219个受管理Markdown页面。公开导出逐文件SHA-256一致，内部链接与元数据校验通过，公开图像路径全部存在。原稿私有备份、运行依赖、输出缓存均不提交。

## 两种审阅与处理

按用户要求使用两个子代理，只读审阅，不进行写入、安装或发布。读者代理提出11项建议，技术代理提出7项问题；全部采纳修订，随后两者定向复核均通过。定向复核为读文档和代码，不声称再次执行所有流程。

| 编号 | 问题 | 修订 |
|---|---|---|
| R1 | 下载入口不明确 | 路线与案例加入仓库、ZIP下载及解压层级 |
| R2 | 不会进入项目目录 | 补macOS/Linux、PowerShell的cd/目录检查，以及RStudio Existing Directory步骤 |
| R3 | 环境安装与运行不一致 | 所有新增第三方依赖例子统一使用.venv完整解释器路径，补Windows命令 |
| R4 | RNA实践直接从library开始 | 包环境页补BiocManager安装airway/DESeq2，旧RNA页明确链接和未实测范围 |
| R5 | 总地图遗漏新路线 | 地图、总览、旧群体路线、Obsidian入口、导出首页、README接入 |
| R6 | 基础语法缺解释 | 补循环/逻辑筛选/函数返回解释、预期输出与手算小改动 |
| R7 | joined尚未生成 | 绘图页先source完整R脚本，再解释参考A、截距2与B系数3.5 |
| R8 | 修改副本不会影响固定输入 | 明确复制整个项目、运行副本脚本、具体改ID及预期错误，说明--output含义 |
| R9 | 群体输入输出混淆 | 解释内置8×12矩阵、导出TSV为输出、A首位点手算与12位置分母 |
| R10 | 群体符号定义不足 | 补a1/θW、HT/HS、dXY定义；LD改用位点1/2避免与群体A/B混淆 |
| R11 | 原则缺可执行完成标准 | 增加路线完成表、低计数收缩例子、完全混杂反例与前置链接 |
| T1 | R数字ID丢前导零 | 显式字符列读取，完整脚本和教程同步；WebR核验001保留 |
| T2 | Python接受NaN/Inf | math.isfinite拒绝非有限值，JSON allow_nan=False；R同步拒绝非有限文本 |
| T3 | LD/FST广播静默错误 | 检查维度、长度/位置数、非空及二元完整性，加入回归检查 |
| T4 | 单细胞矩阵方向混淆 | 区分10x/R常见方向与AnnData细胞×基因，说明obs/var，不一律转置 |
| T5 | 历史推断μ/g轴单位笼统 | 明确每世代μ影响尺度，固定μ时g翻倍只把世代换算年份翻倍 |
| T6 | selscan条件一概而论 | 区分默认分相与显式未分相模式、0/1编码方向、iHS与XP标准化 |
| T7 | GWAS过滤向频谱迁移 | 新概念/软件与旧质控页均阻断MAF过滤/LD剪枝集合的机械复用 |

## 实际运行：R/Python表格

人工测量表8行，元数据故意乱序；按sample_id合并后保留S04缺失。Python 3.14.8执行标准库表格代码和Matplotlib 3.11.2绘图。base R完整脚本通过WebR的R4.6.0（wasm32-unknown-emscripten，webr_0.6.0）运行，包含读取、merge、NA处理、均值、lm和PDF图。

两种输出CSV按字段和数值逐行比较，语义一致，不要求CSV字节格式相同。两者8行、1缺失；A有效n=3、均值2；B有效n=4、均值5.5。R参考A时截距2、B系数3.500000000000002。修改虚拟输入为001后完整R脚本仍保留前导零；把测量值改为NaN后主动停止。Python对应边界由测试覆盖。

R只通过WebR执行，本机未安装原生Rscript；没有安装/运行DESeq2、airway、pandas、tidyverse等第三方专业包，也未验证Windows/macOS安装或IDE。普通Rscript/source命令是给读者的原生运行入口，不能称为本机原生R实测。R PDF用Courier及短标题，渲染预览后确认标签未截断；三张新图均目视核对。

## 实际运行：群体教学

NumPy2.5.4，固定种子20261013；8条人工完整已分相二元单倍型×12个可检测位置，A/B各4条，不变位置保留。

| 指标 | A | B | 合并 |
|---|---:|---:|---:|
| S | 5 | 4 | 5 |
| π/位点 | 0.2222222222 | 0.1805555556 | 0.2291666667 |
| θW/位点 | 0.2272727273 | 0.1818181818 | 0.1606978880 |
| Tajima D | -0.2124916997 | -0.0650102495 | 1.9321045045 |

描述性等群体权重(ΣHT−ΣHS)/ΣHT=0.2467532468，未做有限样本校正，绝非Weir–Cockerham或Hudson软件复现。合并前两位点r²=0.2177777778，B中第一位点单态，r²为null。

中性二倍体Wright–Fisher固定Ne50/500，p0=0.5，40代、500次独立群体模拟，无选择/突变/迁移。末代频率方差0.0800439264/0.009943403984，理论0.08275706036/0.009807447316。没有从数据反推Ne，没有真实选择显著性、VCF、缺失/基因型似然、祖源、ROH或专业历史软件运行。

## 检查

31项测试通过：新增7项验证按ID与乱序合并、缺失与已知均值、重复/不匹配ID、前导零及非有限值；群体π与直接序列两两差异对照、增加不变长度的分母影响、LD配对/等位翻转/单态/形状边界、描述性分化边界与矩阵输入检查。既有24项全部通过。

运行入口（本机使用隔离Python环境；WebR核验在隔离本地依赖中执行）：

```bash
python3 examples/programming_basics.py
.venv/bin/python examples/programming_basics.py --plot
.venv/bin/python examples/population_genetics_demo.py
.venv/bin/python -m unittest discover -s tests -v
```

R代码为examples/programming_basics.R。正常原生入口为Rscript或RStudio source；本轮执行边界见上文，环境信息和跨语言比对结果在assets/programming-round1。群体完整人工汇总和图在assets/omics-population-round1。

新方法正文依据各自官方手册/原始论文；审查后的软件条件额外核对了Bioconductor安装说明、AnnData官方定义、PSMC绘图实现、selscan官方README。专业组学和群体软件流程为原理/文档核对，没有宣称性能基准或实测成功。

## 新增正文

- 分析工作流 / 人工数据贯通群体遗传统计
- 分析工作流 / 同一份样本表贯通R与Python
- 分析工作流 / 组学方法比较与敏感性分析
- 学习路线 / R与Python生信编程入门路线
- 学习路线 / 组学分析方法学习路线
- 学习路线 / 群体遗传学分析学习路线
- 工具 / Notebook脚本与命令行运行
- 工具 / Python变量容器循环与函数
- 工具 / Python读取清理与合并样本表
- 工具 / R与Python安装环境与编辑器
- 工具 / R与Python报错调试与求助
- 工具 / R与Python绘图和统计入门
- 工具 / R与Python路径文件与项目组织
- 工具 / R包Python包与可复现环境
- 工具 / R向量数据框索引与函数
- 工具 / R读取清理与合并样本表
- 工具 / 群体遗传软件与输入选择
- 方法与算法 / FST与群体分化估计
- 方法与算法 / LD衰减与遗传距离分析
- 方法与算法 / RNA计数模型差异表达与效应收缩
- 方法与算法 / 亲缘近交与ROH分析
- 方法与算法 / 代谢组注释定量与多变量分析
- 方法与算法 / 单细胞差异表达与差异丰度
- 方法与算法 / 单细胞降维邻居图与聚类原理
- 方法与算法 / 多组学整合与潜变量模型
- 方法与算法 / 差异峰与差异甲基化方法
- 方法与算法 / 微生物组组成差异与多样性方法
- 方法与算法 / 祖源推断与混合群体模型
- 方法与算法 / 组学批次校正与信号保留
- 方法与算法 / 群体历史共祖与有效群体大小推断
- 方法与算法 / 蛋白质鉴定FDR与差异丰度
- 方法与算法 / 选择扫描与中性替代解释
- 术语与概念 / 有效群体大小漂变与近交
- 术语与概念 / 等位基因频率杂合度与核苷酸多样性
- 术语与概念 / 选择中性模型与群体历史

## 本轮公开素材SHA-256

| 文件 | SHA-256 |
|---|---|
| `assets/omics-population-round1/diversity-and-drift.png` | `b5184bf6bf936ed518995074534b0df937ffde132d651c62ab230dd6f64dd10b` |
| `assets/omics-population-round1/diversity-and-drift.svg` | `e84cd5505393d92dab8ad1c201daee45c84cd1c9b512755fef995a025b16a682` |
| `assets/omics-population-round1/summary.json` | `5d20d2b57b8383c9f4949e68d575b3c7a6dabfa6c1cf281b85d0df8ddaaeae71` |
| `assets/programming-round1/python-summary.json` | `b641d6698111ece6e38b0b84cf4562c123f6ae3b7093b27244c0d0059c87ffe1` |
| `assets/programming-round1/python-values.png` | `6ba4debfbf780422b052a780a21b3368f5f51bbee73ce5c84568e233de88ad80` |
| `assets/programming-round1/r-session-info.txt` | `99a61f8c2302e6a28169995803fa36ffe4cb51cae61b75383d6876a381ad9792` |
| `assets/programming-round1/r-values.pdf` | `78b9ce58bda8b4dfed348a8c6f774f345935fd68d252b85b2894a636ab1deee1` |
| `assets/programming-round1/r-values.png` | `84ef503abc71906cd86c76a47371474fbd9eb5d5c1002bbcb7f3c18008f29df3` |
| `assets/programming-round1/validation.json` | `ff262db841f457fd686725571c689d3453451b19be690ad7e97fa8b11b166f2d` |

## 发布后核验

正文与素材发布完成：主仓库内容提交`5bb3965`，Wiki提交`2ecda8c`。主仓库首次HTTP 408后确认未接收；按相同提交重试成功，没有改写远端历史。

139项公开请求全部通过：77个主仓库变更文件、58个Wiki变更文件（含清单），逐项HTTP 200且SHA-256与本地一致；另4项首页/三条新学习路线HTML入口正常显示Wiki内容。记录见[公开发布核验JSON](omics-population-programming-publication-2026-10-14.json)。审计记录本身随后单独提交，不改变已核验的正文、代码或素材。
