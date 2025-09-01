from typing import Dict, Any
from datetime import datetime
from ...core.state import WorkflowState


class ReportNode:
    """报告生成节点"""
    
    def __call__(self, state: WorkflowState) -> Dict[str, Any]:
        """生成最终报告"""
        try:
            if state.advice is None:
                return {
                    "error": "No advice available for report generation",
                    "prediction": None
                }
            
            advice = state.advice
            
            # 生成最终预测结果
            prediction = {
                "symbol": state.symbol.upper(),
                "timeframe": state.timeframe,
                "direction": advice["direction"],
                "probability": advice["probability"],
                "price_range": advice["price_range"],
                "confidence": advice["confidence"],
                "reasoning": advice["reasoning"],
                "risk_warning": advice["risk_warning"],
                "recommended_action": advice["recommended_action"],
                "generated_at": datetime.now().isoformat(),
                "analysis_summary": self._generate_analysis_summary(state)
            }
            
            return {
                "prediction": prediction,
                "error": None
            }
            
        except Exception as e:
            return {
                "error": f"Report generation failed: {str(e)}",
                "prediction": None
            }
    
    def _generate_analysis_summary(self, state: WorkflowState) -> str:
        """生成分析摘要"""
        summary_parts = []
        
        # 技术指标摘要
        if state.signal_strength:
            strength = state.signal_strength.get("strength", "neutral")
            score = state.signal_strength.get("score", 0)
            signals = state.signal_strength.get("signals", [])
            
            if strength != "neutral":
                summary_parts.append(f"技术信号强度：{strength} (得分: {score})")
            
            if signals:
                summary_parts.append(f"主要信号：{', '.join(signals[:3])}")
        
        # 价格位置摘要
        if state.support_resistance:
            support = state.support_resistance.get("support", 0)
            resistance = state.support_resistance.get("resistance", 0)
            current_price = state.processed_data['close'].iloc[-1] if not state.processed_data.empty else 0
            
            if support > 0 and resistance > 0:
                if current_price < support * 1.02:
                    summary_parts.append("价格接近支撑位")
                elif current_price > resistance * 0.98:
                    summary_parts.append("价格接近阻力位")
                else:
                    summary_parts.append("价格处于支撑阻力区间中部")
        
        # 成交量摘要
        if state.features:
            volume_ratio = state.features.get("volume_ratio", 1)
            if volume_ratio > 1.5:
                summary_parts.append("成交量放大")
            elif volume_ratio < 0.7:
                summary_parts.append("成交量萎缩")
        
        return "；".join(summary_parts) if summary_parts else "技术分析显示中性信号"
