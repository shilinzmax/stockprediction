import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import random


class MockStockDataGenerator:
    """Mock股票数据生成器"""
    
    def __init__(self):
        self.base_prices = {
            'AAPL': 180.0,
            'MSFT': 350.0,
            'GOOGL': 140.0,
            'AMZN': 150.0,
            'TSLA': 250.0,
            'NVDA': 800.0,
            'META': 300.0,
            'NFLX': 400.0,
            'AMD': 120.0,
            'CRM': 200.0
        }
    
    def generate_stock_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """生成模拟股票数据"""
        # 确定数据点数量
        period_days = {
            "5d": 5,
            "1mo": 30,
            "3mo": 90
        }
        
        days = period_days.get(period, 30)
        
        # 获取基础价格
        base_price = self.base_prices.get(symbol.upper(), 100.0)
        
        # 生成日期序列
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # 生成价格数据
        data = []
        current_price = base_price
        
        for i, date in enumerate(dates):
            # 模拟价格波动
            volatility = 0.02  # 2%的日波动率
            change = np.random.normal(0, volatility)
            current_price *= (1 + change)
            
            # 生成OHLCV数据
            high = current_price * (1 + abs(np.random.normal(0, 0.01)))
            low = current_price * (1 - abs(np.random.normal(0, 0.01)))
            open_price = current_price * (1 + np.random.normal(0, 0.005))
            close_price = current_price
            
            # 确保OHLC逻辑正确
            high = max(high, open_price, close_price)
            low = min(low, open_price, close_price)
            
            # 生成成交量
            volume = random.randint(1000000, 10000000)
            
            data.append({
                'date': date,
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close_price, 2),
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        return df
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """获取模拟股票信息"""
        base_price = self.base_prices.get(symbol.upper(), 100.0)
        
        return {
            "symbol": symbol.upper(),
            "name": f"{symbol.upper()} Corporation",
            "sector": "Technology",
            "industry": "Software",
            "market_cap": random.randint(100000000000, 3000000000000),
            "pe_ratio": round(random.uniform(15, 35), 2),
            "dividend_yield": round(random.uniform(0.5, 3.0), 2),
            "52_week_high": round(base_price * 1.3, 2),
            "52_week_low": round(base_price * 0.7, 2),
            "current_price": round(base_price, 2),
            "currency": "USD",
            "exchange": "NASDAQ"
        }


# 全局实例
mock_data_generator = MockStockDataGenerator()
