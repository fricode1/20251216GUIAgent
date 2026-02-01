from openai import OpenAI

# 初始化客户端
client = OpenAI(
    # api_key="sk-6fda4f18a54140c6ae408fdd13cfe97d", 
    api_key='sk-ifyd3QT6bW95eHm4l7hurU0zDOC4nZuTSH1si707s3vJ6EKW',  
    # base_url="https://api.deepseek.com"
    base_url='https://api.moonshot.cn/v1'
)

def translate_text(text):
    # 构建系统提示词，明确要求“一句英文+对应中文”在同一行
    system_prompt = ("将英文翻译成中文。在你生成的结果中，每行包括：1句英文原文，以及中文翻译。n个英文句子对应n行。每个句子的中文翻译不要新起一行。")

    try:
        print('调用大模型')
        response = client.chat.completions.create(
            # model="deepseek-chat",
            model='kimi-k2.5',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"发生错误: {e}"

input_path = r'C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验87：双语播客\data\人类理解论第二卷\locke1690book2_one_sentence_per_line\Chapter xvi - Number.txt'
with open(input_path, "r", encoding="utf-8") as f:
        input_text = f.read()

# 执行翻译
translated_result = translate_text(input_text)

output_path = r'C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验87：双语播客\data\人类理解论第二卷\各章节\Chapter 16.txt'
with open(output_path, "w", encoding="utf-8") as f:
    f.write(translated_result)