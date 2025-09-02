# 🚀 股票预测系统 - Google Colab 完整运行指南

## 📋 项目概述

这是一个基于 LangGraph 的股票预测系统，使用本地 LLM（Qwen2.5:7b）进行股票分析，无需 OpenAI API 密钥。

### 🎯 主要功能
- 实时股票数据获取
- 技术指标计算（RSI、MACD、布林带等）
- AI驱动的股票预测分析
- 本地LLM分析（使用Ollama + Qwen2.5:7b）
- RESTful API接口
- 交互式Web界面

### 🏗️ 技术栈
- **后端**: Python 3.12 + FastAPI + LangGraph + LangChain
- **前端**: React 18 + TypeScript + TailwindCSS
- **AI模型**: Ollama + Qwen2.5:7b (本地运行)
- **数据源**: yfinance (Yahoo Finance)
- **缓存**: 本地Parquet文件缓存

## 🚀 快速开始

### 步骤1: 打开Colab并创建新Notebook

1. 访问 [Google Colab](https://colab.research.google.com/)
2. 创建新的Python 3 notebook
3. 上传 `Stock_Predictor_Colab.ipynb` 文件，或按以下步骤操作

### 步骤2: 安装系统依赖

```python
# 安装系统依赖
!apt-get update
!apt-get install -y curl wget

# 安装Ollama
!curl -fsSL https://ollama.com/install.sh | sh

print("✅ 系统依赖安装完成")
```

### 步骤3: 安装Python依赖

```python
# 安装Python依赖
!pip install -q fastapi uvicorn langgraph langchain langchain-openai yfinance pandas numpy ta pydantic python-multipart python-dotenv httpx aiofiles pyarrow alpha-vantage requests aiohttp ollama jupyter-dash plotly dash

print("✅ Python依赖安装完成")
```

### 步骤4: 启动Ollama服务

```python
# 启动Ollama服务
import subprocess
import time
import threading

def start_ollama():
    subprocess.run(['ollama', 'serve'], check=True)

# 在后台启动Ollama
ollama_thread = threading.Thread(target=start_ollama, daemon=True)
ollama_thread.start()

# 等待服务启动
time.sleep(10)
print("✅ Ollama服务已启动")
```

### 步骤5: 下载LLM模型

```python
# 下载Qwen2.5模型
!ollama pull qwen2.5:7b

# 验证模型
!ollama list

print("✅ 模型下载完成")
```

### 步骤6: 设置环境变量

```python
# 设置环境变量
import os

os.environ["LLM_TYPE"] = "ollama"
os.environ["OLLAMA_MODEL"] = "qwen2.5:7b"
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = "8000"
os.environ["CACHE_TTL_HOURS"] = "24"

print("✅ 环境变量已配置")
```

### 步骤7: 测试Ollama连接

```python
# 测试Ollama连接
import ollama

try:
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{'role': 'user', 'content': 'Hello, are you working?'}]
    )
    print("✅ Ollama测试成功")
    print(f"回复: {response['message']['content']}")
except Exception as e:
    print(f"❌ Ollama测试失败: {e}")
```

### 步骤8: 克隆项目

```python
# 从GitHub克隆项目
!git clone https://github.com/shilinzmax/stockprediction.git
%cd stockprediction/stock-predictor

# 检查项目文件是否存在
import os
if os.path.exists('backend'):
    print("✅ 找到backend文件夹")
    print("📁 项目文件已就绪")
    print("🎉 成功从GitHub克隆项目！")
else:
    print("❌ 未找到backend文件夹")
    print("📁 请检查GitHub仓库结构")
```

### 步骤9: 检查项目结构

```python
# 检查项目文件是否正确克隆
import os

def check_project_files():
    """检查项目文件是否存在"""
    print("🔍 检查项目文件...")
    
    required_items = [
        'backend/',
        'backend/app.py',
        'backend/core/',
        'backend/core/llm.py',
        'backend/core/state.py',
        'backend/graph/',
        'backend/graph/pipeline.py'
    ]
    
    missing_items = []
    existing_items = []
    
    for item in required_items:
        if os.path.exists(item):
            existing_items.append(item)
            print(f"✅ {item}")
        else:
            missing_items.append(item)
            print(f"❌ {item}")
    
    print(f"\n📊 检查结果:")
    print(f"✅ 存在: {len(existing_items)} 个文件/文件夹")
    print(f"❌ 缺失: {len(missing_items)} 个文件/文件夹")
    
    if missing_items:
        print(f"\n❌ 缺少以下文件/文件夹:")
        for item in missing_items:
            print(f"  - {item}")
        return False
    else:
        print(f"\n🎉 所有文件都已正确克隆！")
        print("📁 项目文件已就绪，可以启动应用了")
        return True

# 运行检查
files_ok = check_project_files()
```

### 步骤10: 启动应用（多种方法）

#### 方法1: 使用命令行启动（推荐）

```python
# 使用命令行启动（最简单）
import os

# 切换到正确的目录
os.chdir('/content/stockprediction/stock-predictor')

print("🚀 使用命令行启动应用...")
print("📱 应用将在 http://localhost:8000 启动")
print("📊 API文档: http://localhost:8000/docs")
print("🔗 健康检查: http://localhost:8000/health")
print("📈 预测API: POST http://localhost:8000/predict")
print("\n按 Ctrl+C 停止应用")

# 使用命令行启动
!python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

#### 方法2: 动态导入修复

```python
# 动态导入修复（不修改文件）
import os
import sys

# 切换到正确的目录
os.chdir('/content/stockprediction/stock-predictor')

# 添加Python路径
sys.path.insert(0, '/content/stockprediction/stock-predictor')

def fix_imports_dynamically():
    """动态修复导入问题"""
    print("🔧 动态修复导入问题...")
    
    # 创建core模块的别名
    import backend.core as core
    sys.modules['core'] = core
    
    # 创建graph模块的别名
    import backend.graph as graph
    sys.modules['graph'] = graph
    
    print("✅ 动态导入修复完成")

# 执行动态修复
fix_imports_dynamically()

# 尝试启动应用
try:
    import uvicorn
    from backend.app import app
    
    print("\n🚀 启动股票预测应用...")
    print("📱 应用将在 http://localhost:8000 启动")
    print("📊 API文档: http://localhost:8000/docs")
    print("🔗 健康检查: http://localhost:8000/health")
    print("📈 预测API: POST http://localhost:8000/predict")
    print("\n按 Ctrl+C 停止应用")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
except ImportError as e:
    print(f"\n❌ 导入错误: {e}")
    print("💡 请尝试方法1")
except Exception as e:
    print(f"\n❌ 启动失败: {e}")
    print("🔄 请检查错误信息并重试")
```

#### 方法3: 创建符号链接

```python
# 创建符号链接来解决导入问题
import os
import sys

# 切换到正确的目录
os.chdir('/content/stockprediction/stock-predictor')

# 添加Python路径
sys.path.append('/content/stockprediction/stock-predictor')
sys.path.append('/content/stockprediction')

# 创建符号链接来解决导入问题
def create_symlinks():
    """创建符号链接来解决导入问题"""
    print("🔗 创建符号链接...")
    
    try:
        # 在backend目录下创建core和graph的符号链接
        if not os.path.exists('/content/stockprediction/stock-predictor/core'):
            os.symlink('/content/stockprediction/stock-predictor/backend/core', 
                      '/content/stockprediction/stock-predictor/core')
            print("✅ 创建core符号链接")
        
        if not os.path.exists('/content/stockprediction/stock-predictor/graph'):
            os.symlink('/content/stockprediction/stock-predictor/backend/graph', 
                      '/content/stockprediction/stock-predictor/graph')
            print("✅ 创建graph符号链接")
        
        return True
    except Exception as e:
        print(f"❌ 创建符号链接失败: {e}")
        return False

# 创建符号链接
create_symlinks()

# 检查文件结构
print(f"\n📁 当前目录: {os.getcwd()}")
print(f"📁 backend存在: {os.path.exists('backend')}")
print(f"📁 core符号链接存在: {os.path.exists('core')}")
print(f"📁 graph符号链接存在: {os.path.exists('graph')}")

# 尝试启动应用
try:
    import uvicorn
    from backend.app import app
    
    print("\n🚀 启动股票预测应用...")
    print("📱 应用将在 http://localhost:8000 启动")
    print("📊 API文档: http://localhost:8000/docs")
    print("🔗 健康检查: http://localhost:8000/health")
    print("📈 预测API: POST http://localhost:8000/predict")
    print("\n按 Ctrl+C 停止应用")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
except ImportError as e:
    print(f"\n❌ 导入错误: {e}")
    print("💡 尝试其他方法...")
except Exception as e:
    print(f"\n❌ 启动失败: {e}")
    print("🔄 请检查错误信息并重试")
```

## 🧪 测试API

### 测试健康检查

```python
# 测试API端点
import requests
import json

# 测试健康检查
try:
    response = requests.get("http://localhost:8000/health")
    print("✅ 健康检查:", response.json())
except Exception as e:
    print(f"❌ 健康检查失败: {e}")
```

### 测试股票预测

```python
# 测试股票预测
try:
    prediction_data = {
        "symbol": "AAPL",
        "timeframe": "1d"
    }
    
    response = requests.post(
        "http://localhost:8000/predict",
        json=prediction_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 股票预测成功:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"❌ 预测失败: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ 预测请求失败: {e}")
```

## 🔧 故障排除

### 问题1: "ModuleNotFoundError: No module named 'backend'"

**解决方案**:
1. 确保已运行GitHub克隆步骤
2. 检查是否在正确的目录下
3. 使用命令行启动方法

### 问题2: "ModuleNotFoundError: No module named 'core'"

**解决方案**:
1. 使用动态导入修复方法
2. 或创建符号链接方法
3. 或使用命令行启动

### 问题3: Ollama服务启动失败

**解决方案**:
```python
# 检查Ollama服务状态
!ps aux | grep ollama

# 重启Ollama服务
!pkill ollama
!ollama serve &
time.sleep(5)
print("✅ Ollama服务已重启")
```

### 问题4: 端口被占用

**解决方案**:
```python
# 检查端口使用情况
!netstat -tlnp | grep 8000

# 杀死占用端口的进程
!pkill -f "uvicorn"
```

## 📊 API使用示例

### 获取股票预测

```python
import requests

# 预测AAPL股票
response = requests.post("http://localhost:8000/predict", 
                        json={"symbol": "AAPL", "timeframe": "1d"})
result = response.json()
print(result)
```

### 获取Top 10股票推荐

```python
# 获取Top 10股票推荐
response = requests.get("http://localhost:8000/top-stocks")
result = response.json()
print(result)
```

### 获取股票数据

```python
# 获取股票数据
response = requests.get("http://localhost:8000/stock/AAPL")
result = response.json()
print(result)
```

## 📝 注意事项

1. **会话时间限制**: Colab会话有12小时限制
2. **内存使用**: 监控内存使用情况，避免超出限制
3. **数据持久化**: 重要数据请保存到Google Drive
4. **模型大小**: Qwen2.5:7b模型约4.7GB，确保有足够空间
5. **网络访问**: 确保可以访问外部API获取股票数据

## 🎉 完成！

现在你可以在Colab中运行股票预测系统了！

### 访问方式：
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **股票预测**: POST http://localhost:8000/predict
- **Top股票推荐**: GET http://localhost:8000/top-stocks

### 支持的股票代码：
- 美股: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, NFLX, AMD, CRM
- 其他: 任何yfinance支持的股票代码

### 支持的时间框架：
- 1h: 1小时预测
- 1d: 1天预测
- 1w: 1周预测

祝你使用愉快！🚀
