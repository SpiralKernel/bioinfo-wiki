# R读取清理与合并样本表

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

base R即可完成小表读取与匹配，关键是类型、NA、重复键和输出行顺序。

## 可跟做的步骤

在项目根目录的R会话执行：

```r
measurements <- read.csv("examples/data/programming_measurements.csv",
                         na.strings = c("NA", ""), stringsAsFactors = FALSE,
                         colClasses = c(sample_id = "character", value = "numeric"))
metadata <- read.csv("examples/data/programming_metadata.csv",
                     stringsAsFactors = FALSE, colClasses = "character")
stopifnot(!anyDuplicated(measurements$sample_id),
          !anyDuplicated(metadata$sample_id),
          setequal(measurements$sample_id, metadata$sample_id))
joined <- merge(measurements, metadata, by = "sample_id", sort = FALSE)
joined <- joined[match(measurements$sample_id, joined$sample_id), ]
str(joined)
summary(joined$value)
```

本段针对已提供的小表；完整脚本先将value读为文本，按本例缺失规则转换并拒绝非有限值，另检查空/NA ID、必需列与最终顺序。merge可改变顺序或产生一对多组合，不能只确认行数就假定正确。存在不匹配键时，默认inner merge会丢行；先检查集合再合并。

## 类型与缺失

`NA`不是0，`mean(x)`遇缺失与`mean(x, na.rm=TRUE)`含义不同，后者需同时报告有效n。分类变量转factor前明确水平，样本ID应保持字符串；上面的`colClasses`显式保护ID，不能只靠`stringsAsFactors=FALSE`。例如读入`001`与`010`时应仍是这两个字符串，而非1与10；丢掉前导零后无法从结果恢复身份。

`write.csv(..., row.names=FALSE, na="NA")`明确行号和缺失输出。dplyr/tidyr可简化更复杂操作，但不是第一张表的必需依赖，本轮未执行它们。

完整案例经WebR验证；原生Rscript和第三方包环境未在本机安装。来源：[R数据导入/导出手册](https://cran.r-project.org/doc/manuals/r-release/R-data.html)。
