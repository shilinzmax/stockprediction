#!/usr/bin/env python3
"""
Colab导入修复脚本
修复所有导入路径问题
"""

import os
import re

def fix_imports_in_file(file_path):
    """修复单个文件中的导入"""
    print(f"🔧 修复文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复core导入
        content = re.sub(r'^from core\.', 'from backend.core.', content, flags=re.MULTILINE)
        content = re.sub(r'^from graph\.', 'from backend.graph.', content, flags=re.MULTILINE)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 修复完成: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {file_path} - {e}")
        return False

def main():
    """主函数"""
    print("🔧 开始修复导入路径...")
    
    # 切换到项目目录
    os.chdir('/content/stockprediction/stock-predictor')
    
    # 需要修复的文件列表
    files_to_fix = [
        'backend/test_ollama.py',
        'backend/test_gpt_api.py',
        'backend/graph/nodes/llm_analyze.py',
        'backend/graph/nodes/fetch_data.py',
        'backend/graph/pipeline.py',
        'backend/graph/nodes/report.py',
        'backend/graph/nodes/make_advice.py',
        'backend/graph/nodes/feature_engineer.py'
    ]
    
    success_count = 0
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_imports_in_file(file_path):
                success_count += 1
        else:
            print(f"⚠️ 文件不存在: {file_path}")
    
    print(f"\n🎉 修复完成！成功修复: {success_count}/{len(files_to_fix)} 个文件")
    
    # 测试导入
    print("\n🧪 测试导入...")
    try:
        from backend.app import app
        print("✅ 应用导入成功！")
        return True
    except Exception as e:
        print(f"❌ 应用导入失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 现在可以启动应用了！")
        print("运行: uvicorn.run(app, host='0.0.0.0', port=8000)")
    else:
        print("\n⚠️ 修复失败，请检查错误信息")
