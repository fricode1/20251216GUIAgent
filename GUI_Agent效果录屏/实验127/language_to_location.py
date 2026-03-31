import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def language_to_location(language: str) -> str:
    """从自然语言中提取地理位置信息
    input:
        language: str. 一段文本
    output:
        location: str. 表示地点的文本
    """
    api_key = "sk-588ceaf7b0f542f8881fb62161e9127c"
    model_name = "deepseek-chat"
    base_url = "https://api.deepseek.com"
    llm = ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key=api_key
    )

    # 2. 构建 Prompt 模板
    # 通过系统提示词严格限制模型的输出格式，防止它输出“废话”
    system_prompt = """你是一个专业的地理位置提取助手。
你的唯一任务是从用户输入的自然语言任务描述中，提取出地理位置信息。

严格遵守以下规则：
1. 仅输出提取到的地理位置名称。
2. 绝对不要输出任何额外的解释、语气词或标点符号（如“地点是：”、“提取完毕”等）。
3. 如果输入中没有包含任何地理位置信息，请输出“无”。

【示例】
输入：查询新华路行人违章
输出：新华路

输入：帮我看看明天天气怎么样
输出：无
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "输入：{text}\n输出：")
    ])

    # 3. 使用 LangChain 的 LCEL 语法构建处理链
    # prompt 生成提示词 -> llm 获得大模型响应 -> StrOutputParser 将响应解析为纯文本
    chain = prompt | llm | StrOutputParser()

    # 4. 执行并获取结果
    try:
        # invoke 调用模型并传入参数
        location = chain.invoke({"text": language})
        # 去除可能存在的首尾空格并返回
        return location.strip()
    except Exception as e:
        print(f"大模型调用失败: {e}")
        return ""

# ==========================================
# 测试代码
# ==========================================
if __name__ == "__main__":
    # 请确保你在运行前设置了环境变量，例如:
    # os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxxx"
    
    test_inputs = [
        "查询新华路行人违章",
        "帮我看看朝阳区三里屯周边的交通情况",
        "今天高速封路了吗",
        "把深南大道的监控画面调出来"
    ]
    
    for text in test_inputs:
        loc = lauguage_to_location(text)
        print(f"输入：{text}")
        print(f"输出：{loc}\n" + "-"*30)