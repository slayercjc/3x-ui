# 3x-ui 中文安装脚本同步器

这个项目不复制或修改 3x-ui 的核心程序，只同步官方脚本并对终端提示和 `x-ui` 管理菜单应用中文补丁。

## 使用

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/slayercjc/3x-ui/main/dist/install-cn.sh)
```

生成后的脚本位于 `dist/install-cn.sh` 和 `dist/x-ui-cn.sh`。发布前请先检查 GitHub Actions 的构建结果。

## 同步机制

GitHub Actions 每天检查 `MHSanaei/3x-ui` 的 `main`：

1. 下载官方 `install.sh` 与 `x-ui.sh`；
2. 用 `translations.tsv` 替换已确认的英文提示；
3. 执行脚本格式和来源检查；
4. 生成中文脚本并提交到 `dist/`；
5. 官方脚本结构发生明显变化时让构建失败，避免静默生成错误版本。

中文补丁只作用于翻译表中明确列出的显示文本，不改动命令、变量、URL、参数或安装逻辑。新增提示需要人工加入 `translations.tsv`，不会被机器擅自翻译。

## 安全提示

这是第三方构建流程。每次发布前应检查 Actions diff，并核对官方脚本来源。不要把服务器密码、Token 或私钥提交到仓库。
