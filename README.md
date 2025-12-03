# 🎯 自动点击下单脚本

当前仓库主要使用 `simple_click.py`，通过 `pyautogui` 在 Variational 和 Lighter 的交易页面自动点击下单。

## 快速开始
- 安装依赖：`pip install -r requirements.txt`
- 运行脚本：`python simple_click.py`
  - 选择使用已保存的坐标或重新记录坐标
  - 按提示将鼠标移动到两个交易按钮，等待 3 秒自动记录
- 保持交易页面在前台，脚本会按配置循环点击；快速晃动鼠标可中断

## 可调参数（位于 `simple_click.py` 顶部）
- `order_count`：下单次数
- `interval`：两次下单的间隔（秒）
- `use_double_click`：是否双击
- `click_delay`：单次点击间隔（秒）

## 目录结构
- `simple_click.py`：自动点击脚本
- `coordinates.json`：保存的按钮坐标（运行脚本后生成/更新）
- `requirements.txt`：Python 依赖（仅 `pyautogui`）
- `arbitrage-extension/`：旧的浏览器扩展代码，当前脚本未使用，可忽略

## 注意事项
- 脚本结束时会调用 macOS 的 `afplay` 播放提示音，其他系统可按需调整最后的提示音命令。
- 页面布局变动后需重新记录坐标，确保点击位置正确。
- 建议在虚拟环境中安装依赖，避免污染全局 Python 环境。
