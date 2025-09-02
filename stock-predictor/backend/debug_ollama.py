#!/usr/bin/env python3
"""
调试Ollama API
"""
import ollama

def debug_ollama():
    """调试Ollama API"""
    print("🔍 调试Ollama API...")
    
    try:
        # 检查模型列表
        models = ollama.list()
        print(f"📋 模型列表原始数据: {models}")
        print(f"📋 模型列表类型: {type(models)}")
        
        if 'models' in models:
            print(f"📋 模型数量: {len(models['models'])}")
            for i, model in enumerate(models['models']):
                print(f"📋 模型 {i}: {model}")
                print(f"📋 模型 {i} 类型: {type(model)}")
                if isinstance(model, dict):
                    print(f"📋 模型 {i} 键: {model.keys()}")
        
        # 测试直接调用
        print("\n🧪 测试直接调用...")
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=[{'role': 'user', 'content': 'Hello, how are you?'}]
        )
        print(f"✅ 直接调用成功: {response}")
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ollama()

