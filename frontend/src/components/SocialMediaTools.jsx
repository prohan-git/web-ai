import React, { useState } from 'react';
import { Card, Tabs, Form, Input, Button, Select, InputNumber, Spin, Typography, Alert, Divider } from 'antd';
import apiService from '../services/api';

const { Title, Text, Paragraph } = Typography;
const { TabPane } = Tabs;
const { Option } = Select;
const { TextArea } = Input;

// 常量定义
const SOCIAL_PLATFORMS = ['Instagram', 'TikTok', '小红书', 'Pinterest', 'YouTube', '抖音', 'Twitter'];
const ANALYSIS_TYPES = ['内容分析', '受众分析', '趋势分析', '竞争分析', '增长策略'];

// 社交媒体工具组件
const SocialMediaTools = () => {
  // 状态管理
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [selectedPlatform, setSelectedPlatform] = useState('Instagram');

  // 数据收集表单提交
  const handleCollectData = async (values) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.collectSocialData({
        platform: values.platform,
        contentType: values.contentType,
        keywords: values.keywords,
        creator: values.creator,
        count: values.count,
        useVision: true
      });
      setResults(response);
    } catch (error) {
      setError(error.response?.data?.message || '请求失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 趋势分析表单提交
  const handleAnalyzeTrends = async (values) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.analyzeSocialTrends({
        platform: values.platform,
        niche: values.niche,
        timeframe: values.timeframe,
        count: values.count
      });
      setResults(response);
    } catch (error) {
      setError(error.response?.data?.message || '请求失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 内容创意表单提交
  const handleGenerateIdeas = async (values) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.generateContentIdeas({
        platform: values.platform,
        niche: values.niche,
        keywords: values.keywords.split(',').map(k => k.trim()),
        targetAudience: values.targetAudience,
        contentType: values.contentType,
        count: values.count
      });
      setResults(response);
    } catch (error) {
      setError(error.response?.data?.message || '请求失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 创作者分析表单提交
  const handleAnalyzeCreator = async (values) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.collectSocialData({
        platform: values.platform,
        contentType: 'creator_analysis',
        creator: values.creator,
        analysisType: values.analysisType
      });
      setResults(response);
    } catch (error) {
      setError(error.response?.data?.message || '请求失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 灵感收集表单提交
  const handleCollectInspiration = async (values) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.collectSocialData({
        contentType: 'inspiration',
        keywords: values.keywords.split(',').map(k => k.trim()),
        platforms: values.platforms,
        count: values.count
      });
      setResults(response);
    } catch (error) {
      setError(error.response?.data?.message || '请求失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 渲染结果区域
  const renderResults = () => {
    if (loading) {
      return (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin size="large" />
          <Paragraph style={{ marginTop: '10px' }}>正在处理请求，请稍候...</Paragraph>
        </div>
      );
    }

    if (error) {
      return <Alert message="错误" description={error} type="error" showIcon />;
    }

    if (!results) {
      return null;
    }

    return (
      <div className="results-container">
        <Title level={4}>结果</Title>
        <Divider />
        {results.status === 'success' ? (
          <>
            {results.result && (
              <Paragraph>
                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                  {results.result}
                </pre>
              </Paragraph>
            )}
            {results.data && Array.isArray(results.data) && (
              <ul>
                {results.data.map((item, index) => (
                  <li key={index}>
                    <Text strong>{item.title || item.creator || item.content || `项目 ${index + 1}`}</Text>
                    <Paragraph>{item.description || item.content}</Paragraph>
                    {item.url && (
                      <Text type="secondary">
                        <a href={item.url} target="_blank" rel="noopener noreferrer">
                          查看原始内容
                        </a>
                      </Text>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </>
        ) : (
          <Alert message="请求未成功" description={results.message} type="warning" showIcon />
        )}
      </div>
    );
  };

  return (
    <Card title="社交媒体数据工具" style={{ marginBottom: '24px' }}>
      <Tabs defaultActiveKey="collect" onChange={() => setResults(null)}>
        <TabPane tab="数据收集" key="collect">
          <Form layout="vertical" onFinish={handleCollectData}>
            <Form.Item name="platform" label="平台" initialValue={selectedPlatform} rules={[{ required: true, message: '请选择平台' }]}>
              <Select onChange={(value) => setSelectedPlatform(value)}>
                {SOCIAL_PLATFORMS.map(platform => (
                  <Option key={platform} value={platform}>{platform}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="contentType" label="内容类型" initialValue="trending" rules={[{ required: true, message: '请选择内容类型' }]}>
              <Select>
                <Option value="trending">热门内容</Option>
                <Option value="user_posts">用户发布内容</Option>
                <Option value="hashtag">标签内容</Option>
                <Option value="topic">主题内容</Option>
              </Select>
            </Form.Item>
            <Form.Item name="keywords" label="关键词" rules={[{ required: true, message: '请输入关键词' }]}>
              <Input placeholder="例如：数码评测、旅行摄影" />
            </Form.Item>
            <Form.Item name="creator" label="创作者" dependencies={['contentType']} 
              rules={[({ getFieldValue }) => ({
                required: getFieldValue('contentType') === 'user_posts',
                message: '请输入创作者用户名',
              })]}>
              <Input placeholder="创作者用户名" />
            </Form.Item>
            <Form.Item name="count" label="数量" initialValue={5}>
              <InputNumber min={1} max={20} />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading}>
                收集数据
              </Button>
            </Form.Item>
          </Form>
        </TabPane>

        <TabPane tab="趋势分析" key="trends">
          <Form layout="vertical" onFinish={handleAnalyzeTrends}>
            <Form.Item name="platform" label="平台" initialValue={selectedPlatform} rules={[{ required: true, message: '请选择平台' }]}>
              <Select onChange={(value) => setSelectedPlatform(value)}>
                {SOCIAL_PLATFORMS.map(platform => (
                  <Option key={platform} value={platform}>{platform}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="niche" label="领域" rules={[{ required: true, message: '请输入领域' }]}>
              <Input placeholder="例如：美妆、科技、健身" />
            </Form.Item>
            <Form.Item name="timeframe" label="时间段" initialValue="本周">
              <Select>
                <Option value="今日">今日</Option>
                <Option value="本周">本周</Option>
                <Option value="本月">本月</Option>
                <Option value="本季度">本季度</Option>
              </Select>
            </Form.Item>
            <Form.Item name="count" label="数量" initialValue={10}>
              <InputNumber min={1} max={20} />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading}>
                分析趋势
              </Button>
            </Form.Item>
          </Form>
        </TabPane>

        <TabPane tab="内容创意" key="ideas">
          <Form layout="vertical" onFinish={handleGenerateIdeas}>
            <Form.Item name="platform" label="平台" initialValue={selectedPlatform} rules={[{ required: true, message: '请选择平台' }]}>
              <Select onChange={(value) => setSelectedPlatform(value)}>
                {SOCIAL_PLATFORMS.map(platform => (
                  <Option key={platform} value={platform}>{platform}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="niche" label="领域" rules={[{ required: true, message: '请输入领域' }]}>
              <Input placeholder="例如：美妆、科技、健身" />
            </Form.Item>
            <Form.Item name="keywords" label="关键词" rules={[{ required: true, message: '请输入关键词，多个关键词用逗号分隔' }]}>
              <Input placeholder="关键词1, 关键词2, 关键词3" />
            </Form.Item>
            <Form.Item name="targetAudience" label="目标受众">
              <Input placeholder="例如：18-24岁女性，对美妆感兴趣" />
            </Form.Item>
            <Form.Item name="contentType" label="内容类型" initialValue="混合">
              <Select>
                <Option value="混合">混合</Option>
                <Option value="图文">图文</Option>
                <Option value="短视频">短视频</Option>
                <Option value="直播">直播</Option>
              </Select>
            </Form.Item>
            <Form.Item name="count" label="创意数量" initialValue={5}>
              <InputNumber min={1} max={10} />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading}>
                生成创意
              </Button>
            </Form.Item>
          </Form>
        </TabPane>

        <TabPane tab="创作者分析" key="creator">
          <Form layout="vertical" onFinish={handleAnalyzeCreator}>
            <Form.Item name="platform" label="平台" initialValue={selectedPlatform} rules={[{ required: true, message: '请选择平台' }]}>
              <Select onChange={(value) => setSelectedPlatform(value)}>
                {SOCIAL_PLATFORMS.map(platform => (
                  <Option key={platform} value={platform}>{platform}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="creator" label="创作者" rules={[{ required: true, message: '请输入创作者用户名' }]}>
              <Input placeholder="创作者用户名" />
            </Form.Item>
            <Form.Item name="analysisType" label="分析类型" initialValue="内容分析">
              <Select>
                {ANALYSIS_TYPES.map(type => (
                  <Option key={type} value={type}>{type}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading}>
                分析创作者
              </Button>
            </Form.Item>
          </Form>
        </TabPane>

        <TabPane tab="灵感收集" key="inspiration">
          <Form layout="vertical" onFinish={handleCollectInspiration}>
            <Form.Item name="keywords" label="关键词" rules={[{ required: true, message: '请输入关键词，多个关键词用逗号分隔' }]}>
              <Input placeholder="关键词1, 关键词2, 关键词3" />
            </Form.Item>
            <Form.Item name="platforms" label="平台" initialValue={['Pinterest', 'Instagram']} rules={[{ required: true, message: '请选择至少一个平台' }]}>
              <Select mode="multiple">
                {SOCIAL_PLATFORMS.map(platform => (
                  <Option key={platform} value={platform}>{platform}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="count" label="每个平台收集数量" initialValue={5}>
              <InputNumber min={1} max={10} />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading}>
                收集灵感
              </Button>
            </Form.Item>
          </Form>
        </TabPane>
      </Tabs>

      {renderResults()}
    </Card>
  );
};

export default SocialMediaTools; 