# SnpEff自建数据库与后果解析

> 更新：2026-10-14；状态：可用；验证范围：人工基因案例与实际工具输出核对；具体已测范围见正文。

使用匹配的参考和基因模型建立本地数据库，验证CDS与蛋白，再解析ANN后果。

## 准备环境

需要Java和SnpEff核心文件。本机实际SnpEff5.4c（2026-02-23构建）、OpenJDK25.0.4.1；[官方下载说明](https://pcingola.github.io/SnpEff/download/)要求Java21或更高。核心下载地址含latest时会变化，必须记录实际版本及jar SHA256，不把URL当作固定版本。

解压核心包后保留`snpEff.jar`和完整`snpEff.config`。在Linux/macOS或WSL终端设置`export SNPEFF_JAR="/你的绝对路径/snpEff.jar"`，运行`java -jar "$SNPEFF_JAR" -version`核对。Conda也可安装，但本轮采用官方核心包，不保证各渠道版本一致。

## 自建数据库的必要检查

准备同版本FASTA、GFF/GTF、CDS和蛋白，建立物种配置并使用`build -gff3`。必须阅读构建日志、未找到转录本和序列错误，不应通过跳过CDS/蛋白检查来把错误库包装成成功。[数据库构建](https://pcingola.github.io/SnpEff/snpeff/build_db/)与[GFF/GTF准备](https://pcingola.github.io/SnpEff/snpeff/build_db_gff_gtf/)给出正式约定。

本项目`annotation_demo.py --step build`自动准备人工toy库，实际CDS3条、蛋白3条均OK且错误0。人工模型没有UTR，相关警告已记录；不含复杂剪接、非标准密码或非零phase验证。

## 注释与提取

本例实际调用`ann -nodownload -noLog -noStats -ud 0 toy`；`-ud 0`用于隔离人工上/下游范围，不是实际物种的通用推荐。先读VCF头中的ANN格式，再按ALT、gene、transcript、effect和impact拆成长表。

教学解析器严格匹配本例ANN Allele与ALT；真实复杂Indel可能有不同的等位表达，应标准化并按工具规范映射，不能盲用本例脚本处理任意VCF。详见[人工基因贯通区间注释与后果提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E4%BA%BA%E5%B7%A5%E5%9F%BA%E5%9B%A0%E8%B4%AF%E9%80%9A%E5%8C%BA%E9%97%B4%E6%B3%A8%E9%87%8A%E4%B8%8E%E5%90%8E%E6%9E%9C%E6%8F%90%E5%8F%96)和[按基因转录本与后果提取变异](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%8C%89%E5%9F%BA%E5%9B%A0%E8%BD%AC%E5%BD%95%E6%9C%AC%E4%B8%8E%E5%90%8E%E6%9E%9C%E6%8F%90%E5%8F%96%E5%8F%98%E5%BC%82)。
