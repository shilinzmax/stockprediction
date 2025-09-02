# 金融数据API配置指南

本项目现在支持多个金融数据API，按优先级自动切换：

## API优先级

1. **yfinance** (免费，无需API密钥)
2. **Alpha Vantage** (免费，需要API密钥)
3. **IEX Cloud** (付费，需要API密钥)
4. **Polygon.io** (付费，需要API密钥)
5. **Mock数据** (备用，无需API密钥)

## 获取API密钥

### 1. Alpha Vantage (推荐)
- 网站：https://www.alphavantage.co/support/#api-key
- 费用：免费（每分钟5次请求）
- 注册：简单注册即可获得API密钥

### 2. IEX Cloud
- 网站：https://iexcloud.io/pricing/
- 费用：免费套餐每月50,000次请求
- 注册：需要信用卡验证

### 3. Polygon.io
- 网站：https://polygon.io/pricing/
- 费用：免费套餐每月5次请求
- 注册：需要信用卡验证

## 配置环境变量

在 `.env` 文件中添加以下配置：

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Alternative Financial Data APIs
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
IEX_CLOUD_API_KEY=your_iex_cloud_key_here
POLYGON_IO_API_KEY=your_polygon_io_key_here
```

## API特性对比

| API | 免费额度 | 数据质量 | 响应速度 | 推荐度 |
|-----|---------|---------|---------|--------|
| yfinance | 无限制 | 高 | 快 | ⭐⭐⭐⭐⭐ |
| Alpha Vantage | 5次/分钟 | 高 | 中等 | ⭐⭐⭐⭐ |
| IEX Cloud | 50K/月 | 高 | 快 | ⭐⭐⭐⭐ |
| Polygon.io | 5次/月 | 高 | 快 | ⭐⭐⭐ |
| Mock数据 | 无限制 | 模拟 | 极快 | ⭐⭐ |

## 使用建议

1. **开发测试**：使用Mock数据，无需配置
2. **生产环境**：配置Alpha Vantage API密钥
3. **高并发**：考虑IEX Cloud或Polygon.io
4. **成本控制**：优先使用yfinance和Alpha Vantage

## 故障排除

### yfinance连接问题
- 检查网络连接
- 可能是Yahoo Finance临时限制
- 系统会自动切换到下一个API

### API密钥问题
- 确认密钥格式正确
- 检查API服务状态
- 验证免费额度是否用完

### 数据格式问题
- 所有API返回统一格式
- 自动处理数据转换
- 支持缓存机制

## 监控和日志

系统会记录API使用情况：
- 成功/失败的API调用
- 数据获取时间
- 缓存命中率
- 错误信息

查看日志：
```bash
tail -f logs/api_manager.log
```
