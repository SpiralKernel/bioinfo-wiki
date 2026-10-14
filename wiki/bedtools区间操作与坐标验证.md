# bedtools区间操作与坐标验证

> 更新：2026-10-14；状态：可用；验证范围：人工基因案例与实际工具输出核对；具体已测范围见正文。

用成熟区间工具核对重叠、最近距离和链方向，并明确输出的计数单位。

## 输入与坐标

bedtools读取BED通常使用0起始半开区间。一个1起始单碱基101写成`chrToy 100 101`。人工案例将普通VCF记录的REF跨度转成BED，便于演示；插入锚点、符号SV和BND需要分别定义，不能把该转换当成通用事件跨度。

先安装bedtools并运行`bedtools --version`。本机实际版本2.31.1；Conda可在独立环境安装，安装方式本身未逐平台测试。

## 本项目实际命令

先运行[人工基因贯通区间注释与后果提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E5%9F%BA%E5%9B%A0%E8%B4%AF%E9%80%9A%E5%8C%BA%E9%97%B4%E6%B3%A8%E9%87%8A%E4%B8%8E%E5%90%8E%E6%9E%9C%E6%8F%90%E5%8F%96)，进入其输出的`intervals/`目录：

```bash
bedtools intersect -a variants.bed -b genes.bed -wa -wb
bedtools intersect -a variants.bed -b exons.bed -wa -wb
bedtools intersect -a boundaries.bed -b genes.bed -wao
bedtools closest -a boundaries.bed -b genes.bed -d -t all
bedtools getfasta -fi genome.fa -bed exons.bed -s -name
```

`-wa -wb`保留双方信息，可能一条A输出多行；`-wao`还保留没有重叠的A及零重叠长度。`closest`所需文件按一致的染色体/起点顺序排序，`-t all`保留并列；`getfasta -s`根据BED链取反向互补。

本例基因重叠9对、exon重叠11对；后者仅7个不同记录。并列窗口输出两个距离120的基因。正式分析先声明去重键，不要随意`uniq`后丢失转录本关系。

参考：[intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html)、[closest](https://bedtools.readthedocs.io/en/latest/content/tools/closest.html)。继续读[区间重叠最近基因与候选映射](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8C%BA%E9%97%B4%E9%87%8D%E5%8F%A0%E6%9C%80%E8%BF%91%E5%9F%BA%E5%9B%A0%E4%B8%8E%E5%80%99%E9%80%89%E6%98%A0%E5%B0%84)。
