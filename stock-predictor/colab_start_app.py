#!/usr/bin/env python3
"""
Colab应用启动脚本
解决路径问题并启动股票预测应用
"""

import os
import sys
import subprocess

def setup_environment():
    """设置环境"""
    print("🔧 设置环境...")
    
    # 切换到正确的目录
    project_dir = '/content/stockprediction/stock-predictor'
    os.chdir(project_dir)
    
    # 添加Python路径
    if project_dir not in sys.path:
        sys.path.append(project_dir)
    
    print(f"✅ 已切换到目录: {project_dir}")
    print(f"✅ 已添加Python路径: {project_dir}")
    
    return True

def check_project_structure():
    """检查项目结构"""
    print("🔍 检查项目结构...")
    
    required_files = [
        'backend/app.py',
        'backend/core/llm.py',
        'backend/graph/pipeline.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    if missing_files:
        print(f"\n❌ 缺少文件: {missing_files}")
        return False
    else:
        print("\n🎉 项目结构检查通过！")
        return True

def start_application():
    """启动应用"""
    print("🚀 启动股票预测应用...")
    
    try:
        # 方法1: 使用uvicorn命令行
        print("📱 使用uvicorn命令行启动...")
        result = subprocess.run([
            'python', '-m', 'uvicorn', 
            'backend.app:app', 
            '--host', '0.0.0.0', 
            '--port', '8000'
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ uvicorn命令行启动失败: {e}")
        
        try:
            # 方法2: 使用Python代码启动
            print("📱 使用Python代码启动...")
            import uvicorn
            from backend.app import app
            
            print("📱 应用将在 http://localhost:8000 启动")
            print("📊 API文档: http://localhost:8000/docs")
            print("🔗 健康检查: http://localhost:8000/health")
            print("📈 预测API: POST http://localhost:8000/predict")
            print("\n按 Ctrl+C 停止应用")
            
            uvicorn.run(app, host="0.0.0.0", port=8000)
            
        except ImportError as e:
            print(f"❌ 导入错误: {e}")
            return False
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            return False
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 Colab应用启动工具")
    print("=" * 60)
    
    # 执行步骤
    steps = [
        ("设置环境", setup_environment),
        ("检查项目结构", check_project_structure),
        ("启动应用", start_application)
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
    print(f"🎉 启动完成！成功步骤: {success_count}/{len(steps)}")
    
    return success_count == len(steps)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
