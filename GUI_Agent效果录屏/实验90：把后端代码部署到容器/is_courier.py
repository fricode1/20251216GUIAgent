import os
import json
import requests
import logging
import base64


LLM_URL = 'http://44.71.1.34:8088/lm/v2/chat/completions'
LLM_KEY = '27500F1342E612C5455CAA0B6B492FB3'
def call_LLM(prompt_txt, image_base64_list):
    post_data = {
        'model':'qwen25-vl-72b-instruct',
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_txt
                    }
                ]
            }
        ]
    }
    for image_base64 in image_base64_list:
        post_data["messages"][0]["content"].append({"type":"image_url", "image_url":{"url": "data:image/jpeg;base64," + image_base64}})
    try:
        key = 'Bearer ' + LLM_KEY
        headers = {
            "Authorization": key,
            "Content-Type": "application/json"
        }
        response = requests.post(LLM_URL, json=post_data, headers=headers)
        res = response.json()
    except Exception as e:
        logging.error("call llm exception: " + str(e))
        return None
    if 'choices' in res and len(res['choices']) > 0  and 'message' in res['choices'][0] and 'content' in res['choices'][0]['message']:
        return res['choices'][0]['message']['content']
    return None


def get_career(img_path):
    prompt = '''
    返回JSON字典。如果画面中有外卖员，则返回的JSON字典为：{"is_courier": "yes"}。如果画面中没有外卖员，则返回的JSON字典为：{"is_courier": "no"}
    '''
    with open(img_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
    result = call_LLM(prompt, [img_b64])
    if '"is_courier": "yes"' in result:
        return 'courier'
    else:
        return 'unknown'


if __name__ == '__main__':
    # img_file = '/home/zcc/zhbli/projects/外卖员识别/courier_yes.jpg'
    img_file = '/home/zcc/zhbli/projects/外卖员识别/courier_no.jpg'
    career = get_career(img_file)
    print(career)