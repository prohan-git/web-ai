import React from 'react';
import { Layout, Menu, ConfigProvider, theme, Typography, Button } from 'antd';
import { useNavigate, useLocation, Routes, Route } from 'react-router-dom';
import { 
  ShoppingOutlined, 
  InstagramOutlined, 
  MessageOutlined, 
  OrderedListOutlined,
  UserOutlined,
} from '@ant-design/icons';

// 导入组件
import EcommerceTools from './components/EcommerceTools';
import SocialMediaTools from './components/SocialMediaTools';
import ChatInterface from './components/ChatInterface';
import TaskManagement from './components/TaskManagement';

const { Header, Content, Footer } = Layout;

// 简化的配色方案 - 极简主义
const themeColor = {
  primaryColor: '#333333',  // 深灰色
  secondaryColor: '#666666', // 中灰色
  textPrimary: '#333333',   // 主文本色
  textSecondary: '#888888', // 次要文本
  bgLight: '#f8f8f8',       // 背景浅色
};

// 导航菜单项 - 简化
const menuItems = [
  {
    key: '/ecommerce',
    icon: <ShoppingOutlined />,
    label: '电商工具',
  },
  {
    key: '/social',
    icon: <InstagramOutlined />,
    label: '社交媒体',
  },
  {
    key: '/chat',
    icon: <MessageOutlined />,
    label: 'AI助手',
  },
  {
    key: '/tasks',
    icon: <OrderedListOutlined />,
    label: '任务',
  },
];

// 添加极简样式
const style = document.createElement('style');
style.innerHTML = `
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  }
  
  .content-container {
    background: white;
    border-radius: 4px;
  }
  
  .logo-text {
    font-weight: 500;
    font-size: 18px;
    color: #333;
  }
  
  .minimal-header {
    background: white !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    height: 60px;
    display: flex;
    align-items: center;
    padding: 0 32px;
  }
  
  .menu-item {
    transition: all 0.2s;
  }
  
  .minimal-btn {
    border-radius: 2px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }
  
  .app-content {
    background: #f8f8f8;
    min-height: calc(100vh - 60px);
    padding: 40px;
  }
  
  .minimal-footer {
    background: white;
    padding: 24px;
    color: #888;
    text-align: center;
  }
  
  .ant-menu {
    background: transparent;
    border: none;
  }
  
  .ant-menu-horizontal > .ant-menu-item::after {
    display: none;
  }
  
  .ant-menu-horizontal > .ant-menu-item-selected {
    color: #333;
    font-weight: 500;
  }
`;
document.head.appendChild(style);

const App = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const currentPath = location.pathname === '/' ? '/ecommerce' : location.pathname;

  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: themeColor.primaryColor,
          borderRadius: 2,
          colorText: themeColor.textPrimary,
          colorTextSecondary: themeColor.textSecondary,
        },
      }}
    >
      <Layout style={{ minHeight: '100vh' }}>
        <Header 
          className="minimal-header"
          style={{ 
            position: 'sticky', 
            top: 0, 
            zIndex: 100, 
            width: '100%',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          {/* Logo和站点名称 */}
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span className="logo-text">Web AI</span>
          </div>
          
          {/* 主导航菜单 */}
          <Menu
            mode="horizontal"
            selectedKeys={[currentPath]}
            items={menuItems.map(item => ({
              ...item,
              className: 'menu-item',
              style: { fontSize: '14px' }
            }))}
            style={{ 
              flex: 1, 
              minWidth: '300px',
              marginLeft: '40px',
              justifyContent: 'center'
            }}
            onClick={({ key }) => navigate(key)}
          />
          
          {/* 右侧工具栏 */}
          <div>
            <Button type="primary" size="middle" icon={<UserOutlined />} style={{ backgroundColor: '#333', border: 'none' }}>
              账户
            </Button>
          </div>
        </Header>

        <Content className="app-content">
          {/* 主要内容区域 */}
          <div 
            className="content-container"
            style={{ 
              padding: '40px', 
              marginBottom: '40px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
            }}
          >
            <Routes>
              <Route path="/" element={<EcommerceTools />} />
              <Route path="/ecommerce" element={<EcommerceTools />} />
              <Route path="/social" element={<SocialMediaTools />} />
              <Route path="/chat" element={<ChatInterface />} />
              <Route path="/tasks" element={<TaskManagement />} />
            </Routes>
          </div>
        </Content>

        <Footer className="minimal-footer">
          © {new Date().getFullYear()} Web AI
        </Footer>
      </Layout>
    </ConfigProvider>
  );
};

export default App; 