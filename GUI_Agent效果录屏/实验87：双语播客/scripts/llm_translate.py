from openai import OpenAI
import os

# 初始化客户端
client = OpenAI(
    api_key='sk-ifyd3QT6bW95eHm4l7hurU0zDOC4nZuTSH1si707s3vJ6EKW',  
    base_url='https://api.moonshot.cn/v1'
)

def translate_text(text):
    # 构建系统提示词，明确要求"一句英文+对应中文"在同一行
    system_prompt = ("将英文翻译成中文。在你生成的结果中，每行包括：1句英文原文，以及中文翻译。n个英文句子对应n行。每个句子的中文翻译不要新起一行。")

    try:
        print('调用大模型...')
        response = client.chat.completions.create(
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

# 定义章节映射：罗马数字 -> (阿拉伯数字, 实际文件名中的标题部分)
# 注意：必须与 Get-ChildItem 显示的文件名完全一致（包括空格、大小写、标点）
chapters = {
    'xvii': (17, 'Infinity'),
    'xviii': (18, 'Other simple modes'),
    'xix': (19, 'The modes of thinking'),
    'xx': (20, 'Modes of pleasure and pain'),
    'xxi': (21, 'Power'),
    'xxii': (22, 'Mixed modes'),
    'xxiii': (23, 'Complex ideas of substances'),
    'xxiv': (24, 'Collective ideas of substances'),
    'xxv': (25, 'Relation'),
    'xxvi': (26, 'Cause and effect, and other relations'),
    'xxvii': (27, 'Identity and diversity'),
    'xxviii': (28, 'Other relations'),
    'xxix': (29, 'Clear and obscure, distinct and confused ideas'),
    'xxx': (30, 'Real and fantastical ideas'),
    'xxxi': (31, 'Adequate and inadequate ideas'),
    'xxxii': (32, 'True and false ideas'),
    'xxxiii': (33, 'The association of ideas'),
}

# 基础路径
base_input_dir = r'C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验87：双语播客\data\人类理解论第二卷\locke1690book2_one_sentence_per_line'
base_output_dir = r'C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验87：双语播客\data\人类理解论第二卷\各章节'

# 确保输出目录存在
os.makedirs(base_output_dir, exist_ok=True)

print(f"开始批量翻译，共 {len(chapters)} 个章节...")

# 循环处理每个章节
for roman, (arabic, title) in chapters.items():
    # 构建输入文件路径（与实际文件名完全匹配）
    input_filename = f"Chapter {roman} - {title}.txt"
    input_path = os.path.join(base_input_dir, input_filename)
    
    # 构建输出文件路径（Chapter 17.txt, Chapter 18.txt, ...）
    output_filename = f"Chapter {arabic}.txt"
    output_path = os.path.join(base_output_dir, output_filename)
    
    print(f"\n[{roman.upper()} -> Chapter {arabic}] {title}")
    
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            print(f"  ⚠️  跳过：文件不存在 - {input_filename}")
            continue
            
        # 读取文件
        with open(input_path, "r", encoding="utf-8") as f:
            input_text = f.read()
        
        if not input_text.strip():
            print(f"  ⚠️  跳过：文件为空")
            continue
        
        # 执行翻译
        translated_result = translate_text(input_text)
        
        if "发生错误:" in translated_result:
            print(f"  ❌ 翻译失败：{translated_result}")
            continue
        
        # 写入结果
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_result)
            
        print(f"  ✅ 完成 -> {output_filename}")
        
    except Exception as e:
        print(f"  ❌ 异常：{e}")

print(f"\n批量处理结束！输出目录：{base_output_dir}")