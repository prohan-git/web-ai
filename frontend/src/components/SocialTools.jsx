import React, { useState } from 'react';
import { Card, Tabs, Form, Input, Button, Select, InputNumber, Spin, Typography, Alert, Divider, Tag, List, Space } from 'antd';
import { SearchOutlined, LoadingOutlined, UserOutlined, LikeOutlined, CommentOutlined, LineChartOutlined } from '@ant-design/icons';
import apiService from '../services/api';

const { Title, Text, Paragraph } = Typography;
const { TabPane } = Tabs;
const { Option } = Select;
const { TextArea } = Input;

// 平台常量
const PLATFORMS = ["小红书", "Instagram", "Pinterest", "Twitter", "微博", "抖音", "TikTok", "YouTube"];

// 平台任务类型映射
const PLATFORM_TASKS = {
  "小红书": ["热门话题", "用户笔记", "关键词搜索", "高赞内容", "行业达人", "内容趋势"],
  "Instagram": ["用户帖子", "热门标签", "同类账号", "增长账号", "互动分析"],
  "Pinterest": ["收集灵感板", "趋势搜索", "相关灵感板"],
  "抖音": ["热门挑战", "创作者分析", "热门音乐"],
  "TikTok": ["趋势分析", "创作者搜索"],
  "YouTube": ["频道分析", "视频评论", "相关视频"]
};

// 通用时间段选项
const TIME_PERIODS = ["今日", "本周", "本月", "本季度", "今年"];

const SocialTools = () => {
  const [selectedPlatform, setSelectedPlatform] = useState(PLATFORMS[0]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // 重置状态
  const resetStates = () => {
    setLoading(false);
    setResult(null);
    setError(null);
  };

  // 收集社交媒体数据
  const handleCollectData = async (values) => {
    resetStates();
    setLoading(true);

    try {
      const response = await apiService.social.collect(
        values.platform,
        values.task_type,
        values.params,
        values.use_vision !== false
      );

      if (response.status === 'success') {
        setResult(response);
      } else {
        setError(response.message || '收集数据失败');
      }
    } catch (error) {
      setError(error.message || '请求失败');
    } finally {
      setLoading(false);
    }
  };

  // 查找热门内容
  const handleFindTrending = async (values) => {
    resetStates();
    setLoading(true);

    try {
      const response = await apiService.social.findTrendingContent(
        values.platform,
        values.niche,
        values.count,
        values.time_period,
        values.use_vision !== false
      );

      if (response.status === 'success') {
        setResult(response);
      } else {
        setError(response.message || '查找热门内容失败');
      }
    } catch (error) {
      setError(error.message || '请求失败');
    } finally {
      setLoading(false);
    }
  };

  // 分析创作者
  const handleAnalyzeCreator = async (values) => {
    resetStates();
    setLoading(true);

    try {
      const response = await apiService.social.analyzeCreator(
        values.platform,
        values.creator,
        values.use_vision !== false
      );

      if (response.status === 'success') {
        setResult(response);
      } else {
        setError(response.message || '创作者分析失败');
      }
    } catch (error) {
      setError(error.message || '请求失败');
    } finally {
      setLoading(false);
    }
  };

  // 生成内容创作灵感
  const handleGenerateIdeas = async (values) => {
    resetStates();
    setLoading(true);

    try {
      // 将逗号分隔的关键词转为数组
      const keywords = values.keywords.split(',').map(k => k.trim());
      
      const response = await apiService.social.generateContentIdeas(
        values.platform,
        values.niche,
        keywords,
        values.count
      );

      if (response.status === 'success') {
        setResult(response);
      } else {
        setError(response.message || '生成内容灵感失败');
      }
    } catch (error) {
      setError(error.message || '请求失败');
    } finally {
      setLoading(false);
    }
  };

  // 收集创意灵感
  const handleCollectInspiration = async (values) => {
    resetStates();
    setLoading(true);

    try {
      // 将逗号分隔的关键词和来源转为数组
      const keywords = values.keywords.split(',').map(k => k.trim());
      const sources = values.sources.split(',').map(s => s.trim());
      
      const response = await apiService.social.collectInspiration(
        keywords,
        sources,
        values.count_per_source,
        values.use_vision !== false
      );

      if (response.status === 'success') {
        setResult(response);
      } else {
        setError(response.message || '收集灵感失败');
      }
    } catch (error) {
      setError(error.message || '请求失败');
    } finally {
      setLoading(false);
    }
  };

  // 获取特定平台的任务类型选项
  const getTaskTypeOptions = (platform) => {
    return PLATFORM_TASKS[platform] || [];
  };

  // 渲染结果
  const renderResult = () => {
    if (loading) {
      return (
        <div className="loading-container">
          <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} />
          <Text style={{ marginLeft: 10 }}>正在处理，请稍候...</Text>
        </div>
      );
    }

    if (error) {
      return <Alert message="错误" description={error} type="error" showIcon />;
    }

    if (!result) {
      return null;
    }

    // 尝试将结果解析为JSON
    let jsonResult = null;
    try {
      if (typeof result.result === 'string' && result.result.trim().startsWith('{')) {
        jsonResult = JSON.parse(result.result);
      } else if (typeof result.result === 'object') {
        jsonResult = result.result;
      }
    } catch (e) {
      // 解析失败，使用原始文本
    }

    return (
      <Card title="结果" style={{ marginTop: 16 }}>
        <Paragraph>
          <Text strong>状态: </Text>
          <Tag color={result.status === 'success' ? 'success' : 'error'}>
            {result.status === 'success' ? '成功' : '失败'}
          </Tag>
        </Paragraph>
        
        {jsonResult ? (
          <div>
            <Title level={4}>分析结果</Title>
            <pre>{JSON.stringify(jsonResult, null, 2)}</pre>
          </div>
        ) : (
          <div>
            <Title level={4}>返回内容</Title>
            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
              {result.result}
            </pre>
          </div>
        )}
      </Card>
    );
  };

  return (
    <div>
      <Title level={2}>社交媒体工具</Title>
      <Paragraph>使用AI助手分析社交媒体平台数据，发现趋势，分析竞争对手，获取创作灵感。</Paragraph>
      
      <Tabs defaultActiveKey="trending">
        <TabPane tab="热门内容查找" key="trending">
          <Card title="查找热门/趋势内容">
            <Form layout="vertical" onFinish={handleFindTrending}>
              <Form.Item
                name="platform"
                label="平台"
                rules={[{ required: true, message: '请选择平台' }]}
                initialValue={selectedPlatform}
              >
                <Select onChange={(value) => setSelectedPlatform(value)}>
                  {PLATFORMS.map(platform => (
                    <Option key={platform} value={platform}>{platform}</Option>
                  ))}
                </Select>
              </Form.Item>
              
              <Form.Item
                name="niche"
                label="类目/领域"
                rules={[{ required: true, message: '请输入类目/领域' }]}
              >
                <Input placeholder="如: 美妆、健身、美食、旅行等" />
              </Form.Item>
              
              <Form.Item
                name="count"
                label="结果数量"
                initialValue={10}
              >
                <InputNumber min={1} max={20} />
              </Form.Item>
              
              <Form.Item
                name="time_period"
                label="时间范围"
                initialValue="本周"
              >
                <Select>
                  {TIME_PERIODS.map(period => (
                    <Option key={period} value={period}>{period}</Option>
                  ))}
                </Select>
              </Form.Item>
              
              <Form.Item
                name="use_vision"
                label="使用视觉功能"
                initialValue={true}
                valuePropName="checked"
              >
                <Select>
                  <Option value={true}>是</Option>
                  <Option value={false}>否</Option>
                </Select>
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} icon={<SearchOutlined />}>
                  查找热门内容
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        <TabPane tab="创作者分析" key="creator">
          <Card title="创作者分析">
            <Form layout="vertical" onFinish={handleAnalyzeCreator}>
              <Form.Item
                name="platform"
                label="平台"
                rules={[{ required: true, message: '请选择平台' }]}
                initialValue={selectedPlatform}
              >
                <Select onChange={(value) => setSelectedPlatform(value)}>
                  {PLATFORMS.map(platform => (
                    <Option key={platform} value={platform}>{platform}</Option>
                  ))}
                </Select>
              </Form.Item>
              
              <Form.Item
                name="creator"
                label="创作者用户名"
                rules={[{ required: true, message: '请输入创作者用户名' }]}
              >
                <Input placeholder="输入创作者的用户名/账号" prefix={<UserOutlined />} />
              </Form.Item>
              
              <Form.Item
                name="use_vision"
                label="使用视觉功能"
                initialValue={true}
              >
                <Select>
                  <Option value={true}>是</Option>
                  <Option value={false}>否</Option>
                </Select>
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} icon={<LineChartOutlined />}>
                  分析创作者
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        <TabPane tab="内容灵感生成" key="ideas">
          <Card title="内容创作灵感生成">
            <Form layout="vertical" onFinish={handleGenerateIdeas}>
              <Form.Item
                name="platform"
                label="平台"
                rules={[{ required: true, message: '请选择平台' }]}
                initialValue={selectedPlatform}
              >
                <Select onChange={(value) => setSelectedPlatform(value)}>
                  {PLATFORMS.map(platform => (
                    <Option key={platform} value={platform}>{platform}</Option>
                  ))}
                </Select>
              </Form.Item>
              
              <Form.Item
                name="niche"
                label="内容领域"
                rules={[{ required: true, message: '请输入内容领域' }]}
              >
                <Input placeholder="如: 美妆教程、健身知识、旅行攻略等" />
              </Form.Item>
              
              <Form.Item
                name="keywords"
                label="关键词 (用逗号分隔)"
                rules={[{ required: true, message: '请输入至少一个关键词' }]}
              >
                <Input placeholder="例如: 夏季穿搭,清新风格,日常搭配" />
              </Form.Item>
              
              <Form.Item
                name="count"
                label="创意数量"
                initialValue={10}
              >
                <InputNumber min={1} max={20} />
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  生成内容灵感
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        <TabPane tab="灵感收集" key="inspiration">
          <Card title="多平台创意灵感收集">
            <Form layout="vertical" onFinish={handleCollectInspiration}>
              <Form.Item
                name="keywords"
                label="关键词 (用逗号分隔)"
                rules={[{ required: true, message: '请输入至少一个关键词' }]}
              >
                <Input placeholder="例如: 简约风格,室内设计,北欧风" />
              </Form.Item>
              
              <Form.Item
                name="sources"
                label="来源平台 (用逗号分隔)"
                initialValue="Pinterest,Instagram"
                rules={[{ required: true, message: '请输入至少一个来源平台' }]}
              >
                <Input placeholder="例如: Pinterest,Instagram,Dribbble" />
              </Form.Item>
              
              <Form.Item
                name="count_per_source"
                label="每个来源获取数量"
                initialValue={5}
              >
                <InputNumber min={1} max={10} />
              </Form.Item>
              
              <Form.Item
                name="use_vision"
                label="使用视觉功能"
                initialValue={true}
              >
                <Select>
                  <Option value={true}>是</Option>
                  <Option value={false}>否</Option>
                </Select>
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  收集灵感
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        <TabPane tab="数据收集" key="collect">
          <Card title="从社交平台收集数据">
            <Form layout="vertical" onFinish={handleCollectData}>
              <Form.Item
                name="platform"
                label="平台"
                rules={[{ required: true, message: '请选择平台' }]}
                initialValue={selectedPlatform}
              >
                <Select onChange={(value) => setSelectedPlatform(value)}>
                  {PLATFORMS.map(platform => (
                    <Option key={platform} value={platform}>{platform}</Option>
                  ))}
                </Select>
              </Form.Item>
              
              <Form.Item
                name="task_type"
                label="任务类型"
                rules={[{ required: true, message: '请选择任务类型' }]}
              >
                <Select>
                  {getTaskTypeOptions(selectedPlatform).map(task => (
                    <Option key={task} value={task}>{task}</Option>
                  ))}
                </Select>
              </Form.Item>
              
              <Form.Item
                name="params"
                label="参数 (JSON格式)"
                rules={[{ required: true, message: '请输入参数' }]}
                initialValue="{}"
              >
                <TextArea 
                  rows={4} 
                  placeholder='{"count": 5, "keywords": "关键词"}'
                />
              </Form.Item>
              
              <Form.Item
                name="use_vision"
                label="使用视觉功能"
                initialValue={true}
              >
                <Select>
                  <Option value={true}>是</Option>
                  <Option value={false}>否</Option>
                </Select>
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  收集数据
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
      </Tabs>
      
      {renderResult()}
    </div>
  );
};

export default SocialTools; 