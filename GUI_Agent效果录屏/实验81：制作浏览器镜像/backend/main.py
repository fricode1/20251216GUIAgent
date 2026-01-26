from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import asyncio
import io
import aiofiles
import aiosqlite
from minio import Minio
from minio.error import S3Error
from datetime import datetime
import os
from openai import OpenAI
import re
from typing import Optional

import spider
from rapidocr import RapidOCR

# Initialize OCR engine
ocr_engine = RapidOCR()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MinIO configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = "traffic-violations"

# SQLite database path
DB_PATH = "traffic_violations.db"

# GLM-4 client (智谱AI)
GLM_API_KEY = os.getenv("GLM_API_KEY", "c8f0c58aba1fad293a8ca62f4cb7942d.Zxxt5g3FX1cuiCuo")
llm_client = OpenAI(
    api_key=GLM_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4"
) if GLM_API_KEY else None

# MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Initialize MinIO bucket
async def init_minio():
    try:
        if not minio_client.bucket_exists(MINIO_BUCKET):
            minio_client.make_bucket(MINIO_BUCKET)
            print(f"Created bucket: {MINIO_BUCKET}")
    except S3Error as e:
        print(f"MinIO error: {e}")

# Initialize SQLite database
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS violations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                minio_path TEXT NOT NULL,
                time TEXT NOT NULL,
                location TEXT NOT NULL,
                name TEXT NOT NULL,
                id_number TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

class QueryRequest(BaseModel):
    question: str

class ParsedInfo(BaseModel):
    location: str
    time: str

def parse_question_with_llm(question: str) -> ParsedInfo:
    """Parse location and time from user question using LLM"""
    if llm_client:
        try:
            # Get today's date for the prompt
            today = datetime.now().strftime("%Y年%m月%d日")
            today_yyyymmdd = datetime.now().strftime("%Y%m%d")

            response = llm_client.chat.completions.create(
                model="glm-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"你是一个交通违章查询助手。从用户问题中提取地点和时间，时间格式为YYYYMMDD。\n\n今天的日期是：{today}（{today_yyyymmdd}）\n\n请以JSON格式返回，包含location和time两个字段。"
                    },
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=100
            )
            content = response.choices[0].message.content
            print(content)
            import json

            # Extract JSON from markdown code block if present
            if "```json" in content:
                # Extract content between ```json and ```
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)
            elif "```" in content:
                # Extract content between ``` and ```
                json_match = re.search(r'```\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)

            # Try to extract JSON from response
            result = json.loads(content.strip())
            return ParsedInfo(location=result.get("location", "未知地点"), time=result.get("time", datetime.now().strftime("%Y%m%d")))
        except Exception as e:
            print(e)
            print(f"LLM parsing error: {e}")

    # Fallback: simple regex parsing
    location = "未知地点"
    time = datetime.now().strftime("%Y%m%d")

    # Try to extract location (any Chinese characters or common patterns)
    location_match = re.search(r'([一-龥]+路|[一-龥]+街|[一-龥]+道)', question)
    if location_match:
        location = location_match.group(1)

    # Try to extract time keywords
    if "昨天" in question:
        yesterday = datetime.now().timestamp() - 86400
        time = datetime.fromtimestamp(yesterday).strftime("%Y%m%d")
    elif "前天" in question:
        day_before = datetime.now().timestamp() - 172800
        time = datetime.fromtimestamp(day_before).strftime("%Y%m%d")
    elif "今天" in question:
        time = datetime.now().strftime("%Y%m%d")

    return ParsedInfo(location=location, time=time)

async def run_real_spider(place_text: str, time_text: str):
    """
    Run the real spider and store in MinIO and SQLite
    """
    # Convert YYYYMMDD to YYYY/MM/DD if needed
    if len(time_text) == 8 and time_text.isdigit():
        data_str = f"{time_text[:4]}/{time_text[4:6]}/{time_text[6:]}"
    else:
        # Fallback to current date if format is unexpected
        data_str = datetime.now().strftime("%Y/%m/%d")

    # The spider is synchronous, so we run it in a thread pool to avoid blocking
    import concurrent.futures
    
    def spider_worker():
        try:
            main_tab = spider.login()
            return spider.spider_one_day(data_str, place_text, main_tab, ocr_engine)
        except Exception as e:
            print(f"Spider login/start error: {e}")
            return []

    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        # Start the spider and get the generator
        gen = await loop.run_in_executor(pool, spider_worker)
        
        # Iterate over the generator (this also needs to be in a thread if it blocks)
        while True:
            try:
                # Get next result from generator in thread
                result = await loop.run_in_executor(pool, next, gen, None)
                if result is None:
                    break
                
                # Save to MinIO
                object_name = result["image_name"]
                image_content = result["image_content"]
                
                minio_client.put_object(
                    MINIO_BUCKET,
                    object_name,
                    data=io.BytesIO(image_content),
                    length=len(image_content),
                    content_type="image/png"
                )
                minio_path = f"{MINIO_BUCKET}/{object_name}"
                
                # Generate presigned URL
                from datetime import timedelta
                presigned_url = minio_client.presigned_get_object(
                    MINIO_BUCKET,
                    object_name,
                    expires=timedelta(days=7)
                )
                
                # Save to SQLite
                async with aiosqlite.connect(DB_PATH) as db:
                    await db.execute(
                        """
                        INSERT INTO violations (minio_path, time, location, name, id_number)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (minio_path, result["time"], result["location"], result["name"], result["id_number"])
                    )
                    await db.commit()
                
                yield {
                    "status": "success",
                    "image_url": presigned_url,
                    "image_path": minio_path,
                    "time": result["time"],
                    "location": result["location"],
                    "name": result["name"],
                    "id_number": result["id_number"]
                }
            except StopIteration:
                break
            except Exception as e:
                print(f"Error processing spider result: {e}")
                yield {"status": "error", "message": str(e)}
                break

@app.on_event("startup")
async def startup_event():
    await init_minio()
    await init_db()

@app.post("/api/query")
async def query_violations(request: QueryRequest):
    """Parse user question and return streaming image data"""
    # Parse location and time
    parsed = parse_question_with_llm(request.question)

    async def event_generator():
        async for result in run_real_spider(parsed.location, parsed.time):
            import json
            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/violations")
async def get_violations():
    """Get all violations from database"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM violations ORDER BY created_at DESC") as cursor:
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            print(len(rows))
            return [dict(zip(columns, row)) for row in rows]

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
