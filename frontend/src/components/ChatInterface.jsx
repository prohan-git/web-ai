import React, { useState, useRef, useEffect } from 'react';
import { Card, Input, Button, List, Avatar, Typography, Divider, Spin, notification } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons';
import apiService from '../services/api';

const { Text, Paragraph, Title } = Typography;
const { TextArea } = Input;

const ChatInterface = () => {
  // 状态管理
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 初始化消息
  useEffect(() => {
    setMessages([
      {
        id: 1,
        content: '你好！我是AI助手，很高兴为您服务。请问有什么可以帮到您的吗？',
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString()
      }
    ]);
  }, []);

  // 发送消息
  const handleSendMessage = async () => {
    if (!input.trim()) return;
    
    // 添加用户消息到列表
    const userMessage = {
      id: Date.now(),
      content: input,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    
    try {
      console.log('发送聊天消息:', input);
      // 调用API发送消息
      const response = await apiService.sendChatMessage(input);
      
      console.log('收到API响应:', response);
      
      // 添加AI回复到列表
      const aiMessage = {
        id: Date.now() + 1,
        content: response.response || '无法获取回复', // 使用response.response获取AI回复
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, aiMessage]);
      
      notification.success({
        message: '消息已送达',
        description: '成功获取AI回复',
        placement: 'bottomRight',
        duration: 2
      });
    } catch (error) {
      console.error('聊天API错误:', error);
      // 添加错误消息
      const errorMessage = {
        id: Date.now() + 1,
        content: '发送消息失败: ' + (error.response?.data?.detail || error.message || '未知错误'),
        sender: 'system',
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      
      notification.error({
        message: '发送失败',
        description: '无法获取AI回复，请稍后重试',
        placement: 'bottomRight'
      });
    } finally {
      setLoading(false);
    }
  };

  // 处理按键事件 - 回车发送，Shift+回车换行
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-container">
      <Card 
        title={
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <RobotOutlined style={{ color: '#4353FF', marginRight: 8, fontSize: 20 }} />
            <Title level={4} style={{ margin: 0 }}>AI智能助手</Title>
          </div>
        } 
        bordered={false}
        className="modern-card"
        style={{ 
          height: 'calc(100vh - 280px)', 
          display: 'flex', 
          flexDirection: 'column',
          margin: 0
        }}
      >
        <div 
          style={{ 
            flex: 1, 
            overflow: 'auto', 
            padding: '10px 0',
            backgroundColor: '#F8FAFF',
            borderRadius: '8px',
            padding: '16px'
          }}
        >
          <List
            itemLayout="horizontal"
            dataSource={messages}
            renderItem={(message) => (
              <List.Item 
                style={{ 
                  padding: '8px 0',
                  display: 'flex',
                  justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start'
                }}
              >
                <div 
                  style={{ 
                    maxWidth: '80%',
                    backgroundColor: message.sender === 'ai' ? '#FFFFFF' : '#4353FF',
                    color: message.sender === 'ai' ? '#1F2131' : '#FFFFFF',
                    padding: '12px 16px',
                    borderRadius: message.sender === 'ai' ? '0px 12px 12px 12px' : '12px 0px 12px 12px',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)',
                    position: 'relative'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
                    <Avatar 
                      icon={message.sender === 'ai' ? <RobotOutlined /> : <UserOutlined />} 
                      style={{ 
                        backgroundColor: message.sender === 'ai' ? '#4353FF' : '#7000FF',
                        marginRight: '8px'
                      }} 
                      size="small"
                    />
                    <Text 
                      strong 
                      style={{ 
                        color: message.sender === 'ai' ? '#1F2131' : '#FFFFFF'
                      }}
                    >
                      {message.sender === 'ai' ? 'AI助手' : '您'}
                    </Text>
                    <Text 
                      type="secondary" 
                      style={{ 
                        fontSize: '12px', 
                        marginLeft: '8px',
                        color: message.sender === 'ai' ? '#646A8C' : 'rgba(255,255,255,0.7)'
                      }}
                    >
                      {message.timestamp}
                    </Text>
                  </div>
                  <Paragraph 
                    style={{ 
                      margin: 0, 
                      whiteSpace: 'pre-wrap',
                      fontSize: '14px',
                      lineHeight: '1.6'
                    }}
                  >
                    {message.content}
                  </Paragraph>
                </div>
              </List.Item>
            )}
          />
          <div ref={messagesEndRef} />
          {loading && (
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <Spin size="small" />
              <Text style={{ marginLeft: '10px', color: '#646A8C' }}>AI正在思考...</Text>
            </div>
          )}
        </div>
        
        <Divider style={{ margin: '16px 0' }} />
        
        <div style={{ display: 'flex', alignItems: 'flex-end' }}>
          <TextArea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入消息，按Enter发送，Shift+Enter换行..."
            autoSize={{ minRows: 1, maxRows: 4 }}
            style={{ 
              flex: 1, 
              marginRight: '12px',
              borderRadius: '8px',
              padding: '8px 12px'
            }}
            disabled={loading}
          />
          <Button 
            type="primary" 
            icon={<SendOutlined />} 
            onClick={handleSendMessage} 
            loading={loading}
            style={{
              height: '40px',
              borderRadius: '8px'
            }}
          >
            发送
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default ChatInterface; 