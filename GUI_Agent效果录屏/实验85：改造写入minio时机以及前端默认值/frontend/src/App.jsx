import React, { useState, useEffect } from 'react';
import {
  Layout,
  Card,
  Button,
  Table,
  Modal,
  Form,
  Input,
  DatePicker,
  message,
  Popconfirm,
  Tag,
  Space,
  Image,
} from 'antd';
import { PlusOutlined, DeleteOutlined, EyeOutlined, FileTextOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { violationAPI } from './api';

const { Header, Content } = Layout;
const { RangePicker } = DatePicker;

function App() {
  const [applications, setApplications] = useState([]);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [imageLoading, setImageLoading] = useState(false);
  const [createModalVisible, setCreateModalVisible] = useState(false);
  const [imageModalVisible, setImageModalVisible] = useState(false);
  const [logModalVisible, setLogModalVisible] = useState(false);
  const [selectedAppId, setSelectedAppId] = useState(null);
  const [logs, setLogs] = useState([]);
  const [logLoading, setLogLoading] = useState(false);
  const [form] = Form.useForm();
  
  // 分页状态
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });
  
  const [imagePagination, setImagePagination] = useState({
    current: 1,
    pageSize: 12,
    total: 0,
  });

  // 获取应用列表
  const fetchApplications = async (page = pagination.current, pageSize = pagination.pageSize) => {
    setLoading(true);
    try {
      const response = await violationAPI.getApplications({
        pageNo: page,
        pageSize: pageSize,
      });
      
      if (response.code === '0') {
        setApplications(response.data.list);
        setPagination({
          current: response.data.pageNo,
          pageSize: response.data.pageSize,
          total: response.data.total,
        });
      } else {
        message.error(response.msg || '获取应用列表失败');
      }
    } catch (error) {
      message.error('获取应用列表失败');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // 创建应用
  const handleCreateApplication = async (values) => {
    try {
      const data = {
        name: values.name,
        address: values.address,
        start_time: values.timeRange[0].format('YYYY-MM-DD HH:mm:ss'),
        end_time: values.timeRange[1].format('YYYY-MM-DD HH:mm:ss'),
      };
      
      const response = await violationAPI.createApplication(data);
      
      if (response.code === '0') {
        message.success('创建应用成功');
        setCreateModalVisible(false);
        form.resetFields();
        fetchApplications();
      } else {
        message.error(response.msg || '创建应用失败');
      }
    } catch (error) {
      message.error('创建应用失败');
      console.error(error);
    }
  };

  // 删除应用
  const handleDeleteApplication = async (id) => {
    try {
      const response = await violationAPI.deleteApplication(id);
      
      if (response.code === '0') {
        message.success('删除应用成功');
        fetchApplications();
      } else {
        message.error(response.msg || '删除应用失败');
      }
    } catch (error) {
      message.error('删除应用失败');
      console.error(error);
    }
  };

  // 查看图片
  const handleViewImages = async (appId) => {
    setSelectedAppId(appId);
    setImageModalVisible(true);
    fetchImages(appId, 1, imagePagination.pageSize);
  };

  // 查看日志
  const handleViewLogs = async (appId) => {
    setSelectedAppId(appId);
    setLogModalVisible(true);
    fetchLogs(appId);
  };

  // 获取日志列表
  const fetchLogs = async (appId) => {
    setLogLoading(true);
    try {
      const response = await violationAPI.getLogs(appId);
      if (response.code === '0') {
        setLogs(response.data);
      } else {
        message.error(response.msg || '获取日志失败');
      }
    } catch (error) {
      message.error('获取日志失败');
      console.error(error);
    } finally {
      setLogLoading(false);
    }
  };

  // 获取图片列表
  const fetchImages = async (appId, page = imagePagination.current, pageSize = imagePagination.pageSize) => {
    setImageLoading(true);
    try {
      const response = await violationAPI.getImages({
        id: appId,
        pageNo: page,
        pageSize: pageSize,
      });
      
      if (response.code === '0') {
        setImages(response.data.list);
        setImagePagination({
          current: response.data.pageNo,
          pageSize: response.data.pageSize,
          total: response.data.total,
        });
      } else {
        message.error(response.msg || '获取图片列表失败');
      }
    } catch (error) {
      message.error('获取图片列表失败');
      console.error(error);
    } finally {
      setImageLoading(false);
    }
  };

  // 状态标签渲染
  const renderStatusTag = (status) => {
    const statusConfig = {
      Ready: { color: 'default', text: '准备中' },
      Running: { color: 'processing', text: '运行中' },
      Stopped: { color: 'warning', text: '已停止' },
      Finished: { color: 'success', text: '已完成' },
    };
    
    const config = statusConfig[status] || { color: 'default', text: status };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  // 应用列表表格列定义
  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '应用名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '地址',
      dataIndex: 'address',
      key: 'address',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => renderStatusTag(status),
    },
    {
      title: '开始时间',
      dataIndex: 'start_time',
      key: 'start_time',
    },
    {
      title: '结束时间',
      dataIndex: 'end_time',
      key: 'end_time',
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
        <Space>
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handleViewImages(record.id)}
          >
            查看图片
          </Button>
          <Button
            type="link"
            icon={<FileTextOutlined />}
            onClick={() => handleViewLogs(record.id)}
          >
            查看日志
          </Button>
          <Popconfirm
            title="确定要删除这个应用吗？"
            onConfirm={() => handleDeleteApplication(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  // 初始加载
  useEffect(() => {
    fetchApplications();
  }, []);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#fff', padding: '0 24px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
        <h1 style={{ margin: 0, lineHeight: '64px', fontSize: '24px' }}>交通违章监控系统</h1>
      </Header>
      
      <Content style={{ padding: '24px', background: '#f0f2f5' }}>
        <Card
          title="应用管理"
          extra={
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => setCreateModalVisible(true)}
            >
              创建应用
            </Button>
          }
        >
          <Table
            columns={columns}
            dataSource={applications}
            loading={loading}
            rowKey="id"
            pagination={{
              ...pagination,
              showSizeChanger: true,
              showTotal: (total) => `共 ${total} 条`,
              onChange: (page, pageSize) => {
                fetchApplications(page, pageSize);
              },
            }}
          />
        </Card>

        {/* 创建应用模态框 */}
        <Modal
          title="创建应用"
          open={createModalVisible}
          onCancel={() => {
            setCreateModalVisible(false);
            form.resetFields();
          }}
          onOk={() => form.submit()}
          okText="创建"
          cancelText="取消"
        >
          <Form
            form={form}
            layout="vertical"
            onFinish={handleCreateApplication}
          >
            <Form.Item
              label="应用名称"
              name="name"
              rules={[{ required: true, message: '请输入应用名称' }]}
            >
              <Input placeholder="请输入应用名称" />
            </Form.Item>
            
            <Form.Item
              label="地址"
              name="address"
              rules={[{ required: true, message: '请输入地址' }]}
            >
              <Input placeholder="请输入监控地址" />
            </Form.Item>
            
            <Form.Item
              label="时间范围"
              name="timeRange"
              rules={[{ required: true, message: '请选择时间范围' }]}
            >
              <RangePicker
                showTime
                format="YYYY-MM-DD HH:mm:ss"
                style={{ width: '100%' }}
                placeholder={['开始时间', '结束时间']}
              />
            </Form.Item>
          </Form>
        </Modal>

        {/* 查看图片模态框 */}
        <Modal
          title="抓拍图片"
          open={imageModalVisible}
          onCancel={() => {
            setImageModalVisible(false);
            setImages([]);
            setSelectedAppId(null);
          }}
          footer={null}
          width={1000}
        >
          <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
            {imageLoading ? (
              <div style={{ textAlign: 'center', padding: '50px' }}>加载中...</div>
            ) : images.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '50px', color: '#999' }}>
                暂无图片
              </div>
            ) : (
              <div>
                <Image.PreviewGroup>
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
                    gap: '16px',
                    marginBottom: '16px'
                  }}>
                    {images.map((image, index) => (
                      <Card
                        key={index}
                        hoverable
                        cover={
                          <Image
                            src={image.url}
                            alt={`${image.person_name} - ${image.capture_time}`}
                            style={{ width: '100%', height: '200px', objectFit: 'cover' }}
                          />
                        }
                      >
                        <Card.Meta
                          title={image.person_name}
                          description={
                            <div style={{ fontSize: '12px' }}>
                              <div>身份证: {image.person_id}</div>
                              <div style={{ marginTop: '4px', color: '#999' }}>
                                抓拍时间: {image.capture_time}
                              </div>
                            </div>
                          }
                        />
                      </Card>
                    ))}
                  </div>
                </Image.PreviewGroup>
                
                <div style={{ textAlign: 'center', marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #f0f0f0' }}>
                  <Space>
                    <Button
                      disabled={imagePagination.current === 1}
                      onClick={() => fetchImages(selectedAppId, imagePagination.current - 1, imagePagination.pageSize)}
                    >
                      上一页
                    </Button>
                    <span>
                      第 {imagePagination.current} 页，共 {Math.ceil(imagePagination.total / imagePagination.pageSize)} 页
                    </span>
                    <Button
                      disabled={imagePagination.current * imagePagination.pageSize >= imagePagination.total}
                      onClick={() => fetchImages(selectedAppId, imagePagination.current + 1, imagePagination.pageSize)}
                    >
                      下一页
                    </Button>
                  </Space>
                </div>
              </div>
            )}
          </div>
        </Modal>
        {/* 查看日志模态框 */}
        <Modal
          title="运行日志"
          open={logModalVisible}
          onCancel={() => {
            setLogModalVisible(false);
            setLogs([]);
            setSelectedAppId(null);
          }}
          footer={null}
          width={800}
        >
          <div 
            style={{ 
              maxHeight: '500px', 
              overflowY: 'auto', 
              background: '#001529', 
              color: '#fff', 
              padding: '16px',
              fontFamily: 'monospace',
              borderRadius: '4px'
            }}
          >
            {logLoading ? (
              <div style={{ textAlign: 'center', color: '#aaa' }}>加载中...</div>
            ) : logs.length === 0 ? (
              <div style={{ textAlign: 'center', color: '#aaa' }}>暂无日志</div>
            ) : (
              logs.map((log) => (
                <div key={log.id} style={{ marginBottom: '8px', borderBottom: '1px solid #333', paddingBottom: '4px' }}>
                  <span style={{ color: '#52c41a', marginRight: '8px' }}>[{log.created_at}]</span>
                  <span style={{ color: log.level === 'ERROR' ? '#ff4d4f' : '#1890ff', marginRight: '8px' }}>
                    [{log.level}]
                  </span>
                  <span>{log.message}</span>
                </div>
              ))
            )}
          </div>
        </Modal>
      </Content>
    </Layout>
  );
}

export default App;
