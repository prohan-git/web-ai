# Web AI 前端

这是 Web AI 工具箱的前端项目，提供了电商和社交媒体分析工具的用户界面。

## 功能特点

- 电商运营工具
  - 产品搜索分析
  - 上货素材生成
  - 竞品分析
  - 供应商查找
  - 产品潜力评估
- 社交媒体工具 (待开发)
  - 创作者数据分析
  - 内容趋势发现
  - 创作灵感收集
- 智能对话 (待开发)
- 任务代理 (待开发)

## 技术栈

- React 18
- React Router 6
- Ant Design 5
- Axios

## 开发运行

### 安装依赖

```
npm install
```

### 开发模式运行

```
npm start
```

开发服务器会在 [http://localhost:3000](http://localhost:3000) 运行。

### 构建生产版本

```
npm run build
```

构建文件将输出到 `build` 文件夹。

## 项目结构

```
frontend/
  ├── public/                 # 静态资源
  ├── src/                    # 源代码
  │   ├── components/         # 通用组件
  │   ├── pages/              # 页面组件
  │   ├── services/           # API服务
  │   ├── App.jsx             # 应用主组件
  │   ├── index.jsx           # 入口文件
  │   └── index.css           # 全局样式
  ├── package.json            # 项目依赖配置
  └── README.md               # 项目说明
```

## API 接口

前端通过 `/api/ai` 前缀与后端API进行通信。详细API文档请参考后端项目的 README.md 文件。 