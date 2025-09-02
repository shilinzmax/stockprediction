import os
import json
import random
from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd
import openai
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import ollama

# 加载环境变量
load_dotenv()


class MockLLM:
    """Mock LLM for testing without OpenAI API key"""
    
    def __init__(self):
        self.responses = {
            "bullish": [
                "基于技术分析，该股票显示出强劲的上升趋势。RSI指标显示超卖后反弹，MACD出现金叉信号，成交量放大，预计短期内将继续上涨。",
                "从基本面和技术面分析，该股票具有良好的上涨潜力。移动平均线呈多头排列，布林带收窄后突破上轨，建议关注。",
                "技术指标显示该股票处于上升通道中，支撑位稳固，阻力位有望突破。成交量配合良好，上涨概率较高。"
            ],
            "bearish": [
                "技术分析显示该股票面临下行压力。RSI指标超买，MACD出现死叉，成交量萎缩，预计短期内可能回调。",
                "从技术面看，该股票已接近阻力位，移动平均线开始走平，布林带收窄，短期内上涨空间有限。",
                "技术指标显示该股票可能面临调整。支撑位较弱，成交量不足，建议谨慎操作。"
            ],
            "neutral": [
                "技术分析显示该股票处于横盘整理状态。各项指标相对中性，短期内可能维持震荡走势。",
                "从技术面看，该股票缺乏明确方向性信号。多空力量相对均衡，建议观望等待突破。",
                "技术指标显示该股票处于关键位置，需要更多信号确认方向。建议关注后续走势。"
            ]
        }
    
    def analyze_stock(self, symbol: str, data: Dict[str, Any], timeframe: str) -> Dict[str, Any]:
        """分析股票并返回预测结果"""
        # 基于技术指标生成模拟分析
        indicators = data.get('indicators', {})
        signal_strength = data.get('signal_strength', {})
        
        # 根据信号强度确定方向
        strength = signal_strength.get('strength', 'neutral')
        
        if 'bullish' in strength:
            direction = 'up'
            probability = random.uniform(60, 85)
            price_change = random.uniform(2, 8)
        elif 'bearish' in strength:
            direction = 'down'
            probability = random.uniform(60, 85)
            price_change = random.uniform(-8, -2)
        else:
            direction = 'neutral'
            probability = random.uniform(45, 55)
            price_change = random.uniform(-2, 2)
        
        # 选择对应的分析文本
        analysis_text = random.choice(self.responses.get(direction, self.responses['neutral']))
        
        return {
            "direction": direction,
            "probability": round(probability, 1),
            "price_change_percent": round(price_change, 1),
            "reasoning": analysis_text,
            "confidence": "medium",
            "risk_factors": [
                "市场波动性较高",
                "技术指标可能存在滞后性",
                "基本面因素未考虑在内"
            ]
        }
    
    def generate_top_stocks(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成Top 10股票建议"""
        # 模拟的股票列表
        mock_stocks = [
            {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology"},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Discretionary"},
            {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology"},
            {"symbol": "META", "name": "Meta Platforms Inc.", "sector": "Technology"},
            {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services"},
            {"symbol": "AMD", "name": "Advanced Micro Devices", "sector": "Technology"},
            {"symbol": "CRM", "name": "Salesforce Inc.", "sector": "Technology"}
        ]
        
        recommendations = []
        for stock in mock_stocks:
            direction = random.choice(['up', 'down', 'neutral'])
            probability = random.uniform(55, 80)
            
            if direction == 'up':
                reasoning = f"{stock['name']}在{stock['sector']}领域具有强劲的基本面和技术面支撑，预计短期内表现良好。"
                risk_level = "medium"
                expected_return = f"+{random.uniform(3, 12):.1f}%"
            elif direction == 'down':
                reasoning = f"{stock['name']}面临一些挑战，技术指标显示可能回调，建议谨慎。"
                risk_level = "high"
                expected_return = f"{random.uniform(-8, -2):.1f}%"
            else:
                reasoning = f"{stock['name']}处于横盘整理状态，需要更多信号确认方向。"
                risk_level = "low"
                expected_return = f"{random.uniform(-2, 3):.1f}%"
            
            recommendations.append({
                "symbol": stock['symbol'],
                "name": stock['name'],
                "direction": direction,
                "probability": round(probability, 1),
                "reasoning": reasoning,
                "risk_level": risk_level,
                "expected_return": expected_return
            })
        
        return {
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat(),
            "disclaimer": "本建议仅用于学习研究目的，不构成投资建议。投资有风险，入市需谨慎。"
        }


class OllamaLLM:
    """Ollama 本地 LLM 分析器"""
    
    def __init__(self, model_name: str = "qwen2.5:7b"):
        self.model_name = model_name
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """初始化Ollama LLM实例"""
        try:
            # 检查模型是否可用
            models = ollama.list()
            available_models = [model.model for model in models.models]
            
            if self.model_name not in available_models:
                print(f"❌ 模型 {self.model_name} 未找到，可用模型: {available_models}")
                self.llm = None
                return
            
            # 测试连接
            test_response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': 'Hello'}]
            )
            
            self.llm = True  # 标记为可用
            print(f"✅ Ollama模型初始化成功: {self.model_name}")
            
        except Exception as e:
            print(f"❌ Ollama模型初始化失败: {str(e)}")
            self.llm = None
    
    def _check_and_reinitialize(self):
        """检查并重新初始化LLM"""
        if not self.llm:
            print("🔄 重新初始化Ollama模型...")
            self._initialize_llm()
    
    def analyze_stock(self, symbol: str, data: Dict[str, Any], timeframe: str) -> Dict[str, Any]:
        """使用 Ollama 分析股票"""
        # 检查并重新初始化LLM
        self._check_and_reinitialize()
        
        if not self.llm:
            return {
                "error": "Ollama model not available",
                "direction": None,
                "probability": None,
                "price_change_percent": None,
                "reasoning": None,
                "confidence": None
            }
        
        try:
            # 构建分析提示
            indicators_summary = self._format_indicators(data.get('indicators', {}))
            signal_info = data.get('signal_strength', {})
            
            prompt = f"""
作为专业的股票分析师，请基于以下技术指标数据对股票 {symbol} 进行 {timeframe} 时间框架的分析：

技术指标摘要：
{indicators_summary}

信号强度：{signal_info.get('strength', 'neutral')}
信号得分：{signal_info.get('score', 0)}

请以JSON格式返回分析结果，包含以下字段：
- direction: "up", "down", 或 "neutral"
- probability: 0-100之间的数字，表示预测准确性的概率
- price_change_percent: 预期价格变化百分比
- reasoning: 详细的分析理由（中文）
- confidence: "high", "medium", 或 "low"
- risk_factors: 风险因素列表

注意：请保持客观和谨慎，考虑市场风险。
"""
            
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': '你是一个专业的股票技术分析师，擅长基于技术指标进行股票走势预测。'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            
            # 解析响应
            try:
                result = json.loads(response['message']['content'])
                return result
            except json.JSONDecodeError:
                # 如果解析失败，返回默认结果
                return {
                    "direction": "neutral",
                    "probability": 50.0,
                    "price_change_percent": 0.0,
                    "reasoning": "技术分析结果解析失败，建议谨慎操作。",
                    "confidence": "low",
                    "risk_factors": ["数据解析异常"]
                }
                
        except Exception as e:
            print(f"Ollama API error: {e}")
            return {
                "error": "Ollama model not available",
                "direction": None,
                "probability": None,
                "price_change_percent": None,
                "reasoning": None,
                "confidence": None
            }
    
    def generate_top_stocks(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成Top 10股票建议"""
        # 检查并重新初始化LLM
        self._check_and_reinitialize()
        
        if not self.llm:
            return {
                "error": "Ollama model not available",
                "recommendations": [],
                "generated_at": None,
                "disclaimer": None
            }
        
        try:
            prompt = f"""
作为专业的投资顾问，请基于当前市场情况推荐10只具有投资潜力的股票。

请以JSON格式返回推荐结果，包含以下字段：
- recommendations: 包含10个股票对象的数组，每个对象包含：
  - symbol: 股票代码
  - name: 公司名称
  - direction: "up", "down", 或 "neutral"
  - probability: 0-100之间的数字
  - reasoning: 推荐理由（中文）
  - risk_level: "low", "medium", 或 "high"
  - expected_return: 预期收益率（如"+5.2%"）
- generated_at: 生成时间
- disclaimer: 免责声明

注意：请选择知名的大盘股，并保持客观分析。
"""
            
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': '你是一个专业的投资顾问，擅长股票分析和投资建议。'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            
            try:
                result = json.loads(response['message']['content'])
                return result
            except json.JSONDecodeError:
                return {
                    "error": "Ollama model not available",
                    "recommendations": [],
                    "generated_at": None,
                    "disclaimer": None
                }
                
        except Exception as e:
            print(f"Ollama API error: {e}")
            return {
                "error": "Ollama model not available",
                "recommendations": [],
                "generated_at": None,
                "disclaimer": None
            }
    
    def _format_indicators(self, indicators: Dict[str, Any]) -> str:
        """格式化技术指标数据"""
        if not indicators:
            return "无技术指标数据"
        
        summary = []
        for key, value in indicators.items():
            if isinstance(value, (int, float)) and not pd.isna(value):
                summary.append(f"{key}: {value:.2f}")
            elif hasattr(value, 'iloc') and len(value) > 0:
                summary.append(f"{key}: {value.iloc[-1]:.2f}")
        
        return "\n".join(summary[:10])  # 限制显示前10个指标


class OpenAILLM:
    """OpenAI LLM 分析器"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """初始化LLM实例"""
        if self.api_key and not self.llm:
            try:
                openai.api_key = self.api_key
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.3,
                    max_tokens=1000
                )
                print(f"✅ GPT模型初始化成功: {self.llm.model_name}")
            except Exception as e:
                print(f"❌ GPT模型初始化失败: {str(e)}")
                self.llm = None
        elif not self.api_key:
            print("⚠️ 未配置OpenAI API密钥")
            self.llm = None
    
    def _check_and_reinitialize(self):
        """检查并重新初始化LLM"""
        if not self.llm and self.api_key:
            print("🔄 重新初始化GPT模型...")
            self._initialize_llm()
    
    def analyze_stock(self, symbol: str, data: Dict[str, Any], timeframe: str) -> Dict[str, Any]:
        """使用 OpenAI 分析股票"""
        # 检查并重新初始化LLM
        self._check_and_reinitialize()
        
        if not self.llm:
            # 如果没有 API key，返回错误
            return {
                "error": "GPT model not work, figure out how to fix it",
                "direction": None,
                "probability": None,
                "price_change_percent": None,
                "reasoning": None,
                "confidence": None
            }
        
        try:
            # 构建分析提示
            indicators_summary = self._format_indicators(data.get('indicators', {}))
            signal_info = data.get('signal_strength', {})
            
            prompt = f"""
            作为专业的股票分析师，请基于以下技术指标数据对股票 {symbol} 进行 {timeframe} 时间框架的分析：

            技术指标摘要：
            {indicators_summary}

            信号强度：{signal_info.get('strength', 'neutral')}
            信号得分：{signal_info.get('score', 0)}

            请以JSON格式返回分析结果，包含以下字段：
            - direction: "up", "down", 或 "neutral"
            - probability: 0-100之间的数字，表示预测准确性的概率
            - price_change_percent: 预期价格变化百分比
            - reasoning: 详细的分析理由（中文）
            - confidence: "high", "medium", 或 "low"
            - risk_factors: 风险因素列表

            注意：请保持客观和谨慎，考虑市场风险。
            """
            
            messages = [
                SystemMessage(content="你是一个专业的股票技术分析师，擅长基于技术指标进行股票走势预测。"),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm(messages)
            
            # 解析响应
            try:
                result = json.loads(response.content)
                return result
            except json.JSONDecodeError:
                # 如果解析失败，返回默认结果
                return {
                    "direction": "neutral",
                    "probability": 50.0,
                    "price_change_percent": 0.0,
                    "reasoning": "技术分析结果解析失败，建议谨慎操作。",
                    "confidence": "low",
                    "risk_factors": ["数据解析异常"]
                }
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # 出错时返回错误信息
            return {
                "error": "GPT model not work, figure out how to fix it",
                "direction": None,
                "probability": None,
                "price_change_percent": None,
                "reasoning": None,
                "confidence": None
            }
    
    def generate_top_stocks(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成Top 10股票建议"""
        # 检查并重新初始化LLM
        self._check_and_reinitialize()
        
        if not self.llm:
            return {
                "error": "GPT model not work, figure out how to fix it",
                "recommendations": [],
                "generated_at": None,
                "disclaimer": None
            }
        
        try:
            prompt = f"""
            作为专业的投资顾问，请基于当前市场情况推荐10只具有投资潜力的股票。

            请以JSON格式返回推荐结果，包含以下字段：
            - recommendations: 包含10个股票对象的数组，每个对象包含：
              - symbol: 股票代码
              - name: 公司名称
              - direction: "up", "down", 或 "neutral"
              - probability: 0-100之间的数字
              - reasoning: 推荐理由（中文）
              - risk_level: "low", "medium", 或 "high"
              - expected_return: 预期收益率（如"+5.2%"）
            - generated_at: 生成时间
            - disclaimer: 免责声明

            注意：请选择知名的大盘股，并保持客观分析。
            """
            
            messages = [
                SystemMessage(content="你是一个专业的投资顾问，擅长股票分析和投资建议。"),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm(messages)
            
            try:
                result = json.loads(response.content)
                return result
            except json.JSONDecodeError:
                return {
                    "error": "GPT model not work, figure out how to fix it",
                    "recommendations": [],
                    "generated_at": None,
                    "disclaimer": None
                }
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # 出错时返回错误信息
            return {
                "error": "GPT model not work, figure out how to fix it",
                "recommendations": [],
                "generated_at": None,
                "disclaimer": None
            }
    
    def _format_indicators(self, indicators: Dict[str, Any]) -> str:
        """格式化技术指标数据"""
        if not indicators:
            return "无技术指标数据"
        
        summary = []
        for key, value in indicators.items():
            if isinstance(value, (int, float)) and not pd.isna(value):
                summary.append(f"{key}: {value:.2f}")
            elif hasattr(value, 'iloc') and len(value) > 0:
                summary.append(f"{key}: {value.iloc[-1]:.2f}")
        
        return "\n".join(summary[:10])  # 限制显示前10个指标


# 全局 LLM 实例 - 根据环境变量选择模型
def get_llm_analyzer():
    """根据环境变量选择LLM分析器"""
    llm_type = os.getenv("LLM_TYPE", "openai").lower()
    
    if llm_type == "ollama":
        model_name = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        return OllamaLLM(model_name=model_name)
    elif llm_type == "mock":
        return MockLLM()
    else:
        return OpenAILLM()

# 全局 LLM 实例
llm_analyzer = get_llm_analyzer()
