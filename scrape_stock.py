import yfinance as yf
import pandas as pd
from datetime import datetime

# 定义要爬取的股票代码，例如苹果公司
ticker = 'AAPL'

# 获取最近一年的数据
data = yf.download(ticker, period='1y')

# 添加日期列
data['Date'] = data.index

# 保存到CSV文件
data.to_csv('stock_data.csv', index=False)

print(f"股票数据已保存到 stock_data.csv，包含 {len(data)} 条记录。")
