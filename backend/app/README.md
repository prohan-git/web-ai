# AI 代理与浏览器自动化服务

本项目提供了一套强大的 AI 代理服务，可以执行多种任务，包括对话、浏览器自动化任务、社交媒体数据分析等。

## 功能特点

- 基础 AI 对话功能
- 浏览器自动化任务执行
- 预定义任务模板支持
- 社交媒体数据收集与分析
- 舆情监控与数据分析

## API 接口说明

### 基础对话接口

用于与 AI 进行简单对话。

```
POST /api/v1/ai/chat
```

请求参数：

```json
{
  "message": "你好，请问你是谁？"
}
```

返回示例：

```json
{
  "response": "你好！我是一个 AI 助手，可以帮助你回答问题、执行任务或者进行对话。有什么我可以帮助你的吗？"
}
```

### 浏览器任务执行接口

用于执行特定的浏览器自动化任务。

```
POST /api/v1/ai/task
```

请求参数：

```json
{
  "task": "搜索关于人工智能的最新新闻并总结前3条",
  "use_vision": true
}
```

返回示例：

```json
{
  "status": "success",
  "message": "任务执行成功",
  "result": "1. 谷歌发布最新AI模型Gemini - 据报道，该模型在多项基准测试中超越了GPT-4...\n2. ...",
  "task": "搜索关于人工智能的最新新闻并总结前3条",
  "use_vision": true
}
```

### 模板任务执行接口

使用预定义的任务模板执行任务。

```
POST /api/v1/ai/task/template
```

请求参数：

```json
{
  "template_name": "网页搜索",
  "template_params": {
    "query": "气候变化最新研究"
  },
  "use_vision": true
}
```

返回示例：

```json
{
  "status": "success",
  "message": "任务执行成功",
  "result": "...",
  "task": "搜索以下内容并返回前三个结果的摘要: 气候变化最新研究",
  "use_vision": true
}
```

### 社交媒体数据收集接口

从特定社交媒体平台收集数据。

```
POST /api/v1/ai/social/collect
```

请求参数：

```json
{
  "platform": "小红书",
  "task_type": "热门话题",
  "params": {
    "count": 5
  },
  "use_vision": true
}
```

返回示例：

```json
{
  "status": "success",
  "message": "任务执行成功",
  "result": "...",
  "platform": "小红书",
  "task_type": "热门话题"
}
```

### 舆情监控接口

监控多个平台上关于特定关键词的舆情。

```
POST /api/v1/ai/social/monitor
```

请求参数：

```json
{
  "keywords": ["新能源汽车", "电动车"],
  "platforms": ["微博", "小红书"]
}
```

返回示例：

```json
{
  "status": "success",
  "message": "舆情监控完成",
  "keywords": ["新能源汽车", "电动车"],
  "platforms": ["微博", "小红书"],
  "results": {
    "微博": "...",
    "小红书": "..."
  },
  "errors": []
}
```

### 数据分析接口

分析已收集的数据。

```
POST /api/v1/ai/social/analyze
```

请求参数：

```json
{
  "data": "...(收集到的数据)...",
  "analysis_type": "sentiment"
}
```

返回示例：

```json
{
  "status": "success",
  "message": "数据分析完成",
  "analysis_type": "sentiment",
  "result": "..."
}
```

## 支持的社交媒体平台

- 小红书
- Instagram
- Pinterest
- Twitter
- 微博

## 支持的任务类型

### 小红书

- 热门话题
- 用户笔记
- 关键词搜索

### Instagram

- 用户帖子
- 热门标签

### Pinterest

- 收集灵感板

## 支持的数据分析类型

- sentiment: 情感分析
- topics: 主题提取
- trends: 趋势分析

## 使用示例

### 1. 收集小红书热门话题

```python
import requests
import json

url = "http://localhost:8000/api/v1/ai/social/collect"
payload = {
    "platform": "小红书",
    "task_type": "热门话题",
    "params": {
        "count": 5
    },
    "use_vision": true
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

### 2. 监控多平台舆情

```python
import requests
import json

url = "http://localhost:8000/api/v1/ai/social/monitor"
payload = {
    "keywords": ["新能源汽车", "电动车"],
    "platforms": ["微博", "小红书"]
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

### 3. 执行模板任务

```python
import requests
import json

url = "http://localhost:8000/api/v1/ai/task/template"
payload = {
    "template_name": "网页搜索",
    "template_params": {
        "query": "2023年最新科技趋势"
    },
    "use_vision": true
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

## 注意事项

1. 使用视觉功能（use_vision=true）可能会增加任务执行时间，但可以提高数据收集的准确性
2. 对于社交媒体数据收集，可能需要考虑平台的访问限制和隐私政策
3. 舆情监控任务可能需要较长时间执行，建议设置合理的超时时间 