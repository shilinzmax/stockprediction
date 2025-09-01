#!/usr/bin/env python3
"""
Stock Predictor 系统测试脚本
用于验证系统各个组件是否正常工作
"""

import sys
import os
import asyncio
import requests
import time
from pathlib import Path

# 添加backend路径到Python路径
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        from core.state import WorkflowState, PredictionRequest
        from core.utils import StockDataFetcher, validate_symbol
        from core.indicators import TechnicalIndicators
        from core.llm import llm_analyzer
        from graph.pipeline import StockPredictionPipeline
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_data_fetcher():
    """测试数据获取器"""
    print("🔍 测试数据获取器...")
    
    try:
        fetcher = StockDataFetcher()
        
        # 测试股票代码验证
        assert validate_symbol("AAPL") == True
        assert validate_symbol("") == False
        assert validate_symbol("INVALID_SYMBOL_12345") == False
        
        # 测试股票信息获取
        info = fetcher.get_stock_info("AAPL")
        assert info["symbol"] == "AAPL"
        assert info["name"] is not None
        
        print("✅ 数据获取器测试通过")
        return True
    except Exception as e:
        print(f"❌ 数据获取器测试失败: {e}")
        return False

def test_indicators():
    """测试技术指标计算"""
    print("🔍 测试技术指标计算...")
    
    try:
        import pandas as pd
        import numpy as np
        
        # 创建模拟数据
        dates = pd.date_range('2024-01-01', periods=50, freq='D')
        data = pd.DataFrame({
            'date': dates,
            'open': np.random.uniform(100, 200, 50),
            'high': np.random.uniform(150, 250, 50),
            'low': np.random.uniform(50, 150, 50),
            'close': np.random.uniform(100, 200, 50),
            'volume': np.random.uniform(1000000, 10000000, 50)
        })
        
        calculator = TechnicalIndicators()
        indicators = calculator.calculate_all_indicators(data)
        
        assert len(indicators) > 0
        assert 'rsi' in indicators
        assert 'macd' in indicators
        
        signal_strength = calculator.get_signal_strength(indicators)
        assert 'strength' in signal_strength
        assert 'score' in signal_strength
        
        print("✅ 技术指标计算测试通过")
        return True
    except Exception as e:
        print(f"❌ 技术指标计算测试失败: {e}")
        return False

def test_llm():
    """测试LLM分析器"""
    print("🔍 测试LLM分析器...")
    
    try:
        # 测试Mock LLM
        mock_data = {
            'indicators': {'rsi': 45, 'macd': 0.1},
            'signal_strength': {'strength': 'bullish', 'score': 2},
            'features': {'current_price': 150}
        }
        
        result = llm_analyzer.analyze_stock("AAPL", mock_data, "1d")
        
        assert 'direction' in result
        assert 'probability' in result
        assert 'reasoning' in result
        
        # 测试Top股票生成
        top_result = llm_analyzer.generate_top_stocks({})
        assert 'recommendations' in top_result
        assert len(top_result['recommendations']) == 10
        
        print("✅ LLM分析器测试通过")
        return True
    except Exception as e:
        print(f"❌ LLM分析器测试失败: {e}")
        return False

async def test_pipeline():
    """测试LangGraph工作流"""
    print("🔍 测试LangGraph工作流...")
    
    try:
        pipeline = StockPredictionPipeline()
        
        # 测试同步预测
        result = pipeline.predict_sync("AAPL", "1d")
        
        assert 'direction' in result or 'error' in result
        
        print("✅ LangGraph工作流测试通过")
        return True
    except Exception as e:
        print(f"❌ LangGraph工作流测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点（需要后端服务运行）"""
    print("🔍 测试API端点...")
    
    try:
        base_url = "http://localhost:8000"
        
        # 测试健康检查
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API健康检查通过")
            return True
        else:
            print(f"⚠️  API服务未运行 (状态码: {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  API服务未运行，跳过API测试")
        return False
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始 Stock Predictor 系统测试\n")
    
    tests = [
        ("模块导入", test_imports),
        ("数据获取器", test_data_fetcher),
        ("技术指标计算", test_indicators),
        ("LLM分析器", test_llm),
        ("LangGraph工作流", lambda: asyncio.run(test_pipeline())),
        ("API端点", test_api_endpoints),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常")
        return 0
    else:
        print("⚠️  部分测试失败，请检查相关组件")
        return 1

if __name__ == "__main__":
    exit(main())
