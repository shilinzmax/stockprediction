#!/usr/bin/env python3
"""
修复导入路径脚本
将所有相对导入改为绝对导入
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

if __name__ == "__main__":
    main()
