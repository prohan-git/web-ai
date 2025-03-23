# Web AI 工具集

Web AI 工具集是一个综合性的网络数据分析与内容创作平台，利用人工智能技术提供电商分析、社交媒体数据收集与分析、AI对话等功能。

## 功能特点

### 电商工具
- 产品搜索：在主流电商平台搜索产品
- 上架列表生成：自动生成产品上架的详细描述
- 竞争分析：分析同类产品的竞争状况
- 供应商搜索：查找产品的潜在供应商
- 产品潜力分析：评估产品的市场潜力

### 社交媒体工具
- 数据收集：收集各平台的内容和创作者数据
- 趋势分析：分析各领域的热门趋势
- 内容创意：生成创意内容建议
- 创作者分析：分析创作者的内容风格和表现
- 灵感收集：从多个平台收集创作灵感

### AI助手
- 智能对话：与AI进行实时对话
- 任务指导：获取任务执行的建议和指导

### 任务管理
- 任务创建与管理：创建、监控和管理各类AI任务
- 任务状态跟踪：跟踪任务执行状态和结果

## 技术栈

### 前端
- React.js
- Ant Design
- React Router
- Axios

### 后端
- FastAPI
- Langchain
- DeepSeek API
- browser-use (浏览器自动化库)

## 系统架构

系统采用前后端分离的架构：

1. **前端**：React单页应用，负责用户交互和数据展示
2. **后端API**：FastAPI提供RESTful API服务
3. **AI代理**：基于浏览器的AI代理系统，用于网络数据采集和分析
4. **LLM服务**：通过DeepSeek等大型语言模型提供智能分析能力

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端启动

```bash
cd frontend
npm install
npm start
```

## 开发计划

- [x] 基础框架搭建
- [x] 电商分析工具
- [x] 社交媒体分析工具
- [x] AI对话功能
- [x] 任务管理系统
- [ ] 数据可视化功能
- [ ] 批量任务处理
- [ ] 用户系统与权限管理
- [ ] 移动端适配

## 贡献指南

欢迎贡献代码或提出建议！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可从证 - 详情参见 LICENSE 