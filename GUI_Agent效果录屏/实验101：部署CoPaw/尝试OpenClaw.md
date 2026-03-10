# 目的

OpenClaw 是最具代表性的软件，没有理由不使用。

要想在内网部署，使用docker是最方便的。

https://docs.openclaw.ai/install/docker

https://github.com/openclaw/openclaw/pkgs/container/openclaw

下载镜像。完成。

TODO：
- 在互联网使用镜像。
- 在内网使用镜像。

# 在互联网使用镜像

进入容器
```
docker run -it <镜像名称> /bin/bash
```

启动openclaw
```
openclaw onboard --install-daemon
```

配置大模型。测试连接成功。

Gateway service: Systemd user services are unavailable; skipping service install. Use your container supervisor or `docker compose up -d`

宿主机url启动：localhost 拒绝了我们的连接请求。

tui启动：
not connected to gateway — message not sent

解决方案：下载源代码，里面包括了 docker-compose.yml，因此可以用 `docker compose up -d` 命令。

报错：invalid spec: :/home/node/.openclaw: empty section between colons

解决方案：在ubuntu宿主机中运行。

报同样的错误。

解决方案：运行 docker-setup.sh

报错：未知命令：docker compose

但是在windows的 docker 命令行能够运行 docker compose, ubuntu 中就不行。

这是因为没有安装 docker compose（这是 docker-compose 的替代新版）

docker 的版本是 28.0.4，其发布时间为 2025 年 3 月 25 日。官方推荐配套使用的 Docker Compose 版本是 v2.27.0

https://release-assets.githubusercontent.com/github-production-release-asset/15045751/2745bc6a-045e-4146-9bf2-20f48d359a44?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-03-09T02%3A40%3A55Z&rscd=attachment%3B+filename%3Ddocker-compose-linux-x86_64&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-03-09T01%3A40%3A22Z&ske=2026-03-09T02%3A40%3A55Z&sks=b&skv=2018-11-09&sig=eXR5q6hHtL9vcGTIRIIokEcTolWNeuskCiW%2FQ6nyn8E%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc3MzAyMzEzMiwibmJmIjoxNzczMDIxMzMyLCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.sgrpsf9MZNHpV9gmmQsOb-CxXw3SrPTv3gMMeVQPEbY&response-content-disposition=attachment%3B%20filename%3Ddocker-compose-linux-x86_64&response-content-type=application%2Foctet-stream

Rename the relevant binary for your OS to docker-compose and copy it to $HOME/.docker/cli-plugins

无法使用。解决方案：chmod +x docker-compose 成功

接下来，还需要不用sudo就执行 docker

1. 输入 `cat /etc/group | grep docker` 显示 `docker:x:1001:zcc`
- 输入 `grep docker /etc/group` 显示 `docker:x:1001:zcc`
- 输入 `id $USER` 显示 `uid=1000(zcc) 组=1001(docker)`
2. `sudo usermod -aG docker $USER`
3. 退出终端，重新进入
4. 输入 `groups` 命令，没有显示 docker

注销当前用户，成功。但是：

- 注销当前用户
- 执行 `groups` 命令，显示 docker
- 执行 `docker ps` 命令，显示需要sudo权限

重启电脑。成功。

报错：
```bash
(base)zcc@zcc-pc:~/zhbli/projects/openclaw$ docker-compose up -d
[+]Running 2/2
x openclaw-gateway Error Get "https://registry-1.docker.io/v2/": dial tcp 127.8.0.1:443: connect: connection refused
x openclaw-cli Error Cannot connect to the Docker daemon at unix:///var/run/docker.sock, Is the docker daemon running?
Error response from daemon: Get "https://registry-1.docker.io/v2/": dial tcp 127.0.0.1:443: connect: connection refused
(base)zcc@zcc-pc:~/zhbli/projects/openclaw$
```

运行 docker compose ps 为空，但是我已经下载了openclaw镜像。

查看 docker-compose.yml:
```yml
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE:-openclaw:local}
```
其中 `${变量名:-默认值}` 是 Docker Compose 的「变量插值」写法：
先检查系统 /.env 文件中是否定义了 OPENCLAW_IMAGE 环境变量；
如果定义了，就使用该变量的值作为镜像名（比如 openclaw:latest、my-custom-openclaw:v1.0）；
如果未定义（变量为空 / 不存在），则使用兜底值 openclaw:local（本地构建的 OpenClaw 镜像）。

解决方案：将环境变量设置为 镜像名：版本号 （镜像名必须完整。版本号不能省略）

---

验证服务是否正常运行：docker compose ps：有结果输出。

# 运行 ./docker-setup.sh

该脚本中，只有识别到镜像名为 openclaw:local 时，才会调用本地镜像，否则会从互联网拉取。这就需要修改镜像名。

```bash
docker tag 原镜像名:原标签 openclaw:local
```

决定是直接拉取远程镜像还是本地构建 openclaw:local。这句话说明，要么从远程拉取镜像，要么从头开始构建镜像，这两者都不是我想要的。

# 运行 docker compose up

```bash
openclaw-gateway-1 | 2026-03-10T01:35:54.215+00:00 Gateway failed to start: Error: non-loopback Control UI requires gateway.controlUi.allowedOrigins (set explicit origins), or set gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true to use Host header origin fallback mode
```

当你运行 docker-compose up 时，Docker Compose 程序会在当前运行命令的目录下自动寻找名为 .env 的文件。
