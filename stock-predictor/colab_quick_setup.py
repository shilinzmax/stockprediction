#!/usr/bin/env python3
"""
Colab快速设置脚本
一键设置和启动股票预测系统
"""

import os
import subprocess
import time
import threading
import sys

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

def setup_environment():
    """设置环境"""
    print("🚀 开始设置Colab环境...")
    
    # 安装系统依赖
    commands = [
        ("apt-get update", "更新包列表"),
        ("apt-get install -y curl wget", "安装系统工具"),
        ("curl -fsSL https://ollama.com/install.sh | sh", "安装Ollama")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    # 安装Python依赖
    packages = [
        "fastapi", "uvicorn[standard]", "langgraph", "langchain", 
        "langchain-openai", "yfinance", "pandas", "numpy", "ta",
        "pydantic", "python-multipart", "python-dotenv", "httpx",
        "aiofiles", "pyarrow", "alpha-vantage", "requests", "aiohttp", "ollama"
    ]
    
    for package in packages:
        if not run_command(f"pip install -q {package}", f"安装 {package}"):
            return False
    
    return True

def start_ollama_service():
    """启动Ollama服务"""
    print("🤖 启动Ollama服务...")
    
    def start_ollama():
        subprocess.run(['ollama', 'serve'], check=True)
    
    ollama_thread = threading.Thread(target=start_ollama, daemon=True)
    ollama_thread.start()
    time.sleep(10)
    
    # 验证服务启动
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama服务启动成功")
            return True
    except:
        pass
    
    print("❌ Ollama服务启动失败")
    return False

def download_model():
    """下载LLM模型"""
    print("📥 下载Qwen2.5模型...")
    return run_command("ollama pull qwen2.5:7b", "下载Qwen2.5模型")

def setup_environment_variables():
    """设置环境变量"""
    print("⚙️ 配置环境变量...")
    
    env_vars = {
        "LLM_TYPE": "ollama",
        "OLLAMA_MODEL": "qwen2.5:7b",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "CACHE_TTL_HOURS": "24"
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"  {key}={value}")
    
    print("✅ 环境变量配置完成")
    return True

def clone_project():
    """克隆项目"""
    print("📥 克隆项目...")
    
    if not run_command("git clone https://github.com/shilinzmax/stockprediction.git", "克隆项目"):
        return False
    
    # 切换到项目目录
    os.chdir('/content/stockprediction/stock-predictor')
    print("✅ 已切换到项目目录")
    return True

def test_ollama():
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

def start_application():
    """启动应用"""
    print("🚀 启动股票预测应用...")
    
    try:
        # 使用命令行启动
        result = subprocess.run([
            'python', '-m', 'uvicorn', 
            'backend.app:app', 
            '--host', '0.0.0.0', 
            '--port', '8000'
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 股票预测系统 - Colab快速设置")
    print("=" * 60)
    
    # 执行设置步骤
    steps = [
        ("设置环境", setup_environment),
        ("启动Ollama服务", start_ollama_service),
        ("下载LLM模型", download_model),
        ("配置环境变量", setup_environment_variables),
        ("克隆项目", clone_project),
        ("测试Ollama连接", test_ollama)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        try:
            if step_func():
                success_count += 1
            else:
                print(f"❌ {step_name} 失败")
        except Exception as e:
            print(f"❌ {step_name} 异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎉 设置完成！成功步骤: {success_count}/{len(steps)}")
    
    if success_count == len(steps):
        print("\n✅ 所有步骤都成功完成！")
        print("\n📝 下一步:")
        print("1. 运行: start_application()")
        print("2. 或者使用: !python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000")
        
        # 询问是否启动应用
        try:
            response = input("\n是否现在启动应用？(y/n): ")
            if response.lower() in ['y', 'yes', '是']:
                start_application()
        except:
            print("\n💡 手动启动应用:")
            print("start_application()")
    else:
        print("\n⚠️ 部分步骤失败，请检查错误信息")
    
    return success_count == len(steps)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
