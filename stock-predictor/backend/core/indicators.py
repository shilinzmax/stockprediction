import pandas as pd
import numpy as np
import ta
from typing import Dict, Any


class TechnicalIndicators:
    """技术指标计算器"""
    
    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame) -> Dict[str, Any]:
        """计算所有技术指标"""
        if df.empty or len(df) < 20:
            return {}
        
        # 确保数据按日期排序
        df = df.sort_values('date').reset_index(drop=True)
        
        indicators = {}
        
        # 移动平均线
        indicators['sma_5'] = ta.trend.sma_indicator(df['close'], window=5)
        indicators['sma_10'] = ta.trend.sma_indicator(df['close'], window=10)
        indicators['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
        indicators['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
        
        # 指数移动平均线
        indicators['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
        indicators['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)
        
        # MACD
        macd = ta.trend.MACD(df['close'])
        indicators['macd'] = macd.macd()
        indicators['macd_signal'] = macd.macd_signal()
        indicators['macd_histogram'] = macd.macd_diff()
        
        # RSI
        indicators['rsi'] = ta.momentum.rsi(df['close'], window=14)
        
        # 布林带
        bollinger = ta.volatility.BollingerBands(df['close'])
        indicators['bb_upper'] = bollinger.bollinger_hband()
        indicators['bb_middle'] = bollinger.bollinger_mavg()
        indicators['bb_lower'] = bollinger.bollinger_lband()
        indicators['bb_width'] = bollinger.bollinger_wband()
        
        # 随机指标
        stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
        indicators['stoch_k'] = stoch.stoch()
        indicators['stoch_d'] = stoch.stoch_signal()
        
        # 威廉指标
        indicators['williams_r'] = ta.momentum.williams_r(df['high'], df['low'], df['close'])
        
        # 成交量指标
        indicators['volume_sma'] = ta.volume.volume_sma(df['close'], df['volume'])
        indicators['volume_ema'] = ta.volume.volume_ema(df['close'], df['volume'])
        
        # ATR (平均真实波幅)
        indicators['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'])
        
        # 价格变化
        indicators['price_change'] = df['close'].pct_change()
        indicators['price_change_5d'] = df['close'].pct_change(periods=5)
        
        # 波动率
        indicators['volatility'] = df['close'].rolling(window=20).std()
        
        return indicators
    
    @staticmethod
    def get_signal_strength(indicators: Dict[str, Any], current_idx: int = -1) -> Dict[str, Any]:
        """分析信号强度"""
        if not indicators or current_idx == -1:
            return {"strength": "neutral", "score": 0, "signals": []}
        
        signals = []
        score = 0
        
        # RSI 信号
        rsi = indicators.get('rsi', pd.Series([50]))
        if len(rsi) > current_idx:
            rsi_val = rsi.iloc[current_idx]
            if rsi_val < 30:
                signals.append("RSI超卖")
                score += 2
            elif rsi_val > 70:
                signals.append("RSI超买")
                score -= 2
        
        # MACD 信号
        macd = indicators.get('macd', pd.Series([0]))
        macd_signal = indicators.get('macd_signal', pd.Series([0]))
        if len(macd) > current_idx and len(macd_signal) > current_idx:
            if macd.iloc[current_idx] > macd_signal.iloc[current_idx]:
                signals.append("MACD金叉")
                score += 1
            else:
                signals.append("MACD死叉")
                score -= 1
        
        # 移动平均线信号
        sma_5 = indicators.get('sma_5', pd.Series([0]))
        sma_20 = indicators.get('sma_20', pd.Series([0]))
        if len(sma_5) > current_idx and len(sma_20) > current_idx:
            if sma_5.iloc[current_idx] > sma_20.iloc[current_idx]:
                signals.append("短期均线上穿长期均线")
                score += 1
            else:
                signals.append("短期均线下穿长期均线")
                score -= 1
        
        # 布林带信号
        bb_upper = indicators.get('bb_upper', pd.Series([0]))
        bb_lower = indicators.get('bb_lower', pd.Series([0]))
        if len(bb_upper) > current_idx and len(bb_lower) > current_idx:
            bb_width = bb_upper.iloc[current_idx] - bb_lower.iloc[current_idx]
            if bb_width > 0:
                signals.append("布林带收窄")
                score += 0.5
        
        # 确定信号强度
        if score >= 3:
            strength = "strong_bullish"
        elif score >= 1:
            strength = "bullish"
        elif score <= -3:
            strength = "strong_bearish"
        elif score <= -1:
            strength = "bearish"
        else:
            strength = "neutral"
        
        return {
            "strength": strength,
            "score": score,
            "signals": signals
        }
    
    @staticmethod
    def calculate_support_resistance(df: pd.DataFrame, window: int = 20) -> Dict[str, float]:
        """计算支撑位和阻力位"""
        if df.empty or len(df) < window:
            return {"support": 0, "resistance": 0}
        
        recent_data = df.tail(window)
        
        # 简单的支撑阻力位计算
        support = recent_data['low'].min()
        resistance = recent_data['high'].max()
        
        return {
            "support": float(support),
            "resistance": float(resistance)
        }
