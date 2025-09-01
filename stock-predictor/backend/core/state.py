from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import pandas as pd


class StockData(BaseModel):
    """股票数据模型"""
    symbol: str
    data: pd.DataFrame
    indicators: Dict[str, Any]
    metadata: Dict[str, Any]


class PredictionRequest(BaseModel):
    """预测请求模型"""
    symbol: str
    timeframe: str  # "1h", "1d", "1w"
    current_price: Optional[float] = None


class PredictionResult(BaseModel):
    """预测结果模型"""
    symbol: str
    timeframe: str
    direction: str  # "up", "down", "neutral"
    probability: float  # 0-100
    price_range: Dict[str, float]  # {"min": 100, "max": 110}
    confidence: str  # "high", "medium", "low"
    reasoning: str
    risk_warning: str


class StockAdvice(BaseModel):
    """股票建议模型"""
    symbol: str
    direction: str
    probability: float
    reasoning: str
    risk_level: str
    expected_return: str


class TopStocksResponse(BaseModel):
    """Top 10 股票建议响应"""
    stocks: List[StockAdvice]
    generated_at: str
    disclaimer: str


class WorkflowState(BaseModel):
    """LangGraph 工作流状态"""
    symbol: str
    timeframe: str
    raw_data: Optional[pd.DataFrame] = None
    processed_data: Optional[pd.DataFrame] = None
    indicators: Optional[Dict[str, Any]] = None
    features: Optional[Dict[str, Any]] = None
    llm_analysis: Optional[Dict[str, Any]] = None
    prediction: Optional[PredictionResult] = None
    error: Optional[str] = None
    cache_key: Optional[str] = None
