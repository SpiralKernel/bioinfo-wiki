# Snakemake规则配置与断点续跑

> 更新：2026-10-14；状态：可用；验证范围：人工基因案例与实际工具输出核对；具体已测范围见正文。

将输入、输出、参数和资源声明为规则，让工作流按依赖执行并明确需要交付的产物。

## 规则是产物契约

每条rule声明input、output和执行动作；目标反向确定所需依赖。配置保存可变路径与参数，shell中的路径用`:q`引用。资源声明只帮助调度，不保证工具绝不会超用内存。

本轮实际Snakemake9.27.0、Python3.14.8、本地单核；见[官方入门](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html)、[配置](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html)、[规则](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html)。没有执行集群、云或容器调度。

## 为什么all要列出交付文件

本例有build_database、annotate、intervals、report四条计算规则。若all只要求已存在的summary，缺失的中间表不一定触发重建；这不是“任何文件少了都会自动恢复”。因此all还显式列出注释VCF、后果表和需要交付的区间表。

实际验证：首次运行四条计算规则；无变化重跑没有计算；删除交付表consequences.tsv后，只重跑annotate和report，数据库与区间结果复用，表内容校验值与原来一致。

## 恢复的边界

本轮验证的是缺失输出恢复，不是所有崩溃、中断和数据损坏情形。工作流通常依赖时间戳与元数据判断变化，不应假定自动校验每个内容位。本例报告阶段额外核对输入SHA和数据库SHA，拒绝混用旧结果。

完整操作见[最小注释工作流与Snakemake恢复](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%9C%80%E5%B0%8F%E6%B3%A8%E9%87%8A%E5%B7%A5%E4%BD%9C%E6%B5%81%E4%B8%8ESnakemake%E6%81%A2%E5%A4%8D)。失败时先保留日志、判断部分输出是否可信，再选择重新运行方式。
