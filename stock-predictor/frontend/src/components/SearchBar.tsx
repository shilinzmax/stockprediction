import React, { useState, useEffect } from 'react';
import { Search, TrendingUp } from 'lucide-react';
import { stockAPI } from '../lib/api';
import { SearchResult } from '../lib/types';

interface SearchBarProps {
  onStockSelect: (symbol: string) => void;
  placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({ 
  onStockSelect, 
  placeholder = "输入股票代码或名称，如 AAPL, MSFT, TSLA..." 
}) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // 防抖搜索
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (query.length >= 1) {
        searchStocks(query);
      } else {
        setSuggestions([]);
        setShowSuggestions(false);
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [query]);

  const searchStocks = async (searchQuery: string) => {
    setIsLoading(true);
    try {
      const result: SearchResult = await stockAPI.searchStocks(searchQuery);
      setSuggestions(result.matches);
      setShowSuggestions(true);
    } catch (error) {
      console.error('Search error:', error);
      setSuggestions([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value.toUpperCase());
  };

  const handleSuggestionClick = (symbol: string) => {
    setQuery(symbol);
    setShowSuggestions(false);
    onStockSelect(symbol);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onStockSelect(query.trim());
      setShowSuggestions(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  return (
    <div className="relative w-full max-w-md">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => query.length >= 1 && setShowSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
            placeholder={placeholder}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          />
          {isLoading && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
            </div>
          )}
        </div>
      </form>

      {/* 搜索建议下拉框 */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {suggestions.map((symbol, index) => (
            <div
              key={index}
              onClick={() => handleSuggestionClick(symbol)}
              className="flex items-center px-4 py-2 hover:bg-gray-100 cursor-pointer border-b border-gray-100 last:border-b-0"
            >
              <TrendingUp className="h-4 w-4 text-gray-400 mr-2" />
              <span className="text-sm font-medium">{symbol}</span>
            </div>
          ))}
        </div>
      )}

      {/* 无结果提示 */}
      {showSuggestions && suggestions.length === 0 && query.length >= 1 && !isLoading && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg">
          <div className="px-4 py-2 text-sm text-gray-500">
            未找到匹配的股票代码
          </div>
        </div>
      )}
    </div>
  );
};
