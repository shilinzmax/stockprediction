from typing import Dict, Any
from langgraph.graph import StateGraph, END
from core.state import WorkflowState
from .nodes.fetch_data import FetchDataNode
from .nodes.feature_engineer import FeatureEngineerNode
from .nodes.llm_analyze import LLMAnalyzeNode
from .nodes.make_advice import MakeAdviceNode
from .nodes.report import ReportNode


class StockPredictionPipeline:
    """股票预测 LangGraph 工作流"""
    
    def __init__(self):
        # 初始化节点
        self.fetch_data_node = FetchDataNode()
        self.feature_engineer_node = FeatureEngineerNode()
        self.llm_analyze_node = LLMAnalyzeNode()
        self.make_advice_node = MakeAdviceNode()
        self.report_node = ReportNode()
        
        # 构建工作流图
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """构建 LangGraph 工作流"""
        workflow = StateGraph(WorkflowState)
        
        # 添加节点
        workflow.add_node("fetch_data", self.fetch_data_node)
        workflow.add_node("feature_engineer", self.feature_engineer_node)
        workflow.add_node("llm_analyze", self.llm_analyze_node)
        workflow.add_node("make_advice", self.make_advice_node)
        workflow.add_node("report", self.report_node)
        
        # 设置入口点
        workflow.set_entry_point("fetch_data")
        
        # 添加边
        workflow.add_edge("fetch_data", "feature_engineer")
        workflow.add_edge("feature_engineer", "llm_analyze")
        workflow.add_edge("llm_analyze", "make_advice")
        workflow.add_edge("make_advice", "report")
        workflow.add_edge("report", END)
        
        # 编译工作流
        return workflow.compile()
    
    async def predict(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """执行预测工作流"""
        try:
            # 创建初始状态
            initial_state = WorkflowState(
                symbol=symbol.upper(),
                timeframe=timeframe
            )
            
            # 执行工作流
            result = await self.workflow.ainvoke(initial_state)
            
            # 检查是否有错误
            if result.get("error"):
                return {"error": result["error"]}
            
            # 返回预测结果
            prediction = result.get("prediction")
            if prediction:
                return {
                    "direction": prediction["direction"],
                    "probability": prediction["probability"],
                    "price_range": prediction["price_range"],
                    "confidence": prediction["confidence"],
                    "reasoning": prediction["reasoning"],
                    "risk_warning": prediction["risk_warning"]
                }
            else:
                return {"error": "No prediction generated"}
                
        except Exception as e:
            return {"error": f"Workflow execution failed: {str(e)}"}
    
    def predict_sync(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """同步执行预测工作流"""
        try:
            # 创建初始状态
            initial_state = WorkflowState(
                symbol=symbol.upper(),
                timeframe=timeframe
            )
            
            # 执行工作流
            result = self.workflow.invoke(initial_state)
            
            # 检查是否有错误
            if result.get("error"):
                return {"error": result["error"]}
            
            # 返回预测结果
            prediction = result.get("prediction")
            if prediction:
                return {
                    "direction": prediction["direction"],
                    "probability": prediction["probability"],
                    "price_range": prediction["price_range"],
                    "confidence": prediction["confidence"],
                    "reasoning": prediction["reasoning"],
                    "risk_warning": prediction["risk_warning"]
                }
            else:
                return {"error": "No prediction generated"}
                
        except Exception as e:
            return {"error": f"Workflow execution failed: {str(e)}"}
