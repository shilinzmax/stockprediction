#!/usr/bin/env python3
"""
Colab快速启动脚本
一键设置股票预测系统在Colab中运行
"""

import os
import subprocess
import time
import threading

def run_command(cmd, description=""):
    """运行命令并显示结果"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        return False

def setup_colab():
    """设置Colab环境"""
    print("🚀 开始设置Colab环境...")
    
    # 1. 安装系统依赖
    commands = [
        ("apt-get update", "更新包列表"),
        ("apt-get install -y curl", "安装curl"),
        ("curl -fsSL https://ollama.com/install.sh | sh", "安装Ollama")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    # 2. 安装Python依赖
    packages = [
        "fastapi", "uvicorn[standard]", "langgraph", "langchain", 
        "langchain-openai", "yfinance", "pandas", "numpy", "ta",
        "pydantic", "python-multipart", "python-dotenv", "httpx",
        "aiofiles", "pyarrow", "alpha-vantage", "requests", "aiohttp", "ollama"
    ]
    
    for package in packages:
        if not run_command(f"pip install -q {package}", f"安装 {package}"):
            return False
    
    # 3. 启动Ollama服务
    print("🤖 启动Ollama服务...")
    
    def start_ollama():
        subprocess.run(['ollama', 'serve'], check=True)
    
    ollama_thread = threading.Thread(target=start_ollama, daemon=True)
    ollama_thread.start()
    time.sleep(10)
    
    # 4. 下载模型
    if not run_command("ollama pull qwen2.5:7b", "下载Qwen2.5模型"):
        return False
    
    # 5. 设置环境变量
    print("⚙️ 配置环境变量...")
    os.environ["LLM_TYPE"] = "ollama"
    os.environ["OLLAMA_MODEL"] = "qwen2.5:7b"
    os.environ["HOST"] = "0.0.0.0"
    os.environ["PORT"] = "8000"
    
    print("✅ 环境设置完成！")
    return True

def test_system():
    """测试系统"""
    print("🧪 测试系统...")
    
    try:
        import ollama
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=[{'role': 'user', 'content': 'Hello'}]
        )
        print("✅ 系统测试成功")
        return True
    except Exception as e:
        print(f"❌ 系统测试失败: {e}")
        return False

def start_app():
    """启动应用"""
    print("🚀 启动股票预测应用...")
    
    try:
        import uvicorn
        from backend.app import app
        
        print("📱 应用将在 http://localhost:8000 启动")
        print("📊 API文档: http://localhost:8000/docs")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 股票预测系统 - Colab快速启动")
    print("=" * 60)
    
    # 设置环境
    if setup_colab():
        # 测试系统
        if test_system():
            # 启动应用
            start_app()
        else:
            print("❌ 系统测试失败，请检查配置")
    else:
        print("❌ 环境设置失败，请检查错误信息")
