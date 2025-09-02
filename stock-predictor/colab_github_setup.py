#!/usr/bin/env python3
"""
Colab GitHub项目设置脚本
从GitHub克隆股票预测项目并设置环境
"""

import os
import subprocess
import sys

def clone_github_project():
    """从GitHub克隆项目"""
    print("📥 从GitHub克隆项目...")
    
    try:
        # 克隆项目
        result = subprocess.run([
            'git', 'clone', 
            'https://github.com/shilinzmax/stockprediction.git'
        ], check=True, capture_output=True, text=True)
        
        print("✅ 项目克隆成功")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 克隆失败: {e}")
        return False

def change_to_project_directory():
    """切换到项目目录"""
    print("📁 切换到项目目录...")
    
    try:
        os.chdir('/content/stockprediction/stock-predictor')
        print("✅ 已切换到项目目录")
        return True
    except Exception as e:
        print(f"❌ 切换目录失败: {e}")
        return False

def check_project_structure():
    """检查项目结构"""
    print("🔍 检查项目结构...")
    
    required_items = [
        'backend/',
        'backend/app.py',
        'backend/core/',
        'backend/graph/'
    ]
    
    missing_items = []
    for item in required_items:
        if os.path.exists(item):
            print(f"✅ {item}")
        else:
            missing_items.append(item)
            print(f"❌ {item}")
    
    if missing_items:
        print(f"\n❌ 缺少文件: {missing_items}")
        return False
    else:
        print("\n🎉 项目结构检查通过！")
        return True

def setup_python_path():
    """设置Python路径"""
    print("🐍 设置Python路径...")
    
    project_path = '/content/stockprediction/stock-predictor'
    if project_path not in sys.path:
        sys.path.append(project_path)
        print(f"✅ 已添加路径: {project_path}")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 Colab GitHub项目设置")
    print("=" * 60)
    
    # 执行设置步骤
    steps = [
        ("克隆GitHub项目", clone_github_project),
        ("切换到项目目录", change_to_project_directory),
        ("检查项目结构", check_project_structure),
        ("设置Python路径", setup_python_path)
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
        print("\n✅ 项目设置成功！")
        print("\n📝 下一步:")
        print("1. 运行: uvicorn.run(app, host='0.0.0.0', port=8000)")
        print("2. 或者使用notebook中的启动cell")
    else:
        print("\n⚠️ 部分步骤失败，请检查错误信息")
    
    return success_count == len(steps)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
