# 部署星辰RPA的服务端和客户端

```powershell
# Clone the repository
git clone https://github.com/iflytek/astron-rpa.git
cd astron-rpa

# Enter docker directory
cd docker

# Copy .env
cp .env.example .env

# Modify casdoor service configuration in .env (8000 is the default port)
CASDOOR_EXTERNAL_ENDPOINT="http://localhost:8000"

# 🚀 Start all services
docker compose up
```

## 容器部署星辰RPA（后端）

关键：http://localhost:8000/ 用户名：admin 密码：123（comate帮我找到的）

要确保：http://localhost:32742/api/rpa-auth/user/login-check 显示正常，否则前端报502错误

## 部署星辰RPA前端

```powershell
cd C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\code\astron-rpa

./build.bat -p "C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\code\astron-rpa\astron_py313\Scripts\python.exe"
```

关键：`astron-rpa\resources\conf.yaml`中的服务器地址要改为`localhost`。这是必须的，否则无法连接到后端的注册服务。