import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Minus, Clock, AlertTriangle } from 'lucide-react';
import { PredictionResult } from '../lib/types';
import { stockAPI } from '../lib/api';
import { formatCurrency, formatPercentage, getDirectionColor, getConfidenceColor } from '../lib/utils';

interface PredictPanelProps {
  symbol: string;
  currentPrice?: number;
}

export const PredictPanel: React.FC<PredictPanelProps> = ({ symbol, currentPrice }) => {
  const [predictions, setPredictions] = useState<Record<string, PredictionResult | null>>({
    '1h': null,
    '1d': null,
    '1w': null,
  });
  const [loading, setLoading] = useState<Record<string, boolean>>({
    '1h': false,
    '1d': false,
    '1w': false,
  });
  const [error, setError] = useState<string | null>(null);

  const timeframes = [
    { key: '1h', label: '下一小时', icon: Clock },
    { key: '1d', label: '下一天', icon: TrendingUp },
    { key: '1w', label: '下一周', icon: TrendingUp },
  ];

  const handlePredict = async (timeframe: string) => {
    setLoading(prev => ({ ...prev, [timeframe]: true }));
    setError(null);

    try {
      const result = await stockAPI.predictStock({
        symbol,
        timeframe,
        current_price: currentPrice,
      });
      
      setPredictions(prev => ({ ...prev, [timeframe]: result }));
    } catch (err: any) {
      setError(err.response?.data?.detail || '预测失败，请稍后重试');
    } finally {
      setLoading(prev => ({ ...prev, [timeframe]: false }));
    }
  };

  const getDirectionIcon = (direction: string) => {
    switch (direction.toLowerCase()) {
      case 'up':
        return <TrendingUp className="h-5 w-5 text-green-600" />;
      case 'down':
        return <TrendingDown className="h-5 w-5 text-red-600" />;
      default:
        return <Minus className="h-5 w-5 text-gray-600" />;
    }
  };

  const getDirectionText = (direction: string) => {
    switch (direction.toLowerCase()) {
      case 'up':
        return '上涨';
      case 'down':
        return '下跌';
      default:
        return '横盘';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">AI 预测分析</h3>
        <div className="text-sm text-gray-500">
          基于 LangGraph 工作流
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="h-5 w-5 text-red-600 mr-2" />
            <span className="text-red-800">{error}</span>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {timeframes.map(({ key, label, icon: Icon }) => {
          const prediction = predictions[key];
          const isLoading = loading[key];

          return (
            <div key={key} className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <Icon className="h-5 w-5 text-gray-600 mr-2" />
                  <span className="font-medium text-gray-900">{label}</span>
                </div>
                <button
                  onClick={() => handlePredict(key)}
                  disabled={isLoading}
                  className="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? '预测中...' : '预测'}
                </button>
              </div>

              {prediction ? (
                <div className="space-y-3">
                  {/* 预测结果 */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      {getDirectionIcon(prediction.direction)}
                      <span className="ml-2 font-medium">
                        {getDirectionText(prediction.direction)}
                      </span>
                    </div>
                    <div className={`font-bold ${getDirectionColor(prediction.direction)}`}>
                      {formatPercentage(prediction.probability)}
                    </div>
                  </div>

                  {/* 价格区间 */}
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600 mb-1">预期价格区间</div>
                    <div className="flex justify-between text-sm">
                      <span className="text-red-600">
                        最低: {formatCurrency(prediction.price_range.min)}
                      </span>
                      <span className="text-green-600">
                        最高: {formatCurrency(prediction.price_range.max)}
                      </span>
                    </div>
                  </div>

                  {/* 置信度 */}
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">置信度</span>
                    <span className={`text-sm font-medium ${getConfidenceColor(prediction.confidence)}`}>
                      {prediction.confidence === 'high' ? '高' : 
                       prediction.confidence === 'medium' ? '中' : '低'}
                    </span>
                  </div>

                  {/* 分析理由 */}
                  <div className="bg-blue-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600 mb-1">分析理由</div>
                    <p className="text-sm text-gray-800">{prediction.reasoning}</p>
                  </div>

                  {/* 风险提示 */}
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                    <div className="flex items-start">
                      <AlertTriangle className="h-4 w-4 text-yellow-600 mr-2 mt-0.5 flex-shrink-0" />
                      <p className="text-xs text-yellow-800">{prediction.risk_warning}</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="text-gray-400 mb-2">
                    <Icon className="h-8 w-8 mx-auto" />
                  </div>
                  <p className="text-sm text-gray-500">
                    {isLoading ? '正在分析...' : '点击预测按钮开始分析'}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* 免责声明 */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="flex items-start">
          <AlertTriangle className="h-5 w-5 text-gray-600 mr-2 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-gray-700">
            <p className="font-medium mb-1">重要声明</p>
            <p>
              本预测系统仅用于学习研究目的，所有分析结果不构成投资建议。股票投资存在风险，
              过往表现不代表未来收益。请根据自身风险承受能力谨慎投资，并咨询专业投资顾问。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
