from typing import Dict, Any
import pandas as pd
import numpy as np
from core.state import WorkflowState
from core.indicators import TechnicalIndicators


class FeatureEngineerNode:
    """特征工程节点"""
    
    def __init__(self):
        self.indicators_calculator = TechnicalIndicators()
    
    def __call__(self, state: WorkflowState) -> Dict[str, Any]:
        """处理数据并计算技术指标"""
        try:
            if state.raw_data is None or state.raw_data.empty:
                return {
                    "error": "No raw data available for processing",
                    "processed_data": None,
                    "indicators": None
                }
            
            # 数据预处理
            processed_data = self._preprocess_data(state.raw_data)
            
            # 计算技术指标
            indicators = self.indicators_calculator.calculate_all_indicators(processed_data)
            
            # 计算信号强度
            signal_strength = self.indicators_calculator.get_signal_strength(indicators)
            
            # 计算支撑阻力位
            support_resistance = self.indicators_calculator.calculate_support_resistance(processed_data)
            
            # 提取特征
            features = self._extract_features(processed_data, indicators, signal_strength)
            
            return {
                "processed_data": processed_data,
                "indicators": indicators,
                "signal_strength": signal_strength,
                "support_resistance": support_resistance,
                "features": features,
                "error": None
            }
            
        except Exception as e:
            return {
                "error": f"Feature engineering failed: {str(e)}",
                "processed_data": None,
                "indicators": None
            }
    
    def _preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """数据预处理"""
        df = data.copy()
        
        # 确保日期列存在且为datetime类型
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        elif df.index.name == 'Date' or 'Date' in df.columns:
            if 'Date' in df.columns:
                df['date'] = pd.to_datetime(df['Date'])
            else:
                df['date'] = pd.to_datetime(df.index)
        
        # 确保数值列为float类型
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 处理缺失值
        df = df.ffill().bfill()
        
        # 按日期排序
        df = df.sort_values('date').reset_index(drop=True)
        
        return df
    
    def _extract_features(self, data: pd.DataFrame, indicators: Dict[str, Any], 
                         signal_strength: Dict[str, Any]) -> Dict[str, Any]:
        """提取特征"""
        if data.empty:
            return {}
        
        latest_data = data.iloc[-1]
        
        features = {
            # 价格特征
            "current_price": float(latest_data.get('close', 0)),
            "price_change_1d": float(data['close'].pct_change().iloc[-1]) if len(data) > 1 else 0,
            "price_change_5d": float(data['close'].pct_change(periods=5).iloc[-1]) if len(data) > 5 else 0,
            "price_change_20d": float(data['close'].pct_change(periods=20).iloc[-1]) if len(data) > 20 else 0,
            
            # 成交量特征
            "volume_ratio": float(latest_data.get('volume', 0) / data['volume'].mean()) if data['volume'].mean() > 0 else 1,
            "volume_trend": float(data['volume'].pct_change().iloc[-1]) if len(data) > 1 else 0,
            
            # 波动率特征
            "volatility_20d": float(data['close'].rolling(20).std().iloc[-1]) if len(data) > 20 else 0,
            "atr": float(indicators.get('atr', pd.Series([0])).iloc[-1]) if 'atr' in indicators and len(indicators['atr']) > 0 else 0,
            
            # 技术指标特征
            "rsi": float(indicators.get('rsi', pd.Series([50])).iloc[-1]) if 'rsi' in indicators and len(indicators['rsi']) > 0 else 50,
            "macd_signal": 1 if indicators.get('macd', pd.Series([0])).iloc[-1] > indicators.get('macd_signal', pd.Series([0])).iloc[-1] else -1 if 'macd' in indicators and 'macd_signal' in indicators else 0,
            
            # 移动平均线特征
            "sma_5_20_ratio": float(indicators.get('sma_5', pd.Series([0])).iloc[-1] / indicators.get('sma_20', pd.Series([1])).iloc[-1]) if 'sma_5' in indicators and 'sma_20' in indicators else 1,
            "price_sma_20_ratio": float(latest_data.get('close', 0) / indicators.get('sma_20', pd.Series([1])).iloc[-1]) if 'sma_20' in indicators else 1,
            
            # 信号强度
            "signal_score": float(signal_strength.get('score', 0)),
            "signal_strength": signal_strength.get('strength', 'neutral'),
            
            # 时间特征
            "day_of_week": latest_data['date'].dayofweek if 'date' in latest_data else 0,
            "hour": latest_data['date'].hour if 'date' in latest_data else 12,
        }
        
        return features
