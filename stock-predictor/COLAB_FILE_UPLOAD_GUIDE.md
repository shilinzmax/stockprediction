# 📁 Colab文件上传指南

## 🚨 解决 "ModuleNotFoundError: No module named 'backend'" 错误

这个错误是因为在Colab中还没有上传你的项目文件。以下是详细的解决步骤：

## 📋 步骤1: 准备项目文件

确保你的项目结构如下：
```
stock-predictor/
├── backend/
│   ├── app.py
│   ├── core/
│   ├── graph/
│   └── requirements.txt
├── frontend/
└── README.md
```

## 📤 步骤2: 上传文件到Colab

### 方法1: 手动上传（推荐）

1. **打开Colab文件面板**
   - 点击左侧的文件夹图标 📁
   - 或者使用快捷键 `Ctrl+Shift+F`

2. **上传项目文件**
   - 点击"上传到会话存储"按钮
   - 选择整个项目文件夹
   - 等待上传完成

3. **验证上传**
   - 检查是否能看到 `backend/` 文件夹
   - 确认 `backend/app.py` 文件存在

### 方法2: 从GitHub克隆

如果你已经将项目推送到GitHub：

```python
# 克隆项目
!git clone https://github.com/your-username/stock-predictor.git

# 进入项目目录
%cd stock-predictor

# 验证文件结构
!ls -la
!ls -la backend/
```

### 方法3: 使用Google Drive

1. **上传到Google Drive**
   - 将项目文件夹上传到Google Drive
   - 确保文件夹结构正确

2. **挂载Drive**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

3. **复制文件**
   ```python
   !cp -r /content/drive/MyDrive/stock-predictor /content/
   %cd stock-predictor
   ```

## 🔍 步骤3: 验证文件结构

运行以下代码检查文件是否正确上传：

```python
import os

# 检查项目结构
def check_project_structure():
    required_files = [
        'backend/app.py',
        'backend/core/llm.py',
        'backend/core/state.py',
        'backend/graph/pipeline.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少以下文件:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ 所有必要文件都已上传")
        return True

# 运行检查
check_project_structure()
```

## 🚀 步骤4: 启动应用

文件上传完成后，运行以下代码启动应用：

```python
# 启动FastAPI应用
import uvicorn
import os

# 检查项目文件是否存在
if not os.path.exists('backend'):
    print("❌ 错误: 未找到backend文件夹")
    print("📁 请先上传项目文件到Colab")
else:
    try:
        from backend.app import app
        
        print("🚀 启动股票预测应用...")
        print("📱 应用将在 http://localhost:8000 启动")
        print("📊 API文档: http://localhost:8000/docs")
        
        # 启动服务器
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("📁 请确保backend文件夹包含所有必要的Python文件")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
```

## 🔧 故障排除

### 问题1: 文件上传失败
**解决方案:**
- 检查网络连接
- 尝试分批上传文件
- 使用Google Drive作为中转

### 问题2: 文件结构不正确
**解决方案:**
```python
# 重新组织文件结构
!mkdir -p backend
!mv *.py backend/ 2>/dev/null || true
!mv core backend/ 2>/dev/null || true
!mv graph backend/ 2>/dev/null || true
```

### 问题3: 权限问题
**解决方案:**
```python
# 设置文件权限
!chmod -R 755 backend/
!chmod -R 755 frontend/
```

### 问题4: 路径问题
**解决方案:**
```python
# 添加当前目录到Python路径
import sys
sys.path.append('/content')
sys.path.append('/content/stock-predictor')
```

## 📝 完整的上传和启动流程

```python
# 1. 检查文件是否存在
import os
if os.path.exists('backend'):
    print("✅ 项目文件已上传")
else:
    print("❌ 请先上传项目文件")
    print("💡 使用左侧文件面板上传整个项目文件夹")

# 2. 设置Python路径
import sys
sys.path.append('/content')

# 3. 启动应用
if os.path.exists('backend'):
    try:
        from backend.app import app
        import uvicorn
        
        print("🚀 启动应用...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
```

## 💡 提示

1. **文件大小限制**: Colab有文件大小限制，大文件可能需要压缩
2. **会话持久性**: 文件在会话结束后会丢失，重要数据请保存到Drive
3. **网络访问**: 确保可以访问外部API获取股票数据
4. **内存使用**: 监控内存使用情况，避免超出限制

按照这些步骤操作，你应该能够成功在Colab中运行股票预测系统！
