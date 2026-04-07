from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List


# 1. 定义期望的输出结构 (Pydantic Model)
class LocationResult(BaseModel):
    output_location_list: List[str] = Field(
        description="根据用户的确认回复，提取出的最终地点列表。如果用户删除了某些地点，请勿包含；如果用户新增了地点，请加入其中。"
    )

def confirm_locations(input_location_list: List[str]) -> List[str]:
    # 2. 初始化大模型并绑定结构化输出
    llm = ChatOpenAI(
        base_url="https://api.deepseek.com",  # 关键点：替换为本地地址
        api_key="sk-1168fbfd73ae4fbb8dfc6b3b6b7db27b",                    # 关键点：本地部署通常不需要真实 Key
        model="deepseek-chat"                       # 关键点：指定你本地运行的模型名称
    )
    structured_llm = llm.with_structured_output(LocationResult, method="function_calling")

    # 3. 询问用户
    print(f"\n系统检测到以下地点：{input_location_list}")
    user_reply = input("请确认是否保留这些地点？(可回复'全部确认'，或告知删除/新增哪些地点): ")

    # 4. 构建 Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个地点提取助手。初始地点列表为：{input_list}。请根据用户的回复，推断出最终的地点列表。"),
        ("human", "用户的回复是：{user_reply}")
    ])

    # 5. 组装 Chain 并执行
    chain = prompt | structured_llm
    result = chain.invoke({
        "input_list": input_location_list,
        "user_reply": user_reply
    })

    return result.output_location_list

# ================= 测试运行 =================
if __name__ == "__main__":
    input_list = ["北京", "上海", "广州"]
    output_list = confirm_locations(input_list)
    print(f"\n[最终输出] output_location_list: {output_list}")