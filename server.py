from fastapi import FastAPI

import logging
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化 FastAPI 应用
app = FastAPI()

# Add error handlers to your FastAPI app
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": str(exc.detail)
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation error",
            "details": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": f"Internal server error: {str(exc)}"
        }
    )


# 添加路由配置

# 添加路由
from api.test_case_api import router
app.include_router(router)



if __name__ == "__main__":
    # 线上容器环境启动方式不一样，请不要添加任何其他逻辑到此处，否则将不会执行
    # 如果需要添加一些应用初始化逻辑，请添加至 `lifespan.lifespan()` `yield` 代码之前
    # 如果想在应用关闭时，添加一些额外的任务，可以添加至 `lifespan.lifespan()` `yield` 代码之后
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

