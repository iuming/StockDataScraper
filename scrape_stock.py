"""
股票数据抓取脚本（支持多股票、增量更新、空数据诊断）。

用法示例：
1. 默认抓取AAPL：python scrape_stock.py
2. 多股票：TICKERS="AAPL,MSFT,GOOGL" python scrape_stock.py
3. 指定日期：START=2023-01-01 END=2025-09-11 python scrape_stock.py
4. 自动增量合并CSV，无重复。

环境变量：
  TICKERS  股票代码，逗号分隔
  START    开始日期，格式YYYY-MM-DD
  END      结束日期，格式YYYY-MM-DD

注意：如遇“No data found”，请确保Python>=3.10且yfinance为最新版。
"""
import os
from datetime import datetime, timedelta

from typing import List, Optional

import pandas as pd
import yfinance as yf

OUTPUT_FILE = "stock_data.csv"

def log(msg: str, level: str = "INFO") -> None:
	print(f"[{level}] {msg}")


def parse_tickers(env_value: Optional[str]) -> List[str]:
	"""解析股票代码环境变量"""
	if not env_value:
		return ["AAPL"]
	return [t.strip().upper() for t in env_value.split(",") if t.strip()]


def date_from_env(var_name: str, default: datetime) -> datetime:
	"""从环境变量读取日期，支持多种格式"""
	val = os.getenv(var_name)
	if not val:
		return default
	for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
		try:
			return datetime.strptime(val, fmt)
		except ValueError:
			continue
	raise ValueError(f"环境变量 {var_name} 日期格式不正确: {val}")


def fetch_one(ticker: str, start: datetime, end: datetime) -> pd.DataFrame:
	"""抓取单只股票数据，返回DataFrame"""
	end_plus = end + timedelta(days=1)  # yfinance end为开区间
	try:
		df = yf.download(
			ticker,
			start=start.strftime("%Y-%m-%d"),
			end=end_plus.strftime("%Y-%m-%d"),
			interval="1d",
			auto_adjust=False,
			progress=False,
			threads=True,
		)
	except Exception as e:
		log(f"yfinance 抓取 {ticker} 异常: {e}", "ERROR")
		return pd.DataFrame()
	if df.empty:
		log(f"{ticker} 未获取到数据。可能原因：1) yfinance 版本过旧 2) 网络被阻断 3) 符号错误 4) 非交易日区间。", "WARN")
		return df
	df["Ticker"] = ticker
	df["Date"] = df.index.tz_localize(None) if hasattr(df.index, 'tz') else df.index
	# 规范列顺序
	cols = [
		"Date",
		"Ticker",
		"Open",
		"High",
		"Low",
		"Close",
		"Adj Close" if "Adj Close" in df.columns else "Close",
		"Volume",
	]
	cols = [c for c in cols if c in df.columns]
	return df[cols]


def merge_incremental(new_df: pd.DataFrame, path: str) -> pd.DataFrame:
	"""合并新旧数据，去重并排序"""
	if not os.path.exists(path):
		return new_df.sort_values(["Ticker", "Date"]) if not new_df.empty else new_df
	try:
		old = pd.read_csv(path, parse_dates=["Date"], low_memory=False)
	except Exception as e:
		log(f"读取已有文件失败，将重建: {e}", "WARN")
		return new_df
	combined = pd.concat([old, new_df], ignore_index=True)
	combined = combined.drop_duplicates(subset=["Ticker", "Date"]).sort_values(["Ticker", "Date"]).reset_index(drop=True)
	return combined



def main() -> None:
	"""主流程"""
	tickers = parse_tickers(os.getenv("TICKERS"))
	today = datetime.utcnow().date()
	# 默认抓取最近 365 天（含今天）
	default_start = datetime.combine(today - timedelta(days=365), datetime.min.time())
	default_end = datetime.combine(today, datetime.min.time())
	start = date_from_env("START", default_start)
	end = date_from_env("END", default_end)

	if start > end:
		raise ValueError("开始日期不能晚于结束日期")

	log(f"抓取股票: {tickers}")
	log(f"时间区间: {start.date()} -> {end.date()}")

	all_frames: List[pd.DataFrame] = []
	for t in tickers:
		df = fetch_one(t, start, end)
		if not df.empty:
			all_frames.append(df)

	if not all_frames:
		log("所有股票均未返回数据，请检查：1) Python版本>=3.10? 2) yfinance是否最新? 3) 是否被网络限制? 4) 符号拼写。", "ERROR")
		return

	new_data = pd.concat(all_frames, ignore_index=True)
	final = merge_incremental(new_data, OUTPUT_FILE)
	final.to_csv(OUTPUT_FILE, index=False)
	log(f"已写入 {OUTPUT_FILE}，共 {len(final)} 条记录，本次新增 {len(new_data)} 条，涉及 {len(tickers)} 只股票。")


if __name__ == "__main__":
	main()
