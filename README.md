# Harei 重构版

## 运行方式

1. 复制环境变量示例并修改：

```bash
cp .env.example .env
```

2. 构建并运行 Docker：

```bash
docker build -t harei .
docker run --env-file .env -p 8000:8000 harei
```

3. 访问：

- 前台：`http://localhost:8000/`
- 管理端：`http://localhost:8000/message`

## 目录说明

- `server/` 后端 Flask 服务
- `web/` 前端 React 应用
- `assets/` 业务图片与背景图
- `uploads/` 上传文件与缩略图
- `blivedm/` 直播间 SDK
