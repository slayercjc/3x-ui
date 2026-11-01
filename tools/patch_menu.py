#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]

menu = '''show_usage() {
    echo -e "┌────────────────────────────────────────────────────────────────┐
│  ${blue}x-ui 控制菜单用法（子命令）：${plain}                                  │
│                                                                │
│  ${blue}x-ui${plain}                       - 管理面板脚本             │
│  ${blue}x-ui start${plain}                 - 启动                     │
│  ${blue}x-ui stop${plain}                  - 停止                     │
│  ${blue}x-ui restart${plain}               - 重启                     │
│  ${blue}x-ui status${plain}                - 当前状态                 │
│  ${blue}x-ui settings${plain}              - 当前设置                 │
│  ${blue}x-ui enable${plain}                - 启用开机自启             │
│  ${blue}x-ui disable${plain}               - 禁用开机自启             │
│  ${blue}x-ui log${plain}                   - 查看日志                 │
│  ${blue}x-ui banlog${plain}                - 查看 Fail2ban 封禁日志   │
│  ${blue}x-ui update${plain}                - 更新                     │
│  ${blue}x-ui legacy${plain}                - 旧版本                   │
│  ${blue}x-ui install${plain}               - 安装                     │
│  ${blue}x-ui uninstall${plain}             - 卸载                     │
└────────────────────────────────────────────────────────────────┘"
}'''

path = root / "dist" / "x-ui-cn.sh"
text = path.read_text(encoding="utf-8")
text, count = re.subn(r"show_usage\(\) \{.*?^\}", menu, text, count=1, flags=re.MULTILINE | re.DOTALL)
if count != 1:
    raise SystemExit("show_usage function was not found; upstream layout changed")

install = root / "dist" / "install-cn.sh"
install_text = install.read_text(encoding="utf-8")
replacements = {
    "Fail2ban setup complete.": "Fail2ban 设置完成。",
    "Setting up Fail2ban for the IP Limit feature...": "正在为 IP 限制功能设置 Fail2ban……",
    "x-ui v": "x-ui v",
    "installation finished, it is running now...": "安装完成，当前正在运行……",
    "Uninstalled Successfully.": "卸载成功。",
    "If you need to install this panel again, you can use below command:": "如果需要重新安装此面板，请使用以下命令：",
    "bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)": "bash <(curl -fsSL https://raw.githubusercontent.com/slayercjc/3x-ui/main/dist/install-cn.sh)",
}
for old, new in replacements.items():
    install_text = install_text.replace(old, new)

# The release archive installs the official management script after the panel
# files are unpacked. Replace the live command at the end of installation so
# future `x-ui` invocations use the translated script as well.
marker = "\n# 3x-ui-cn: install the translated management menu after the official install.\n"
if marker not in install_text:
    install_text += marker + '''
if [[ -x /usr/bin/x-ui ]]; then
    _xui_cn_url="https://raw.githubusercontent.com/slayercjc/3x-ui/main/dist/x-ui-cn.sh"
    if curl -fsSL "${_xui_cn_url}" -o /usr/bin/x-ui-cn.tmp; then
        chmod +x /usr/bin/x-ui-cn.tmp
        mv -f /usr/bin/x-ui-cn.tmp /usr/bin/x-ui
        if [[ -n "${xui_folder:-}" && -d "${xui_folder}" ]]; then
            curl -fsSL "${_xui_cn_url}" -o "${xui_folder}/x-ui.sh"
            chmod +x "${xui_folder}/x-ui.sh"
        fi
    fi
fi
'''
install.write_text(install_text, encoding="utf-8", newline="\n")
path.write_text(text, encoding="utf-8", newline="\n")
print("Static Chinese menu patch applied")
