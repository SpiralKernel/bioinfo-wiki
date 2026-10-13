# 中文生信 Wiki

面向入门学生，按研究问题查概念、理解算法、选择流程并完成实践。

## 建议从这里开始

- [中文生信学习地图](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%B8%AD%E6%96%87%E7%94%9F%E4%BF%A1%E5%AD%A6%E4%B9%A0%E5%9C%B0%E5%9B%BE)：了解前置知识和阅读顺序。
- [群体分析与GWAS学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E5%88%86%E6%9E%90%E4%B8%8EGWAS%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)：沿熟悉的主线进入分析。
- [GWAS软件选择与比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E9%80%89%E6%8B%A9%E4%B8%8E%E6%AF%94%E8%BE%83)：按场景选模型，进入各软件详解。
- [组学分析总览与选型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E5%88%86%E6%9E%90%E6%80%BB%E8%A7%88%E4%B8%8E%E9%80%89%E5%9E%8B)：按测量对象选择组学流程。
- [关键词索引](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%B3%E9%94%AE%E8%AF%8D%E7%B4%A2%E5%BC%95)：搜索中文名、英文名和缩写。

## 可以立即运行的练习

- [合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)：120 样本、600 位点的实测示例。
- [公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)：四个软件、七种配置的公开数据案例。
- [BLAST原理与种子延伸](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLAST%E5%8E%9F%E7%90%86%E4%B8%8E%E7%A7%8D%E5%AD%90%E5%BB%B6%E4%BC%B8)：用人工字符串理解启发式与精确比对。

其他流程分别提供官方公开数据和实践入口，并注明文档核对与实际运行的区别。

## 学习路线（4）

- [GWAS软件选择与比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E9%80%89%E6%8B%A9%E4%B8%8E%E6%AF%94%E8%BE%83)：先根据性状、样本相关性、物种和数据规模选择模型，再选择能够实现并验证它的软件。
- [中文生信学习地图](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%B8%AD%E6%96%87%E7%94%9F%E4%BF%A1%E5%AD%A6%E4%B9%A0%E5%9C%B0%E5%9B%BE)：从问题、数据和检查点进入生信，按需要跳转到概念、算法、组学流程及实践。
- [组学分析总览与选型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E5%88%86%E6%9E%90%E6%80%BB%E8%A7%88%E4%B8%8E%E9%80%89%E5%9E%8B)：先明确测量对象和研究问题，再选择输入、模型及可以支持的结论。
- [群体分析与GWAS学习路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E5%88%86%E6%9E%90%E4%B8%8EGWAS%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF)：从基因型编码和样本审计出发，依次完成群体探索、关联分析和证据解释。

## 术语与概念（31）

- [ASV与微生物多样性](https://github.com/SpiralKernel/bioinfo-wiki/wiki/ASV%E4%B8%8E%E5%BE%AE%E7%94%9F%E7%89%A9%E5%A4%9A%E6%A0%B7%E6%80%A7)：ASV 是扩增子分析中的序列特征，群落多样性指标则从不同角度概括样本内和样本间差异。
- [FASTA与FASTQ](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FASTA%E4%B8%8EFASTQ)：FASTA 保存序列及标题，FASTQ 还保存逐碱基质量信息，二者服务于不同分析阶段。
- [Hardy-Weinberg平衡与检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Hardy-Weinberg%E5%B9%B3%E8%A1%A1%E4%B8%8E%E6%A3%80%E9%AA%8C)：HWE描述理想化随机结合条件下的基因型比例，偏离检验是诊断线索而不是自动删除规则。
- [LOCO与近端污染](https://github.com/SpiralKernel/bioinfo-wiki/wiki/LOCO%E4%B8%8E%E8%BF%91%E7%AB%AF%E6%B1%A1%E6%9F%93)：LOCO在检验某条染色体时把它排除出背景遗传表示，以减少局部信号被背景模型吸收。
- [MAF与MAC及稀有变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/MAF%E4%B8%8EMAC%E5%8F%8A%E7%A8%80%E6%9C%89%E5%8F%98%E5%BC%82)：频率描述相对比例，等位基因计数描述实际信息量；低频位点需要同时审查样本与统计近似。
- [P值效应量与多重检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/P%E5%80%BC%E6%95%88%E5%BA%94%E9%87%8F%E4%B8%8E%E5%A4%9A%E9%87%8D%E6%A3%80%E9%AA%8C)：P 值衡量特定零假设下的数据相容性，效应量描述差异大小；大量检验需要额外控制错误。
- [SAM与BAM及CRAM](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SAM%E4%B8%8EBAM%E5%8F%8ACRAM)：SAM、BAM 和 CRAM 表达序列比对记录，坐标排序、索引和参考资源决定很多下游操作能否正确进行。
- [SNP与基因型是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SNP%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%98%AF%E4%BB%80%E4%B9%88)：SNP 描述单碱基位点的变异，基因型描述某个体在该位点携带的等位基因组合。
- [UMI与细胞条形码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/UMI%E4%B8%8E%E7%BB%86%E8%83%9E%E6%9D%A1%E5%BD%A2%E7%A0%81)：细胞条形码帮助区分测量单元，UMI 用于识别分子标签；二者不是同一类标识符。
- [VCF与基因型编码](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VCF%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E7%BC%96%E7%A0%81)：VCF 以位点为记录，保存参考与替代等位基因，以及每个样本的基因型和其他字段。
- [Wald似然比与得分检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Wald%E4%BC%BC%E7%84%B6%E6%AF%94%E4%B8%8E%E5%BE%97%E5%88%86%E6%A3%80%E9%AA%8C)：不同检验从参数、似然改善或零模型局部变化评估证据，软件输出的P值必须注明检验类型。
- [二分类性状OR与病例对照不平衡](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%8C%E5%88%86%E7%B1%BB%E6%80%A7%E7%8A%B6OR%E4%B8%8E%E7%97%85%E4%BE%8B%E5%AF%B9%E7%85%A7%E4%B8%8D%E5%B9%B3%E8%A1%A1)：二分类关联需要核对标签、病例与对照中的等位基因计数，以及模型是否能处理稀疏和相关样本。
- [亲缘关系与遗传关系矩阵](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%B2%E7%BC%98%E5%85%B3%E7%B3%BB%E4%B8%8E%E9%81%97%E4%BC%A0%E5%85%B3%E7%B3%BB%E7%9F%A9%E9%98%B5)：样本之间的遗传相关性可以用矩阵表达，但不同估计量的尺度和假设需要分别说明。
- [从DNA到RNA和蛋白质](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BB%8EDNA%E5%88%B0RNA%E5%92%8C%E8%9B%8B%E7%99%BD%E8%B4%A8)：区分基因、转录本和蛋白质层级，是理解不同组学测量对象和标识符的起点。
- [关联模型中的协变量与残差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%B3%E8%81%94%E6%A8%A1%E5%9E%8B%E4%B8%AD%E7%9A%84%E5%8D%8F%E5%8F%98%E9%87%8F%E4%B8%8E%E6%AE%8B%E5%B7%AE)：协变量定义调整后的比较，残差描述模型尚未解释的部分；二者都不能靠机械添加代替研究设计。
- [参考基因组与注释版本](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%82%E8%80%83%E5%9F%BA%E5%9B%A0%E7%BB%84%E4%B8%8E%E6%B3%A8%E9%87%8A%E7%89%88%E6%9C%AC)：参考基因组给出坐标与序列，注释说明基因等要素的位置；分析必须记录二者的具体版本。
- [基因标识符与同源基因](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E6%A0%87%E8%AF%86%E7%AC%A6%E4%B8%8E%E5%90%8C%E6%BA%90%E5%9F%BA%E5%9B%A0)：基因符号、稳定标识符和跨物种同源关系表达不同信息，映射时必须记录来源与版本。
- [基因组坐标与区间](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E5%9D%90%E6%A0%87%E4%B8%8E%E5%8C%BA%E9%97%B4)：坐标必须同时带有参考版本、序列名和端点规则，格式转换不能只改文件扩展名。
- [定相与基因型填充](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AE%9A%E7%9B%B8%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E5%A1%AB%E5%85%85)：定相推断等位基因位于哪条单倍型，填充推断未观测基因型，两者都需保留不确定性。
- [实验设计与统计功效](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8E%E7%BB%9F%E8%AE%A1%E5%8A%9F%E6%95%88)：实验设计决定哪些问题能被回答；功效是指定效应与检验条件下发现信号的概率。
- [峰与FRiP及TSS富集](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B3%B0%E4%B8%8EFRiP%E5%8F%8ATSS%E5%AF%8C%E9%9B%86)：峰是相对背景具有信号富集的区域，FRiP 和 TSS 富集用于从不同角度评价部分染色质测量。
- [批次效应与混杂](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%89%B9%E6%AC%A1%E6%95%88%E5%BA%94%E4%B8%8E%E6%B7%B7%E6%9D%82)：批次效应来自技术过程；当批次与研究分组重合时，数据可能无法区分两者的影响。
- [比对相似性同源性与覆盖率](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%AF%94%E5%AF%B9%E7%9B%B8%E4%BC%BC%E6%80%A7%E5%90%8C%E6%BA%90%E6%80%A7%E4%B8%8E%E8%A6%86%E7%9B%96%E7%8E%87)：比对是建立位置对应，相似性是可度量的观察，同源性是关于共同演化来源的推断。
- [测序深度覆盖度与质量分数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E6%B7%B1%E5%BA%A6%E8%A6%86%E7%9B%96%E5%BA%A6%E4%B8%8E%E8%B4%A8%E9%87%8F%E5%88%86%E6%95%B0)：深度、覆盖范围、碱基质量和比对质量衡量不同问题，不能用单个平均数替代整体质控。
- [生物学重复与技术重复](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%9F%E7%89%A9%E5%AD%A6%E9%87%8D%E5%A4%8D%E4%B8%8E%E6%8A%80%E6%9C%AF%E9%87%8D%E5%A4%8D)：生物学重复体现独立生物单位的变化，技术重复衡量同一材料的测量变化。
- [缺失值与零值](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BC%BA%E5%A4%B1%E5%80%BC%E4%B8%8E%E9%9B%B6%E5%80%BC)：零值是已记录的数值，缺失表示没有可用观测；把二者混用会改变统计问题。
- [置信区间与重采样](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BD%AE%E4%BF%A1%E5%8C%BA%E9%97%B4%E4%B8%8E%E9%87%8D%E9%87%87%E6%A0%B7)：置信区间描述估计精度；重采样必须尊重独立单位和研究设计。
- [群体结构是什么](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E6%98%AF%E4%BB%80%E4%B9%88)：群体结构描述样本之间并非完全均匀的遗传差异模式，分析前需要同时排查技术来源。
- [计数丰度与标准化](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%AE%A1%E6%95%B0%E4%B8%B0%E5%BA%A6%E4%B8%8E%E6%A0%87%E5%87%86%E5%8C%96)：原始计数、相对丰度和变换后的数值对应不同问题，模型输入必须与其假设一致。
- [连锁不平衡与LD剪枝](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BF%9E%E9%94%81%E4%B8%8D%E5%B9%B3%E8%A1%A1%E4%B8%8ELD%E5%89%AA%E6%9E%9D)：连锁不平衡描述位点等位基因之间的非随机关联，LD 剪枝用于减少所选位点集合中的冗余。
- [零模型与方差组分](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%9B%B6%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BB%84%E5%88%86)：零模型描述没有当前待检验位点效应时的背景；方差组分表示模型中不同变异来源的规模。

## 方法与算法（8）

- [BLAST原理与种子延伸](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLAST%E5%8E%9F%E7%90%86%E4%B8%8E%E7%A7%8D%E5%AD%90%E5%BB%B6%E4%BC%B8)：BLAST 是序列局部相似性检索的启发式方法族；理解种子、延伸和统计评估比只记命令更重要。
- [FarmCPU与BLINK原理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/FarmCPU%E4%B8%8EBLINK%E5%8E%9F%E7%90%86)：FarmCPU与BLINK通过迭代选择背景位点帮助检验其他位点，背景选择本身也是分析方法的一部分。
- [PCA原理与实现](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PCA%E5%8E%9F%E7%90%86%E4%B8%8E%E5%AE%9E%E7%8E%B0)：主成分分析寻找解释数据变化的正交方向；输入矩阵的定义和尺度直接影响结果。
- [Smith-Waterman局部比对](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Smith-Waterman%E5%B1%80%E9%83%A8%E6%AF%94%E5%AF%B9)：Smith–Waterman 用动态规划找到给定打分规则下的最优局部比对，适合理解序列比对的精确基线。
- [富集分析与GSEA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8EGSEA)：功能富集把特征列表或排序与知识集合连接，结论取决于背景、映射、排序和多重检验。
- [数据泄漏与交叉验证](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%95%B0%E6%8D%AE%E6%B3%84%E6%BC%8F%E4%B8%8E%E4%BA%A4%E5%8F%89%E9%AA%8C%E8%AF%81)：预测评估需要让测试数据保持独立，并在训练折内学习预处理和特征选择。
- [线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)：回归把研究变量与协变量联系到表型，混合模型进一步表示样本相关性或层级结构。
- [群体结构与GWAS有什么关系](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84%E4%B8%8EGWAS%E6%9C%89%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB)：当遗传背景同时关联表型和位点频率时，简单关联可能混入群体差异，需要结合设计和模型处理。

## 工具（22）

- [BLAST本地检索实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BLAST%E6%9C%AC%E5%9C%B0%E6%A3%80%E7%B4%A2%E5%AE%9E%E8%B7%B5)：用本地数据库理解查询、数据库构建与结果字段，并将正式结论建立在覆盖率和统计解释上。
- [BOLT-LMM关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/BOLT-LMM%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)：BOLT-LMM面向较大队列的混合模型关联，模型模式、样本适用性、参考资源与输出列需要同时核对。
- [EMMAX关联分析与旧流程兼容](https://github.com/SpiralKernel/bioinfo-wiki/wiki/EMMAX%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E4%B8%8E%E6%97%A7%E6%B5%81%E7%A8%8B%E5%85%BC%E5%AE%B9)：EMMAX是混合模型关联的经典实现，理解旧文件编码与顺序是复现已有分析的关键。
- [GAPIT多模型GWAS实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GAPIT%E5%A4%9A%E6%A8%A1%E5%9E%8BGWAS%E5%AE%9E%E8%B7%B5)：GAPIT把多种关联与预测方法组织在R接口中；每次应明确模型、样本交集及输出，而不是把一键运行当成模型选择。
- [GCTA与MLMA关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GCTA%E4%B8%8EMLMA%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)：GCTA包含多种遗传统计任务；MLMA使用稠密GRM做关联，不能与GREML或fastGWA模块混称。
- [GEMMA线性混合模型实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GEMMA%E7%BA%BF%E6%80%A7%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B%E5%AE%9E%E8%B7%B5)：GEMMA以显式亲缘矩阵拟合关联模型，适合学习固定效应、背景相关性和检验方法的连接。
- [Linux与项目目录实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Linux%E4%B8%8E%E9%A1%B9%E7%9B%AE%E7%9B%AE%E5%BD%95%E5%AE%9E%E8%B7%B5)：先学会识别路径、检查文本和保存日志，就能建立可追溯的最小分析项目。
- [PLINK2使用与版本管理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PLINK2%E4%BD%BF%E7%94%A8%E4%B8%8E%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86)：PLINK 2 用于基因型处理、PCA 和关联等任务；参数与默认行为需要绑定具体版本。
- [PLINK2关联分析详解](https://github.com/SpiralKernel/bioinfo-wiki/wiki/PLINK2%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E8%AF%A6%E8%A7%A3)：PLINK 2的关联接口按性状拟合回归；正确读取性状、协变量、计数等位基因与错误码比记住一条命令更重要。
- [REGENIE两步关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/REGENIE%E4%B8%A4%E6%AD%A5%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)：REGENIE先学习背景遗传预测，再结合按染色体留出的预测检验位点；两步文件、样本与性状必须保持对应。
- [SAIGE单变异关联分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SAIGE%E5%8D%95%E5%8F%98%E5%BC%82%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90)：SAIGE先拟合零混合模型，再做单变异检验；二分类的SPA处理与样本相关性建模需要共同核对。
- [TASSEL关联分析实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/TASSEL%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E5%AE%9E%E8%B7%B5)：TASSEL通过图形界面和命令行组织遗传数据与GLM/MLM分析，关键是理解taxa交集、固定效应与亲缘输入。
- [fastGWA与fastGWA-GLMM](https://github.com/SpiralKernel/bioinfo-wiki/wiki/fastGWA%E4%B8%8EfastGWA-GLMM)：fastGWA利用稀疏关系和快速检验提高可扩展性；数量性状与二分类模块需要分别配置和核验。
- [rMVP关联分析实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/rMVP%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E5%AE%9E%E8%B7%B5)：rMVP通过外存矩阵和并行运行关联分析，转换后的样本顺序及协变量对应是最重要的检查点。
- [可复现分析与工作流管理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%AF%E5%A4%8D%E7%8E%B0%E5%88%86%E6%9E%90%E4%B8%8E%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%AE%A1%E7%90%86)：把输入、依赖、参数和产物放进可追踪的运行记录，才能区分计算复现与结果解释。
- [合成数据贯通PCA与GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9APCA%E4%B8%8EGWAS)：用固定随机种子的人工数据练习文件交接、质控、PCA 与数量性状关联，不需要下载真实个体数据。
- [常见生信图表的阅读与制作](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B8%B8%E8%A7%81%E7%94%9F%E4%BF%A1%E5%9B%BE%E8%A1%A8%E7%9A%84%E9%98%85%E8%AF%BB%E4%B8%8E%E5%88%B6%E4%BD%9C)：先读坐标、数据变换和独立单位，再判断图形支持什么结论。
- [日志排错与最小复现](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%97%A5%E5%BF%97%E6%8E%92%E9%94%99%E4%B8%8E%E6%9C%80%E5%B0%8F%E5%A4%8D%E7%8E%B0)：从第一条实际错误定位输入、环境和资源问题，用最小复现验证修复。
- [服务器资源与批量任务](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%9C%8D%E5%8A%A1%E5%99%A8%E8%B5%84%E6%BA%90%E4%B8%8E%E6%89%B9%E9%87%8F%E4%BB%BB%E5%8A%A1)：任务需要同时估计计算、内存、磁盘和时间，申请线程并不等于程序会自动使用它们。
- [样本表与数据审计实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%A0%B7%E6%9C%AC%E8%A1%A8%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%AE%A1%E8%AE%A1%E5%AE%9E%E8%B7%B5)：先把样本身份、实验设计和文件位置核对清楚，再进入任何统计分析。
- [结果报告与数据共享](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%93%E6%9E%9C%E6%8A%A5%E5%91%8A%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%85%B1%E4%BA%AB)：报告应让读者追溯从研究设计、输入和参数到结果的路径，并区分数据开放与受限访问。
- [软件环境与依赖管理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AF%E4%BB%B6%E7%8E%AF%E5%A2%83%E4%B8%8E%E4%BE%9D%E8%B5%96%E7%AE%A1%E7%90%86)：一个可复现环境需要记录软件版本、依赖、平台及参考数据，只有环境名称并不足够。

## 数据库（6）

- [Ensembl参考与注释查询](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Ensembl%E5%8F%82%E8%80%83%E4%B8%8E%E6%B3%A8%E9%87%8A%E6%9F%A5%E8%AF%A2)：Ensembl把参考组装、基因模型、变异与同源信息联系起来，查询结果必须携带物种和发布版本。
- [GEO数据检索与样本核对](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GEO%E6%95%B0%E6%8D%AE%E6%A3%80%E7%B4%A2%E4%B8%8E%E6%A0%B7%E6%9C%AC%E6%A0%B8%E5%AF%B9)：GEO连接研究、样本与处理数据，选择数据前先确认实验设计和矩阵数值含义。
- [GO术语注释与证据](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GO%E6%9C%AF%E8%AF%AD%E6%B3%A8%E9%87%8A%E4%B8%8E%E8%AF%81%E6%8D%AE)：GO用结构化术语描述基因产物相关功能，术语、注释关系和证据类型需要分开阅读。
- [SRA与ENA读段检索](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SRA%E4%B8%8EENA%E8%AF%BB%E6%AE%B5%E6%A3%80%E7%B4%A2)：读段归档中的study、sample、experiment与run有不同层级，下载与合并必须保留这些关系。
- [UniProt蛋白条目与证据](https://github.com/SpiralKernel/bioinfo-wiki/wiki/UniProt%E8%9B%8B%E7%99%BD%E6%9D%A1%E7%9B%AE%E4%B8%8E%E8%AF%81%E6%8D%AE)：蛋白数据库条目同时包含序列和注释证据，人工审阅状态不等于每项功能都已实验验证。
- [公共数据库与数据获取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%85%B1%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8E%E6%95%B0%E6%8D%AE%E8%8E%B7%E5%8F%96)：根据需要的数据层级选择资源，并把 accession、原始文件、处理矩阵和版本信息分别记录。

## 分析工作流（25）

- [ATAC-seq入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/ATAC-seq%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：从可及性测序读段得到区域信号与差异分析，重点检查信号质量、重复一致性和共同计数区域。
- [ChIP-seq入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/ChIP-seq%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：ChIP-seq 分析目标富集相对背景的信号分布，必须区分对照、抗体目标与信号宽度。
- [DNA甲基化分析入门](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DNA%E7%94%B2%E5%9F%BA%E5%8C%96%E5%88%86%E6%9E%90%E5%85%A5%E9%97%A8)：甲基化分析需要匹配测量技术，以覆盖和重复信息估计位点或区域差异。
- [GWAS从数据准备到结果解释](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E4%BB%8E%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87%E5%88%B0%E7%BB%93%E6%9E%9C%E8%A7%A3%E9%87%8A)：将基因型、表型和设计信息连接到合适的关联模型，并审查效应方向与证据边界。
- [GWAS参数选择与敏感性分析](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E5%8F%82%E6%95%B0%E9%80%89%E6%8B%A9%E4%B8%8E%E6%95%8F%E6%84%9F%E6%80%A7%E5%88%86%E6%9E%90)：参数改变会改变信息、背景与检验集合，敏感性分析应有预先理由和完整记录。
- [GWAS常见报错与排查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E5%B8%B8%E8%A7%81%E6%8A%A5%E9%94%99%E4%B8%8E%E6%8E%92%E6%9F%A5)：先把失败定位到身份、格式、模型、数值或资源，再用最小例子验证修复。
- [GWAS曼哈顿图QQ图与膨胀因子](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E6%9B%BC%E5%93%88%E9%A1%BF%E5%9B%BEQQ%E5%9B%BE%E4%B8%8E%E8%86%A8%E8%83%80%E5%9B%A0%E5%AD%90)：图形用于定位信号与诊断分布，必须连同样本结构、检验、LD和模型背景解释。
- [GWAS结果字段与等位基因统一](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E7%BB%93%E6%9E%9C%E5%AD%97%E6%AE%B5%E4%B8%8E%E7%AD%89%E4%BD%8D%E5%9F%BA%E5%9B%A0%E7%BB%9F%E4%B8%80)：跨软件结果表先统一位点、效应方向、性状尺度和P值表示，再比较统计量。
- [GWAS软件结果比较与一致性检查](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E7%BB%93%E6%9E%9C%E6%AF%94%E8%BE%83%E4%B8%8E%E4%B8%80%E8%87%B4%E6%80%A7%E6%A3%80%E6%9F%A5)：先用同一模型检查软件交接，再解释不同模型的结果；单一数据集的显著数量不构成软件排名。
- [GWAS软件输入转换与样本对齐](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E8%BE%93%E5%85%A5%E8%BD%AC%E6%8D%A2%E4%B8%8E%E6%A0%B7%E6%9C%AC%E5%AF%B9%E9%BD%90)：转换必须保持样本身份、位点身份、等位基因编码和性状含义；格式可以读入不代表转换正确。
- [RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)：从基因计数和实验设计出发，估计表达差异，并区分统计证据、效应大小与功能解释。
- [代谢组入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BB%A3%E8%B0%A2%E7%BB%84%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：代谢组分析先审查峰特征与测量质量，再讨论统计差异和代谢物身份。
- [公开小鼠数据贯通多软件GWAS](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80%E5%B0%8F%E9%BC%A0%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9A%E5%A4%9A%E8%BD%AF%E4%BB%B6GWAS)：用固定版本的公开小鼠数据完成质控、PCA、多软件关联、等位基因统一和诊断图，学习每一步的交接与判断。
- [单细胞转录组入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8D%95%E7%BB%86%E8%83%9E%E8%BD%AC%E5%BD%95%E7%BB%84%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：从细胞或液滴计数出发，检查质量、探索细胞状态，并将供体层面的比较与细胞聚类区分。
- [变异注释与候选证据整理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%B3%A8%E9%87%8A%E4%B8%8E%E5%80%99%E9%80%89%E8%AF%81%E6%8D%AE%E6%95%B4%E7%90%86)：注释把变异映射到转录本与已知资源；候选优先级需要多种证据，注释后果并非功能定论。
- [基因型质控与过滤](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E5%9E%8B%E8%B4%A8%E6%8E%A7%E4%B8%8E%E8%BF%87%E6%BB%A4)：先评估样本和位点质量，再按分析目标制定可追溯的过滤规则。
- [基因组重测序与变异检测](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%9F%BA%E5%9B%A0%E7%BB%84%E9%87%8D%E6%B5%8B%E5%BA%8F%E4%B8%8E%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B)：从 DNA 读段得到可用于群体分析的变异数据，关键是参考一致性、样本级检查和统一的分型流程。
- [多组学整合入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%A4%9A%E7%BB%84%E5%AD%A6%E6%95%B4%E5%90%88%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：整合多个测量层级前，先确认样本对应、特征尺度和具体目标，再选择联合分析方法。
- [小RNA分析入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B0%8FRNA%E5%88%86%E6%9E%90%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：小RNA测序关注短RNA群体，接头处理、长度选择和注释分配直接影响计数。
- [微生物组分析入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%BE%AE%E7%94%9F%E7%89%A9%E7%BB%84%E5%88%86%E6%9E%90%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：先区分标记基因扩增子和全样本宏基因组，再选择特征构建、分类与群落比较路线。
- [用PCA探索样本的群体结构](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%A8PCA%E6%8E%A2%E7%B4%A2%E6%A0%B7%E6%9C%AC%E7%9A%84%E7%BE%A4%E4%BD%93%E7%BB%93%E6%9E%84)：从经过质控的基因型出发，减少位点冗余、计算主成分，并结合样本信息检查结果。
- [空间转录组入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%A9%BA%E9%97%B4%E8%BD%AC%E5%BD%95%E7%BB%84%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：将表达矩阵与空间坐标和组织图像对应，分析空间模式，并区分 spot、细胞和切片层级。
- [系统发育树入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%B3%BB%E7%BB%9F%E5%8F%91%E8%82%B2%E6%A0%91%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：系统发育推断从可比较的同源序列出发，树的拓扑、枝长和支持度回答不同问题。
- [蛋白质组入门与实践](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%9B%8B%E7%99%BD%E8%B4%A8%E7%BB%84%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E8%B7%B5)：将质谱证据或蛋白定量表连接到可解释的蛋白层面比较，先区分鉴定、定量和差异检验。
- [长读长测序分析入门](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%95%BF%E8%AF%BB%E9%95%BF%E6%B5%8B%E5%BA%8F%E5%88%86%E6%9E%90%E5%85%A5%E9%97%A8)：长读长有助于跨越复杂区域与连接转录结构，流程选择仍取决于平台、数据类型和研究目标。

## 编写与维护

[项目、代码与发布说明](https://github.com/SpiralKernel/bioinfo-wiki)。原稿在 Obsidian 维护，发布版自动生成导航与关键词索引。
