import os
import hashlib
import pandas as pd
import yfinance as yf
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from .mock_data import mock_data_generator
from .api_manager import api_manager


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
    
    async def fetch_stock_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """获取股票数据"""
        # 先尝试从缓存获取
        cached_data = self.cache.get_cached_data(symbol, period)
        if cached_data is not None:
            return cached_data
        
        try:
            # 使用API管理器获取数据
            data = await api_manager.get_stock_data(symbol, period)
            
            if data.empty:
                raise ValueError(f"No data found for symbol: {symbol}")
            
            # 缓存数据
            self.cache.cache_data(symbol, period, data)
            
            return data
            
        except Exception as e:
            print(f"All APIs failed for {symbol}, using mock data: {str(e)}")
            # 使用Mock数据作为备用
            mock_data = mock_data_generator.generate_stock_data(symbol, period)
            # 缓存Mock数据
            self.cache.cache_data(symbol, period, mock_data)
            return mock_data
    
    def fetch_stock_data_sync(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """同步获取股票数据"""
        import asyncio
        try:
            # 检查是否在事件循环中
            loop = asyncio.get_running_loop()
            # 如果在事件循环中，使用线程池执行
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self.fetch_stock_data(symbol, period))
                return future.result()
        except RuntimeError:
            # 如果没有运行的事件循环，直接运行
            return asyncio.run(self.fetch_stock_data(symbol, period))
    
    async def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """获取股票基本信息"""
        try:
            # 使用API管理器获取信息
            info = await api_manager.get_stock_info(symbol)
            return info
        except Exception as e:
            print(f"All APIs failed for {symbol} info, using mock info: {str(e)}")
            # 使用Mock信息作为备用
            return mock_data_generator.get_stock_info(symbol)
    
    def get_stock_info_sync(self, symbol: str) -> Dict[str, Any]:
        """同步获取股票基本信息"""
        import asyncio
        try:
            # 检查是否在事件循环中
            loop = asyncio.get_running_loop()
            # 如果在事件循环中，使用线程池执行
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self.get_stock_info(symbol))
                return future.result()
        except RuntimeError:
            # 如果没有运行的事件循环，直接运行
            return asyncio.run(self.get_stock_info(symbol))


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
