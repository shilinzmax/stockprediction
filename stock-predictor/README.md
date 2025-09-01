# Stock Predictor - AI驱动的股票预测系统

一个基于 LangGraph 工作流的全栈股票预测系统，提供实时股票数据展示、AI驱动的走势预测和投资建议。

## 🎯 功能特性

### 核心功能
- **股票数据展示**: 实时获取和展示股票OHLCV数据、技术指标
- **AI预测分析**: 基于LangGraph工作流的智能预测（1小时/1天/1周）
- **Top 10推荐**: AI生成的股票投资建议列表
- **技术指标**: RSI、MACD、布林带、移动平均线等
- **支撑阻力位**: 自动计算关键价格位置

### 技术栈
- **后端**: Python 3.11 + FastAPI + LangGraph + LangChain
- **前端**: React 18 + TypeScript + TailwindCSS + Recharts
- **AI模型**: OpenAI GPT-3.5-turbo (可配置Mock LLM)
- **数据源**: yfinance (Yahoo Finance)
- **缓存**: 本地Parquet文件缓存

## 🚀 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- pnpm 或 npm

### 一键启动开发环境

```bash
# 克隆项目
git clone <repository-url>
cd stock-predictor

# 一键启动（自动安装依赖并启动前后端服务）
./start_dev.sh
```

启动后访问：
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 手动安装和启动

#### 后端设置
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选）
cp env.example .env
# 编辑 .env 文件，添加 OPENAI_API_KEY

# 启动后端服务
python app.py
```

#### 前端设置
```bash
cd frontend

# 安装依赖
pnpm install  # 或 npm install

# 启动开发服务器
pnpm run dev  # 或 npm run dev
```

## 🐳 Docker 部署

### 使用 Docker Compose
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 单独构建服务
```bash
# 构建后端
docker build -t stock-predictor-backend ./backend

# 构建前端
docker build -t stock-predictor-frontend ./frontend
```

## 📊 系统架构

### LangGraph 工作流
```
数据获取 → 特征工程 → LLM分析 → 建议生成 → 报告输出
    ↓         ↓         ↓         ↓         ↓
FetchData → FeatureEng → LLMAnalyze → MakeAdvice → Report
```

### 核心模块
- **数据获取**: yfinance API + 本地缓存
- **技术指标**: ta-lib 技术分析库
- **AI分析**: OpenAI GPT-3.5-turbo / Mock LLM
- **预测引擎**: LangGraph 状态机工作流
- **前端展示**: React + Recharts 图表

## 🔧 配置说明

### 环境变量
```bash
# OpenAI API Key (可选，没有会自动使用Mock LLM)
OPENAI_API_KEY=your_api_key_here

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 缓存配置
CACHE_DIR=data
CACHE_TTL_HOURS=1
```

### Mock LLM 模式
如果没有配置 OpenAI API Key，系统会自动启用 Mock LLM 模式：
- 基于技术指标生成模拟预测结果
- 提供稳定的测试数据
- 完全可用的演示功能

## 📈 使用指南

### 1. 股票搜索
- 在搜索框输入股票代码（如 AAPL、MSFT、TSLA）
- 支持自动补全和搜索建议
- 点击搜索结果快速选择

### 2. 数据查看
- 查看最近30天的OHLCV数据
- 技术指标实时计算和展示
- 支撑位和阻力位自动标注

### 3. AI预测
- 点击"预测"按钮进行AI分析
- 支持1小时、1天、1周三个时间框架
- 显示预测方向、概率、价格区间和置信度

### 4. 投资建议
- 查看AI生成的Top 10股票推荐
- 包含预期方向、概率、理由和风险等级
- 定期刷新获取最新建议

## ⚠️ 重要声明

**本系统仅用于学习研究目的，所有分析结果和预测数据不构成投资建议。**

- 股票投资存在风险，过往表现不代表未来收益
- 请根据自身风险承受能力谨慎投资
- 建议咨询专业投资顾问
- AI预测存在不确定性，请理性对待预测结果

## 🛠️ 开发指南

### 项目结构
```
stock-predictor/
├── backend/                 # 后端服务
│   ├── app.py              # FastAPI 主应用
│   ├── core/               # 核心模块
│   │   ├── state.py        # 数据模型
│   │   ├── utils.py        # 工具函数
│   │   ├── indicators.py   # 技术指标
│   │   └── llm.py          # LLM 分析器
│   ├── graph/              # LangGraph 工作流
│   │   ├── pipeline.py     # 主工作流
│   │   └── nodes/          # 工作流节点
│   └── data/               # 数据缓存目录
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # React 组件
│   │   ├── pages/          # 页面组件
│   │   └── lib/            # 工具库
│   └── public/             # 静态资源
└── docker-compose.yml      # Docker 配置
```

### API 接口
- `GET /api/stock/{symbol}` - 获取股票数据
- `POST /api/predict` - 预测股票走势
- `GET /api/top-stocks` - 获取Top 10推荐
- `GET /api/search/{query}` - 搜索股票

### 扩展开发
1. **添加新的技术指标**: 在 `core/indicators.py` 中扩展
2. **自定义LLM分析**: 修改 `core/llm.py` 中的分析逻辑
3. **新增工作流节点**: 在 `graph/nodes/` 中创建新节点
4. **前端组件扩展**: 在 `frontend/src/components/` 中添加组件

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- 🎯 完整的股票预测工作流
- 📊 实时数据展示和图表
- 🤖 AI驱动的预测分析
- 🐳 Docker 容器化支持

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Python Web框架
- [React](https://reactjs.org/) - 用户界面库
- [yfinance](https://github.com/ranaroussi/yfinance) - 股票数据API
- [Recharts](https://recharts.org/) - React图表库

---

**免责声明**: 本系统仅用于学习研究目的，不构成投资建议。投资有风险，入市需谨慎。
