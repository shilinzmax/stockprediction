import React from 'react';
import {
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Bar,
  ReferenceLine,
} from 'recharts';
import { StockPriceData, SupportResistance } from '../lib/types';
import { formatCurrency, formatDate } from '../lib/utils';

interface PriceChartProps {
  data: StockPriceData[];
  supportResistance?: SupportResistance;
  height?: number;
}

export const PriceChart: React.FC<PriceChartProps> = ({ 
  data, 
  supportResistance,
  height = 400 
}) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
        <p className="text-gray-500">暂无数据</p>
      </div>
    );
  }

  // 准备图表数据
  const chartData = data.map(item => ({
    ...item,
    date: new Date(item.date).toLocaleDateString('zh-CN', { 
      month: 'short', 
      day: 'numeric' 
    }),
    // 计算价格变化
    priceChange: item.close - item.open,
    priceChangePercent: ((item.close - item.open) / item.open) * 100,
  }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium">{label}</p>
          <div className="space-y-1 text-sm">
            <p>
              <span className="text-gray-600">开盘:</span> 
              <span className="ml-2 font-medium">{formatCurrency(data.open)}</span>
            </p>
            <p>
              <span className="text-gray-600">最高:</span> 
              <span className="ml-2 font-medium text-green-600">{formatCurrency(data.high)}</span>
            </p>
            <p>
              <span className="text-gray-600">最低:</span> 
              <span className="ml-2 font-medium text-red-600">{formatCurrency(data.low)}</span>
            </p>
            <p>
              <span className="text-gray-600">收盘:</span> 
              <span className="ml-2 font-medium">{formatCurrency(data.close)}</span>
            </p>
            <p>
              <span className="text-gray-600">成交量:</span> 
              <span className="ml-2 font-medium">{data.volume.toLocaleString()}</span>
            </p>
            <p>
              <span className="text-gray-600">涨跌:</span> 
              <span className={`ml-2 font-medium ${data.priceChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {data.priceChange >= 0 ? '+' : ''}{data.priceChangePercent.toFixed(2)}%
              </span>
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">价格走势图</h3>
        <p className="text-sm text-gray-600">最近30天OHLCV数据</p>
      </div>
      
      <div style={{ height: height }} className="w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="date" 
              stroke="#666"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="#666"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip content={<CustomTooltip />} />
            
            {/* 支撑位和阻力位参考线 */}
            {supportResistance && (
              <>
                <ReferenceLine 
                  y={supportResistance.support} 
                  stroke="#10b981" 
                  strokeDasharray="5 5"
                  label={{ value: "支撑位", position: "topRight" }}
                />
                <ReferenceLine 
                  y={supportResistance.resistance} 
                  stroke="#ef4444" 
                  strokeDasharray="5 5"
                  label={{ value: "阻力位", position: "topRight" }}
                />
              </>
            )}
            
            {/* 成交量柱状图 */}
            <Bar 
              dataKey="volume" 
              fill="#e5e7eb" 
              opacity={0.3}
              yAxisId="volume"
            />
            
            {/* 价格线 */}
            <Line
              type="monotone"
              dataKey="close"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#3b82f6' }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      
      {/* 图例 */}
      <div className="flex items-center justify-center space-x-6 mt-4 text-sm">
        <div className="flex items-center">
          <div className="w-4 h-0.5 bg-blue-500 mr-2"></div>
          <span className="text-gray-600">收盘价</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-gray-300 mr-2 opacity-30"></div>
          <span className="text-gray-600">成交量</span>
        </div>
        {supportResistance && (
          <>
            <div className="flex items-center">
              <div className="w-4 h-0.5 bg-green-500 mr-2" style={{ borderStyle: 'dashed' }}></div>
              <span className="text-gray-600">支撑位</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-0.5 bg-red-500 mr-2" style={{ borderStyle: 'dashed' }}></div>
              <span className="text-gray-600">阻力位</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
