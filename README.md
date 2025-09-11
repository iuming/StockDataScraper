# 股票数据爬取脚本

这个项目使用Python脚本每天自动爬取股票数据，并使用GitHub Actions进行自动化。

## 功能

- 使用 akshare 库获取美股数据（稳定可靠，无限流问题）
- 支持多股票批量抓取
- 将数据保存到CSV文件，自动去重合并
- GitHub Actions 自动化运行（工作日每天更新）
- 错误监控和自动Issue创建

## 脚本版本

1. **scrape_stock.py** - 原版本（基于yfinance，可能遇到限流）
2. **scrape_stock_akshare.py** - 推荐版本（基于akshare，更稳定）

## 设置

1. 克隆或下载这个仓库到本地。
2. 安装依赖：`pip install -r requirements.txt`
3. 运行脚本：`python scrape_stock_akshare.py`

## 环境变量用法

支持通过环境变量自定义：

- `TICKERS`：股票代码，逗号分隔。例如：`TICKERS="AAPL,MSFT,GOOGL" python scrape_stock_akshare.py`
- `START`：开始日期，格式如 `2023-01-01`
- `END`：结束日期，格式如 `2025-09-11`

如不指定，默认抓取热门美股最近30天数据。

## GitHub Actions

### 基础版本 (daily-stock-scrape.yml)
- 每个工作日凌晨2点UTC自动运行
- 抓取预设的5只热门美股
- 自动提交更新到仓库

### 增强版本 (enhanced-stock-scrape.yml)
- 支持手动触发并自定义参数
- 智能检测是否有新数据才提交
- 生成详细的更新摘要
- 失败时自动创建Issue
- 上传日志文件便于调试

### 手动触发步骤
1. 进入仓库的 Actions 页面
2. 选择 "Enhanced Stock Data Scraper"
3. 点击 "Run workflow"
4. 可选择自定义股票代码、开始日期等参数

## 特性说明

- 支持多股票批量抓取
- 自动增量合并到 `stock_data.csv`，不会重复
- 支持断点续抓、空数据诊断
- 智能调度：仅在工作日运行（股市开市时间）

## 常见问题

- 若出现 "No data found" 或数据为空，请确保：
  1. Python 版本 >= 3.10
  2. akshare 已安装并为最新版
  3. 网络未被限制
  4. 股票代码拼写正确

## 数据格式

CSV文件包含以下列：
- Date: 日期
- Ticker: 股票代码  
- Open: 开盘价
- High: 最高价
- Low: 最低价
- Close: 收盘价
- Volume: 成交量

## 注意事项

1. 确保你的GitHub仓库Actions权限已开启
2. 私有仓库需要配置适当的写入权限
3. 建议Fork后在自己的仓库中使用
4. akshare数据免费，但请合理使用避免过于频繁的请求
