from typing import Dict, Any
import random
from ...core.state import WorkflowState


class MakeAdviceNode:
    """生成建议节点"""
    
    def __call__(self, state: WorkflowState) -> Dict[str, Any]:
        """生成投资建议"""
        try:
            if state.llm_analysis is None:
                return {
                    "error": "No LLM analysis available for advice generation",
                    "advice": None
                }
            
            analysis = state.llm_analysis
            
            # 基于分析结果生成建议
            direction = analysis.get("direction", "neutral")
            probability = analysis.get("probability", 50)
            price_change = analysis.get("price_change_percent", 0)
            reasoning = analysis.get("reasoning", "技术分析显示中性信号")
            confidence = analysis.get("confidence", "medium")
            
            # 计算价格区间
            current_price = state.processed_data['close'].iloc[-1] if not state.processed_data.empty else 100
            price_change_decimal = price_change / 100
            
            if direction == "up":
                min_price = current_price * (1 + price_change_decimal * 0.5)
                max_price = current_price * (1 + price_change_decimal * 1.5)
            elif direction == "down":
                min_price = current_price * (1 + price_change_decimal * 1.5)
                max_price = current_price * (1 + price_change_decimal * 0.5)
            else:
                min_price = current_price * (1 + price_change_decimal * 0.8)
                max_price = current_price * (1 + price_change_decimal * 1.2)
            
            # 生成风险提示
            risk_factors = analysis.get("risk_factors", [])
            risk_warning = self._generate_risk_warning(direction, probability, risk_factors)
            
            advice = {
                "direction": direction,
                "probability": probability,
                "price_range": {
                    "min": round(min_price, 2),
                    "max": round(max_price, 2)
                },
                "confidence": confidence,
                "reasoning": reasoning,
                "risk_warning": risk_warning,
                "recommended_action": self._get_recommended_action(direction, probability, confidence)
            }
            
            return {
                "advice": advice,
                "error": None
            }
            
        except Exception as e:
            return {
                "error": f"Advice generation failed: {str(e)}",
                "advice": None
            }
    
    def _generate_risk_warning(self, direction: str, probability: float, risk_factors: list) -> str:
        """生成风险提示"""
        base_warning = "本预测仅用于学习研究目的，不构成投资建议。投资有风险，入市需谨慎。"
        
        if probability < 60:
            base_warning += " 预测概率较低，建议谨慎操作。"
        
        if direction == "down":
            base_warning += " 预测显示下跌趋势，请注意风险控制。"
        elif direction == "up":
            base_warning += " 预测显示上涨趋势，但仍需关注市场变化。"
        
        if risk_factors:
            base_warning += f" 主要风险因素：{', '.join(risk_factors[:3])}。"
        
        return base_warning
    
    def _get_recommended_action(self, direction: str, probability: float, confidence: str) -> str:
        """获取推荐操作"""
        if confidence == "low" or probability < 55:
            return "建议观望，等待更多信号确认"
        elif direction == "up" and probability >= 65:
            return "可考虑适量买入，设置止损位"
        elif direction == "down" and probability >= 65:
            return "建议减仓或观望，避免追高"
        else:
            return "保持现有仓位，密切关注市场变化"
