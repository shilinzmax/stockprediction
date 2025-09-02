#!/usr/bin/env python3
"""
测试Ollama本地模型集成
"""
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量使用Ollama
os.environ["LLM_TYPE"] = "ollama"
os.environ["OLLAMA_MODEL"] = "qwen2.5:7b"

# 加载环境变量
load_dotenv()

from core.llm_manager import get_llm_analyzer, get_llm_status

def test_ollama_integration():
    """测试Ollama集成"""
    print("🧪 测试Ollama本地模型集成...")
    
    # 获取LLM状态
    status = get_llm_status()
    print(f"📊 LLM状态: {status}")
    
    if not status["available"]:
        print(f"❌ LLM不可用: {status['reason']}")
        return False
    
    # 获取LLM分析器
    llm = get_llm_analyzer()
    print(f"✅ 成功获取LLM分析器: {type(llm).__name__}")
    
    # 测试股票分析
    print("\n🔍 测试股票分析...")
    test_data = {
        "indicators": {
            "rsi": 65.5,
            "macd": 0.25,
            "bb_upper": 150.0,
            "bb_lower": 140.0,
            "sma_20": 145.0
        },
        "signal_strength": {
            "strength": "bullish",
            "score": 75
        }
    }
    
    try:
        result = llm.analyze_stock("AAPL", test_data, "1天")
        print(f"📈 分析结果: {result}")
        
        if result.get("error"):
            print(f"❌ 分析失败: {result['error']}")
            return False
        else:
            print("✅ 股票分析测试成功")
            
    except Exception as e:
        print(f"❌ 分析异常: {str(e)}")
        return False
    
    # 测试Top股票推荐
    print("\n🏆 测试Top股票推荐...")
    try:
        result = llm.generate_top_stocks({})
        print(f"📊 推荐结果: {result}")
        
        if result.get("error"):
            print(f"❌ 推荐失败: {result['error']}")
            return False
        else:
            print("✅ Top股票推荐测试成功")
            
    except Exception as e:
        print(f"❌ 推荐异常: {str(e)}")
        return False
    
    print("\n🎉 所有测试通过！Ollama集成成功！")
    return True

if __name__ == "__main__":
    success = test_ollama_integration()
    sys.exit(0 if success else 1)

