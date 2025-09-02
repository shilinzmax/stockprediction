#!/usr/bin/env python3
"""
GPT API测试脚本
用于测试GPT模型是否正常工作
"""

import asyncio
import requests
import json
from core.llm_manager import get_llm_analyzer, get_gpt_status
from core.state import PredictionRequest

def test_gpt_status():
    """测试GPT状态"""
    print("🔍 检查GPT状态...")
    status = get_gpt_status()
    
    print(f"GPT可用: {status['available']}")
    if status['available']:
        print(f"模型: {status.get('model', 'Unknown')}")
        print(f"温度: {status.get('temperature', 'Unknown')}")
        print(f"API密钥已配置: {status.get('api_key_configured', False)}")
    else:
        print(f"原因: {status.get('reason', 'Unknown')}")
    
    return status['available']

def test_llm_analyzer():
    """测试LLM分析器"""
    print("\n🧠 测试LLM分析器...")
    
    try:
        llm_analyzer = get_llm_analyzer()
        
        # 测试简单的分析
        test_data = {
            "symbol": "AAPL",
            "current_price": 150.0,
            "indicators": {
                "rsi": 45,
                "macd": 0.5,
                "sma_20": 148.0,
                "sma_50": 145.0
            }
        }
        
        print("发送测试数据到GPT...")
        result = llm_analyzer.analyze_stock_data(test_data)
        
        if result and not result.get("error"):
            print("✅ GPT分析成功!")
            print(f"方向: {result.get('direction', 'Unknown')}")
            print(f"概率: {result.get('probability', 'Unknown')}")
            print(f"推理: {result.get('reasoning', 'No reasoning provided')[:100]}...")
            return True
        else:
            print(f"❌ GPT分析失败: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ LLM分析器测试失败: {str(e)}")
        return False

async def test_prediction_pipeline():
    """测试预测管道"""
    print("\n🔮 测试预测管道...")
    
    try:
        from graph.pipeline import StockPredictionPipeline
        pipeline = StockPredictionPipeline()
        
        # 创建测试请求
        request = PredictionRequest(
            symbol="AAPL",
            timeframe="1d"
        )
        
        print("运行预测管道...")
        result = await pipeline.predict(request.symbol, request.timeframe)
        
        if result and not result.get("error"):
            print("✅ 预测管道成功!")
            print(f"方向: {result.get('direction', 'Unknown')}")
            print(f"概率: {result.get('probability', 'Unknown')}")
            print(f"价格范围: {result.get('price_range', 'Unknown')}")
            return True
        else:
            print(f"❌ 预测管道失败: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 预测管道测试失败: {str(e)}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🌐 测试API端点...")
    
    base_url = "http://localhost:8000"
    
    # 测试GPT状态端点
    try:
        response = requests.get(f"{base_url}/api/gpt-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ GPT状态端点正常")
            print(f"GPT可用: {data.get('gpt_available', False)}")
            return True
        else:
            print(f"❌ GPT状态端点失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到API服务器: {str(e)}")
        print("请确保服务器正在运行: python app.py")
        return False

async def main():
    """主测试函数"""
    print("🚀 开始GPT API测试...\n")
    
    # 测试1: GPT状态
    gpt_available = test_gpt_status()
    
    if not gpt_available:
        print("\n❌ GPT不可用，请检查配置:")
        print("1. 确保在.env文件中设置了OPENAI_API_KEY")
        print("2. 确保API密钥有效且有余额")
        print("3. 检查网络连接")
        return
    
    # 测试2: LLM分析器
    llm_works = test_llm_analyzer()
    
    # 测试3: 预测管道
    pipeline_works = await test_prediction_pipeline()
    
    # 测试4: API端点
    api_works = test_api_endpoints()
    
    # 总结
    print("\n📊 测试结果总结:")
    print(f"GPT状态: {'✅' if gpt_available else '❌'}")
    print(f"LLM分析器: {'✅' if llm_works else '❌'}")
    print(f"预测管道: {'✅' if pipeline_works else '❌'}")
    print(f"API端点: {'✅' if api_works else '❌'}")
    
    if all([gpt_available, llm_works, pipeline_works, api_works]):
        print("\n🎉 所有测试通过! GPT API工作正常!")
    else:
        print("\n⚠️ 部分测试失败，请检查配置和日志")

if __name__ == "__main__":
    asyncio.run(main())
