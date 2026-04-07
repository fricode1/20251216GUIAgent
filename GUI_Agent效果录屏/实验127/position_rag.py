import json
import requests
from typing import List
from collections import defaultdict
from pydantic import BaseModel, Field

from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI

# ================= 1. 自定义本地 BGE 向量模型 =================
class LocalBGEEmbeddings(Embeddings):
    """
    自定义 LangChain Embedding 类，用于对接本地 HTTP 部署的 BGE 模型
    """
    def __init__(self, api_url: str):
        self.api_url = api_url

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        给文档列表（即知识库里的标签）提取特征向量
        注意：这里的 json payload 和 response 解析需要根据你实际的 HTTP API 接口格式进行修改！
        """
        # 假设你的 HTTP 接口接收 {"texts": ["文本1", "文本2"]} 这样的格式
        payload = {"texts": texts}
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # 假设你的接口返回格式为 {"embeddings": [[0.1, 0.2...], [0.3, 0.4...]]}
            # 请根据实际情况修改提取字段
            return data["embeddings"]
        except Exception as e:
            print(f"请求本地 BGE 模型失败: {e}")
            raise e

    def embed_query(self, text: str) -> List[float]:
        """
        给用户查询（单条文本）提取特征向量
        """
        # 直接复用上面的方法，包成列表，取出第一个结果
        return self.embed_documents([text])[0]


# ================= 2. 核心匹配逻辑 =================
class LocalRAGMatcher:
    def __init__(self, json_file_path: str, bge_api_url: str):
        print("1. 正在初始化本地 BGE 向量模型...")
        # 实例化我们刚才写的自定义 BGE 类
        self.embeddings = LocalBGEEmbeddings(api_url=bge_api_url)
        
        print("2. 正在解析 JSON 并构建 FAISS 向量知识库...")
        docs = self._load_data(json_file_path)
        # 这一步会调用你的本地 HTTP 接口，把几百个标签全部变成向量存进 FAISS
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        
        print("3. 正在组装大模型推理链...")
        self._build_chain()
        print("初始化完成！\n")

    def _load_data(self, file_path: str) -> List[Document]:
        """解析 JSON，合并相同标签名，并转为 LangChain 识别的 Document 格式"""
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        label_to_ids = defaultdict(list)
        for item in raw_data.get('data', []):
            label_name = item.get('labelName')
            item_id = item.get('id')
            if label_name and item_id is not None:
                label_to_ids[label_name].append(item_id)
                
        docs = []
        for name, ids in label_to_ids.items():
            docs.append(Document(page_content=name, metadata={"ids": ids}))
        return docs

    def _build_chain(self):
        """构建检索后的 LLM 决策链条"""
        # 这里的大模型（LLM）用于最后一步做逻辑判断。
        # 如果你的 LLM 也是本地部署的（例如 vLLM/Ollama 部署的 Qwen），可以修改 base_url
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo", # 替换为你的大模型名称
            api_key="sk-xxxxxx",   # 替换为你的 API KEY
            # base_url="http://localhost:8000/v1", # 如果是本地兼容大模型，解开这行注释
            temperature=0
        )

        class MatchResult(BaseModel):
            is_matched: bool = Field(description="是否找到了合适的标签")
            matched_label: str = Field(description="匹配上的标签名称")
            ids: list[int] = Field(description="匹配标签对应的 ID 列表")

        parser = JsonOutputParser(pydantic_object=MatchResult)

        prompt = PromptTemplate(
            template="用户的需求是：【{query}】\n\n"
                     "从向量库检索到的最接近的候选标签如下：\n"
                     "{candidates}\n\n"
                     "请选出一个最符合用户意图的标签。\n"
                     "{format_instructions}\n",
            input_variables=["query", "candidates"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        self.chain = prompt | self.llm | parser

    def match(self, query: str, top_k: int = 5):
        # 1. FAISS 向量检索（此时会调用 bge_api_url 把 query 变成向量）
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
        retrieved_docs = retriever.invoke(query)
        
        # 2. 整理检索结果
        candidates_str = ""
        for i, doc in enumerate(retrieved_docs):
            candidates_str += f"{i+1}. 标签: {doc.page_content} | IDs: {doc.metadata['ids']}\n"
            
        # 3. 让大模型做最终判断
        return self.chain.invoke({
            "query": query,
            "candidates": candidates_str
        })


# ================= 3. 运行测试 =================
if __name__ == "__main__":
    # ⚠️ 【重要】请将这里替换为你实际部署 BGE 模型的 HTTP 接口地址
    # 例如 FastAPI 写的服务: http://127.0.0.1:5000/embed
    MY_BGE_API_URL = "http://localhost:8080/api/embeddings" 
    
    # 初始化 RAG 系统
    # 假设之前的 JSON 文件叫 labels.json
    matcher = LocalRAGMatcher("labels.json", bge_api_url=MY_BGE_API_URL)
    
    # 模拟测试
    queries = ["哪里有庙？", "想吃点东西", "车坏了去哪修"]
    
    for q in queries:
        print(f"用户: {q}")
        res = matcher.match(q)
        print(f"AI结果: {res}\n")