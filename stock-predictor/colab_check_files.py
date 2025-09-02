#!/usr/bin/env python3
"""
Colab文件检查脚本
检查项目文件是否正确上传到Colab
"""

import os
import sys

def check_project_files():
    """检查项目文件是否存在"""
    print("🔍 检查项目文件...")
    
    # 必需的文件和文件夹
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
        
        print(f"\n💡 解决方案:")
        print("1. 使用左侧文件面板上传项目文件夹")
        print("2. 确保上传整个项目结构")
        print("3. 检查文件是否在根目录下")
        
        return False
    else:
        print(f"\n🎉 所有文件都已正确上传！")
        return True

def check_python_imports():
    """检查Python导入是否正常"""
    print("\n🐍 检查Python导入...")
    
    try:
        # 添加当前目录到Python路径
        sys.path.append('/content')
        sys.path.append('/content/stock-predictor')
        
        # 尝试导入主要模块
        from backend.app import app
        print("✅ backend.app 导入成功")
        
        from backend.core.llm import get_llm_analyzer
        print("✅ backend.core.llm 导入成功")
        
        from backend.graph.pipeline import StockPredictionPipeline
        print("✅ backend.graph.pipeline 导入成功")
        
        print("\n🎉 所有Python模块导入成功！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("\n💡 解决方案:")
        print("1. 检查文件是否完整上传")
        print("2. 确保Python路径正确")
        print("3. 检查文件权限")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🔍 Colab项目文件检查工具")
    print("=" * 60)
    
    # 检查文件是否存在
    files_ok = check_project_files()
    
    if files_ok:
        # 检查Python导入
        imports_ok = check_python_imports()
        
        if imports_ok:
            print("\n🎉 项目文件检查完成！可以启动应用了。")
            print("\n📝 下一步:")
            print("1. 运行: uvicorn.run(app, host='0.0.0.0', port=8000)")
            print("2. 或者使用notebook中的启动cell")
        else:
            print("\n⚠️ 文件存在但导入失败，请检查文件内容")
    else:
        print("\n⚠️ 文件检查失败，请先上传项目文件")
    
    return files_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
