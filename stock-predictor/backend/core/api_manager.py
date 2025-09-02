import os
import asyncio
import aiohttp
import requests
import pandas as pd
import yfinance as yf
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)


class APIManager:
    """多API数据源管理器"""
    
    def __init__(self):
        # API配置
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.iex_cloud_key = os.getenv('IEX_CLOUD_API_KEY')
        self.polygon_io_key = os.getenv('POLYGON_IO_API_KEY')
        
        # API优先级（按可靠性排序）
        self.api_priority = [
            'yfinance',
            'alpha_vantage',
            'iex_cloud',
            'polygon_io',
            'mock'
        ]
        
        # 初始化Alpha Vantage
        if self.alpha_vantage_key:
            self.alpha_vantage = TimeSeries(key=self.alpha_vantage_key)
            self.alpha_vantage_fd = FundamentalData(key=self.alpha_vantage_key)
        else:
            self.alpha_vantage = None
            self.alpha_vantage_fd = None
    
    async def get_stock_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """获取股票数据，按优先级尝试不同API"""
        
        for api_name in self.api_priority:
            try:
                logger.info(f"Trying {api_name} for {symbol}")
                
                if api_name == 'yfinance':
                    data = await self._get_yfinance_data(symbol, period)
                elif api_name == 'alpha_vantage':
                    data = await self._get_alpha_vantage_data(symbol, period)
                elif api_name == 'iex_cloud':
                    data = await self._get_iex_cloud_data(symbol, period)
                elif api_name == 'polygon_io':
                    data = await self._get_polygon_io_data(symbol, period)
                elif api_name == 'mock':
                    data = await self._get_mock_data(symbol, period)
                
                if data is not None and not data.empty:
                    logger.info(f"Successfully got data from {api_name}")
                    return data
                    
            except Exception as e:
                logger.warning(f"{api_name} failed for {symbol}: {str(e)}")
                continue
        
        # 如果所有API都失败，返回空DataFrame
        logger.error(f"All APIs failed for {symbol}")
        return pd.DataFrame()
    
    async def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """获取股票基本信息"""
        
        for api_name in self.api_priority:
            try:
                if api_name == 'yfinance':
                    info = await self._get_yfinance_info(symbol)
                elif api_name == 'alpha_vantage':
                    info = await self._get_alpha_vantage_info(symbol)
                elif api_name == 'iex_cloud':
                    info = await self._get_iex_cloud_info(symbol)
                elif api_name == 'polygon_io':
                    info = await self._get_polygon_io_info(symbol)
                elif api_name == 'mock':
                    info = await self._get_mock_info(symbol)
                
                if info:
                    return info
                    
            except Exception as e:
                logger.warning(f"{api_name} info failed for {symbol}: {str(e)}")
                continue
        
        return self._get_default_info(symbol)
    
    # YFinance API
    async def _get_yfinance_data(self, symbol: str, period: str) -> pd.DataFrame:
        """使用yfinance获取数据"""
        def _fetch():
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            if not data.empty:
                data = data.reset_index()
                data.columns = [col.lower() for col in data.columns]
            return data
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)
    
    async def _get_yfinance_info(self, symbol: str) -> Dict[str, Any]:
        """使用yfinance获取股票信息"""
        def _fetch():
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                "symbol": symbol,
                "name": info.get("longName", symbol),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
                "current_price": info.get("currentPrice", 0),
                "currency": info.get("currency", "USD"),
                "exchange": info.get("exchange", "Unknown")
            }
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)
    
    # Alpha Vantage API
    async def _get_alpha_vantage_data(self, symbol: str, period: str) -> pd.DataFrame:
        """使用Alpha Vantage获取数据"""
        if not self.alpha_vantage:
            raise Exception("Alpha Vantage API key not configured")
        
        def _fetch():
            # 根据period选择函数
            if period in ['1d', '5d']:
                data, _ = self.alpha_vantage.get_intraday(symbol=symbol, interval='5min')
            else:
                data, _ = self.alpha_vantage.get_daily(symbol=symbol)
            
            if data:
                df = pd.DataFrame(data).T
                df.index = pd.to_datetime(df.index)
                df.columns = ['open', 'high', 'low', 'close', 'volume']
                df = df.astype(float)
                return df.reset_index()
            return pd.DataFrame()
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)
    
    async def _get_alpha_vantage_info(self, symbol: str) -> Dict[str, Any]:
        """使用Alpha Vantage获取股票信息"""
        if not self.alpha_vantage_fd:
            raise Exception("Alpha Vantage API key not configured")
        
        def _fetch():
            try:
                overview, _ = self.alpha_vantage_fd.get_company_overview(symbol=symbol)
                if overview:
                    return {
                        "symbol": symbol,
                        "name": overview.get("Name", symbol),
                        "sector": overview.get("Sector", "Unknown"),
                        "industry": overview.get("Industry", "Unknown"),
                        "market_cap": float(overview.get("MarketCapitalization", 0)),
                        "pe_ratio": float(overview.get("PERatio", 0)),
                        "dividend_yield": float(overview.get("DividendYield", 0)),
                        "52_week_high": float(overview.get("52WeekHigh", 0)),
                        "52_week_low": float(overview.get("52WeekLow", 0)),
                        "current_price": float(overview.get("50DayMovingAverage", 0)),
                        "currency": "USD",
                        "exchange": overview.get("Exchange", "Unknown")
                    }
            except:
                pass
            return None
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)
    
    # IEX Cloud API
    async def _get_iex_cloud_data(self, symbol: str, period: str) -> pd.DataFrame:
        """使用IEX Cloud获取数据"""
        if not self.iex_cloud_key:
            raise Exception("IEX Cloud API key not configured")
        
        # 根据period确定范围
        range_map = {
            '1d': '1d',
            '5d': '5d',
            '1mo': '1m',
            '3mo': '3m',
            '6mo': '6m',
            '1y': '1y',
            '2y': '2y',
            '5y': '5y'
        }
        
        range_param = range_map.get(period, '1m')
        url = f"https://cloud.iexapis.com/stable/stock/{symbol}/chart/{range_param}?token={self.iex_cloud_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        df = pd.DataFrame(data)
                        df['date'] = pd.to_datetime(df['date'])
                        df = df.set_index('date')
                        df = df[['open', 'high', 'low', 'close', 'volume']]
                        return df.reset_index()
        return pd.DataFrame()
    
    async def _get_iex_cloud_info(self, symbol: str) -> Dict[str, Any]:
        """使用IEX Cloud获取股票信息"""
        if not self.iex_cloud_key:
            raise Exception("IEX Cloud API key not configured")
        
        url = f"https://cloud.iexapis.com/stable/stock/{symbol}/company?token={self.iex_cloud_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "symbol": symbol,
                        "name": data.get("companyName", symbol),
                        "sector": data.get("sector", "Unknown"),
                        "industry": data.get("industry", "Unknown"),
                        "market_cap": 0,  # IEX Cloud需要额外API调用
                        "pe_ratio": 0,
                        "dividend_yield": 0,
                        "52_week_high": 0,
                        "52_week_low": 0,
                        "current_price": 0,
                        "currency": "USD",
                        "exchange": data.get("exchange", "Unknown")
                    }
        return None
    
    # Polygon.io API
    async def _get_polygon_io_data(self, symbol: str, period: str) -> pd.DataFrame:
        """使用Polygon.io获取数据"""
        if not self.polygon_io_key:
            raise Exception("Polygon.io API key not configured")
        
        # 计算日期范围
        end_date = datetime.now()
        if period == '1d':
            start_date = end_date - timedelta(days=1)
        elif period == '5d':
            start_date = end_date - timedelta(days=5)
        elif period == '1mo':
            start_date = end_date - timedelta(days=30)
        elif period == '3mo':
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_str}/{end_str}?apikey={self.polygon_io_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('results'):
                        df = pd.DataFrame(data['results'])
                        df['date'] = pd.to_datetime(df['t'], unit='ms')
                        df = df.set_index('date')
                        df = df.rename(columns={
                            'o': 'open',
                            'h': 'high', 
                            'l': 'low',
                            'c': 'close',
                            'v': 'volume'
                        })
                        df = df[['open', 'high', 'low', 'close', 'volume']]
                        return df.reset_index()
        return pd.DataFrame()
    
    async def _get_polygon_io_info(self, symbol: str) -> Dict[str, Any]:
        """使用Polygon.io获取股票信息"""
        if not self.polygon_io_key:
            raise Exception("Polygon.io API key not configured")
        
        url = f"https://api.polygon.io/v3/reference/tickers/{symbol}?apikey={self.polygon_io_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('results'):
                        result = data['results']
                        return {
                            "symbol": symbol,
                            "name": result.get("name", symbol),
                            "sector": "Unknown",
                            "industry": "Unknown",
                            "market_cap": 0,
                            "pe_ratio": 0,
                            "dividend_yield": 0,
                            "52_week_high": 0,
                            "52_week_low": 0,
                            "current_price": 0,
                            "currency": "USD",
                            "exchange": result.get("primary_exchange", "Unknown")
                        }
        return None
    
    # Mock数据
    async def _get_mock_data(self, symbol: str, period: str) -> pd.DataFrame:
        """使用Mock数据生成器"""
        from .mock_data import mock_data_generator
        
        def _fetch():
            return mock_data_generator.generate_stock_data(symbol, period)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)
    
    async def _get_mock_info(self, symbol: str) -> Dict[str, Any]:
        """使用Mock信息生成器"""
        from .mock_data import mock_data_generator
        
        def _fetch():
            return mock_data_generator.get_stock_info(symbol)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)
    
    def _get_default_info(self, symbol: str) -> Dict[str, Any]:
        """默认股票信息"""
        return {
            "symbol": symbol,
            "name": symbol,
            "sector": "Unknown",
            "industry": "Unknown",
            "market_cap": 0,
            "pe_ratio": 0,
            "dividend_yield": 0,
            "52_week_high": 0,
            "52_week_low": 0,
            "current_price": 0,
            "currency": "USD",
            "exchange": "Unknown"
        }


# 全局API管理器实例
api_manager = APIManager()
