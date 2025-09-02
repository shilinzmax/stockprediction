from typing import Dict, Any
import pandas as pd
from backend.core.state import WorkflowState
from backend.core.utils import StockDataFetcher


class FetchDataNode:
    """数据获取节点"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
    
    def __call__(self, state: WorkflowState) -> Dict[str, Any]:
        """获取股票数据"""
        try:
            # 根据时间框架确定数据周期
            period_map = {
                "1h": "5d",  # 1小时预测需要5天数据
                "1d": "1mo", # 1天预测需要1个月数据
                "1w": "3mo"  # 1周预测需要3个月数据
            }
            
            period = period_map.get(state.timeframe, "1mo")
            
            # 获取股票数据（使用同步方法）
            raw_data = self.data_fetcher.fetch_stock_data_sync(state.symbol, period)
            
            if raw_data.empty:
                return {
                    "error": f"No data found for symbol: {state.symbol}",
                    "raw_data": None
                }
            
            # 生成缓存键
            cache_key = f"{state.symbol}_{state.timeframe}_{period}"
            
            return {
                "raw_data": raw_data,
                "cache_key": cache_key,
                "error": None
            }
            
        except Exception as e:
            return {
                "error": f"Failed to fetch data: {str(e)}",
                "raw_data": None
            }
