# 全类型变异检测第二轮（2026-10-15）

新增28篇正文、修订21篇已有正文，另更新写作入口、关键词索引、首页、侧边栏和README。正文290→318，共321个受管理Wiki Markdown文件。按输入、平台、倍性和证据组织SNP/Indel、SV、CNV/PAV、STR/VNTR、TE插入、组装比较和体细胞变异；这些类别存在交叉，不能简单相加为互斥事件数。

## 内容与入口

[总览与证据地图](../wiki/全类型变异检测总览与证据地图.md)先区分从reads发现变异、对候选集合分型、从既有VCF提取结果，再连接学习路线、基础概念、软件和工作流。新增内容包括1篇路线、6篇概念、3篇方法、11篇工具和7篇工作流。

工具页补充FreeBayes、DeepVariant、Clair3、cuteSV、pbsv、SVIM-asm/dipcall、CNVkit、TRGT、ExpansionHunter、McClintock/xTea及Truvari。保留已有GATK、bcftools、DELLY等入口。指南明确区分命令模板与本轮实际运行；并未把全部软件或真实数据验证标记为完成。

## 实际环境与输入

Linux隔离环境：Python3.11.17、Sniffles2.8.1、Truvari5.5.0、FreeBayes1.3.10、minimap2 2.30-r1287、samtools1.22.1；另外运行TRGT5.1.0-ec66463。这些是本轮固定实测版本，不代表最新版本推荐。主要包约束见[环境模板](../examples/environments/variant-calling.yml)，完整Conda构建及Python发行包见[environment.json](../assets/variant-detection-round2/environment.json)。回归检查和绘图另加SciPy、Matplotlib；未逐平台重新创建环境模板。

SV案例使用固定种子20261015构造100kb参考序列、两个样本各160条16kb无测序错误的人工读段；变异样本包含杂合500bp缺失和300bp插入，另一份样本为参考对照。这不是HiFi真实错误模型。FreeBayes复用已有完全人工参考和40条短读段。输入SHA256及脚本SHA256见[provenance.json](../assets/variant-detection-round2/provenance.json)，短读长输入SHA另见[FreeBayes汇总](../assets/variant-detection-round2/freebayes-summary.json)。

TRGT使用PacBio仓库固定提交`b21c6217eeaef9a080205932fe29f730dc00e31f`提供的5个微型输入，总计342,835字节。清单保存每个文件URL、大小与SHA256：[trgt-inputs.json](../examples/data/variant-detection/trgt-inputs.json)。下载的Linux x86_64工具版本和发布包SHA见[下载记录](../assets/variant-detection-round2/trgt-downloads.json)。工具与原始fixture遵循[其原协议](https://github.com/PacificBiosciences/trgt/blob/b21c6217eeaef9a080205932fe29f730dc00e31f/LICENSE.md)，没有改标为MIT或CC0；公开仓库不分发工具或原始BAM。本轮仅用于PacBio提供的输入。

## 实际结果和解释边界

| 案例 | 本次结果 | 解释限制 |
|---|---|---|
| 人工SV发现 | 500bp DEL、300bp INS均检出，V01均为0/1 | 两个简单人工事件，不估计真实准确率 |
| Truvari匹配 | TP-base=2、TP-comp=2、FP=0、FN=0；2个GT匹配，0个GT不匹配 | 仅指定区域及明确匹配参数，不能外推复杂重排 |
| 参考对照单样本调用 | 0条变异记录 | 无记录不等于已完成参考分型 |
| SNF群体调用 | R01两个位点均保留缺失 | 不把缺失批量改成0/0 |
| R01候选强制分型派生文件 | 两位点GT=0/0、DV=0、DR=31/27、GQ=0 | GQ=0，不作为高置信参考证据 |
| FreeBayes二倍体短读长 | chrToy:105 C>T，GT=0/1 | 未验证多倍体或真实小变异性能 |
| TRGT官方微型输入 | TR1，AL=33/33bp，MC字符串11/11，SD=15/14 | 单个位点，不是人群或平台性能评估 |

SV流程实际执行minimap2、samtools、Sniffles发现/SNF群体/强制分型、Truvari比较。[SV汇总](../assets/variant-detection-round2/sv-summary.json)与[匹配汇总](../assets/variant-detection-round2/truvari-summary.json)可核对原值。Truvari限定区域，并显式设置PASS、最小大小50、距离100、相似度0.7、单一匹配；不混用TP-base与TP-comp。

TRGT目录区间为BED的`chrA:10001–10061`，即0基半开区间；重复本体的1基闭区间为10002–10061，共60bp。VCF POS=10001是左侧padding锚点，AL=33不含该锚点。不能因教程标题涉及重复扩增就把本例称为相对参考的扩增。完整字段见[TRGT汇总](../assets/variant-detection-round2/trgt-summary.json)。

### Sniffles2.8.1格式兼容处理

本轮实际遇到强制分型输出的FORMAT四个键`GT:GQ:DR:DV`对应五个值，末尾多一个缺失相位值；且样本表头继承候选V01，实际输入BAM是R01。原生VCF无法由htslib正常解析，保留原件，不原地改写。

[脚本](../examples/variant_calling_demo.py)仅针对已确认的`genotypeSource=Sniffles2_2.8.1`、已声明PS、单样本且完全匹配的四键/五值末尾点格式生成派生文件：补充PS键，并在确认BAM RG的SM仅为R01后修正样本表头。GT/GQ/DR/DV、原始值和前8列不变；其他版本或格式不匹配则停止。[审计摘要](../assets/variant-detection-round2/force-format-audit.json)保留原生/派生表头、样本值与两份SHA。

强制分型INFO中的SUPPORT/VAF/COVERAGE可能继承候选V01，不能当作R01支持；此处只读取当前样本FORMAT的DR/DV。群体调用另行提供参考序列，保留有效REF与锚点；没有用兼容处理把群体缺失改为参考。

## 两位子代理的纠错与询问

两位代理分别负责入门读者视角和技术事实，均完成初稿审查与修订后复核。问题由主代理查原始输出、安装源码和官方文档后处理；没有留下需要用户决定的阻塞项。

| 角色提出的问题 | 已处理的结果 |
|---|---|
| 读者：从哪个输入开始，发现和提取是否混淆？ | 总览先分reads发现、候选分型、已有VCF提取；提前列平台、倍性和物种条件 |
| 读者：CN=1能否写成缺失，缺失值能否补零？ | 区分拷贝数基线、PAV定义和未知状态；群体实例保留缺失 |
| 读者：TRGT的目录、路径、单位和重复中断怎么理解？ | 解释catalog文件含义，统一TRGT_BIN路径；给出BED/VCF换算、AL/MC单位及中断示例 |
| 读者：如何看结果、重跑会不会覆盖？ | 补全json.tool命令、字段表和结果图；分析脚本拒绝非空输出目录 |
| 技术：cuteSV是否默认分型，pbsv的CCS分支是否正确？ | cuteSV模板显式使用--genotype，pbsv区分CCS选项与平台；仍标未实际运行 |
| 技术：Sniffles强制分型是否样本错标，格式是否有效？ | 核对BAM与安装源码，限定版本的派生兼容处理并保留原件、SHA及GQ=0解释 |
| 技术：FreeBayes缺少SVTYPE时解析是否崩溃？ | 改为先检查INFO字段是否存在，不伪造SV字段；加入回归检查 |
| 技术：两条BND是否两件事件，TP和GT是否正确统计？ | 区分记录、断点连接和完整复杂事件；报告两类TP与GT匹配，不臆造复杂事件重建 |
| 技术：TRGT锚点、MC类型、数据授权能否核对？ | 用实际VCF核对坐标和字符串字段，固定官方fixture及原协议 |

最终复核确认上述问题已解决。结果图使用标准Matplotlib生成并经过视觉检查；[图及其范围说明](../assets/variant-detection-round2/README.md)明确两个案例的不同单位。

## 验证与维护

新增7项自动测试，覆盖小变异缺失SVTYPE、限定格式兼容及拒绝条件、非空输出保护、实际SV与FreeBayes、实际官方TRGT及输入SHA拒绝。完整54项测试通过、无跳过；[测试记录](../assets/variant-detection-round2/tests.txt)。其他软件命令模板不因这54项测试而被标记为实测。

最终调用脚本在新输出目录重跑，公开汇总来自最终代码。导出检查318篇正文的属性、别名、内部链接和代码块；发布同步检查321个受管理页面。Obsidian写回前逐页核对原稿初始SHA，既有原稿先留私有备份；遇到并发改动则停止。Wiki发布保留远程人工修改保护。

真实SV基准、真实CNV/LOH、真实TE、组装比较、复杂重排重建、体细胞检测以及多平台/多倍体系统比较仍未运行。相关页已提供选型、输入、步骤和验证边界，后续应逐条补公开数据贯通案例，而非把概览等同于全部实测完成。
