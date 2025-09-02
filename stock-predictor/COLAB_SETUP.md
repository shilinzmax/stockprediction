# Google Colab 部署指南

## 🚀 快速开始

### 1. 打开Colab Notebook
- 访问 [Google Colab](https://colab.research.google.com/)
- 创建新的Python 3 notebook

### 2. 安装依赖
在第一个cell中运行：

```python
# 安装系统依赖
!apt-get update
!apt-get install -y curl

# 安装Ollama
!curl -fsSL https://ollama.com/install.sh | sh

# 安装Python依赖
!pip install -q fastapi uvicorn langgraph langchain langchain-openai yfinance pandas numpy ta pydantic python-multipart python-dotenv httpx aiofiles pyarrow alpha-vantage requests aiohttp ollama

# 安装前端依赖（如果需要）
!pip install -q jupyter-dash plotly dash
```

### 3. 下载项目文件
```python
# 克隆项目（如果从GitHub）
!git clone https://github.com/your-username/stock-predictor.git
%cd stock-predictor

# 或者直接上传文件到Colab
# 使用左侧文件面板上传项目文件
```

### 4. 启动Ollama服务
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
time.sleep(5)
print("✅ Ollama服务已启动")
```

### 5. 下载LLM模型
```python
# 下载Qwen2.5模型
!ollama pull qwen2.5:7b

# 验证模型
!ollama list
```

### 6. 配置环境变量
```python
import os

# 设置环境变量
os.environ["LLM_TYPE"] = "ollama"
os.environ["OLLAMA_MODEL"] = "qwen2.5:7b"
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = "8000"

print("✅ 环境变量已配置")
```

### 7. 测试系统
```python
# 测试Ollama连接
import ollama

try:
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{'role': 'user', 'content': 'Hello, are you working?'}]
    )
    print("✅ Ollama测试成功:", response['message']['content'])
except Exception as e:
    print("❌ Ollama测试失败:", str(e))
```

### 8. 启动应用
```python
# 启动FastAPI应用
import uvicorn
from backend.app import app

# 在Colab中启动服务器
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🔧 高级配置

### 使用GPU加速
```python
# 检查GPU可用性
import torch
print("CUDA可用:", torch.cuda.is_available())
print("GPU数量:", torch.cuda.device_count())

# 如果使用GPU版本的Ollama
!ollama pull qwen2.5:7b
```

### 持久化存储
```python
# 挂载Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 将项目保存到Drive
!cp -r /content/stock-predictor /content/drive/MyDrive/
```

### 自定义模型
```python
# 下载其他模型
!ollama pull llama2:7b
!ollama pull mistral:7b

# 切换模型
os.environ["OLLAMA_MODEL"] = "llama2:7b"
```

## 📊 性能优化

### 1. 内存管理
```python
import gc
import psutil

# 监控内存使用
def check_memory():
    memory = psutil.virtual_memory()
    print(f"内存使用: {memory.percent}%")
    if memory.percent > 80:
        gc.collect()
        print("已清理内存")

# 定期检查内存
import time
while True:
    check_memory()
    time.sleep(60)
```

### 2. 缓存优化
```python
# 设置更大的缓存
os.environ["CACHE_TTL_HOURS"] = "24"
os.environ["CACHE_DIR"] = "/content/drive/MyDrive/stock-cache"
```

### 3. 并发控制
```python
# 限制并发请求
os.environ["MAX_CONCURRENT_REQUESTS"] = "5"
```

## 🚨 注意事项

### 1. Colab限制
- 会话时间限制：12小时
- 内存限制：12GB RAM
- 存储限制：临时存储会在会话结束后清除

### 2. 最佳实践
- 定期保存工作到Google Drive
- 使用较小的模型以节省内存
- 监控资源使用情况
- 设置自动重启机制

### 3. 故障排除
```python
# 检查服务状态
!ps aux | grep ollama

# 重启Ollama
!pkill ollama
!ollama serve &

# 检查端口
!netstat -tlnp | grep 8000
```

## 📱 访问应用

启动后，你可以通过以下方式访问：
- 本地访问：`http://localhost:8000`
- 公共访问：使用Colab的公共URL功能

## 🔄 自动化脚本

创建一个完整的启动脚本：

```python
# 完整启动脚本
def setup_colab_environment():
    """设置Colab环境"""
    print("🚀 开始设置Colab环境...")
    
    # 安装依赖
    print("📦 安装依赖...")
    !pip install -q fastapi uvicorn langgraph langchain langchain-openai yfinance pandas numpy ta pydantic python-multipart python-dotenv httpx aiofiles pyarrow alpha-vantage requests aiohttp ollama
    
    # 启动Ollama
    print("🤖 启动Ollama...")
    import subprocess
    import threading
    import time
    
    def start_ollama():
        subprocess.run(['ollama', 'serve'], check=True)
    
    ollama_thread = threading.Thread(target=start_ollama, daemon=True)
    ollama_thread.start()
    time.sleep(5)
    
    # 下载模型
    print("📥 下载模型...")
    !ollama pull qwen2.5:7b
    
    # 配置环境
    print("⚙️ 配置环境...")
    import os
    os.environ["LLM_TYPE"] = "ollama"
    os.environ["OLLAMA_MODEL"] = "qwen2.5:7b"
    
    print("✅ 环境设置完成！")

# 运行设置
setup_colab_environment()
```

这样你就可以在Colab上高效运行你的股票预测系统了！
