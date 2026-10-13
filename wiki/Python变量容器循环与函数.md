# Python变量容器循环与函数

> 更新：2026-10-14；状态：可用；验证范围：官方语言文档核对；基础样本表案例已运行，R通过WebR验证；安装与第三方包按页说明。

先学变量、列表、字典、条件与函数，再用表格任务练习索引和缺失。

## 一个可读的小例子

```python
values = [1.0, 2.0, None, 4.0]
observed = []
for value in values:
    if value is not None:
        observed.append(value)

def average(numbers):
    if not numbers:
        raise ValueError("没有可用观测")
    return sum(numbers) / len(numbers)

print(average(observed))
```

列表按顺序存值，字典如`{"sample_id": "S01", "condition": "A"}`按键存字段。Python从0索引，切片右端不包含；`values[0]`是首项。`=`赋值，`==`比较，缩进决定代码块，字符串必须加引号。

## 常见错误

`None`表示没有对应对象，不能直接与数字相加；pandas/NumPy还有各自缺失表示。`"2"`是文本，不是数值2，读文件后需检查类型。列表与NumPy数组的`+`也不同，不能凭外观猜算术行为。

函数把输入变成返回值，变量作用域和参数要明确；先写小函数并用已知结果检查，别一开始把所有步骤堆在大Notebook里。

完整表格程序见[Python读取清理与合并样本表](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Python%E8%AF%BB%E5%8F%96%E6%B8%85%E7%90%86%E4%B8%8E%E5%90%88%E5%B9%B6%E6%A0%B7%E6%9C%AC%E8%A1%A8)和[同一份样本表贯通R与Python](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%90%8C%E4%B8%80%E4%BB%BD%E6%A0%B7%E6%9C%AC%E8%A1%A8%E8%B4%AF%E9%80%9AR%E4%B8%8EPython)。上述逻辑与实测程序一致，完整案例有运行记录。来源：[Python官方入门](https://docs.python.org/3/tutorial/introduction.html)、[控制流](https://docs.python.org/3/tutorial/controlflow.html)。

## 按顺序读代码

`values`保存四项，其中`None`表示本练习的缺失。`observed=[]`先建立空列表；`for`逐项取值，`if`只保留不是None的项，`.append(value)`把该项放进列表尾部。循环结束得到`[1.0, 2.0, 4.0]`。

`def`定义函数，调用时才运行函数体。`if not numbers`检查空列表；有值时`return`返回总和除以项数。最后`print`显示约`2.3333333333333335`，不是4项的均值。把4改为6，重新从头运行，应得到3；先手算再核对。
