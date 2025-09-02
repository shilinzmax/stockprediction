#!/usr/bin/env python3
"""
Google Colab 版本的股票预测应用
适配Colab环境的FastAPI应用
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Dict, Any
import os
from pathlib import Path

# 设置Colab环境
def setup_colab_environment():
    """设置Colab环境"""
    # 创建必要的目录
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 设置环境变量
    os.environ["CACHE_DIR"] = str(data_dir)
    os.environ["CACHE_TTL_HOURS"] = "1"
    os.environ["LOG_LEVEL"] = "INFO"
    
    # 添加当前目录到Python路径
    import sys
    sys.path.append(".")

# 设置环境
setup_colab_environment()

# 导入项目模块
try:
    from backend.core.state import PredictionRequest, PredictionResult, TopStocksResponse
    from backend.core.utils import StockDataFetcher, validate_symbol
    from backend.core.indicators import TechnicalIndicators
    from backend.core.llm_manager import get_llm_analyzer, get_gpt_status
    from backend.graph.pipeline import StockPredictionPipeline
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已上传完整的项目文件到Colab")
    raise

# 创建FastAPI应用
app = FastAPI(
    title="Stock Prediction API - Colab Version",
    description="基于 LangGraph 的股票预测系统 (Google Colab版本)",
    version="1.0.0-colab"
)

# 配置 CORS - 允许Colab访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Colab中允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
try:
    data_fetcher = StockDataFetcher()
    indicators_calculator = TechnicalIndicators()
    prediction_pipeline = StockPredictionPipeline()
    llm_analyzer = get_llm_analyzer()
    print("✅ 组件初始化成功")
except Exception as e:
    print(f"❌ 组件初始化失败: {e}")
    raise

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Stock Prediction API - Colab Version",
        "version": "1.0.0-colab",
        "status": "running",
        "environment": "Google Colab"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy", 
        "timestamp": "2024-01-01T00:00:00Z",
        "environment": "Google Colab"
    }

@app.get("/api/gpt-status")
async def gpt_status():
    """GPT模型状态检查"""
    try:
        status = get_gpt_status()
        return {
            "gpt_available": status["available"],
            "model": status.get("model"),
            "temperature": status.get("temperature"),
            "api_key_configured": status.get("api_key_configured"),
            "reason": status.get("reason"),
            "environment": "Google Colab"
        }
    except Exception as e:
        return {
            "gpt_available": False,
            "error": str(e),
            "environment": "Google Colab"
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
            "support_resistance": support_resistance,
            "environment": "Google Colab"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock data: {str(e)}")

@app.post("/api/predict")
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

@app.get("/api/top-stocks")
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
    
    # 简单的股票搜索
    common_stocks = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", 
        "AMD", "CRM", "ORCL", "INTC", "CSCO", "ADBE", "PYPL", "UBER",
        "SPOT", "TWTR", "SNAP", "PINS", "SQ", "ROKU", "ZM", "DOCU"
    ]
    
    # 过滤匹配的股票
    matches = [stock for stock in common_stocks if query.upper() in stock]
    
    return {
        "query": query,
        "matches": matches[:10],  # 限制返回10个结果
        "environment": "Google Colab"
    }

def start_colab_server():
    """启动Colab服务器"""
    print("🚀 启动Google Colab股票预测系统...")
    print("📊 系统将在后台运行")
    print("🔗 使用以下命令访问API:")
    print("   - 根路径: http://localhost:8000")
    print("   - API文档: http://localhost:8000/docs")
    print("   - 健康检查: http://localhost:8000/health")
    
    # 启动服务器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    start_colab_server()

