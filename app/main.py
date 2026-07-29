from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.core.config import settings
from app.api.v1 import api_router
from app.db.init_db import init_db

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="生鲜称重连锁系统 API 文档",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def root():
    return {
        "message": f"欢迎使用{settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION,
        "docs": "/api/docs"
    }

@app.get("/admin")
async def admin_page():
    admin_file = FRONTEND_DIR / "admin.html"
    if admin_file.exists():
        return FileResponse(str(admin_file))
    return {"error": "admin.html not found"}

@app.get("/cashier")
async def cashier_page():
    cashier_file = FRONTEND_DIR / "cashier.html"
    if cashier_file.exists():
        return FileResponse(str(cashier_file))
    return {"error": "cashier.html not found"}

@app.on_event("startup")
async def startup_event():
    init_db()
    print(f"{settings.PROJECT_NAME} v{settings.PROJECT_VERSION} 启动成功")
