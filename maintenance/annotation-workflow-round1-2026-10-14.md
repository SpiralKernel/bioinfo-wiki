# 注释、比对与工作流第一轮（2026-10-14）

补上变异提取之后的基因模型、后果解释及可复跑工作流。新增28篇正文，修订11篇已有正文；另更新Obsidian写作入口、自动索引、仓库README和自动导航。总正文246→274，GitHub Wiki管理277个Markdown文件（正文加首页、侧边栏和索引）。这不是整个Wiki已完成的声明。

## 新内容

- 路线2篇：注释学习路线、缺口与维护优先级。
- 概念10篇：GFF/GTF、CDS/phase/剪接、链方向、后果等级、转录本选择、同源家族、低深度似然、多倍体剂量、细胞器异质性、泛基因组参考偏差。
- 方法2篇：区间/最近基因/候选映射、罕见变异负荷与SKAT。
- 工具6篇：bedtools、SnpEff、VEP、samtools、minimap2/BWA选择、Snakemake。
- 工作流8篇：注释资源准备、按ALT提取、参考转换、特殊场景分流、人工注释、FASTQ调用链、Snakemake恢复、浏览器证据。

旧概览连接到专门工具页，VEP/SnpEff别名归到各自的工具页。可复现管理页删去此前未执行的简化包装，改为实际案例入口。输入版本、转录本与多ALT关系是本轮主要检查点。

## 实际环境

Linux，本地单核/短序列；Python3.14.8、SnpEff5.4c（构建2026-02-23）、OpenJDK25.0.4.1、bedtools2.31.1、minimap2 2.30-r1287、samtools1.22/HTSlib1.22、bcftools1.22、Snakemake9.27.0。配图使用Matplotlib3.11.2；其教学Python环境含NumPy2.5.4与SciPy1.18.1。

工具在被忽略的本地目录中隔离安装。bedtools、minimap2和samtools用官方源码编译；samtools禁用curses/libcurl/bz2/lzma/ref-cache，仅验证本地文件操作。SnpEff使用官方核心包，未将可变latest URL当作版本固定依据。Java官方文档要求21+，本机使用25。Snakemake在独立venv用pip安装，不改变全局Python。

实际归档URL、SHA与大小见[source-downloads.json](../assets/annotation-workflow-round1/source-downloads.json)。jar SHA256：`5e8f75cbf908a33c6fb2e65c81e66fe31236cb21bb0195541c4703d8202c22b3`。不提交工具二进制、缓存或下载归档。Conda安装行是读者环境模板，不是本机安装记录。

## 输入与实际结果

固定输入[examples/data/annotation](../examples/data/annotation)全部人工构造：1600bp参考、2基因/3转录本、3条120bp标准CDS及蛋白、12条VCF记录/13ALT、7个边界区间，以及40条单端150bp人工reads。

[annotation_demo.py](../examples/annotation_demo.py)实际运行：

- SnpEff本地构库，3条CDS和3条蛋白检查均OK、错误0；没有使用跳过检查的选项。模型无UTR、无调控/PWM资源，相关预期提示不代表这些功能已验证。
- 12条VCF产生21条后果行：HIGH6、MODERATE6、LOW3、MODIFIER6。HIGH行只对应3个不同记录-ALT。
- multi:T=stop_gained/HIGH，multi:A=missense/MODERATE；筛选不泄漏到另一ALT。
- 325对txPlus1为missense（c.85G>A/p.Ala29Thr），对txPlus2为intron。
- 负链996 G>A对应c.5C>T/p.Ala2Val。
- bedtools gene重叠9对；exon11对对应7个不同记录；并列最近两个基因均距120。单碱基边界检查通过。
- 报告阶段核对当前输入及已建数据库校验值，拒绝混用不同阶段旧结果。

[genome_alignment_demo.py](../examples/genome_alignment_demo.py)实际运行minimap2→samtools→bcftools，得到chrToy:105 C>T、GT=0/1。40条primary reads均mapped，参考覆盖却只有169/1600bp=10.5625%，平均深度3.75。这个调用任务只预设一个SNV，不是从reads检出注释用的全部12条VCF记录。

结果副本与图在[assets/annotation-workflow-round1](../assets/annotation-workflow-round1)。annotation-summary仅省略本机绝对路径日志行，版本、检查计数和SHA保留；不发布含本机路径的原始构库/工作流日志。公开后果TSV把空文本字段显示为.，不改变列数和筛选关系。图已生成并视觉检查。

## 工作流实测与修正

[Snakefile](../examples/workflows/annotation/Snakefile)含build_database、annotate、intervals、report四条计算规则，all列出需要交付的报告、VCF和表格。

首个验证发现：若all只要求已存在的summary，删除中间后果表不一定触发重建。修正为显式要求交付表后，在新的独立目录重跑[验证器](../examples/validate_annotation_workflow.py)：

1. 首次执行四条计算规则及all，计算顺序允许调度差异。
2. 无变化重跑没有计算，跟踪产物时间戳不变。
3. 仅删除新验证目录内生成的consequences.tsv后，执行annotate/report/all；恢复表内容SHA与原表一致，数据库与区间结果时间戳不变，报告重新生成。

[实际验证JSON](../assets/annotation-workflow-round1/workflow-validation.json)记录结果。其summary SHA针对独立运行的原始summary，不等于删去本机路径后的公开annotation-summary。验证器拒绝已有工作目录，不清理读者的既有项目。

本轮仅验证缺失输出恢复，未验证强制中断、集群、云、容器或任意静默损坏；工作流并非自动对所有文件做内容校验的系统。

## 自动检查

新增7项有明确错误边界的测试：单碱基/非法GFF、两条链CDS重建、多ALT后果归属、实际边界命中、输入改变拒绝旧报告、错误蛋白拒绝构库、缺少BAM EOF检查失败。

全套45项通过、无跳过；实际环境提供bcftools及fill-tags、SnpEff/Java、bedtools、minimap2、samtools。记录见[tests.txt](../assets/annotation-workflow-round1/tests.txt)。Snakemake首次/无变化/恢复由独立验证器完成，未把这些三次运行计入45项单元/集成测试。

导出校验274篇正文的属性、内部链接、代码块与别名；写回Obsidian前核对所有变更页与本轮开始时的SHA，已有原稿先留私有备份，遇到并发修改会停止。发布仍采用受管理清单及远程人工改动保护。

## 未执行范围与剩余任务

VEP、CrossMap、IGV桌面、SKAT/专业罕见变异检验、OrthoFinder、BWA、多倍体/细胞器/泛基因组专业流程未执行；对应页是有来源的选型或操作指南。人工模型仅标准密码、phase0、完整CDS，非复杂物种注释基准。

真实物种数据库、原生R/Bioconductor真实RNA-seq、专业SV/CNV/STR/TE调用、组装、系统发育、QTL精细定位及原始蛋白/代谢处理等，见[维护优先级](../wiki/生信缺口清单与维护优先级.md)。新手可以先完成已运行的小闭环，再进入这些任务。
