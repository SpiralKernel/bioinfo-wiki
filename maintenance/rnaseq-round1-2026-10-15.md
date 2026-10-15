# 真实RNA计数与原生R第一轮（2026-10-15）

新增16篇正文，修订16篇已有正文；更新写作入口、索引、README和自动导航。正文274→290，管理293个Wiki Markdown文件。补齐公开真实计数→配对DESeq2→诊断与解释；尚未从FASTQ重新生成计数。

## 本轮内容

一条bulkRNA-seq路线；六篇概念（设计/对比、大小因子、负二项离散度、过滤/NA、VST/rlog、收缩/阈值）；一篇复杂交互/LRT方法；四篇工具（DESeq2、featureCounts、Salmon/tximport、STAR）；四篇工作流（公开airway、输入核对、FASTQ上游、结果报告）。专门术语与案例相互链接，避免在概览页复制所有操作。

旧RNA教程与模型页改为实际原生R范围；基础R样本表又在原生R执行，编程页的旧“未安装原生R”说明同步修正。GS等未运行的专业R包仍保留未测说明。

## 实际环境与输入

Linux，隔离Conda环境；R4.4.3、DESeq2 1.46.0、airway1.26.0、apeglm1.28.0、jsonlite2.0.0。这是实际复跑的固定版本，不是最新版本推荐。安装首次遭网络IncompleteRead中断，复用缓存重试成功；未修改全局R环境。

读者环境模板[examples/environments/rnaseq.yml](../examples/environments/rnaseq.yml)固定主要包版本，精确Linux构建见[linux-conda-packages.json](../assets/rnaseq-round1/linux-conda-packages.json)与[explicit记录](../assets/rnaseq-round1/linux-conda-explicit.txt)。完整依赖约400.9MB下载计划，不提交环境目录或缓存；未逐平台安装验证。

使用airway包的`airway`对象（不是另一个`gse`对象），公开研究GSE52778。4条人气道平滑肌细胞系、各有处理/对照，共8个样本。计数对象63,677行；原处理参考GRCh37/Ensembl75、STAR和summarizeOverlaps，依据[数据包来源说明](https://bioconductor.org/packages/release/data/experiment/vignettes/airway/inst/doc/airway.html)。这属于读取公开处理后计数，不是本轮运行原论文上游流程。

[provenance.json](../assets/rnaseq-round1/provenance.json)保存实际airway.RData、导出计数/样本及完整结果SHA256。计数CSV、全部结果、dds/vsd RDS在忽略的examples/output，读者用固定包和脚本重建；公开仅汇总、top50、样本设计/QC/PCA表、环境记录与图。公开样本运行ID来自原公开数据，无新增私有个体资料。

## 实际运行与检查结果

[rnaseq_airway_demo.R](../examples/rnaseq_airway_demo.R)先故意乱序样本表再按ID重排，核对4×2配对。总原始计数≥10预过滤，保留22,369个基因；`~ cell + dex`设计秩5、剩余自由度3，trt相对untrt，alpha0.05。

| 操作 | 本次结果 |
|---|---|
| 普通Wald FDR<0.05 | 4,030；上调2,208、下调1,822 |
| 有P且有padj | 17,165 |
| 独立过滤：有P、padj为NA | 5,204 |
| 保留基因集合内P为NA | 0；全零基因已在预过滤移除 |
| 关闭独立过滤的诊断对照 | 3,820显著 |
| 专门检验H0：绝对log2FC≤1 | 243显著 |
| VST PCA前两轴解释比例 | 47.84%、23.38% |

本次实际核对反向对比翻转LFC但双侧P/padj不变；关闭独立过滤的padj与BH相符；apeglm收缩结果保留原Wald P/padj。apeglm后验SD独立命名，未与收缩LFC拼造新的普通P。

VST用于PCA/距离，计数模型输入仍是原始计数。MA图边界三角代表超出显示范围，原表未截断；火山图纵轴是原P，颜色按padj，原始与收缩LFC的来源明确。图已视觉检查，修正PCA顶端标签和补充细胞系图例。[绘图脚本](../examples/plot_rnaseq_airway.R)可读已保存模型单独重画，无需重新拟合。

最终代码在新的独立输出目录完整重跑，summary与首次运行一致；没有把相同发现数视为所有软件/版本的唯一复现标准。非空输出目录拒绝重新分析，避免覆盖已有结果；绘图脚本仅重画已存在结果的图。

## 自动检查与基础R

基础输入函数[rnaseq_input_checks.R](../examples/rnaseq_input_checks.R)和[R检查脚本](../examples/test_rnaseq_inputs.R)验证10个输入/设计断言：ID乱序对齐、重复与缺样本、分数/负数/NA计数、空文库、合法配对设计、完全混杂、无剩余自由度。

新增2个Python集成测试运行原生R检查并验证既有结果不被覆盖。全套47项通过、无跳过（含之前的实际注释/比对/变异集成测试）；[记录](../assets/rnaseq-round1/tests.txt)。10个R断言由其中一个测试调用，不另外累计成10项Python测试。实际模型的5项结果性质检查在案例中执行，不计入47项。

旧programming_basics.R在同一原生R完整执行，仍得到8行、1缺失、A有效n=3/均值2、B有效n=4/均值5.5、条件系数3.5，并输出base R PDF。[记录](../assets/rnaseq-round1/base-R-programming.txt)。此前WebR验证仍是历史记录，本轮没有据此宣称所有R包或IDE都已验证。

导出校验290篇正文的属性、内部链接和代码块。写回Obsidian前逐页核对本轮初始SHA，已有原稿先留私有备份；若有并发修改会停止。Wiki同步仍使用受管理清单和远程人工修改保护。

## 未测范围与后续

未运行真实FASTQ、STAR、featureCounts、Salmon/tximport、nf-core/rnaseq、rlog、edgeR/voom、交互/LRT、富集、qPCR或功能实验。对应页是明确标注的指南；没有把本例4030个基因当成原论文结论的完全复现。

维护优先级已把“原生R真实计数DESeq2”标为本轮完成，留下真实FASTQ与多方法比较。下一批仍可按优先级进入专业SV/CNV/STR/TE、实际物种注释数据库、组装/系统发育和QTL精细定位；见[缺口清单](../wiki/生信缺口清单与维护优先级.md)。

## 发布核验

内容提交`e15c32f`与Wiki提交`7b09130`已推送。对该内容提交检查99项全部通过：主仓库变更文件59项、Wiki原文36项、重点HTML页面4项；文件核对SHA256，HTML核对Wiki正文和标题。核验针对当时的内容提交，本段和JSON随后另存为维护提交。[公开核验记录](rnaseq-publication-2026-10-15.json)。
