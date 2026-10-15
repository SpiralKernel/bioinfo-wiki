# VCF中的SVTYPEEND与BND

> 更新：2026-10-15；状态：可用；验证范围：官方文档与原始研究核对；专业检测命令为模板，未执行完整真实数据流程。

结构变异的类型、跨度、断点和伴随记录需要联合解释，不能只读POS或ALT长度。

## 先读头部

`SVTYPE`常标记DEL/INS/DUP/INV/CNV/BND等类型；`END`描述记录所涉及的末端，含义与坐标规则要结合类别；`SVLEN`的符号、数目和定义也按格式版本/调用器核对。符号ALT如`<DEL>`不包含完整被删除序列，不能用字符串长度推断缺失大小。

序列解析的SV也可能直接给很长REF/ALT，不能只提取尖括号记录。`*`表示跨越该位置的删除等位表示，和`<NON_REF>`、任意缺失值不是同一东西。

## BND记录

BND用断端及方向描述连接，例如ALT中的括号包含远端染色体和坐标。`MATEID`可指向伴随断端记录，`EVENT`可关联事件；不是所有调用器都输出相同字段或两条记录。

本例bnd1和bnd2互相引用，2条记录对应1个人工事件。只按ID计数或筛一个染色体可能保留一端；应说明输出是断端记录集还是完整事件集。DELLY某些输出使用CHR2等字段，不能强求所有工具都有MATEID。

## 区域与精度

缺失的锚点可能在目标区间之外，记录跨度仍与目标重叠；插入位置和BND不是普通区间。对不精确断点还需读置信范围字段。导出BED前明确是否包含锚点及目标是受影响碱基、插入位置还是断点。

操作见[按类型提取SNPIndel与结构变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%8C%89%E7%B1%BB%E5%9E%8B%E6%8F%90%E5%8F%96SNPIndel%E4%B8%8E%E7%BB%93%E6%9E%84%E5%8F%98%E5%BC%82)和[按区域样本与基因型提取变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%8C%89%E5%8C%BA%E5%9F%9F%E6%A0%B7%E6%9C%AC%E4%B8%8E%E5%9F%BA%E5%9B%A0%E5%9E%8B%E6%8F%90%E5%8F%96%E5%8F%98%E5%BC%82)。权威字段与方向定义：[VCF规范](https://samtools.github.io/hts-specs/VCFv4.5.pdf)。

## 本轮整理入口

[断点置信区间与事件方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%96%AD%E7%82%B9%E7%BD%AE%E4%BF%A1%E5%8C%BA%E9%97%B4%E4%B8%8E%E4%BA%8B%E4%BB%B6%E6%96%B9%E5%90%91)解释偏移范围；[复杂重排与BND事件图](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%A4%8D%E6%9D%82%E9%87%8D%E6%8E%92%E4%B8%8EBND%E4%BA%8B%E4%BB%B6%E5%9B%BE)区分记录、连接与事件。
