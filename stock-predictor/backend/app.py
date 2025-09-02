from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from backend.core.state import PredictionRequest, PredictionResult, TopStocksResponse
from backend.core.utils import StockDataFetcher, validate_symbol
from backend.core.indicators import TechnicalIndicators
from backend.core.llm_manager import get_llm_analyzer, get_gpt_status
from backend.graph.pipeline import StockPredictionPipeline

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="Stock Prediction API",
    description="基于 LangGraph 的股票预测系统",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
data_fetcher = StockDataFetcher()
indicators_calculator = TechnicalIndicators()
prediction_pipeline = StockPredictionPipeline()
llm_analyzer = get_llm_analyzer()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Stock Prediction API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


@app.get("/api/gpt-status")
async def gpt_status():
    """GPT模型状态检查"""
    status = get_gpt_status()
    return {
        "gpt_available": status["available"],
        "model": status.get("model"),
        "temperature": status.get("temperature"),
        "api_key_configured": status.get("api_key_configured"),
        "reason": status.get("reason")
    }


@app.get("/api/stock/{symbol}")
async def get_stock_data(symbol: str):
    """获取股票数据"""
    if not validate_symbol(symbol):
        raise HTTPException(status_code=400, detail="Invalid stock symbol")
    
    try:
        # 获取股票数据
        data = data_fetcher.fetch_stock_data_sync(symbol.upper())
        stock_info = data_fetcher.get_stock_info_sync(symbol.upper())
        
        # 计算技术指标
        indicators = indicators_calculator.calculate_all_indicators(data)
        signal_strength = indicators_calculator.get_signal_strength(indicators)
        
        # 计算支撑阻力位
        support_resistance = indicators_calculator.calculate_support_resistance(data)
        
        return {
            "symbol": symbol.upper(),
            "info": stock_info,
            "data": data.tail(30).to_dict('records'),  # 返回最近30天数据
            "indicators": {k: float(v.iloc[-1]) if hasattr(v, 'iloc') and len(v) > 0 else float(v) 
                          for k, v in indicators.items() if not (hasattr(v, 'empty') and v.empty)},
            "signal_strength": signal_strength,
            "support_resistance": support_resistance
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock data: {str(e)}")


@app.post("/api/predict", response_model=PredictionResult)
async def predict_stock(request: PredictionRequest):
    """预测股票走势"""
    if not validate_symbol(request.symbol):
        raise HTTPException(status_code=400, detail="Invalid stock symbol")
    
    if request.timeframe not in ["1h", "1d", "1w"]:
        raise HTTPException(status_code=400, detail="Invalid timeframe")
    
    try:
        # 使用 LangGraph 工作流进行预测
        result = await prediction_pipeline.predict(request.symbol, request.timeframe)
        
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
        
        return PredictionResult(
            symbol=request.symbol.upper(),
            timeframe=request.timeframe,
            direction=result["direction"],
            probability=result["probability"],
            price_range=result["price_range"],
            confidence=result["confidence"],
            reasoning=result["reasoning"],
            risk_warning="本预测仅用于学习研究目的，不构成投资建议。投资有风险，入市需谨慎。"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/api/top-stocks", response_model=TopStocksResponse)
async def get_top_stocks():
    """获取Top 10股票建议"""
    try:
        # 获取一些市场数据作为上下文
        market_data = {
            "timestamp": "2024-01-01T00:00:00Z",
            "market_status": "open"
        }
        
        # 使用 LLM 生成建议
        print(f"Generating top stocks with market data: {market_data}")
        result = llm_analyzer.generate_top_stocks(market_data)
        print(f"LLM result: {result}")
        
        # 检查是否有错误
        if result.get("error"):
            print(f"LLM returned error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
        
        return TopStocksResponse(
            stocks=result["recommendations"],
            generated_at=result["generated_at"],
            disclaimer=result["disclaimer"]
        )
        
    except Exception as e:
        error_msg = str(e) if str(e) else "Unknown error occurred"
        print(f"Top stocks generation error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Failed to generate top stocks: {error_msg}")


@app.get("/api/search/{query}")
async def search_stocks(query: str):
    """搜索股票"""
    if len(query) < 1:
        raise HTTPException(status_code=400, detail="Query too short")
    
    # 简单的股票搜索（实际项目中可以集成更完整的搜索API）
    common_stocks = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", 
        "AMD", "CRM", "ORCL", "INTC", "CSCO", "ADBE", "PYPL", "UBER",
        "SPOT", "TWTR", "SNAP", "PINS", "SQ", "ROKU", "ZM", "DOCU"
    ]
    
    # 过滤匹配的股票
    matches = [stock for stock in common_stocks if query.upper() in stock]
    
    return {
        "query": query,
        "matches": matches[:10]  # 限制返回10个结果
    }


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
