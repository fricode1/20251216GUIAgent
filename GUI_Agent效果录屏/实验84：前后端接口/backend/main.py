from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import asyncio
import io
import aiosqlite
from minio import Minio
from minio.error import S3Error
from datetime import datetime, timedelta
import os
from typing import Optional, Dict
import concurrent.futures
import uuid

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

# Background task storage
running_tasks: Dict[int, asyncio.Task] = {}



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
        # Applications table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                address TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Ready',
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)
        
        # Images table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                minio_path TEXT NOT NULL,
                url TEXT NOT NULL,
                time TEXT NOT NULL,
                location TEXT NOT NULL,
                name TEXT NOT NULL,
                id_number TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
            )
        """)
        
        await db.commit()

# Request Models
class CreateApplicationRequest(BaseModel):
    name: str = Field(..., description="应用名称")
    start_time: str = Field(..., description="开始日期 yyyy-MM-dd HH:mm:ss")
    end_time: str = Field(..., description="结束日期 yyyy-MM-dd HH:mm:ss")
    address: str = Field(..., description="地址")

# Response Models
class StandardResponse(BaseModel):
    code: str
    msg: str

class ApplicationItem(BaseModel):
    id: int
    name: str
    created_at: str
    status: str
    address: str
    start_time: str
    end_time: str

class ApplicationListData(BaseModel):
    list: list[ApplicationItem]
    total: int
    pageNo: int
    pageSize: int

class ApplicationListResponse(BaseModel):
    code: str
    msg: str
    data: ApplicationListData

class ImageItem(BaseModel):
    created_at: str
    url: str

class ImageListData(BaseModel):
    list: list[ImageItem]
    total: int
    pageNo: int
    pageSize: int

class ImageListResponse(BaseModel):
    code: str
    msg: str = Field(alias="message")
    data: ImageListData

    class Config:
        populate_by_name = True

async def get_application_status(start_time_str: str, end_time_str: str) -> str:
    """Determine application status based on time window"""
    try:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        
        if now < start_time:
            return "Ready"
        elif start_time <= now <= end_time:
            return "Running"
        else:
            return "Finished"
    except Exception as e:
        print(f"Error parsing time: {e}")
        return "Ready"

async def run_spider_for_application(app_id: int, address: str, start_time: str, end_time: str):
    """
    Run spider for a specific application
    """
    try:
        # Parse time range to get date
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        data_str = start_dt.strftime("%Y/%m/%d")
        
        # The spider is synchronous, run it in thread pool
        def spider_worker():
            try:
                return spider.spider_one_day_dummy(data_str, address, None, ocr_engine)
            except Exception as e:
                print(f"Spider error: {e}")
                return iter([])
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            gen = await loop.run_in_executor(pool, spider_worker)
            
            while True:
                try:
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
                    presigned_url = minio_client.presigned_get_object(
                        MINIO_BUCKET,
                        object_name,
                        expires=timedelta(days=7)
                    )
                    
                    # Save to SQLite
                    async with aiosqlite.connect(DB_PATH) as db:
                        await db.execute(
                            """
                            INSERT INTO images (application_id, minio_path, url, time, location, name, id_number)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (app_id, minio_path, presigned_url, result["time"], result["location"], result["name"], result["id_number"])
                        )
                        await db.commit()
                    
                    print(f"Saved image for app {app_id}: {result['name']} at {result['location']}")
                    
                except StopIteration:
                    break
                except Exception as e:
                    print(f"Error processing spider result: {e}")
                    break
        
        # Mark application as finished
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE applications SET status = ? WHERE id = ?",
                ("Finished", app_id)
            )
            await db.commit()
        
    except Exception as e:
        print(f"Error in spider task for app {app_id}: {e}")
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE applications SET status = ? WHERE id = ?",
                ("Stopped", app_id)
            )
            await db.commit()

async def check_and_start_tasks():
    """Background task to check and start applications based on time window"""
    while True:
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                async with db.execute(
                    "SELECT id, name, start_time, end_time, address, status FROM applications"
                ) as cursor:
                    rows = await cursor.fetchall()
                    
                    for row in rows:
                        app_id, name, start_time, end_time, address, status = row
                        new_status = await get_application_status(start_time, end_time)
                        
                        # Update status if changed
                        if new_status != status:
                            await db.execute(
                                "UPDATE applications SET status = ? WHERE id = ?",
                                (new_status, app_id)
                            )
                            await db.commit()
                            
                            # Start spider task if status changed to Running
                            if new_status == "Running" and app_id not in running_tasks:
                                print(f"Starting spider task for application {app_id}")
                                task = asyncio.create_task(
                                    run_spider_for_application(app_id, address, start_time, end_time)
                                )
                                running_tasks[app_id] = task
                            
                            # Stop spider task if status is no longer Running
                            elif new_status != "Running" and app_id in running_tasks:
                                print(f"Stopping spider task for application {app_id}")
                                running_tasks[app_id].cancel()
                                del running_tasks[app_id]
            
            # Check every 10 seconds
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error in background task checker: {e}")
            await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    await init_minio()
    await init_db()
    # Start background task checker
    asyncio.create_task(check_and_start_tasks())

@app.post("/violation", response_model=StandardResponse)
async def create_application(request: CreateApplicationRequest):
    """创建新的违章监控应用"""
    try:
        print(f"Received request: {request}")
        
        # Validate time format
        try:
            datetime.strptime(request.start_time, "%Y-%m-%d %H:%M:%S")
            datetime.strptime(request.end_time, "%Y-%m-%d %H:%M:%S")
        except ValueError as ve:
            return StandardResponse(code="400", msg=f"Invalid time format: {str(ve)}")
        
        # Set initial status to Running (immediate execution)
        status = "Running"
        
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                """
                INSERT INTO applications (name, start_time, end_time, address, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (request.name, request.start_time, request.end_time, request.address, status)
            )
            await db.commit()
            app_id = cursor.lastrowid
        
        print(f"Created application {app_id} with status {status}")
        
        # Start spider immediately upon creation
        if app_id not in running_tasks:
            task = asyncio.create_task(
                run_spider_for_application(app_id, request.address, request.start_time, request.end_time)
            )
            running_tasks[app_id] = task
            print(f"Started spider task immediately for application {app_id}")
        
        return StandardResponse(code="0", msg="success")
    except Exception as e:
        print(f"Error creating application: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/violation", response_model=ApplicationListResponse)
async def get_applications(
    pageSize: int = Query(10, description="每页条数"),
    pageNo: int = Query(1, description="页码")
):
    """查询应用列表（支持分页）"""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Get total count
            async with db.execute("SELECT COUNT(*) FROM applications") as cursor:
                row = await cursor.fetchone()
                total = row[0]
            
            # Get paginated results
            offset = (pageNo - 1) * pageSize
            async with db.execute(
                """
                SELECT id, name, created_at, status, address, start_time, end_time
                FROM applications
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
                """,
                (pageSize, offset)
            ) as cursor:
                rows = await cursor.fetchall()
                
                applications = [
                    ApplicationItem(
                        id=row[0],
                        name=row[1],
                        created_at=row[2],
                        status=row[3],
                        address=row[4],
                        start_time=row[5],
                        end_time=row[6]
                    )
                    for row in rows
                ]
        
        return ApplicationListResponse(
            code="0",
            msg="success",
            data=ApplicationListData(
                list=applications,
                total=total,
                pageNo=pageNo,
                pageSize=pageSize
            )
        )
    except Exception as e:
        print(f"Error getting applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/violation/{id}", response_model=StandardResponse)
async def delete_application(id: int):
    """删除应用"""
    try:
        # Stop running task if exists
        if id in running_tasks:
            running_tasks[id].cancel()
            del running_tasks[id]
        
        async with aiosqlite.connect(DB_PATH) as db:
            # Check if application exists
            async with db.execute("SELECT id FROM applications WHERE id = ?", (id,)) as cursor:
                row = await cursor.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Application not found")
            
            # Delete application (cascade will delete related images)
            await db.execute("DELETE FROM applications WHERE id = ?", (id,))
            await db.commit()
        
        return StandardResponse(code="0", msg="success")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/violation/images", response_model=ImageListResponse)
async def get_images(
    pageSize: int = Query(10, description="每页条数"),
    pageNo: int = Query(1, description="页码"),
    id: Optional[int] = Query(None, description="应用id")
):
    """查询图片列表（支持分页和按应用id过滤）"""
    try:
        print(f"Received query params: pageSize={pageSize}, pageNo={pageNo}, id={id}")
        
        async with aiosqlite.connect(DB_PATH) as db:
            # Build query based on whether id is provided
            if id is not None:
                print(f"Filtering by application_id = {id}")
                # Filter by application_id
                count_query = "SELECT COUNT(*) FROM images WHERE application_id = ?"
                select_query = """
                    SELECT created_at, url
                    FROM images
                    WHERE application_id = ?
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                """
                count_params = (id,)
                
                # Get total count
                async with db.execute(count_query, count_params) as cursor:
                    row = await cursor.fetchone()
                    total = row[0]
                print(f"Total images for application {id}: {total}")
                
                # Get paginated results
                offset = (pageNo - 1) * pageSize
                select_params = (id, pageSize, offset)
            else:
                print("Fetching all images (no id filter)")
                # Get all images
                count_query = "SELECT COUNT(*) FROM images"
                select_query = """
                    SELECT created_at, url
                    FROM images
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                """
                
                # Get total count
                async with db.execute(count_query) as cursor:
                    row = await cursor.fetchone()
                    total = row[0]
                print(f"Total images (all): {total}")
                
                # Get paginated results
                offset = (pageNo - 1) * pageSize
                select_params = (pageSize, offset)
            
            # Execute select query
            async with db.execute(select_query, select_params) as cursor:
                rows = await cursor.fetchall()
                
                images = [
                    ImageItem(
                        created_at=row[0],
                        url=row[1]
                    )
                    for row in rows
                ]
        
        return ImageListResponse(
            code="0",
            msg="success",
            data=ImageListData(
                list=images,
                total=total,
                pageNo=pageNo,
                pageSize=pageSize
            )
        )
    except Exception as e:
        print(f"Error getting images: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
