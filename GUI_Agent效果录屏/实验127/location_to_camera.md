# 功能要求
输入：地点
输出：该地点对应的apeId
举例：
输入：新华路
输出：41138130001312152683

# 实现方式

python函数：
```python
def location_to_camera(location):
    """根据地点查询摄像头ID
    input:
        location: str
    return:
        camera_id: str
    """
```

# 请求网址
https://62.168.243.10:19080/data/api/v1/device/list

# 请求方法
POST

# 请求标头
```text
Authorization: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImU3OGZlOWYxLWE1YzAtNDg0OS1iMTUxLTE3MmZkZjY3MTIzNiJ9.FgNeLLZAiaI3VE3fBZONZ7aWHiROGjIFso0hnv1D1yZXmLvQhe9Z0SSMXINucSrvIkCP_ab5LCsmeFk-tPhoyQ
```

# 载荷
```json
{"pageNumber":1,"pageSize":1,"queryCondition":"新华路"}
```

# 响应
```json
{
    "code": "0",
    "msg": "操作成功",
    "data": {
        "pageNumber": 1,
        "pageSize": 10,
        "total": 1296,
        "totalPage": 130,
        "list": [
            {
                "apeId": "41138130001312152683",
                "name": "邓州市新华路胜利所门前",
                "model": "hikvision",
                "ipAddr": "41.220.39.102",
                "ipv6Addr": null,
                "port": 8000,
                "longitude": 112.108673,
                "latitude": 32.688807,
                "placeCode": null,
                "place": null,
                "orgCode": null,
                "capDirection": null,
                "monitorDirection": null,
                "monitorAreadesc": null,
                "isOnline": "0",
                "ownerApsId": null,
                "userId": null,
                "password": null,
                "cameraFeatureType": null,
                "cameraType": null,
                "cameraFeature": null,
                "cameraTypePoint": null,
                "cameraTypePosition": null,
                "sourceType": 1,
                "screenshotUrl": null
            }
        ]
    }
}
```