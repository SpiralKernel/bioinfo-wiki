# TASSEL关联分析实践

> 更新：2026-10-13；状态：可用；验证范围：官方文档与原始研究核对；本页命令模板未在本机运行。

TASSEL通过图形界面和命令行组织遗传数据与GLM/MLM分析，关键是理解taxa交集、固定效应与亲缘输入。

## 定位与版本入口

TASSEL用于性状关联、LD及其他遗传分析，在作物研究中常见。当前官方站点已迁至[maize-genetics.github.io/tassel](https://maize-genetics.github.io/tassel/)；旧网站和旧版Pipeline教程可能采用不同参数。本页按TASSEL 5当前文档核对，未安装执行Java流程。

GLM与MLM是本页重点；GBS分型等上游任务与关联并非同一步。模型选择见[GWAS软件选择与比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E9%80%89%E6%8B%A9%E4%B8%8E%E6%AF%94%E8%BE%83)。

## 先做一个GUI学习练习

从官方Getting Started获取测试数据。依次载入基因型、性状、群体结构协变量及所需亲缘矩阵，查看taxa与位点数量。先做一个明确的GLM，再以相同个体加入K做MLM，保存各自输入交集和参数。

观察界面自动合并后的对象，不只看文件导入成功。表型或协变量类型、缺失、同名个体和交集都可能改变实际分析范围。

## 命令行MLM结构

下面是按当前Pipeline接口改写的模板，未运行。文件需按TASSEL格式准备，`structure.txt`已经是整理好的独立协变量列，`kinship.txt`是匹配的TASSEL关系矩阵：

```bash
./run_pipeline.pl \
  -fork1 -importGuess genotype.hmp.txt \
  -fork2 -importGuess traits.txt \
  -fork3 -importGuess structure.txt \
  -fork4 -importGuess kinship.txt \
  -combine5 -input1 -input2 -input3 -intersect \
  -mlm -mlmVarCompEst P3D -mlmCompressionLevel Optimum \
  -input4 -export mlm_output
```

fork与combine组织输入依赖；实际taxa交集是分析对象。P3D与压缩配置改变估计过程，不应把所有TASSEL MLM视为同一个未近似模型。旧版教程可能要求显式`-runfork`，当前文档的行为已变化。

## 群体结构与K怎样准备

PC与群体成员比例Q是不同协变量来源；Q各列和为1时需检查与截距的共线。教程中的`excludeLastTrait`等操作有特定输入背景，不能机械删除自己的最后一列PC。

K的定义、taxa名称和矩阵顺序要与输入对象对应。不能把GEMMA的纯数值K直接改名后假定符合TASSEL格式，见[GWAS软件输入转换与样本对齐](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E8%BD%AF%E4%BB%B6%E8%BE%93%E5%85%A5%E8%BD%AC%E6%8D%A2%E4%B8%8E%E6%A0%B7%E6%9C%AC%E5%AF%B9%E9%BD%90)。

## 输出与排错

核对每个性状的分析个体、位点、效应和检验表。检验表与等位基因效应表可能需要分别保存，再按位点及相应模型连接；不根据某个默认列位置推断计数方向。

出现空结果先查taxa交集、导入的数据类型和有效性状；内存不足则评估Java堆、数据规模及任务设计。GUI生成的图仍需图注与统计解释，见[GWAS曼哈顿图QQ图与膨胀因子](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E6%9B%BC%E5%93%88%E9%A1%BF%E5%9B%BEQQ%E5%9B%BE%E4%B8%8E%E8%86%A8%E8%83%80%E5%9B%A0%E5%AD%90)。

深入：[官方主页](https://maize-genetics.github.io/tassel/)、[Pipeline实例](https://maize-genetics.github.io/tassel/pipelines/pipeline-tutorial/)、[CLI参考](https://maize-genetics.github.io/tassel/pipelines/tassel5-pipeline-cli/)、[TASSEL原始软件论文](https://doi.org/10.1093/bioinformatics/btm308)。
