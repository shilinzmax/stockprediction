from typing import Dict, Any
from core.state import WorkflowState
from core.llm_manager import get_llm_analyzer


class LLMAnalyzeNode:
    """LLM 分析节点"""
    
    def __init__(self):
        self.llm = get_llm_analyzer()
    
    def __call__(self, state: WorkflowState) -> Dict[str, Any]:
        """使用 LLM 分析股票"""
        try:
            if state.processed_data is None or state.indicators is None:
                return {
                    "error": "No processed data or indicators available for analysis",
                    "llm_analysis": None
                }
            
            # 准备分析数据
            analysis_data = {
                "indicators": state.indicators,
                "signal_strength": state.signal_strength,
                "features": state.features,
                "support_resistance": state.support_resistance,
                "current_price": state.processed_data['close'].iloc[-1] if not state.processed_data.empty else 0
            }
            
            # 使用 LLM 进行分析
            llm_result = self.llm.analyze_stock(
                symbol=state.symbol,
                data=analysis_data,
                timeframe=state.timeframe
            )
            
            # 检查LLM结果是否包含错误
            if llm_result.get("error"):
                return {
                    "llm_analysis": None,
                    "error": llm_result["error"]
                }
            
            return {
                "llm_analysis": llm_result,
                "error": None
            }
            
        except Exception as e:
            return {
                "error": f"LLM analysis failed: {str(e)}",
                "llm_analysis": None
            }
