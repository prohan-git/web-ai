import React, { useState } from 'react';
import { Card, Tabs, Form, Input, Button, Select, InputNumber, Spin, Typography, Alert, Divider } from 'antd';
import apiService from '../services/api';

const { Title, Paragraph, Text } = Typography;
const { TabPane } = Tabs;
const { Option } = Select;
const { TextArea } = Input;

// 电商平台选项
const PLATFORMS = [
  { label: '亚马逊', value: '亚马逊' },
  { label: '淘宝', value: '淘宝' },
  { label: '京东', value: '京东' },
  { label: '拼多多', value: '拼多多' },
  { label: '天猫', value: '天猫' },
  { label: '速卖通', value: '速卖通' },
  { label: 'Shopee', value: 'Shopee' },
  { label: '1688', value: '1688' },
  { label: '阿里巴巴', value: '阿里巴巴' },
];

// 上货模板类型
const LISTING_TEMPLATES = [
  { label: '标准上货', value: '标准上货' },
  { label: '亚马逊专用', value: '亚马逊专用' },
  { label: '简约风格', value: '简约风格' },
  { label: '详细描述', value: '详细描述' },
  { label: '创意文案', value: '创意文案' },
];

// 任务类型选项（按平台分类）
const TASK_TYPES = {
  '亚马逊': [
    { label: '热销产品', value: '热销产品' },
    { label: '评价分析', value: '评价分析' },
    { label: '竞品比较', value: '竞品比较' },
    { label: '产品趋势', value: '产品趋势' },
    { label: 'BSR变化', value: 'BSR变化' },
  ],
  '淘宝': [
    { label: '热销分析', value: '热销分析' },
    { label: '店铺考察', value: '店铺考察' },
    { label: '直播数据', value: '直播数据' },
    { label: '价格区间', value: '价格区间' },
  ],
  '拼多多': [
    { label: '爆款产品', value: '爆款产品' },
    { label: '低价策略', value: '低价策略' },
    { label: '团购效果', value: '团购效果' },
  ],
  '1688': [
    { label: '供应商考察', value: '供应商考察' },
    { label: '工厂直供', value: '工厂直供' },
    { label: '原料搜索', value: '原料搜索' },
  ],
};

const EcommerceTools = () => {
  // 状态管理
  const [searchProductsForm] = Form.useForm();
  const [generateListingForm] = Form.useForm();
  const [analyzeCompetitionForm] = Form.useForm();
  const [findSuppliersForm] = Form.useForm();
  const [productPotentialForm] = Form.useForm();
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [selectedPlatform, setSelectedPlatform] = useState('亚马逊');
  
  // 根据选择的平台更新任务类型选项
  const getTaskTypeOptions = (platform) => {
    return TASK_TYPES[platform] || [];
  };
  
  // 清除结果和错误
  const resetStates = () => {
    setResult(null);
    setError(null);
  };
  
  // 处理搜索产品表单提交
  const handleSearchProducts = async (values) => {
    resetStates();
    setLoading(true);
    
    try {
      const response = await apiService.searchProducts({
        platform: values.platform,
        task_type: values.task_type,
        use_vision: values.use_vision || true
      });
      
      setResult(response);
    } catch (error) {
      setError(error.response?.data?.detail || error.message);
    } finally {
      setLoading(false);
    }
  };
  
  // 处理生成上货素材表单提交
  const handleGenerateListing = async (values) => {
    resetStates();
    setLoading(true);
    
    try {
      const response = await apiService.generateListing(values);
      setResult(response);
    } catch (error) {
      setError(error.response?.data?.detail || error.message);
    } finally {
      setLoading(false);
    }
  };
  
  // 处理竞品分析表单提交
  const handleAnalyzeCompetition = async (values) => {
    resetStates();
    setLoading(true);
    
    try {
      const { product_keyword, platform, use_vision } = values;
      const response = await apiService.ecommerce.analyzeCompetition(
        product_keyword,
        platform,
        use_vision
      );
      
      setResult(response);
    } catch (error) {
      setError(error.response?.data?.detail || error.message);
    } finally {
      setLoading(false);
    }
  };
  
  // 处理查找供应商表单提交
  const handleFindSuppliers = async (values) => {
    resetStates();
    setLoading(true);
    
    try {
      const { product, count, use_vision } = values;
      const response = await apiService.ecommerce.findSuppliers(
        product,
        count,
        use_vision
      );
      
      setResult(response);
    } catch (error) {
      setError(error.response?.data?.detail || error.message);
    } finally {
      setLoading(false);
    }
  };
  
  // 处理产品潜力分析表单提交
  const handleProductPotential = async (values) => {
    resetStates();
    setLoading(true);
    
    try {
      const { product_info, niche, platform, dimensions } = values;
      // 将维度字符串拆分为数组
      const dimensionsArray = dimensions ? dimensions.split(',').map(item => item.trim()) : undefined;
      
      const response = await apiService.ecommerce.analyzeProductPotential(
        product_info,
        niche,
        platform,
        dimensionsArray
      );
      
      setResult(response);
    } catch (error) {
      setError(error.response?.data?.detail || error.message);
    } finally {
      setLoading(false);
    }
  };
  
  // 渲染结果
  const renderResult = () => {
    if (!result) return null;
    
    return (
      <div style={{ marginTop: 24 }}>
        <Divider>分析结果</Divider>
        <Card>
          <Title level={4}>状态: {result.status}</Title>
          {result.message && <Paragraph>{result.message}</Paragraph>}
          
          {result.result || result.listing_content || result.analysis_result || result.supplier_info ? (
            <div>
              <Text strong>详细内容:</Text>
              <pre style={{ 
                background: '#f5f5f5', 
                padding: 16, 
                borderRadius: 4,
                overflowX: 'auto',
                whiteSpace: 'pre-wrap',
                maxHeight: '500px',
                overflow: 'auto'
              }}>
                {result.result || result.listing_content || result.analysis_result || result.supplier_info}
              </pre>
            </div>
          ) : null}
        </Card>
      </div>
    );
  };
  
  return (
    <div className="ecommerce-tools">
      <Title level={2}>电商运营工具</Title>
      <Paragraph>
        利用AI强大能力辅助您的电商运营，包括产品选择、上货素材生成、竞争分析等功能。
      </Paragraph>
      
      <Tabs defaultActiveKey="search" size="large">
        {/* 产品搜索 */}
        <TabPane tab="产品搜索" key="search">
          <Card title="电商平台产品搜索">
            <Form
              form={searchProductsForm}
              layout="vertical"
              onFinish={handleSearchProducts}
              initialValues={{ platform: '亚马逊', use_vision: true }}
            >
              <Form.Item
                name="platform"
                label="电商平台"
                rules={[{ required: true, message: '请选择平台' }]}
              >
                <Select 
                  options={PLATFORMS} 
                  onChange={(value) => setSelectedPlatform(value)}
                />
              </Form.Item>
              
              <Form.Item
                name="task_type"
                label="任务类型"
                rules={[{ required: true, message: '请选择任务类型' }]}
              >
                <Select options={getTaskTypeOptions(selectedPlatform)} />
              </Form.Item>
              
              <Form.Item
                name="keywords"
                label="关键词"
              >
                <Input placeholder="请输入搜索关键词" />
              </Form.Item>
              
              <Form.Item
                name="category"
                label="类目"
              >
                <Input placeholder="请输入产品类目" />
              </Form.Item>
              
              <Form.Item
                name="count"
                label="数量"
                initialValue={5}
              >
                <InputNumber min={1} max={20} />
              </Form.Item>
              
              <Form.Item
                name="use_vision"
                valuePropName="checked"
                label="使用视觉"
                initialValue={true}
              >
                <Select>
                  <Option value={true}>是</Option>
                  <Option value={false}>否</Option>
                </Select>
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  开始搜索
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        {/* 上货素材生成 */}
        <TabPane tab="上货素材" key="listing">
          <Card title="电商上货素材生成">
            <Form
              form={generateListingForm}
              layout="vertical"
              onFinish={handleGenerateListing}
              initialValues={{ template_type: '标准上货' }}
            >
              <Form.Item
                name="template_type"
                label="模板类型"
                rules={[{ required: true, message: '请选择模板类型' }]}
              >
                <Select options={LISTING_TEMPLATES} />
              </Form.Item>
              
              <Form.Item
                name="product"
                label="产品名称"
                rules={[{ required: true, message: '请输入产品名称' }]}
              >
                <Input placeholder="请输入产品名称，例如：便携式蓝牙音箱" />
              </Form.Item>
              
              <Form.Item
                name="features"
                label="产品特点"
              >
                <TextArea 
                  placeholder="请输入产品特点，多个特点用逗号分隔" 
                  autoSize={{ minRows: 3, maxRows: 6 }}
                />
              </Form.Item>
              
              <Form.Item
                name="platform"
                label="目标平台"
              >
                <Select options={PLATFORMS} allowClear placeholder="选择目标平台（可选）" />
              </Form.Item>
              
              <Form.Item
                name="description"
                label="产品描述"
              >
                <TextArea 
                  placeholder="可选：产品的详细描述" 
                  autoSize={{ minRows: 3, maxRows: 6 }}
                />
              </Form.Item>
              
              <Form.Item
                name="cost"
                label="产品成本"
              >
                <InputNumber 
                  placeholder="可选：产品成本价格" 
                  min={0}
                  step={0.01}
                  style={{ width: '100%' }}
                />
              </Form.Item>
              
              <Form.Item
                name="competitor_prices"
                label="竞品价格"
              >
                <Input placeholder="可选：竞品价格范围，例如：99-199元" />
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  生成上货素材
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        {/* 竞品分析 */}
        <TabPane tab="竞品分析" key="competition">
          <Card title="竞品情况分析">
            <Form
              form={analyzeCompetitionForm}
              layout="vertical"
              onFinish={handleAnalyzeCompetition}
              initialValues={{ platform: '亚马逊', use_vision: true }}
            >
              <Form.Item
                name="product_keyword"
                label="产品关键词"
                rules={[{ required: true, message: '请输入产品关键词' }]}
              >
                <Input placeholder="请输入产品关键词，例如：蓝牙耳机" />
              </Form.Item>
              
              <Form.Item
                name="platform"
                label="目标平台"
                rules={[{ required: true, message: '请选择平台' }]}
              >
                <Select options={PLATFORMS} />
              </Form.Item>
              
              <Form.Item
                name="use_vision"
                valuePropName="checked"
                label="使用视觉"
                initialValue={true}
              >
                <Select>
                  <Option value={true}>是</Option>
                  <Option value={false}>否</Option>
                </Select>
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  分析竞品
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        {/* 供应商查找 */}
        <TabPane tab="供应商查找" key="suppliers">
          <Card title="产品供应商查找">
            <Form
              form={findSuppliersForm}
              layout="vertical"
              onFinish={handleFindSuppliers}
              initialValues={{ count: 5, use_vision: true }}
            >
              <Form.Item
                name="product"
                label="产品名称"
                rules={[{ required: true, message: '请输入产品名称' }]}
              >
                <Input placeholder="请输入产品名称，例如：蓝牙音箱" />
              </Form.Item>
              
              <Form.Item
                name="count"
                label="供应商数量"
                initialValue={5}
              >
                <InputNumber min={1} max={20} />
              </Form.Item>
              
              <Form.Item
                name="use_vision"
                valuePropName="checked"
                label="使用视觉"
                initialValue={true}
              >
                <Select>
                  <Option value={true}>是</Option>
                  <Option value={false}>否</Option>
                </Select>
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  查找供应商
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        {/* 产品潜力分析 */}
        <TabPane tab="产品潜力" key="potential">
          <Card title="产品市场潜力分析">
            <Form
              form={productPotentialForm}
              layout="vertical"
              onFinish={handleProductPotential}
              initialValues={{ platform: '全平台' }}
            >
              <Form.Item
                name="product_info"
                label="产品信息"
                rules={[{ required: true, message: '请输入产品信息' }]}
              >
                <TextArea 
                  placeholder="请详细描述产品信息，包括功能、特点等" 
                  autoSize={{ minRows: 3, maxRows: 6 }}
                />
              </Form.Item>
              
              <Form.Item
                name="niche"
                label="产品领域/类目"
                rules={[{ required: true, message: '请输入产品所在领域' }]}
              >
                <Input placeholder="请输入产品所在领域，例如：家居、电子、美妆等" />
              </Form.Item>
              
              <Form.Item
                name="platform"
                label="目标平台"
                initialValue="全平台"
              >
                <Select>
                  <Option value="全平台">全平台</Option>
                  {PLATFORMS.map(platform => (
                    <Option key={platform.value} value={platform.value}>{platform.label}</Option>
                  ))}
                </Select>
              </Form.Item>
              
              <Form.Item
                name="dimensions"
                label="评估维度"
                help="多个维度用逗号分隔，留空使用默认维度（市场规模、竞争程度、利润空间等）"
              >
                <Input placeholder="例如：市场规模,竞争程度,利润空间,趋势发展,进入壁垒" />
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  分析产品潜力
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
      </Tabs>
      
      {/* 加载状态 */}
      {loading && (
        <div style={{ textAlign: 'center', margin: '20px 0' }}>
          <Spin size="large" tip="正在处理，请稍候...这可能需要1-2分钟" />
        </div>
      )}
      
      {/* 错误信息 */}
      {error && (
        <Alert
          message="请求错误"
          description={error}
          type="error"
          showIcon
          style={{ marginTop: 16 }}
        />
      )}
      
      {/* 结果展示 */}
      {renderResult()}
    </div>
  );
};

export default EcommerceTools; 