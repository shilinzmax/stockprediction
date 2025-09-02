# 🚀 Google Colab 部署指南

本指南将帮助您将股票预测系统部署到Google Colab环境中运行。

## 📋 准备工作

### 1. 项目文件准备
确保您有以下文件结构：
```
stock-predictor/
├── backend/                 # 后端代码
│   ├── core/               # 核心模块
│   ├── graph/              # LangGraph工作流
│   └── data/               # 数据目录
├── colab_requirements.txt  # Colab依赖
├── colab_setup.py         # 设置脚本
├── colab_app.py           # Colab应用
└── COLAB_GUIDE.md         # 本指南
```

### 2. 环境要求
- Google Colab 账户
- 稳定的网络连接
- 可选：OpenAI API Key（用于真实AI预测）

## 🎯 部署步骤

### 方法一：使用设置脚本（推荐）

1. **上传项目文件**
   ```python
   # 在Colab中运行
   from google.colab import files
   uploaded = files.upload()
   ```

2. **解压项目文件**（如果是压缩包）
   ```python
   import zipfile
   with zipfile.ZipFile('stock-predictor.zip', 'r') as zip_ref:
       zip_ref.extractall('.')
   ```

3. **运行设置脚本**
   ```python
   # 安装依赖并启动系统
   !python colab_setup.py
   ```

### 方法二：手动设置

1. **安装依赖包**
   ```python
   # 安装核心依赖
   !pip install fastapi uvicorn langgraph langchain langchain-openai
   !pip install yfinance pandas numpy ta pydantic
   !pip install python-multipart python-dotenv httpx aiofiles
   !pip install pyarrow alpha-vantage requests aiohttp
   !pip install ipywidgets plotly dash jupyter-dash
   ```

2. **设置环境变量**
   ```python
   import os
   from pathlib import Path
   
   # 创建数据目录
   data_dir = Path("data")
   data_dir.mkdir(exist_ok=True)
   
   # 设置环境变量
   os.environ["CACHE_DIR"] = str(data_dir)
   os.environ["CACHE_TTL_HOURS"] = "1"
   os.environ["LOG_LEVEL"] = "INFO"
   ```

3. **启动应用**
   ```python
   # 启动Colab版本的应用
   !python colab_app.py
   ```

## 🔧 配置选项

### OpenAI API Key（可选）
```python
import os

# 设置OpenAI API Key（可选）
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# 如果没有API Key，系统会自动使用Mock LLM
```

### 环境变量配置
```python
# 服务器配置
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = "8000"

# 缓存配置
os.environ["CACHE_DIR"] = "data"
os.environ["CACHE_TTL_HOURS"] = "1"

# 日志配置
os.environ["LOG_LEVEL"] = "INFO"
```

## 🌐 访问系统

### 1. 本地访问
启动后，您可以通过以下地址访问：
- **根路径**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

### 2. 使用ngrok公开访问（可选）
```python
# 安装ngrok
!pip install pyngrok

# 启动ngrok隧道
from pyngrok import ngrok
public_url = ngrok.connect(8000)
print(f"公开访问地址: {public_url}")
```

## 📊 使用示例

### 1. 获取股票数据
```python
import requests

# 获取AAPL股票数据
response = requests.get("http://localhost:8000/api/stock/AAPL")
data = response.json()
print(f"股票数据: {data}")
```

### 2. 进行股票预测
```python
import requests

# 预测AAPL 1天走势
prediction_data = {
    "symbol": "AAPL",
    "timeframe": "1d"
}

response = requests.post("http://localhost:8000/api/predict", json=prediction_data)
result = response.json()
print(f"预测结果: {result}")
```

### 3. 获取Top 10推荐
```python
import requests

# 获取Top 10股票推荐
response = requests.get("http://localhost:8000/api/top-stocks")
recommendations = response.json()
print(f"推荐股票: {recommendations}")
```

### 4. 搜索股票
```python
import requests

# 搜索股票
response = requests.get("http://localhost:8000/api/search/AAPL")
search_results = response.json()
print(f"搜索结果: {search_results}")
```

## 🎨 前端界面（可选）

由于Colab主要支持Python环境，前端界面需要特殊处理：

### 使用Dash创建Web界面
```python
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import requests

# 创建Dash应用
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("股票预测系统"),
    dcc.Input(id='stock-input', value='AAPL', type='text'),
    html.Button('获取数据', id='get-data-button'),
    dcc.Graph(id='stock-chart'),
    html.Div(id='prediction-output')
])

@app.callback(
    [Output('stock-chart', 'figure'),
     Output('prediction-output', 'children')],
    [Input('get-data-button', 'n_clicks')],
    [dash.dependencies.State('stock-input', 'value')]
)
def update_chart(n_clicks, stock_symbol):
    if n_clicks:
        # 获取股票数据
        response = requests.get(f"http://localhost:8000/api/stock/{stock_symbol}")
        data = response.json()
        
        # 创建图表
        fig = go.Figure(data=go.Candlestick(
            x=data['data']['Date'],
            open=data['data']['Open'],
            high=data['data']['High'],
            low=data['data']['Low'],
            close=data['data']['Close']
        ))
        
        # 获取预测
        pred_response = requests.post("http://localhost:8000/api/predict", 
                                    json={"symbol": stock_symbol, "timeframe": "1d"})
        prediction = pred_response.json()
        
        return fig, f"预测结果: {prediction['direction']} (概率: {prediction['probability']}%)"
    
    return {}, ""

# 运行Dash应用
app.run_server(host='0.0.0.0', port=8050, debug=True)
```

## ⚠️ 注意事项

### 1. Colab限制
- **会话时间限制**: Colab免费版有12小时会话限制
- **内存限制**: 免费版有内存使用限制
- **网络限制**: 某些网络请求可能被限制

### 2. 性能优化
```python
# 减少内存使用
import gc
gc.collect()

# 限制数据量
os.environ["MAX_DATA_POINTS"] = "1000"
```

### 3. 错误处理
```python
try:
    # 您的代码
    pass
except Exception as e:
    print(f"错误: {e}")
    # 错误处理逻辑
```

## 🔍 故障排除

### 常见问题

1. **模块导入错误**
   ```python
   # 确保路径正确
   import sys
   sys.path.append('.')
   ```

2. **端口占用**
   ```python
   # 检查端口使用情况
   !lsof -i :8000
   ```

3. **依赖安装失败**
   ```python
   # 强制重新安装
   !pip install --force-reinstall package_name
   ```

4. **API连接问题**
   ```python
   # 检查服务状态
   import requests
   try:
       response = requests.get("http://localhost:8000/health")
       print("服务正常运行")
   except:
       print("服务未启动")
   ```

## 📈 高级功能

### 1. 批量预测
```python
import asyncio
import aiohttp

async def batch_predict(symbols, timeframes):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in symbols:
            for timeframe in timeframes:
                task = session.post("http://localhost:8000/api/predict", 
                                  json={"symbol": symbol, "timeframe": timeframe})
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return [await r.json() for r in results]

# 使用示例
symbols = ["AAPL", "MSFT", "GOOGL"]
timeframes = ["1d", "1w"]
results = await batch_predict(symbols, timeframes)
```

### 2. 实时监控
```python
import time
import threading

def monitor_stocks(symbols, interval=60):
    while True:
        for symbol in symbols:
            response = requests.get(f"http://localhost:8000/api/stock/{symbol}")
            data = response.json()
            print(f"{symbol}: {data['indicators']['rsi']:.2f}")
        time.sleep(interval)

# 启动监控
monitor_thread = threading.Thread(target=monitor_stocks, args=(["AAPL", "MSFT"], 60))
monitor_thread.start()
```

## 🎉 完成！

现在您已经成功将股票预测系统部署到Google Colab中！

### 下一步建议：
1. 尝试不同的股票代码进行预测
2. 实验不同的时间框架
3. 查看技术指标和信号强度
4. 获取AI生成的投资建议

### 获取帮助：
- 查看API文档: http://localhost:8000/docs
- 检查系统状态: http://localhost:8000/health
- 查看GPT状态: http://localhost:8000/api/gpt-status

---

**免责声明**: 本系统仅用于学习研究目的，所有预测结果不构成投资建议。投资有风险，入市需谨慎。

