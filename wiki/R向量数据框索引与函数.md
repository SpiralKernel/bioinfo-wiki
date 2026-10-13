# R向量数据框索引与函数

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

先掌握向量、缺失、数据框和索引，理解R的向量化与因子编码。

## 基础例子

```r
values <- c(1, 2, NA, 4)
observed <- values[!is.na(values)]
average <- function(x) {
  if (length(x) == 0) stop("没有可用观测")
  mean(x)
}
average(observed)
```

R从1索引，`values[1]`是首项，`values[0]`是空选择。`<-`常用于赋值，`==`用于比较；`NA`是缺失，`NULL`不是同一概念，`NA == NA`不能代替`is.na`。

## 数据框

```r
dat <- data.frame(sample_id = c("S01", "S02"),
                  value = c(1, 2), stringsAsFactors = FALSE)
dat$value
dat[dat$value > 1, , drop = FALSE]
```

数据框常以行表示样本、列表示变量；`$`按列名取对象，`[行,列]`按二维选择。`drop=FALSE`帮助保留表结构。列表的`[`与`[[`返回层级也不同。

R很多操作按向量执行，长度不同时可能重复利用较短向量，应检查长度，不能让回收规则静默替代样本对齐。分类变量用factor，并明确参考水平；不能把1/2/3编码自动当连续剂量。

例子属于base R，完整表格/模型脚本经WebR运行验证。来源：[R入门手册](https://cran.r-project.org/doc/manuals/r-release/R-intro.html)，继续[R读取清理与合并样本表](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E8%AF%BB%E5%8F%96%E6%B8%85%E7%90%86%E4%B8%8E%E5%90%88%E5%B9%B6%E6%A0%B7%E6%9C%AC%E8%A1%A8)。

## 按顺序读代码

`c(...)`组合成向量，`<-`保存它。`is.na(values)`逐项判断缺失，得到`FALSE FALSE TRUE FALSE`；`!`取反，再由方括号选择非缺失项，得到`1 2 4`。这是一次按逻辑向量筛选，与Python循环逐项收集的写法不同。

`function(x)`定义函数，长度为0就停止，否则计算mean；R函数把最后一个表达式作为返回值。`average(observed)`应显示`[1] 2.333333`，其中`[1]`是显示位置，不是额外结果。把4改为6后结果为3。

数据框例子中`dat$value`返回`1 2`；筛选后只有S02、value=2这一行。逗号前是行条件，逗号后留空表示保留所有列；`drop=FALSE`要求仍返回数据框。
