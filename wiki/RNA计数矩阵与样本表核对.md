# RNA计数矩阵与样本表核对

> 更新：2026-10-15；状态：可用；验证范围：原生R与公开airway计数案例已执行；范围和结果见正文。

先用样本ID建立明确对应，再检查计数合法性和设计；文件列顺序不能代替身份。

## 最小输入契约

计数矩阵行是唯一基因ID、列是唯一sample_id；样本表至少包括sample_id、条件及必要的配对/批次因素。sample_id应按字符串读取，保留前导零。不让R自动改列名后再猜对应关系。

检查两边样本集合完全相同，然后按计数列顺序重排样本表，最后断言一致。不能只因两张表都有8列/8行就直接拼接。重复ID应停止，一对多信息不能静默覆盖。

## 数值和来源

普通整数计数接口要求有限、非负、非缺失的计数；分数、TPM和已经标准化的数值需回到来源解释，而不是四舍五入冒充原始计数。某些估计计数通过专门接口导入，见[Salmon定量与tximport基因汇总](https://github.com/SpiralKernel/bioinfo-wiki/wiki/Salmon%E5%AE%9A%E9%87%8F%E4%B8%8Etximport%E5%9F%BA%E5%9B%A0%E6%B1%87%E6%80%BB)。

检查空文库、异常文库总量、基因ID版本和过滤记录。全零基因可以按预先规则移除；样本整列为0则应查上游。

## 本轮实际验证

案例故意倒置样本表再按ID重排；基础检查还测试重复/缺样本、分数/负数/NA、空文库、完全混杂和无剩余自由度。运行`Rscript examples/test_rnaseq_inputs.R`，无需第三方R包。

这些检查不是所有错误的穷举。能通过不代表样本生物身份没有交换；仍需核对实验记录和QC。继续读[RNA设计矩阵配对与对比方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E8%AE%BE%E8%AE%A1%E7%9F%A9%E9%98%B5%E9%85%8D%E5%AF%B9%E4%B8%8E%E5%AF%B9%E6%AF%94%E6%96%B9%E5%90%91)、[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)。
