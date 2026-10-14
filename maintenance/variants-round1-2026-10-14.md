# 变异检测、分型与提取首轮记录 · 2026-10-14

## 内容与原稿

新增30篇完整正文：1条路线、6篇概念、5篇原理、6篇软件、12篇工作流。覆盖SNV/Indel/MNV、SV断点与事件、CNV/PAV、STR/重复扩增、TE插入、生殖系与体细胞场景，以及标准化、类型/区域/样本提取和质量处理。

更新13篇已有正文，另更新Obsidian开始写作入口和自动关键词索引。原稿保存前核对基线SHA-256并备份修改页，共写入45个Markdown；保存后逐文件确认与暂存审阅版一致。导出246篇正文及首页/侧边栏/关键词索引，共249个受管理Markdown。导出元数据、内链、代码块、文件哈希及公开图像路径检查通过。

## 实际软件与构建

Linux、Python3.14.8；官方固定源码bcftools1.22，bundled HTSlib1.22；源码隔离编译并执行+fill-tags插件。构建关闭libcurl、bz2、lzma和ref-cache，本轮测试仅用本地VCF/BCF/SAM/FASTA及BGZF/CSI操作，不评价远程协议或其他压缩功能。绘图使用已验证的项目Matplotlib环境。

源码下载地址：https://github.com/samtools/bcftools/releases/download/1.22/bcftools-1.22.tar.bz2

源码包SHA-256：`f2ab9e2f605b1203a7e9cbfb0a3eb7689322297f8c34b45dc5237fe57d98489f`。

没有在Windows/macOS逐一安装测试Conda/Bioconda；安装命令按官方资料整理。不是以固定测试版本声称当前最新版本。

## 固定人工输入与实际结果

examples/data/variants包含两条人工参考（1400/400 bp）及fai、16记录/3样本VCF、一个BED目标、S01样本表、40条人工已比对SAM记录，以及独立PAV状态示例。所有数据人工构造，不对应真实样本/物种/基因。

variant_extraction_demo.py复制输入到独立输出后运行bcftools，拒绝输出覆盖/包含输入目录。命令使用参数数组而非shell拼接，记录相对路径，不公开本机二进制位置。输出细节与命令记录在assets/variants-round1，可由源码和固定输入重建。

| 检查 | 实际结果 |
|---|---|
| 多等位拆分 | 16→17条，mixed两个ALT分别重编码GT |
| 左对齐 | left_shift从200变179 |
| 序列分类 | SNV5、Indel3、MNV1，共9条 |
| 原子化序列集合 | 9→10条，不把新记录认作独立事件 |
| 符号/标记集合 | DEL、INV、DUP、CNV、STR、TE各1；BND2条 |
| BND事件关系 | 2个互相MATEID引用的断端，共1个EVENT |
| FILTER | 仅PASS15；PASS或未评估16 |
| BED位置302 | 按record跨度命中small_del1；按POS命中0 |
| 单样本携带 | 先选S01再筛GT=alt，15条 |
| 质量表达式 | 同一样本DP/GQ条件16，跨样本条件17 |
| 小变异调用 | 人工40条SAM中20REF/20ALT，chrToy:100 G→A，GT=0/1 |

SNV原AC5/AN6/AF0.833333；view选择S01后AC1/AN2但旧AF仍0.833333；+fill-tags明确重算AF=0.5。low_site低质量S01被掩蔽，S02保持0/0，记录仍存在，重算AC0/AN2/AF0。PASS不保证每个样本GT合格。

类型表针对本例构造的互斥记录分组；生物学上CNV、TE、STR与SV可交叉，不能推广为通用分类法。缺失、无报告、纯合参考及未知状态保持区分。

## PAV矩阵整理

pav_matrix_demo.py用标准库读取已人工指定的present/absent/unknown证据，按特征/样本匹配，拒绝重复，不把缺少证据的组合填0。3×3矩阵得到5个1、2个0、2个NA；只做格式整理，不从序列发现PAV，也不进行同源或共线性推断。

## 检查及修订

38项测试通过，无跳过。新增7项覆盖输入/输出目录隔离、FASTA索引偏移与全部VCF REF一致、混合ALT拆分后的独立GT核对、错误REF主动停止、BND伴随关系、PAV乱序/未知与缺少组合、重复PAV证据拒绝。其余31项原有检查全部通过。若运行环境没有bcftools，3项工具集成测试会明确跳过；本次通过指定BCFTOOLS_BIN和匹配BCFTOOLS_PLUGINS实际执行。

开发中实测定位并修正：相对二进制路径在切换工作目录后失效，现先转绝对执行路径；把样本子集和GT表达式合在同一命令会因评估顺序得到意外记录，现明确分两步，文档同步给出正确15条。查明&/&&及PASS/点的差异并加入人工反例。

最后执行入口：

```bash
python3 examples/variant_extraction_demo.py --bcftools /你的实际路径/bcftools
python3 examples/pav_matrix_demo.py
.venv/bin/python examples/plot_variant_extraction.py
.venv/bin/python -m unittest discover -s tests -v
```

源码安装用户还需将BCFTOOLS_PLUGINS指向相同构建的plugins目录；测试使用BCFTOOLS_BIN指向对应工具。读者的Conda入口及项目路径见Wiki环境页。配图逐项来自实际summary.json，并已目视检查标题、轴、类别及数值。

## 未执行范围与资料

未运行真实read mapper、真实队列小变异检测、GATK、DeepVariant、Clair3、Sniffles、DELLY、CNVkit、SyRI、ExpansionHunter、TRGT、ngs_te_mapper2、McClintock、hap.py或Truvari。相应专业检测命令为官方资料核对的模板，不是性能验证。CN、REPCN与TEFAMILY在人工VCF中是预先指定值，后两者为自定义教学字段；不能当作对应专业检测结果或通用字段。

核对资料包括VCF规范、bcftools官方安装/调用/查询/表达式/fill-tags说明及1.22源码，GATK生殖系与体细胞教程，DELLY/Sniffles当前README，Clair3当前接口及DeepVariant固定r1.9示例，CNVkit分段/导出，SyRI示例，EH/TRGT输出及TE软件说明。专业模板不承诺跨所有版本通用；DELLY sr/lr接口与旧版尤其需区分。正文保留具体原始来源链接和更新时间。

## 新增正文

- 分析工作流 / CNV检测与结果提取
- 分析工作流 / PAV检测与存在缺失矩阵
- 分析工作流 / STR与重复扩增检测及提取
- 分析工作流 / VCF标准化多等位拆分与表示
- 分析工作流 / 人工VCF贯通变异分类与提取
- 分析工作流 / 体细胞与低频变异分析边界
- 分析工作流 / 变异位点过滤与基因型掩蔽
- 分析工作流 / 按区域样本与基因型提取变异
- 分析工作流 / 按类型提取SNPIndel与结构变异
- 分析工作流 / 短读长SNP与Indel检测流程
- 分析工作流 / 转座子插入检测与提取
- 分析工作流 / 长读长小变异检测与模型选择
- 学习路线 / 变异检测分型与提取学习路线
- 工具 / DELLY结构变异与群体分型
- 工具 / GATK小变异检测与联合分型
- 工具 / Sniffles长读长结构变异实践
- 工具 / bcftools变异操作与表达式
- 工具 / 变异检测软件选择与适用场景
- 工具 / 重复序列与转座子变异软件
- 方法与算法 / CNV深度校正分段与拷贝数估计
- 方法与算法 / SV合并匹配与群体再分型
- 方法与算法 / 变异评估真值集合与可检测区域
- 方法与算法 / 小变异检测的似然与局部组装
- 方法与算法 / 结构变异检测的读对分裂读段与组装
- 术语与概念 / GVCF联合分型与参考置信度
- 术语与概念 / SNVIndelMNV与复杂变异
- 术语与概念 / STR重复扩增与移动元件插入
- 术语与概念 / VCF中的SVTYPEEND与BND
- 术语与概念 / 变异质量基因型质量与等位平衡
- 术语与概念 / 结构变异CNV与PAV

## 素材SHA-256

| 文件 | SHA-256 |
|---|---|
| `cnv.tsv` | `b81356da1dba6a1bd3fc4d33559bf614077283d2d78cdf985da2f01d0bfb2a79` |
| `commands.json` | `7290bb84df9432ffa9d9c7efc6fc716bfbf77d7c1084cf2a579d05c6bfca1d54` |
| `normalized.vcf` | `fa2464dc960de4905ccbb058d97b8817559e30b69763dab648f86aa1aebe8d2f` |
| `pav-matrix.tsv` | `d265386266c60600756845a6b4ff7be5ad74b6ececbe5a511b00fe0fa032f4dd` |
| `pav-summary.json` | `a08162bc40f7ae4c9a02ced2f1687f339cab39d199b1afe552184efd08e4df09` |
| `str.tsv` | `7d40a1341ea35f514d0ec32147d8aa1a81877c6646820b4f3b18d3f83fa3864e` |
| `summary.json` | `26b107916ec2861fd239e2cb431f3b9cb0ef7440039be0ec9ab32a0d1c54e77d` |
| `variant-records.png` | `5d3029cbe52d21baa45e46d0e75670c05b2e455d194b4429eac3cc19fc8ad10c` |
| `variant-records.svg` | `a60c879a0071cc523910a6e16a6d3d299354de7eac6cf5cdb2ff83fc08b86332` |
