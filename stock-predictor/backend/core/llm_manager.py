"""
LLM管理器 - 全局单例模式管理GPT模型
"""
import os
from typing import Optional
from dotenv import load_dotenv
from .llm import OpenAILLM, OllamaLLM, MockLLM, get_llm_analyzer

# 加载环境变量
load_dotenv()


class LLMManager:
    """LLM管理器 - 单例模式"""
    
    _instance = None
    _llm_analyzer = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """初始化LLM分析器"""
        if self._llm_analyzer is None:
            print("🚀 初始化全局LLM管理器...")
            self._llm_analyzer = get_llm_analyzer()
            print("✅ 全局LLM管理器初始化完成")
    
    def get_llm_analyzer(self):
        """获取LLM分析器实例"""
        return self._llm_analyzer
    
    def is_llm_available(self) -> bool:
        """检查LLM是否可用"""
        if self._llm_analyzer is None:
            return False
        
        # 根据LLM类型检查可用性
        if isinstance(self._llm_analyzer, OpenAILLM):
            return self._llm_analyzer.llm is not None
        elif isinstance(self._llm_analyzer, OllamaLLM):
            return self._llm_analyzer.llm is not None
        elif isinstance(self._llm_analyzer, MockLLM):
            return True
        
        return False
    
    def get_llm_status(self) -> dict:
        """获取LLM状态信息"""
        if self._llm_analyzer is None:
            return {
                "available": False,
                "reason": "LLM分析器未初始化",
                "type": "unknown"
            }
        
        llm_type = type(self._llm_analyzer).__name__
        
        if isinstance(self._llm_analyzer, OpenAILLM):
            if not self._llm_analyzer.api_key:
                return {
                    "available": False,
                    "reason": "未配置OpenAI API密钥",
                    "type": "openai"
                }
            
            if not self._llm_analyzer.llm:
                return {
                    "available": False,
                    "reason": "GPT模型初始化失败",
                    "type": "openai"
                }
            
            return {
                "available": True,
                "type": "openai",
                "model": self._llm_analyzer.llm.model_name,
                "temperature": self._llm_analyzer.llm.temperature,
                "api_key_configured": bool(self._llm_analyzer.api_key)
            }
        
        elif isinstance(self._llm_analyzer, OllamaLLM):
            if not self._llm_analyzer.llm:
                return {
                    "available": False,
                    "reason": "Ollama模型初始化失败",
                    "type": "ollama"
                }
            
            return {
                "available": True,
                "type": "ollama",
                "model": self._llm_analyzer.model_name,
                "api_key_configured": False
            }
        
        elif isinstance(self._llm_analyzer, MockLLM):
            return {
                "available": True,
                "type": "mock",
                "model": "Mock LLM",
                "api_key_configured": False
            }
        
        return {
            "available": False,
            "reason": "未知的LLM类型",
            "type": llm_type
        }


# 全局LLM管理器实例
llm_manager = LLMManager()

# 便捷函数
def get_llm_analyzer():
    """获取LLM分析器实例"""
    return llm_manager.get_llm_analyzer()

def is_llm_available() -> bool:
    """检查LLM是否可用"""
    return llm_manager.is_llm_available()

def get_llm_status() -> dict:
    """获取LLM状态信息"""
    return llm_manager.get_llm_status()

# 向后兼容的函数
def is_gpt_available() -> bool:
    """检查GPT是否可用（向后兼容）"""
    return llm_manager.is_llm_available()

def get_gpt_status() -> dict:
    """获取GPT状态信息（向后兼容）"""
    return llm_manager.get_llm_status()
