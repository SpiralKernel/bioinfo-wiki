# pbsv发现签名与联合调用

> 更新：2026-10-15；状态：可用；验证范围：官方文档与方法核对；专业命令为模板，本轮未执行该流程。

pbsv把比对中的结构信号与后续调用分为不同阶段，平台适用性和签名格式需要配套。

## 两阶段模板及平台分支

使用该版本支持的PacBio比对数据和参考，保存read group及样本信息；本轮未执行pbsv：

```bash
pbsv discover sample.bam sample.svsig.gz
pbsv call reference.fa sample.svsig.gz sample.sv.vcf
```

上方展示CLR等对应分支的基本接口；CCS/HiFi调用按当前官方说明加`--ccs`，例如`pbsv call --ccs reference.fa sample.svsig.gz sample.sv.vcf`，其discover及比对设置也要配套核对。多样本输入、串联重复资源和平台参数以[官方pbsv说明](https://github.com/PacificBiosciences/pbsv)为准。svsig是本工具的中间证据格式，不能与Sniffles SNF或普通VCF互换。

## 检查与比较

查看样本、类型、支持、GT和过滤，分别评估序列与事件存在。改变预处理或平台版本后，签名与调用参数应成套更新。

pbsv、cuteSV和Sniffles是可比较的代表实现，选择还取决于平台、覆盖和下游需求，不因同样输出VCF就假定字段含义相同。操作范围与评估见[变异检测软件选择与适用场景](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8F%98%E5%BC%82%E6%A3%80%E6%B5%8B%E8%BD%AF%E4%BB%B6%E9%80%89%E6%8B%A9%E4%B8%8E%E9%80%82%E7%94%A8%E5%9C%BA%E6%99%AF)、[SV事件匹配与一对一评估](https://github.com/SpiralKernel/bioinfo-wiki/wiki/SV%E4%BA%8B%E4%BB%B6%E5%8C%B9%E9%85%8D%E4%B8%8E%E4%B8%80%E5%AF%B9%E4%B8%80%E8%AF%84%E4%BC%B0)。
