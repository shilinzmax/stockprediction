# 🚀 股票预测系统 - Colab 简化运行指南

## 📋 快速开始（5分钟设置）

### 步骤1: 打开Colab
1. 访问 [Google Colab](https://colab.research.google.com/)
2. 创建新的Python 3 notebook

### 步骤2: 一键设置（复制粘贴运行）

```python
# 一键设置脚本
!apt-get update && apt-get install -y curl
!curl -fsSL https://ollama.com/install.sh | sh
!pip install -q fastapi uvicorn langgraph langchain langchain-openai yfinance pandas numpy ta pydantic python-multipart python-dotenv httpx aiofiles pyarrow alpha-vantage requests aiohttp ollama

import subprocess
import threading
import time

def start_ollama():
    subprocess.run(['ollama', 'serve'], check=True)

ollama_thread = threading.Thread(target=start_ollama, daemon=True)
ollama_thread.start()
time.sleep(10)

!ollama pull qwen2.5:7b

import os
os.environ["LLM_TYPE"] = "ollama"
os.environ["OLLAMA_MODEL"] = "qwen2.5:7b"

print("✅ 环境设置完成！")
```

### 步骤3: 克隆项目

```python
!git clone https://github.com/shilinzmax/stockprediction.git
%cd stockprediction/stock-predictor
print("✅ 项目克隆完成！")
```

### 步骤4: 启动应用

```python
# 方法1: 命令行启动（推荐）
!python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

如果方法1失败，尝试方法2：

```python
# 方法2: 动态导入修复
import sys
import backend.core as core
import backend.graph as graph
sys.modules['core'] = core
sys.modules['graph'] = graph

import uvicorn
from backend.app import app
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 步骤5: 测试API

```python
import requests

# 测试健康检查
response = requests.get("http://localhost:8000/health")
print("健康检查:", response.json())

# 测试股票预测
response = requests.post("http://localhost:8000/predict", 
                        json={"symbol": "AAPL", "timeframe": "1d"})
print("预测结果:", response.json())
```

## 🎯 访问地址

- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **股票预测**: POST http://localhost:8000/predict

## 🔧 常见问题

### 问题1: "ModuleNotFoundError: No module named 'backend'"
**解决**: 确保已运行克隆项目步骤

### 问题2: "ModuleNotFoundError: No module named 'core'"
**解决**: 使用动态导入修复方法

### 问题3: Ollama服务启动失败
**解决**: 重新运行启动Ollama的代码

## 📊 使用示例

```python
# 预测AAPL股票
import requests

response = requests.post("http://localhost:8000/predict", 
                        json={"symbol": "AAPL", "timeframe": "1d"})
result = response.json()

print(f"股票: {result.get('symbol', 'N/A')}")
print(f"方向: {result.get('direction', 'N/A')}")
print(f"概率: {result.get('probability', 'N/A')}%")
print(f"理由: {result.get('reasoning', 'N/A')}")
```

## 🎉 完成！

现在你可以在Colab中运行股票预测系统了！

### 支持的股票代码：
- 美股: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, NFLX, AMD, CRM
- 其他: 任何yfinance支持的股票代码

### 支持的时间框架：
- 1h: 1小时预测
- 1d: 1天预测  
- 1w: 1周预测

祝你使用愉快！🚀
