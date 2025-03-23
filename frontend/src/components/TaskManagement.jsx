import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Input, Select, message, Tag, Space, Tooltip, Typography } from 'antd';
import { PlusOutlined, SearchOutlined, ReloadOutlined, DeleteOutlined, EyeOutlined, PlayCircleOutlined } from '@ant-design/icons';
import apiService from '../services/api';

const { Option } = Select;
const { TextArea } = Input;
const { Text } = Typography;

const TaskManagement = () => {
  // 状态管理
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [currentTask, setCurrentTask] = useState(null);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // 任务类型和状态选项
  const taskTypes = ['浏览器任务', '社交媒体', '电商分析', '数据收集', '内容生成'];
  const taskStatuses = ['待执行', '执行中', '已完成', '失败'];
  
  // 获取任务列表
  const fetchTasks = async () => {
    setLoading(true);
    try {
      const response = await apiService.getTasks();
      setTasks(response.data || []);
    } catch (error) {
      console.error('获取任务列表失败:', error);
      message.error('获取任务列表失败');
    } finally {
      setLoading(false);
    }
  };
  
  // 首次加载时获取任务
  useEffect(() => {
    fetchTasks();
  }, []);
  
  // 创建新任务
  const handleCreateTask = async (values) => {
    try {
      await apiService.createTask(values);
      message.success('任务创建成功');
      setModalVisible(false);
      form.resetFields();
      fetchTasks();
    } catch (error) {
      console.error('创建任务失败:', error);
      message.error('创建任务失败: ' + (error.response?.data?.message || error.message));
    }
  };
  
  // 删除任务
  const handleDeleteTask = async (taskId) => {
    try {
      await apiService.deleteTask(taskId);
      message.success('任务删除成功');
      fetchTasks();
    } catch (error) {
      console.error('删除任务失败:', error);
      message.error('删除任务失败');
    }
  };
  
  // 查看任务详情
  const handleViewTask = (task) => {
    setCurrentTask(task);
    setDetailModalVisible(true);
  };
  
  // 执行任务
  const handleExecuteTask = async (taskId) => {
    try {
      await apiService.updateTask(taskId, { status: '执行中' });
      message.success('任务已开始执行');
      fetchTasks();
    } catch (error) {
      console.error('执行任务失败:', error);
      message.error('执行任务失败');
    }
  };
  
  // 表格列定义
  const columns = [
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
      render: (text) => <Text strong>{text}</Text>,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type) => {
        let color;
        switch (type) {
          case '浏览器任务':
            color = 'blue';
            break;
          case '社交媒体':
            color = 'green';
            break;
          case '电商分析':
            color = 'orange';
            break;
          case '数据收集':
            color = 'purple';
            break;
          case '内容生成':
            color = 'cyan';
            break;
          default:
            color = 'default';
        }
        return <Tag color={color}>{type}</Tag>;
      },
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => {
        let color;
        switch (status) {
          case '待执行':
            color = 'default';
            break;
          case '执行中':
            color = 'processing';
            break;
          case '已完成':
            color = 'success';
            break;
          case '失败':
            color = 'error';
            break;
          default:
            color = 'default';
        }
        return <Tag color={color}>{status}</Tag>;
      },
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="查看详情">
            <Button 
              type="text" 
              icon={<EyeOutlined />} 
              onClick={() => handleViewTask(record)}
            />
          </Tooltip>
          {record.status === '待执行' && (
            <Tooltip title="执行">
              <Button 
                type="text" 
                icon={<PlayCircleOutlined />} 
                onClick={() => handleExecuteTask(record.id)}
              />
            </Tooltip>
          )}
          <Tooltip title="删除">
            <Button 
              type="text" 
              danger 
              icon={<DeleteOutlined />} 
              onClick={() => handleDeleteTask(record.id)}
            />
          </Tooltip>
        </Space>
      ),
    },
  ];
  
  return (
    <Card title="任务管理" style={{ marginBottom: '24px' }}>
      <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between' }}>
        <Space>
          <Button 
            type="primary" 
            icon={<PlusOutlined />} 
            onClick={() => setModalVisible(true)}
          >
            新建任务
          </Button>
          <Button 
            icon={<ReloadOutlined />} 
            onClick={fetchTasks}
            loading={loading}
          >
            刷新
          </Button>
        </Space>
        
        <Space>
          <Input.Search 
            placeholder="搜索任务" 
            allowClear 
            onSearch={(value) => console.log('搜索:', value)} 
            style={{ width: 200 }}
          />
          <Select 
            placeholder="任务类型" 
            allowClear 
            style={{ width: 120 }}
            onChange={(value) => console.log('筛选类型:', value)}
          >
            {taskTypes.map(type => (
              <Option key={type} value={type}>{type}</Option>
            ))}
          </Select>
          <Select 
            placeholder="状态" 
            allowClear 
            style={{ width: 100 }}
            onChange={(value) => console.log('筛选状态:', value)}
          >
            {taskStatuses.map(status => (
              <Option key={status} value={status}>{status}</Option>
            ))}
          </Select>
        </Space>
      </div>
      
      <Table 
        columns={columns} 
        dataSource={tasks} 
        rowKey="id" 
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
      
      {/* 新建任务表单 */}
      <Modal
        title="新建任务"
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreateTask}
        >
          <Form.Item
            name="name"
            label="任务名称"
            rules={[{ required: true, message: '请输入任务名称' }]}
          >
            <Input placeholder="请输入任务名称" />
          </Form.Item>
          
          <Form.Item
            name="type"
            label="任务类型"
            rules={[{ required: true, message: '请选择任务类型' }]}
          >
            <Select placeholder="请选择任务类型">
              {taskTypes.map(type => (
                <Option key={type} value={type}>{type}</Option>
              ))}
            </Select>
          </Form.Item>
          
          <Form.Item
            name="description"
            label="任务描述"
          >
            <TextArea rows={4} placeholder="请输入任务描述" />
          </Form.Item>
          
          <Form.Item
            name="parameters"
            label="任务参数"
          >
            <TextArea 
              rows={6} 
              placeholder="请输入任务参数（JSON格式）" 
            />
          </Form.Item>
          
          <Form.Item style={{ marginBottom: 0 }}>
            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button 
                style={{ marginRight: 8 }} 
                onClick={() => setModalVisible(false)}
              >
                取消
              </Button>
              <Button type="primary" htmlType="submit">
                创建
              </Button>
            </div>
          </Form.Item>
        </Form>
      </Modal>
      
      {/* 任务详情 */}
      <Modal
        title="任务详情"
        visible={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="back" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>,
        ]}
        width={700}
      >
        {currentTask && (
          <div>
            <div style={{ marginBottom: '16px' }}>
              <Text strong style={{ marginRight: '8px' }}>任务名称:</Text>
              <Text>{currentTask.name}</Text>
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <Text strong style={{ marginRight: '8px' }}>任务类型:</Text>
              <Tag color="blue">{currentTask.type}</Tag>
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <Text strong style={{ marginRight: '8px' }}>任务状态:</Text>
              <Tag color={
                currentTask.status === '已完成' ? 'success' : 
                currentTask.status === '执行中' ? 'processing' : 
                currentTask.status === '失败' ? 'error' : 'default'
              }>
                {currentTask.status}
              </Tag>
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <Text strong style={{ marginRight: '8px' }}>创建时间:</Text>
              <Text>{currentTask.created_at}</Text>
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <Text strong style={{ marginRight: '8px' }}>更新时间:</Text>
              <Text>{currentTask.updated_at}</Text>
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <Text strong>任务描述:</Text>
              <div style={{ background: '#f5f5f5', padding: '8px', borderRadius: '4px', marginTop: '8px' }}>
                <Text>{currentTask.description || '无描述'}</Text>
              </div>
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <Text strong>任务参数:</Text>
              <div style={{ background: '#f5f5f5', padding: '8px', borderRadius: '4px', marginTop: '8px', maxHeight: '200px', overflow: 'auto' }}>
                <pre>{currentTask.parameters ? JSON.stringify(JSON.parse(currentTask.parameters), null, 2) : '无参数'}</pre>
              </div>
            </div>
            
            {currentTask.result && (
              <div>
                <Text strong>任务结果:</Text>
                <div style={{ background: '#f5f5f5', padding: '8px', borderRadius: '4px', marginTop: '8px', maxHeight: '200px', overflow: 'auto' }}>
                  <pre>{typeof currentTask.result === 'string' ? currentTask.result : JSON.stringify(currentTask.result, null, 2)}</pre>
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>
    </Card>
  );
};

export default TaskManagement; 