# Python读取清理与合并样本表

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

先保存样本ID和缺失含义，再按键合并，不能靠两张表行号相同推断对应。

## 从标准库开始

[同一份样本表贯通R与Python](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%8C%E4%B8%80%E4%BB%BD%E6%A0%B7%E6%9C%AC%E8%A1%A8%E8%B4%AF%E9%80%9AR%E4%B8%8EPython)的Python程序使用`csv.DictReader`，读每行字段，检查必需列、空/重复ID和两表ID集合。测量中的NA保留缺失，不填0；按样本ID匹配元数据，并保留原测量顺序。

## pandas对应写法

以下为官方接口模板，本轮完整教学脚本不依赖pandas，未把本段当独立实测：

```python
import pandas as pd
measurements = pd.read_csv("examples/data/programming_measurements.csv",
                           dtype={"sample_id": "string"})
metadata = pd.read_csv("examples/data/programming_metadata.csv",
                       dtype={"sample_id": "string"})
assert measurements["sample_id"].notna().all()
assert metadata["sample_id"].notna().all()
assert measurements["sample_id"].is_unique
assert metadata["sample_id"].is_unique
assert set(measurements["sample_id"]) == set(metadata["sample_id"])
joined = measurements.merge(metadata, on="sample_id", how="left",
                            validate="one_to_one", indicator=True)
assert (joined["_merge"] == "both").all()
print(joined.groupby("condition")["value"].agg(["count", "mean"]))
```

`.loc`按标签选择，`.iloc`按整数位置选择；列名拼写、类型和重复键会改变行为。写CSV通常设`index=False`，避免多出行号列。数值型ID可能丢前导零，故先定义字符串类型。

## 清理原则

保留原始表；记录缺失、转换失败与排除理由。不能只在一张表按条件删行后按位置拼回另一张表；不同单位也不能直接平均。

来源：[pandas入门](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)、[merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)。
