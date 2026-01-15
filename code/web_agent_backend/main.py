from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

app = FastAPI()

# 【核心步骤】将 "static" 文件夹挂载到 "/static" 这个路由下
# directory="static" 指的是本地文件夹名字
# name="static" 是 FastAPI 内部调用的名字
app.mount("/static", StaticFiles(directory="static"), name="static")

# 方案 A：直接在浏览器访问 http://127.0.0.1:8000/static/my_image.jpg 就能看到

# 方案 B：写一个接口，动态返回图片的完整 URL
@app.get("/get-image-info")
def get_image_info(request: Request):
    # 假设图片名叫 my_image.jpg
    image_name = "my_image.jpg"
    
    # 构建完整的 URL 路径
    # request.base_url 会自动获取当前服务器的域名和端口 (如 http://127.0.0.1:8000/)
    base_url = str(request.base_url)
    image_url = f"{base_url}static/{image_name}"
    
    return {
        "file_name": image_name,
        "url": image_url
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)