import React, { useState, useEffect } from 'react';
import { TrendingUp, AlertTriangle, BarChart3 } from 'lucide-react';
import { SearchBar } from '../components/SearchBar';
import { PriceChart } from '../components/PriceChart';
import { PredictPanel } from '../components/PredictPanel';
import { TopList } from '../components/TopList';
import { StockData } from '../lib/types';
import { stockAPI } from '../lib/api';
import { formatCurrency, formatPercentage } from '../lib/utils';

export const Dashboard: React.FC = () => {
  const [selectedSymbol, setSelectedSymbol] = useState<string>('AAPL');
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStockData = async (symbol: string) => {
    setLoading(true);
    setError(null);

    try {
      const data = await stockAPI.getStockData(symbol);
      setStockData(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || '获取股票数据失败，请稍后重试');
      setStockData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedSymbol) {
      fetchStockData(selectedSymbol);
    }
  }, [selectedSymbol]);

  const handleStockSelect = (symbol: string) => {
    setSelectedSymbol(symbol);
  };

  const getPriceChangeColor = (change: number) => {
    if (change > 0) return 'text-green-600';
    if (change < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  const getPriceChangeBgColor = (change: number) => {
    if (change > 0) return 'bg-green-100';
    if (change < 0) return 'bg-red-100';
    return 'bg-gray-100';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 头部 */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-xl font-bold text-gray-900">Stock Predictor</h1>
              <span className="ml-3 text-sm text-gray-500">AI驱动的股票预测系统</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                基于 LangGraph + OpenAI
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 搜索区域 */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">股票搜索</h2>
              <div className="text-sm text-gray-500">
                支持股票代码搜索，如 AAPL, MSFT, TSLA
              </div>
            </div>
            <SearchBar onStockSelect={handleStockSelect} />
          </div>
        </div>

        {/* 主要内容区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 左侧：股票信息和图表 */}
          <div className="lg:col-span-2 space-y-6">
            {/* 股票基本信息 */}
            {stockData && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">
                      {stockData.info.name} ({stockData.info.symbol})
                    </h2>
                    <p className="text-sm text-gray-600">
                      {stockData.info.sector} • {stockData.info.industry}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-gray-900">
                      {formatCurrency(stockData.info.current_price, stockData.info.currency)}
                    </div>
                    <div className="text-sm text-gray-500">
                      市值: {formatCurrency(stockData.info.market_cap, stockData.info.currency)}
                    </div>
                  </div>
                </div>

                {/* 技术指标摘要 */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">RSI</div>
                    <div className="text-lg font-semibold">
                      {stockData.indicators.rsi?.toFixed(1) || 'N/A'}
                    </div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">MACD</div>
                    <div className="text-lg font-semibold">
                      {stockData.indicators.macd?.toFixed(3) || 'N/A'}
                    </div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">信号强度</div>
                    <div className="text-lg font-semibold">
                      {stockData.signal_strength.strength || 'neutral'}
                    </div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">信号得分</div>
                    <div className="text-lg font-semibold">
                      {stockData.signal_strength.score || 0}
                    </div>
                  </div>
                </div>

                {/* 支撑阻力位 */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-green-50 rounded-lg p-3">
                    <div className="text-sm text-green-600">支撑位</div>
                    <div className="text-lg font-semibold text-green-800">
                      {formatCurrency(stockData.support_resistance.support, stockData.info.currency)}
                    </div>
                  </div>
                  <div className="bg-red-50 rounded-lg p-3">
                    <div className="text-sm text-red-600">阻力位</div>
                    <div className="text-lg font-semibold text-red-800">
                      {formatCurrency(stockData.support_resistance.resistance, stockData.info.currency)}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 价格图表 */}
            {stockData && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <PriceChart 
                  data={stockData.data} 
                  supportResistance={stockData.support_resistance}
                />
              </div>
            )}

            {/* 错误状态 */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                <div className="flex items-center">
                  <AlertTriangle className="h-6 w-6 text-red-600 mr-3" />
                  <div>
                    <h3 className="text-lg font-medium text-red-800">获取数据失败</h3>
                    <p className="text-red-700">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {/* 加载状态 */}
            {loading && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">正在加载股票数据...</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* 右侧：预测面板 */}
          <div className="space-y-6">
            {stockData && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <PredictPanel 
                  symbol={stockData.symbol} 
                  currentPrice={stockData.info.current_price}
                />
              </div>
            )}
          </div>
        </div>

        {/* Top 10 推荐股票 */}
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <TopList />
          </div>
        </div>

        {/* 底部免责声明 */}
        <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <div className="flex items-start">
            <AlertTriangle className="h-6 w-6 text-yellow-600 mr-3 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-medium text-yellow-800 mb-2">重要声明</h3>
              <div className="text-yellow-700 space-y-2">
                <p>
                  本系统仅用于学习研究目的，所有分析结果和预测数据不构成投资建议。
                  股票投资存在风险，过往表现不代表未来收益。
                </p>
                <p>
                  请根据自身风险承受能力谨慎投资，并咨询专业投资顾问。
                  投资决策应基于全面的基本面分析，而不仅仅依赖技术指标。
                </p>
                <p>
                  系统使用 AI 技术进行预测分析，但 AI 预测存在不确定性，
                  市场变化可能超出模型预期，请理性对待预测结果。
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
