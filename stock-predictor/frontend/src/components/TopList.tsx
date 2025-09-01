import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Minus, RefreshCw, AlertTriangle } from 'lucide-react';
import { TopStocksResponse, StockAdvice } from '../lib/types';
import { stockAPI } from '../lib/api';
import { formatPercentage, getDirectionColor, getRiskLevelColor, formatDateTime } from '../lib/utils';

export const TopList: React.FC = () => {
  const [topStocks, setTopStocks] = useState<TopStocksResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTopStocks = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await stockAPI.getTopStocks();
      setTopStocks(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || '获取推荐股票失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTopStocks();
  }, []);

  const getDirectionIcon = (direction: string) => {
    switch (direction.toLowerCase()) {
      case 'up':
        return <TrendingUp className="h-4 w-4 text-green-600" />;
      case 'down':
        return <TrendingDown className="h-4 w-4 text-red-600" />;
      default:
        return <Minus className="h-4 w-4 text-gray-600" />;
    }
  };

  const getDirectionText = (direction: string) => {
    switch (direction.toLowerCase()) {
      case 'up':
        return '看涨';
      case 'down':
        return '看跌';
      default:
        return '中性';
    }
  };

  const getRiskLevelText = (riskLevel: string) => {
    switch (riskLevel.toLowerCase()) {
      case 'low':
        return '低风险';
      case 'medium':
        return '中风险';
      case 'high':
        return '高风险';
      default:
        return '未知';
    }
  };

  if (loading && !topStocks) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <RefreshCw className="h-8 w-8 text-blue-600 animate-spin mx-auto mb-4" />
            <p className="text-gray-600">正在生成股票推荐...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">本周推荐股票 Top 10</h3>
          <p className="text-sm text-gray-600">基于 AI 分析的投资建议</p>
        </div>
        <button
          onClick={fetchTopStocks}
          disabled={loading}
          className="flex items-center px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          刷新
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="h-5 w-5 text-red-600 mr-2" />
            <span className="text-red-800">{error}</span>
          </div>
        </div>
      )}

      {topStocks && (
        <>
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      排名
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      股票代码
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      公司名称
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      预期方向
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      概率
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      预期收益
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      风险等级
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      推荐理由
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {topStocks.stocks.map((stock, index) => (
                    <tr key={stock.symbol} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{index + 1}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {stock.symbol}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {stock.name || stock.symbol}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          {getDirectionIcon(stock.direction)}
                          <span className={`ml-2 text-sm font-medium ${getDirectionColor(stock.direction)}`}>
                            {getDirectionText(stock.direction)}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {formatPercentage(stock.probability)}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className={`text-sm font-medium ${
                          stock.expected_return.startsWith('+') ? 'text-green-600' : 
                          stock.expected_return.startsWith('-') ? 'text-red-600' : 'text-gray-600'
                        }`}>
                          {stock.expected_return}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          stock.risk_level === 'low' ? 'bg-green-100 text-green-800' :
                          stock.risk_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {getRiskLevelText(stock.risk_level)}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-600 max-w-xs truncate">
                          {stock.reasoning}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* 生成时间和免责声明 */}
          <div className="space-y-4">
            <div className="text-sm text-gray-500 text-center">
              生成时间: {formatDateTime(topStocks.generated_at)}
            </div>
            
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-start">
                <AlertTriangle className="h-5 w-5 text-yellow-600 mr-2 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-yellow-800">
                  <p className="font-medium mb-1">重要声明</p>
                  <p>{topStocks.disclaimer}</p>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
