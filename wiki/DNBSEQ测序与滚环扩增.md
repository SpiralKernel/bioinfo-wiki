# DNBSEQ测序与滚环扩增

> 更新：2026-10-13；状态：可用；验证范围：官方平台资料与原始研究核对；原理及判读，未执行湿实验或平台测序。

DNBSEQ用环状模板产生DNA纳米球，纳米球制备与前序文库PCR应分别理解。

## 核心结构

相关路线以环状模板经滚环复制产生包含多份模板信息的DNA纳米球DNB，再在阵列上读出。RCA/RCR和常规PCR的模板利用方式不同，大量拷贝仍来自相应原始分子。

cPAS是相关读出体系名称，具体实现需看化学版本；不能把历史公司的全部读出方案和当前产品混为同一技术。

## 不宜简单叫全程PCR-free

DNB形成阶段不等于前序建库。输入文库可能经过PCR、靶向扩增或其他处理；纳米球阶段避免指数PCR，不能推导整个样本没有扩增偏差。

第三方文库转换涉及结构、索引和拆分兼容。支持一种布局不代表全部文库可直接互换。

## 数据和比较

常见交付可为单双端FASTQ，接头、命名、索引方向和质量处理仍需核对。相同格式不意味着不同平台误差与选择完全相同。

在可比输入和目标下比较覆盖、重复、错误及目标范围，不据宣传做统一排名。来源：[MGI DNBSEQ](https://us.global-mgitech.com/technologies/dnbseq-technology/)。连接见[第二代测序原理与平台比较](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%AC%AC%E4%BA%8C%E4%BB%A3%E6%B5%8B%E5%BA%8F%E5%8E%9F%E7%90%86%E4%B8%8E%E5%B9%B3%E5%8F%B0%E6%AF%94%E8%BE%83)、[测序错误重复偏差与嵌合体](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%B5%8B%E5%BA%8F%E9%94%99%E8%AF%AF%E9%87%8D%E5%A4%8D%E5%81%8F%E5%B7%AE%E4%B8%8E%E5%B5%8C%E5%90%88%E4%BD%93)。
