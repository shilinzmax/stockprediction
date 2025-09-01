import os
import hashlib
import pandas as pd
import yfinance as yf
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path


class DataCache:
    """数据缓存管理"""
    
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, symbol: str, period: str) -> str:
        """生成缓存键"""
        return hashlib.md5(f"{symbol}_{period}".encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{cache_key}.parquet"
    
    def get_cached_data(self, symbol: str, period: str) -> Optional[pd.DataFrame]:
        """获取缓存数据"""
        cache_key = self._get_cache_key(symbol, period)
        cache_path = self._get_cache_path(cache_key)
        
        if cache_path.exists():
            try:
                df = pd.read_parquet(cache_path)
                # 检查数据是否过期（超过1小时）
                if 'timestamp' in df.columns:
                    last_update = pd.to_datetime(df['timestamp'].iloc[-1])
                    if datetime.now() - last_update < timedelta(hours=1):
                        return df
            except Exception as e:
                print(f"Error reading cache: {e}")
        
        return None
    
    def cache_data(self, symbol: str, period: str, data: pd.DataFrame):
        """缓存数据"""
        cache_key = self._get_cache_key(symbol, period)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            # 添加时间戳
            data_with_timestamp = data.copy()
            data_with_timestamp['timestamp'] = datetime.now()
            data_with_timestamp.to_parquet(cache_path)
        except Exception as e:
            print(f"Error caching data: {e}")


class StockDataFetcher:
    """股票数据获取器"""
    
    def __init__(self):
        self.cache = DataCache()
    
    def fetch_stock_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """获取股票数据"""
        # 先尝试从缓存获取
        cached_data = self.cache.get_cached_data(symbol, period)
        if cached_data is not None:
            return cached_data
        
        try:
            # 从 yfinance 获取数据
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                raise ValueError(f"No data found for symbol: {symbol}")
            
            # 清理数据
            data = data.reset_index()
            data.columns = [col.lower() for col in data.columns]
            
            # 缓存数据
            self.cache.cache_data(symbol, period, data)
            
            return data
            
        except Exception as e:
            raise ValueError(f"Failed to fetch data for {symbol}: {str(e)}")
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """获取股票基本信息"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "symbol": symbol,
                "name": info.get("longName", symbol),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                "market_cap": info.get("marketCap", 0),
                "current_price": info.get("currentPrice", 0),
                "currency": info.get("currency", "USD")
            }
        except Exception as e:
            return {
                "symbol": symbol,
                "name": symbol,
                "sector": "Unknown",
                "industry": "Unknown",
                "market_cap": 0,
                "current_price": 0,
                "currency": "USD"
            }


def validate_symbol(symbol: str) -> bool:
    """验证股票代码格式"""
    if not symbol or len(symbol) < 1 or len(symbol) > 10:
        return False
    
    # 基本格式检查：字母数字组合
    return symbol.replace(".", "").replace("-", "").isalnum()


def format_currency(amount: float, currency: str = "USD") -> str:
    """格式化货币显示"""
    if currency == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def calculate_percentage_change(current: float, previous: float) -> float:
    """计算百分比变化"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100
