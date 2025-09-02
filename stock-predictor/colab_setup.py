#!/usr/bin/env python3
"""
Google Colab 环境设置脚本
专为在Colab中运行股票预测系统而设计
"""

import os
import sys
import subprocess
import time
import threading
import requests
from pathlib import Path

def install_system_dependencies():
    """安装系统依赖"""
    print("🔧 安装系统依赖...")
    
    commands = [
        "apt-get update",
        "apt-get install -y curl wget",
        "curl -fsSL https://ollama.com/install.sh | sh"
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ {cmd} 完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ {cmd} 失败: {e}")
            return False
    
    return True

def install_python_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "langgraph",
        "langchain",
        "langchain-openai",
        "yfinance",
        "pandas",
        "numpy",
        "ta",
        "pydantic",
        "python-multipart",
        "python-dotenv",
        "httpx",
        "aiofiles",
        "pyarrow",
        "alpha-vantage",
        "requests",
        "aiohttp",
        "ollama",
        "jupyter-dash",
        "plotly",
        "dash"
    ]
    
    try:
        for package in packages:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", package], check=True)
        print("✅ Python依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Python依赖安装失败: {e}")
        return False

def start_ollama_service():
    """启动Ollama服务"""
    print("🤖 启动Ollama服务...")
    
    def run_ollama():
        try:
            subprocess.run(['ollama', 'serve'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Ollama服务启动失败: {e}")
    
    # 在后台启动Ollama
    ollama_thread = threading.Thread(target=run_ollama, daemon=True)
    ollama_thread.start()
    
    # 等待服务启动
    time.sleep(10)
    
    # 检查服务是否启动
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama服务启动成功")
            return True
    except:
        pass
    
    print("❌ Ollama服务启动失败")
    return False

def download_llm_model(model_name="qwen2.5:7b"):
    """下载LLM模型"""
    print(f"📥 下载模型: {model_name}")
    
    try:
        result = subprocess.run(['ollama', 'pull', model_name], check=True, capture_output=True, text=True)
        print(f"✅ 模型 {model_name} 下载完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 模型下载失败: {e}")
        return False

def setup_environment():
    """设置环境变量"""
    print("⚙️ 配置环境变量...")
    
    env_vars = {
        "LLM_TYPE": "ollama",
        "OLLAMA_MODEL": "qwen2.5:7b",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "CACHE_TTL_HOURS": "24",
        "LOG_LEVEL": "INFO"
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"  {key}={value}")
    
    print("✅ 环境变量配置完成")

def test_ollama_connection():
    """测试Ollama连接"""
    print("🧪 测试Ollama连接...")
    
    try:
        import ollama
        
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=[{'role': 'user', 'content': 'Hello, are you working?'}]
        )
        
        print("✅ Ollama测试成功")
        print(f"回复: {response['message']['content'][:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ollama测试失败: {e}")
        return False

def create_colab_notebook():
    """创建Colab演示notebook"""
    print("📓 创建Colab演示notebook...")
    
    notebook_content = '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 股票预测系统 - Colab演示\\n",
    "\\n",
    "这个notebook演示了如何在Google Colab中运行股票预测系统。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 运行设置脚本\\n",
    "!python colab_setup.py"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 启动应用\\n",
    "import uvicorn\\n",
    "from backend.app import app\\n",
    "\\n",
    "uvicorn.run(app, host=\\"0.0.0.0\\", port=8000)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}'''
    
    with open("stock_predictor_demo.ipynb", "w") as f:
        f.write(notebook_content)
    
    print("✅ Colab演示notebook创建完成")

def main():
    """主函数"""
    print("🚀 开始设置Google Colab环境...")
    print("=" * 50)
    
    # 检查是否在Colab环境中
    try:
        import google.colab
        print("✅ 检测到Colab环境")
    except ImportError:
        print("⚠️ 未检测到Colab环境，但脚本仍可运行")
    
    # 执行设置步骤
    steps = [
        ("安装系统依赖", install_system_dependencies),
        ("安装Python依赖", install_python_dependencies),
        ("启动Ollama服务", start_ollama_service),
        ("下载LLM模型", lambda: download_llm_model("qwen2.5:7b")),
        ("配置环境变量", setup_environment),
        ("测试Ollama连接", test_ollama_connection),
        ("创建演示notebook", create_colab_notebook)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\\n📋 {step_name}...")
        try:
            if step_func():
                success_count += 1
            else:
                print(f"❌ {step_name} 失败")
        except Exception as e:
            print(f"❌ {step_name} 异常: {e}")
    
    print("\\n" + "=" * 50)
    print(f"🎉 设置完成！成功步骤: {success_count}/{len(steps)}")
    
    if success_count == len(steps):
        print("\\n✅ 所有步骤都成功完成！")
        print("\\n📝 下一步:")
        print("1. 运行: python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000")
        print("2. 或者使用: !python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000")
        print("3. 访问应用: http://localhost:8000")
    else:
        print("\\n⚠️ 部分步骤失败，请检查错误信息")
    
    return success_count == len(steps)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)