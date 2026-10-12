# 中文生信 Wiki

面向入门学生，从群体分析和 GWAS 开始，逐步整理术语、方法与分析工作流。

**阅读入口：[GitHub Wiki](https://github.com/SpiralKernel/bioinfo-wiki/wiki)**

当前处于试写阶段，首批四篇文章只有标题与提纲，正文待作者编写。

## 首批文章

- [SNP与基因型是什么](wiki/SNP与基因型是什么.md)
- [群体结构是什么](wiki/群体结构是什么.md)
- [用PCA探索样本的群体结构](wiki/用PCA探索样本的群体结构.md)
- [群体结构与GWAS有什么关系](wiki/群体结构与GWAS有什么关系.md)

## 编写与发布

在 Obsidian 的 `知识库/中文生信Wiki` 中编写原稿。本仓库的 `wiki/` 保存导出的发布版，`scripts/` 保存导出与发布工具。

第一次使用，需要先进入 GitHub 的 Wiki 页面，点击创建第一页并保存。随后才能克隆 Wiki 的独立 Git 仓库。

完成编辑后，在本仓库目录执行：

```bash
python3 scripts/export_wiki.py --source '/你的Obsidian库/知识库/中文生信Wiki'
bash scripts/publish_wiki.sh
```

导出脚本会处理六类内容目录中的 Markdown 文件，移除 YAML 属性，并将内部链接转换为 Wiki 页面链接。首次导出会包含待写提纲，页面保留“待编写”标记。

脚本需要 Python 3.9 及以上版本和 Git；已登录 GitHub CLI 时，发布脚本会使用其凭据。

脚本不会修改原稿。内部链接无法解析、页面重名或使用了尚未支持的笔记嵌入时，导出会停止并提示位置。`附件/` 会一并复制；图片请使用标准 Markdown 语法，发布前检查其相对路径是否与导出后的目录一致。Obsidian 的 `![[...]]` 嵌入目前需要先手工改成 Markdown 链接。

`publish_wiki.sh` 首次运行会在本仓库旁克隆 `bioinfo-wiki.wiki`，后续先拉取更新，再同步并提交发布版。修改 Wiki 网页前，请先把相同修改补回 Obsidian 原稿，避免下次导出时丢失。

为保留人工维护的文件，脚本不自动删除旧页面；原稿改名或删除后，需要同步清理本仓库 `wiki/` 与 Wiki 仓库中的对应旧文件。

## 目录

```text
scripts/export_wiki.py    导出 Obsidian 文章，生成首页和侧边栏
scripts/publish_wiki.sh   发布到 Wiki 独立仓库
wiki/                    可提交和检查的发布文件
```
