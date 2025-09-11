# 股票数据爬取脚本

这个项目使用Python脚本每天自动爬取股票数据，并使用GitHub Actions进行自动化。

## 功能

- 使用yfinance库获取股票数据（例如苹果公司的股价）
- 将数据保存到CSV文件
- GitHub Actions每天自动运行脚本并更新数据

## 设置

1. 克隆或下载这个仓库到本地。
2. 安装依赖：`pip install -r requirements.txt`
3. 运行脚本：`python scrape_stock.py`

## GitHub Actions

- Workflow文件位于 `.github/workflows/daily-stock-scrape.yml`
- 每天午夜UTC自动运行
- 可以手动触发

## 自定义

- 修改 `scrape_stock.py` 中的 `ticker` 变量来选择不同的股票
- 调整 `period` 参数来获取不同时间范围的数据

## 注意

确保你的GitHub仓库是公开的，或者配置适当的权限以允许Actions推送更改。
