# 创建布控应用

## 连接方式

POST

## 创建应用地址

https://62.168.243.10:19080/mrag/api/deploy/tasks/create

## headers

Authorization = eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA

## body

```json
{
    "name": "test1",
    "target_type": "person",
    "desc": "test2",
    "deploy_type": 0,
    "image_base64": "",
    "space_time_list": [
        {
            "device_id": "41132867111327248002",
            "start_time": "2026-03-17 00:00:00",
            "end_time": "2026-03-24 23:59:59",
            "time_slot_list": []
        }
    ],
    "text": "穿白衣服的人",
    "distance": 0.8,
    "prompt": "描述:\n如果目标图片符合描述及示例图片，返回 Y，如果不是则返回 N。不要包含其他字符。\n上传的最后一张图片为目标图片。其他图片为目标示例图片。",
    "prompt_image_base64_list": []
}
```

# 列出所有布控应用

## 连接方式

GET

## 列出所有布控应用的地址

https://62.168.243.10:19080/mrag/api/deploy/tasks/list

## headers

Authorization = eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA

## 响应

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "total": 24,
        "list": [
            {
                "id": "14",
                "name": "骑电动车未戴头盔",
                "status": 1,
                "desc": "骑电动车未戴头盔",
                "distance": "0.7",
                "text": "骑电动车",
                "prompt": "你是一个专业的看图高手。帮我判别图中目标是否在未戴头盔的情况下骑电动车。如果有返回 Y，如果无返回 N。不要包含其他字符。\n",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130305001316199781",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001311657847",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001315713755",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001316374669",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001319169410",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001316977053",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001310000059",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001317028811",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001314135602",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001315510613",
                        "start_time": "2025-10-28 00:00:00",
                        "end_time": "2025-11-04 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "16",
                "name": "脏兮兮的拉着油桶的车辆",
                "status": 0,
                "desc": "脏兮兮的拉着油桶的车辆",
                "distance": "0.7",
                "text": "脏兮兮的拉着油桶的车辆",
                "prompt": "第1张图，是脏兮兮的拉着油桶的车辆，请返回Y。\n第2张图，是拉着废铁的车辆，不是脏兮兮的拉着油桶的车辆，请返回N。\n参考上述样例，判断第3张图是否为脏兮兮的拉着油桶的车辆，若是返回Y，若不是返回N。\n不要包含其他字符。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41139301001310367045",
                        "start_time": "2025-11-05 18:27:40",
                        "end_time": "2025-11-08 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130305001310000020",
                        "start_time": "2025-11-05 18:27:40",
                        "end_time": "2025-11-08 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130305001311318184",
                        "start_time": "2025-11-05 18:27:40",
                        "end_time": "2025-11-08 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130305001313099897",
                        "start_time": "2025-11-05 18:27:40",
                        "end_time": "2025-11-08 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": [
                    "data:image/jpeg;base64,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",
                    "data:image/jpeg;base64,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"
                ]
            },
            {
                "id": "17",
                "name": "打架",
                "status": 0,
                "desc": "打架",
                "distance": "0.7",
                "text": "打架",
                "prompt": "描述:  图像中的人员是否与他人推搡，疑似产生争执。\n如果是返回 Y，如果不是则返回 N。不要包含其他字符。\n",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130202001313235064",
                        "start_time": "2025-11-05 19:03:25",
                        "end_time": "2025-11-12 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "21",
                "name": "渣土车",
                "status": 0,
                "desc": "渣土车",
                "distance": "0.71",
                "text": "渣土车",
                "prompt": "图中的车辆是否拉着渣土（渣土就是建筑垃圾、土等），如果是返回Y，如果不是返回N。注意：车斗中未拉东西的空车，返回N。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130460001310298713",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130460001310680238",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130460001310966054",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130460001310559877",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41139394001310402797",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130460001310602348",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41139394001310512325",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130460001310089884",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130460001310626066",
                        "start_time": "2025-11-13 00:00:00",
                        "end_time": "2025-11-30 23:59:59",
                        "time_slot_list": [
                            "08:00:00-18:00:00"
                        ]
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "40",
                "name": "八一路人群聚集",
                "status": 0,
                "desc": "八一路人群聚集",
                "distance": "0.6",
                "text": "一群人",
                "prompt": "# 任务\n\n你是一名负责图像安全分析助手，任务是按照步骤系统的判断图中是否存在人群聚集的情况。请严格按照以下要求分析提供的图片。请避免推测任何无法从图像中直接获取的信息。\n\n# 具体步骤：\n## 步骤一：定位人体\n- 识别人物数量，找出画面中的人类个体的位置\n## 步骤二：判断是否构成人群\n- 根据人数、分布密度、彼此距离，判断是否出现人群。\n- 判断人群标准：\n-- 多人密集站在一起\n-- 多人处于有限的空间内\n-- 聚集度高于普通行走或分散分布\n## 步骤三: 综合判断是否存在“人群聚集”情况\n- 若画面中存在聚集现象，请按照如下请情况分析：\n-- 聚集的人数>3\n-- 聚集发生在路边或广场上\n-- 聚集方式方式为：站立、围成一圈、打斗\n## 步骤四：排除特殊情况 \n- 排除掉人群一起等红绿灯的情况\n## 步骤五：返回格式\n- 如果图像中存在人群聚集的目标，返回 Y。\n- 如果图像中不存在人群聚集，返回 N。\n- 不要包含其他字符。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130305001310179745",
                        "start_time": "2025-12-08 15:53:50",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "21:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001311079157",
                        "start_time": "2025-12-08 15:53:50",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "21:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130306001318174828",
                        "start_time": "2025-12-08 15:53:50",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "21:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130306001310000021",
                        "start_time": "2025-12-08 15:53:50",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "21:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130306001317772319",
                        "start_time": "2025-12-08 15:53:50",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "21:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001310000006",
                        "start_time": "2025-12-08 15:53:50",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "21:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001310121081",
                        "start_time": "2025-12-08 15:53:50",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "21:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "45",
                "name": "打架斗殴",
                "status": 0,
                "desc": "打架",
                "distance": "0.65",
                "text": "打架",
                "prompt": "# 任务\n\n你是一名负责图像安全分析助手，任务是按照步骤系统的判断图中的人员是否在打架斗殴。请严格按照以下要求分析提供的图片。请避免推测任何无法从图像中直接获取的信息。\n\n# 步骤\n\n## 步骤1：检测并定位人\n- 定位画面中所有可见的人体。\n\n## 步骤2：检测可能的冲突姿态与动作\n- 检查并列出下列任何可见动作/姿态证据（逐项判断是否存在）：\n\t- 举臂、拳击姿势（握拳、前臂抬起）\n    - 推、拉、抓握（双手接触、抓扯衣服）\n    - 踢、跺脚、倒地、摔倒、被压制（身体接触并伴随非平稳姿态）\n    - 肢体相互碰撞、抱摔或多人围攻姿态\n    - 面部表情（若清晰）显示恐惧/痛苦/痛苦/愤怒\n    - 物品作为武器（棍棒、瓶子、刀）——仅描述可见物体与其相对位置，不进行武器鉴定\n    - 大量运动模糊集中在人物交互区域（暗示激烈肢体接触或快速动作）\n\n## 步骤3：判断是否属于“打架斗殴”\n- 综合步骤2的证据，按照下面标准判断是否存在打架斗殴：\n    - **强证据（倾向判定为打架）**至少两个个体有相互施力（拳打、推拉、抓扯、抱摔、踢）或一人倒地且明显由他人施力造成。或多人围绕一人并有直接肢体接触。\n    - **弱证据（需复核）**有激烈肢体接近但模糊或遮挡导致无法确认互相施力（例如双手接触但不确定是拥抱还是抓扯）。\n\n## 步骤4：返回要求\n-- 若存在打架斗殴的人员：返回Y\n-- 若不存在打架斗殴的人员：返回N\n-- 不要包含其他字符。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130202001317538656",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001314912940",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001310000032",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001310000063",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001317750640",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001313235064",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001310987134",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001315196938",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001315241747",
                        "start_time": "2025-12-08 18:03:33",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "47",
                "name": "八一路人群聚集（23点-凌晨5点）",
                "status": 0,
                "desc": "人群聚集",
                "distance": "0.61",
                "text": "一群人",
                "prompt": "# 任务\n\n你是一名负责图像安全分析助手，任务是按照步骤系统的判断图中是否存在人群聚集的情况。请严格按照以下要求分析提供的图片。请避免推测任何无法从图像中直接获取的信息。\n\n# 具体步骤：\n## 步骤一：定位人体\n- 识别人物数量，找出画面中的人类个体的位置\n## 步骤二：判断是否构成人群\n- 根据人数、分布密度、彼此距离，判断是否出现人群。\n- 判断人群标准：\n-- 多人密集站在一起\n-- 多人处于有限的空间内\n-- 聚集度高于普通行走或分散分布\n## 步骤三: 综合判断是否存在“人群聚集”情况\n- 若画面中存在聚集现象，请按照如下请情况分析：\n-- 聚集的人数>3\n-- 聚集发生在路边或广场上\n-- 聚集方式方式为：站立、围成一圈、打斗\n## 步骤四：排除特殊情况 \n- 排除掉人群一起等红绿灯的情况\n## 步骤五：返回格式\n- 如果图像中存在人群聚集的目标，返回 Y。\n- 如果图像中不存在人群聚集，返回 N。\n- 不要包含其他字符。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130305001310179745",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001311079157",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001310000006",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001310185023",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130306001317772319",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130306001318174828",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130306001310000021",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001319233145",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001318395768",
                        "start_time": "2025-12-09 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "23:00:00-23:59:59",
                            "00:00:00-05:00:00"
                        ]
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "50",
                "name": "骑电动车违规载人3",
                "status": 0,
                "desc": "骑电动车违规载人3",
                "distance": "0.62",
                "text": "两个人骑电动车",
                "prompt": "# 任务\n\n你是一名负责图像安全分析助手，任务是按照步骤系统的判断图中是否存在电动车摩托车违规载人的情况（乘坐2人及以上）。请严格按照以下要求分析提供的图片。请避免推测任何无法从图像中直接获取的信息。\n\n# 具体步骤：\n## 步骤一：检测并定位核心主体\n- 识别图中是否存在两轮车，如电动车、摩托车\n\n## 步骤二：统计两轮车乘员数量\n- 违规判定标准：电动车、摩托车核定载人数为1人（驾驶位），实际乘坐人数大于等于2人，且非临时上下车状态\n- 若无法准确计数，则不按违规进行判定\n\n## 步骤三：返回要求\n- 若骑电动车或摩托车的载人情况：\n-- 不违规，返回N\n-- 违规载人，返回Y\n-- 不要包含其他字符。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130305001317425068",
                        "start_time": "2025-12-11 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001316188835",
                        "start_time": "2025-12-11 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001310000026",
                        "start_time": "2025-12-11 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001310000021",
                        "start_time": "2025-12-11 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130202001310000047",
                        "start_time": "2025-12-11 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130202001313083516",
                        "start_time": "2025-12-11 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001310137356",
                        "start_time": "2025-12-11 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001313294415",
                        "start_time": "2025-12-11 00:00:00",
                        "end_time": "2025-12-31 23:59:59",
                        "time_slot_list": [
                            "07:00:00-08:30:00",
                            "11:30:00-13:00:00",
                            "16:30:00-18:00:00"
                        ]
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "61",
                "name": "育阳桥烟花燃放",
                "status": 0,
                "desc": "烟花燃放",
                "distance": "0.67",
                "text": "烟花燃放",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成燃放烟花行为的研判，请严格遵循以下逻辑执行分析： \n一、图像基础信息解析\n- 识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等） \n二、烟花相关视觉特征检测\n- 烟火特征识别：检测画面中是否存在烟花燃放的典型视觉特征，包括但不限于：\n-- 动态光效：瞬间爆发的彩色亮光（红黄绿蓝等）、持续的火花轨迹、烟雾扩散形成的团状/条状光影\n-- 实体特征：升空的烟花弹体、地面未燃放的烟花筒/烟花盒、燃放后残留的纸屑\n-- 行为特征：人物手持烟花棒的摆动动作、弯腰点烟烟花的肢体姿态、多人围站观看烟花的聚集行为\n- 干扰目标排除：将画面中易混淆的视觉元素与烟花特征做区分，排除干扰项\n-- 光源干扰：汽车尾灯、刹车灯，路灯闪烁，节日彩灯\n-- 其他物体：车辆排气管的烟雾、电焊施工的弧光\n三、燃放烟花行为的定位与确认\n- 若检测出烟花相关的视觉特征，需记录\n- 结合人体目标检测结果，确认是否存在“人-烟花”的关联行为，判断是否为人类主动操作燃放烟花的行为，排除自然因素或物体意外产生的类似视觉效果\n四、燃放烟花行为等级判定\n- 无燃放行为：画面中未检测到任何烟花相关视觉特征\n- 疑似燃放行为：检测到模糊的火花/烟雾特征，无法明确区分是否为烟花燃放\n- 确认燃放行为：清晰检测到烟花燃放的光效/实体/行为特征，且能确认是人类主动操作的燃放行为\n五、返回格式 \n如果图中存在疑似燃放行为/确认燃放行为的情况，返回Y \n如果图中无燃放行为情况，返回N \n不要包含其他字符\n",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130208001311950893",
                        "start_time": "2026-01-05 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": [
                            "18:00:00-23:59:59",
                            "00:00:00-06:00:00"
                        ]
                    },
                    {
                        "device_id": "41130302001312953948",
                        "start_time": "2026-01-05 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": [
                            "18:00:00-23:59:59",
                            "00:00:00-06:00:00"
                        ]
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "64",
                "name": "未成年持械并聚众",
                "status": 1,
                "desc": "仲景桥南边东下台阶处枪\n仲景大桥南头南\n湿地公园西枪\n光武桥东头南\n育阳桥北西湿地下台阶处枪\n滨河路育阳桥北头东",
                "distance": "0.67",
                "text": "人群",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集、持械斗殴行为的研判，请严格遵循以下逻辑执行分析： \n一、图像基础信息解析\n- 识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等） \n二、人群目标检测与统计\n- 采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影） 统计区域内的人体目标总数，记录画面中人体目标的总数量 \n- 聚众特征分析：计算人群的空间分布密度，判断人群聚集状态\n-- 分散：个体间距大于2米，无明显聚集趋势\n-- 聚众：多人形成团块聚集，个体间距小于1米，且聚集人数大于等于3人，\n三、斗殴行为的识别\n- 肢体动作检测：识别画面中的人体异常肢体动作，典型斗殴行为特征包括：\n-- 攻击性的动作：挥拳、踢踹、撕扯、拖拽、扑倒、连续挥打；\n-- 防御性的动作：抱头躲避、格挡、后退避让；\n-- 群体交互动作：多人围堵单一目标，相互推搡形成肢体冲突，多人参与的对抗性动作。\n- 行为真实性验证：排除非斗殴类肢体动作干扰（嬉戏打闹、拥抱、意外碰撞），结合动作的连续性，激烈程度及人群反应，验证斗殴行为是否成立\n四、持械特征检测与识别\n- 器械目标检测：识别画面中是否存在可作为斗殴工具的器械，具体类型包括：\n-- 管制类器械：刀具（匕首、砍刀）、棍棒（钢管、木棍）、砖石块、玻璃瓶、金属器械；\n-- 非管制器械：桌椅、拖把杆、健身器械、工具锤等；\n- 持械行为确认：检测人体与器械的关联关系，判断是否存在手持器械、挥舞器械、用器械击打他人等行为，排除以下干扰项：\n-- 环境固定物（树枝、围栏）\n-- 光影误判（物体阴影、反光等）\n五、事件等级判定\n无异常：画面人数小于等于三人，无聚集行为，人体肢体动作均为正常活动（行走、站立、交谈）\n疑似聚众：聚集人数3-5人，个体间距小于1米，存在推搡等轻微肢体接触，但无明显斗殴动作，未检测到器械\n聚众：聚集人数3-5人，多人形成团块聚集，个体间距小于1米\n聚众斗殴：聚集人数大于等于5人，出现挥打、踢踹、撕扯等明确斗殴动作，未检测出持械行为，或3-4人出现激烈肢体对抗行为\n持械聚众斗殴：聚集人数大于等于3人，既检测到斗殴行为，又识别出持械动作或器械存在，且器械被用于攻击性动作\n严重持械斗殴：聚集人数大于等于8人，持械类型为管制刀具等攻击性器械，出现多人围殴，器械击打人体倒地等严重暴力行为\n六、返回格式 \n如果图中存在疑似聚众、聚众、聚众斗殴、持械聚众斗殴、严重持械斗殴的情况，返回Y \n如果图中无异常行为情况，返回N \n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41137206001315969280",
                        "start_time": "2026-01-06 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41137206001318918146",
                        "start_time": "2026-01-06 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130204001318094949",
                        "start_time": "2026-01-06 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41137207001310000004",
                        "start_time": "2026-01-06 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130302001315654367",
                        "start_time": "2026-01-06 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130302001312953948",
                        "start_time": "2026-01-06 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41137206001317690583",
                        "start_time": "2026-01-06 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "66",
                "name": "吾悦广场聚集",
                "status": 0,
                "desc": "建设路360高空\n360广场东南角球\n人民路建设路东",
                "distance": "0.69",
                "text": "街景",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、排除非聚集行为的人群数量\n排除画面中人群数量多时的行为（如聚集街边等车/多辆电动车路面行驶等），再统计人群聚集人数数量\n五、人群聚集等级判定\n重度聚集：画面总人数大于30人，形成大面积连续人群聚集且人群无明显流动空间\n中度聚集：画面总人数11-30人，形成2-3个聚集团块且存在人群流动缓慢现象\n轻度聚集：画面总人数4-10人，形成1个小型聚集团块\n六、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130307001310057412",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130307001310037789",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001310000064",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "68",
                "name": "宛城万悦城聚集",
                "status": 0,
                "desc": "市民中心2号楼万悦城鸟瞰 范蠡路南都路北 南都路向北高空",
                "distance": "0.69",
                "text": "街景",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、排除非聚集行为的人群数量\n排除画面中人群数量多时的行为（如聚集街边等车/多辆电动车路面行驶/篮球场人群打球等），再统计人群聚集人数数量\n五、人群聚集等级判定\n重度聚集：画面总人数大于30人，形成大面积连续人群聚集且人群无明显流动空间\n中度聚集：画面总人数11-30人，形成2-3个聚集团块且存在人群流动缓慢现象\n轻度聚集：画面总人数4-10人，形成1个小型聚集团块\n六、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41139303001310233896",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130203001310000023",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130203001310050350",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "69",
                "name": "宛城万达聚集",
                "status": 0,
                "desc": "明山路万达广场\n中州路明山路\n南都路向北高空",
                "distance": "0.69",
                "text": "街道",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、排除非聚集行为的人群数量\n排除画面中人群数量多时的行为（如聚集街边等车/多辆电动车路面行驶/篮球场人群打球等），再统计人群聚集人数数量\n五、人群聚集等级判定\n重度聚集：画面总人数大于30人，形成大面积连续人群聚集且人群无明显流动空间\n中度聚集：画面总人数11-30人，形成2-3个聚集团块且存在人群流动缓慢现象\n轻度聚集：画面总人数4-10人，形成1个小型聚集团块\n六、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41139303001310446456",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41139303001310982912",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130203001310050350",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "71",
                "name": "高新吾悦广场聚集",
                "status": 0,
                "desc": "创业大厦高新区政府区域高空AR球\n独山大道新城国际高空\n独山大道信臣路南",
                "distance": "0.69",
                "text": "街道",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、排除非聚集行为的人群数量\n排除画面中人群数量多时的行为（如聚集街边等车/多辆电动车路面行驶/篮球场人群打球等），再统计人群聚集人数数量\n五、人群聚集等级判定\n重度聚集：画面总人数大于30人，形成大面积连续人群聚集且人群无明显流动空间\n中度聚集：画面总人数11-30人，形成2-3个聚集团块且存在人群流动缓慢现象\n轻度聚集：画面总人数4-10人，形成1个小型聚集团块\n六、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130460001310045582",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130204001310074093",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130460001310234103",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "72",
                "name": "未成年聚集点位",
                "status": 0,
                "desc": "人民路民主街口球\n中州路菜市街交叉口东北角\n孔明路明山路南\n人民路中州路北\n新华路明山路口\n人民路新华路东\n滨河路向阳荷花南口东北角报警球机\n人民路人民公园西门枪",
                "distance": "0.69",
                "text": "人群",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、排除非聚集行为的人群数量\n排除画面中人群数量多时的行为（如聚集街边等车/多辆电动车路面行驶/篮球场人群打球/老年人跳广场舞/街边小吃摊买饭等），再统计人群聚集人数数量\n五、人群聚集等级判定\n重度聚集：画面总人数大于30人，形成大面积连续人群聚集且人群无明显流动空间\n中度聚集：画面总人数11-30人，形成2-3个聚集团块且存在人群流动缓慢现象\n轻度聚集：画面总人数4-10人，形成1个小型聚集团块\n六、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130202001315658894",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001313124529",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130204001314199958",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001310000075",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130204001310000046",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001310000071",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130201001310142573",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001315708674",
                        "start_time": "2026-01-09 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "76",
                "name": "七一游园聚集",
                "status": 0,
                "desc": "七一路七一游园枪 七一游园东门内枪",
                "distance": "0.67",
                "text": "人",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、人群聚集等级判定\n重度聚集：画面总人数大于40人，形成大面积连续人群聚集，覆盖广场核心区域，且人群无明显流动空间/无明显个体间距\n中度聚集：画面总人数21-40人，形成3-4个聚集团块，部分间距小于1米\n轻度聚集：画面总人数11-20人，形成1-2个小型休闲聚团\n五、正常行为过滤规则\n过滤休闲健身聚集：画面中可见做广场舞/打太极等人群成规律队列/动作的健身群体\n过滤游玩聚集：可见游玩群体，如打羽毛球/踢毽子，带小孩玩的群体\n过滤自然聚集：河边/步道上正在散步或者赏景的人群，无停留聚团特征\n六、满足以下任一条即为异常情况\n非休闲时段如晚上九点以后到凌晨的公园核心区/湖边等区域出现轻度及以上聚集行为\n聚集人群呈现围堵/推搡/聚集在危险区域如湖边河边等异常行为\n七、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集/异常情况的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130302001316073892",
                        "start_time": "2026-01-14 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130302001312697519",
                        "start_time": "2026-01-14 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "77",
                "name": "政府/信访局聚集",
                "status": 0,
                "desc": "南阳市卧龙区政府门口枪 南阳市信访局门口枪",
                "distance": "0.68",
                "text": "人",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、人群聚集等级判定\n重度聚集：画面总人数大于20人，形成大面积连续人群聚集，封堵门口/道路\n中度聚集：画面总人数11-20人，形成2-3个聚集团块，部分间距小于1米\n轻度聚集：画面总人数4-10人，形成1个小型聚团\n五、正常行为过滤规则\n过滤办事相关聚集：画面中可见进入门口/取号等候的人群\n过滤公务相关聚集：可见安保/警务人员/政府工作人员的通勤群体\n过滤临时路过聚集：画面中路过的人群/外卖员等，无停留聚团特征\n六、满足以下任一条即为异常情况\n政府门口/信访局等出入口出现轻度及以上聚集\n聚集人群携带横幅/标语牌设备，或呈现举牌，高声呼喊的异常姿态\n聚集人群封堵政府门口通道/阻碍车辆通行等异常行为\n七、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集/异常情况的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130302001310000028",
                        "start_time": "2026-01-14 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130305001319493735",
                        "start_time": "2026-01-14 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "78",
                "name": "夜间未成年人聚集",
                "status": 0,
                "desc": "人民路-中心广场-北中国银行-门口东\n南阳市鸿德广场中行口",
                "distance": "0.68",
                "text": "人",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、人群聚集等级判定\n重度聚集：画面总人数大于15人，形成大面积连续人群聚集，封堵学校门口/人行道\n中度聚集：画面总人数9-15人，形成2-3个聚集团块，部分间距小于1米\n轻度聚集：画面总人数5-8人，形成1个小型聚团\n五、正常行为过滤规则\n过滤放学等候聚集：画面中可见家长/车辆，聚集在学校指定等候区人群\n过滤过路聚集：仅短暂经过马路的群体，无停留聚团特征\n过滤交通等候聚集：公交站/网约车点小于5人的等候群体，无停留聚团特征\n六、满足以下任一条即为异常情况\n晚上22点后出现轻度及以上聚集，且无家长/老师陪同\n聚集未成年携带管制器具，烟酒/打火机等，或呈现打架/欺凌的异常姿态\n画面中呈现翻越护栏/破坏公共设施/聚集在酒吧/网吧门口等异常姿态\n人群中出现推搡/斗殴行为\n七、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集/异常情况的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130305001312315000",
                        "start_time": "2026-01-14 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": [
                            "19:00:00-23:59:59",
                            "00:00:00-04:00:00"
                        ]
                    },
                    {
                        "device_id": "41130305001317583650",
                        "start_time": "2026-01-14 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": [
                            "19:00:00-23:59:59",
                            "00:00:00-04:00:00"
                        ]
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "80",
                "name": "吾悦/万达/大悦城人群聚集",
                "status": 0,
                "desc": "360广场东南角球\n人民路建设路东\n范蠡路南都路北\n孔明路明山路西\n独山大道信臣路南",
                "distance": "0.68",
                "text": "一群人",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成人群聚集状态研判，请严格遵循以下逻辑执行分析：\n一、图像基础信息解析\n识别监控画面的拍摄视角（如俯视/鸟瞰/高空/平视/侧视），画面场景类型（如城市道路/商业广场/车站/居民区等）\n二、人群目标检测与统计\n采用人体目标检测算法，识别画面中所有人体目标，（含完整人体/半身人体/行人轮廓），排除非人体干扰目标（如雕塑/广告牌人像/车辆阴影）\n统计区域内的人体目标总数，记录画面中人体目标的总数量\n三、人群分布分析\n分析人群的空间分布特征：判断人群是分散分布（个体间距大于2米），局部聚集（多人聚集形成团块）还是整体聚集（大面积区域内人群连续分布）\n四、人群聚集等级判定\n重度聚集：画面总人数大于100人，形成大面积连续人群聚集且人群无明显流动空间/无明显个体间距\n中度聚集：画面总人数51-100人，形成3-5个聚集团块且存在人群流动缓慢现象，部分区域人群连续分布\n轻度聚集：画面总人数21-50人，形成1-2个小型聚集团块，间距1-2米\n五、正常行为过滤规则\n过滤消费相关聚集：画面中可见商场出入口排队队列，促销展台周边的围观人群\n过滤设施关联聚集：出租车/网约车候车点的人群\n过滤运营相关聚集：保洁/安保人员，搬运货品商户的群体\n过滤临时路过聚集：画面中路过的人群/外卖员等，无停留聚团特征\n过滤放学等候聚集：画面中可见家长/车辆，聚集在学校指定等候区人群\n过滤过路聚集：仅短暂经过马路的群体，无停留聚团特征\n过滤交通等候聚集：公交站/网约车点小于5人的等候群体，无停留聚团特征\n六、满足以下任一条即为异常情况\n广场中央空地区域出现中度及以上聚集\n聚集人群呈现围堵/对峙/举牌等异常行为\n七、返回格式\n如果图中存在重度聚集/中度聚集/轻度聚集/异常情况的情况，返回Y\n如果图中不存在人群聚集的情况，返回N\n不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130307001310037789",
                        "start_time": "2026-01-15 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001310000064",
                        "start_time": "2026-01-15 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130203001310000023",
                        "start_time": "2026-01-15 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130203001310000049",
                        "start_time": "2026-01-15 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130460001310234103",
                        "start_time": "2026-01-15 00:00:00",
                        "end_time": "2026-02-28 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "85",
                "name": "翻越栏杆新",
                "status": 1,
                "desc": "人民路民主街东南角100米路东枪 人民路民主街口球",
                "distance": "0.67",
                "text": "翻越栏杆的人",
                "prompt": "你是计算机视觉安全领域的智能分析模型，需基于监控画面图像信息，按照标准化步骤完成翻越护栏状态研判，请严格遵循以下逻辑执行分析： \n一、核心前置判定\n 马路护栏及道路场景识别\n 护栏类型：画面中存在市政道路护栏，包括中央隔离护栏/机非隔离护栏/人行道边缘护栏，特征为连续线性分布\n二、行人翻越行为的视觉特征判定\n 行人翻越护栏的行为需要通过肢体姿态与空间位置的组合特征判定，分为预备翻越，正在翻越，翻越完成三个阶段的特征识别，具体为\n 预备翻越：行人身体正对护栏，双脚离地会单脚蹬踏护栏底部，双手抓握护栏顶端，身体前倾，重心向护栏方向偏移\n 正在翻越：行人身体部分或全部悬空与护栏正上方，躯干与护栏呈交叉状态，手脚分别位于护栏两侧，或身体完全跨越护栏中轴线\n 翻越完成：行人身体已完全抵达护栏另一侧，双脚落地，身体朝向背离护栏方向，或正快速离开护栏区域 \n三、给你的三张图片是两个角度行人翻越护栏的案例，参考图片进行学习，包括但不限于行人翻越护栏的位置/衣着/动作。 \n四、返回格式 如果图中存在预备翻越/正在翻越/翻越完成的情况，返回Y 如果图中不存在翻越护栏的情况，返回N 不要包含其他字符",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130202001310154105",
                        "start_time": "2026-02-05 00:00:00",
                        "end_time": "2026-02-12 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41130202001315658894",
                        "start_time": "2026-02-05 00:00:00",
                        "end_time": "2026-02-12 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": [
                    "data:image/jpeg;base64,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",
                    "data:image/jpeg;base64,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",
                    "data:image/jpeg;base64,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"
                ]
            },
            {
                "id": "88",
                "name": "翻越护栏1",
                "status": 1,
                "desc": "人民路-中心广场-东北，人民路民主街口球",
                "distance": "0.8",
                "text": "翻越栏杆",
                "prompt": "描述: 1、识别栏杆和人，人没有骑行交通工具；2、人和栏杆有接触；3、人有类似图片中的动作.\n如果目标图片符合描述及示例图片，返回 Y，如果不是则返回 N。不要包含其他字符。\n",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41130305001312437578",
                        "start_time": "2026-03-06 00:00:00",
                        "end_time": "2026-03-13 23:59:59",
                        "time_slot_list": [
                            "08:00:00-12:00:00",
                            "13:00:00-18:00:00"
                        ]
                    },
                    {
                        "device_id": "41130202001315658894",
                        "start_time": "2026-03-06 00:00:00",
                        "end_time": "2026-03-13 23:59:59",
                        "time_slot_list": [
                            "08:00:00-12:00:00",
                            "13:00:00-18:00:00"
                        ]
                    }
                ],
                "prompt_image_url_list": [
                    "data:image/jpeg;base64,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",
                    "data:image/jpeg;base64,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",
                    "data:image/jpeg;base64,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"
                ]
            },
            {
                "id": "89",
                "name": "test",
                "status": 0,
                "desc": "test",
                "distance": "0.8",
                "text": "穿黑衣服的人",
                "prompt": "描述:\n如果目标图片符合描述及示例图片，返回 Y，如果不是则返回 N。不要包含其他字符。\n上传的最后一张图片为目标图片。其他图片为目标示例图片。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41132867111327248002",
                        "start_time": "2026-03-17 00:00:00",
                        "end_time": "2026-03-24 23:59:59",
                        "time_slot_list": []
                    },
                    {
                        "device_id": "41139902000000774413",
                        "start_time": "2026-03-17 00:00:00",
                        "end_time": "2026-03-24 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "90",
                "name": "test1",
                "status": 0,
                "desc": "test2",
                "distance": "0.8",
                "text": "穿白衣服的人",
                "prompt": "描述:\n如果目标图片符合描述及示例图片，返回 Y，如果不是则返回 N。不要包含其他字符。\n上传的最后一张图片为目标图片。其他图片为目标示例图片。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41132867111327248002",
                        "start_time": "2026-03-17 00:00:00",
                        "end_time": "2026-03-24 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            },
            {
                "id": "91",
                "name": "test1",
                "status": 1,
                "desc": "test2",
                "distance": "0.8",
                "text": "穿白衣服的人",
                "prompt": "描述:\n如果目标图片符合描述及示例图片，返回 Y，如果不是则返回 N。不要包含其他字符。\n上传的最后一张图片为目标图片。其他图片为目标示例图片。",
                "deploy_type": 0,
                "left_seconds": 0,
                "right_seconds": 0,
                "image_url": null,
                "space_time_list": [
                    {
                        "device_id": "41132867111327248002",
                        "start_time": "2026-03-17 00:00:00",
                        "end_time": "2026-03-24 23:59:59",
                        "time_slot_list": []
                    }
                ],
                "prompt_image_url_list": []
            }
        ]
    }
}
```

# 启动布控应用

## 连接方式

POST

## 启动布控应用地址

https://62.168.243.10:19080/mrag/api/deploy/tasks/start


## headers

Authorization = eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA

## body

{"id":"91"}

# 查看布控结果

## 连接方式

GET

## 查看布控结果网址

https://62.168.243.10:19080/mrag/api/deploy/alarm/list?id=21&pageNo=1&pageSize=10

## headers

Authorization = eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA

## 响应

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "total": 53,
        "list": [
            {
                "url": "http://62.168.243.12:19111/upload/20251124/07/59/1763942351568_873_YoQJXU.jpg",
                "id": "29856",
                "bbox": {
                    "x1": 949,
                    "y1": 284,
                    "x2": 1527,
                    "y2": 961
                },
                "time": "2025-11-24 07:59:12",
                "lng": null,
                "lat": null,
                "similar": 0.7125,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251124/07/59/1763942351574_474_PFObRA.jpg",
                "id": "29857",
                "bbox": {
                    "x1": 949,
                    "y1": 284,
                    "x2": 1527,
                    "y2": 961
                },
                "time": "2025-11-24 07:59:12",
                "lng": null,
                "lat": null,
                "similar": 0.7125,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251124/07/59/1763942343686_860_3kVDSw.jpg",
                "id": "29855",
                "bbox": {
                    "x1": 949,
                    "y1": 284,
                    "x2": 1527,
                    "y2": 961
                },
                "time": "2025-11-24 07:59:04",
                "lng": null,
                "lat": null,
                "similar": 0.7124,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251122/15/32/1763796748544_525_Io0YXJ.jpg",
                "id": "29835",
                "bbox": {
                    "x1": 699,
                    "y1": 367,
                    "x2": 1172,
                    "y2": 881
                },
                "time": "2025-11-22 15:32:29",
                "lng": null,
                "lat": null,
                "similar": 0.7377,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251122/15/32/1763796748567_988_1xYCtI.jpg",
                "id": "29836",
                "bbox": {
                    "x1": 699,
                    "y1": 367,
                    "x2": 1172,
                    "y2": 881
                },
                "time": "2025-11-22 15:32:29",
                "lng": null,
                "lat": null,
                "similar": 0.7376,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251122/15/32/1763796744843_568_xlB28U.jpg",
                "id": "29834",
                "bbox": {
                    "x1": 699,
                    "y1": 367,
                    "x2": 1172,
                    "y2": 881
                },
                "time": "2025-11-22 15:32:25",
                "lng": null,
                "lat": null,
                "similar": 0.7376,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251122/14/55/1763794525757_985_t4pkca.jpg",
                "id": "29833",
                "bbox": {
                    "x1": 1,
                    "y1": 4,
                    "x2": 723,
                    "y2": 302
                },
                "time": "2025-11-22 14:55:26",
                "lng": null,
                "lat": null,
                "similar": 0.7107,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251122/14/34/1763793277150_241_lyOSln.jpg",
                "id": "29832",
                "bbox": {
                    "x1": 936,
                    "y1": 285,
                    "x2": 1274,
                    "y2": 458
                },
                "time": "2025-11-22 14:34:37",
                "lng": null,
                "lat": null,
                "similar": 0.7127,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251122/10/41/1763779272646_851_LEnKgu.jpg",
                "id": "29831",
                "bbox": {
                    "x1": 1288,
                    "y1": 38,
                    "x2": 1917,
                    "y2": 407
                },
                "time": "2025-11-22 10:41:13",
                "lng": null,
                "lat": null,
                "similar": 0.7163,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            },
            {
                "url": "http://62.168.243.12:19111/upload/20251122/10/41/1763779268120_113_kEbRvS.jpg",
                "id": "29830",
                "bbox": {
                    "x1": 1288,
                    "y1": 38,
                    "x2": 1917,
                    "y2": 407
                },
                "time": "2025-11-22 10:41:08",
                "lng": null,
                "lat": null,
                "similar": 0.7163,
                "type": "vehicle",
                "device_name": null,
                "alarm_status": -1
            }
        ]
    }
}
```