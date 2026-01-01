import os
from openai import OpenAI

def get_sop_guideline(user_input, reference_text):
    """
    调用大模型生成严格的线性操作指南
    """
    client = OpenAI(
        api_key='sk-efe1c9004f7e4de0a8ade26120301c6d',
        base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    )

    # 强化约束：强制动词开头，禁止未来式，禁止分支，禁止建议
    system_prompt = (
        "你是一个Web系统操作指令生成器。你必须将参考资料转化为一系列严格的、即时执行的操作步骤。\n"
        "【强制要求】：\n"
        "1. 格式要求：必须使用数字编号（1., 2., 3...），每一步必须以具体的动词开头，例如“点击...”、“输入...”、“选择...”、“上传...”。\n"
        "2. 消除分支：不允许出现“或”、“或者”、“如果...则...”、“若...请...”。必须指定一个确定的操作路径。\n"
        "3. 消除建议：禁止出现“建议...”、“定期查看...”、“请注意...”。只描述动作本身。\n"
        "4. 消除未来假设：禁止描述任务完成后的收尾工作（如“抓捕后上报”、“成功后如何”）。只包含当前能立即执行的操作序列。\n"
        "5. 消除多余描述：不要解释为什么这么做，不要假设用户所在的物理场景（如开车、户外等）。\n"
        "6. 唯一路径：如果资料中有多种方式，请只选择其中一种最直接的方式并固定下来。"
    )

    user_prompt = f"""
参考资料：
---
{reference_text}
---

用户需求：
{user_input}

请根据参考资料生成该任务的纯操作步骤序列：
"""

    try:
        completion = client.chat.completions.create(
            model="qwen-long-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0, # 将随机性降至最低
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"调用模型出错: {e}"

def main():
    # file_path = 'reference.txt'
    file_path = 'qwen.txt'
    if not os.path.exists(file_path):
        print(f"错误：未在当前目录下找到 {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        reference_content = f.read()

    print("=== 严格指令 SOP 生成器 ===")
    user_task = input("请输入任务描述：")

    if not user_task.strip():
        return

    print("\n正在生成线性操作步骤...\n")
    result = get_sop_guideline(user_task, reference_content)
    
    print("-" * 30)
    print(result)
    print("-" * 30)

if __name__ == "__main__":
    main()