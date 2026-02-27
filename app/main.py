# app/main.py

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import time

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import StockAPIException
from app.routes import predict, health, metrics
from app.models.schemas import ErrorResponse

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Advanced Stock Prediction API with ML models",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(
        "Incoming request",
        extra={
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host if request.client else "unknown"
        }
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log response
    logger.info(
        "Request completed",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2)
        }
    )
    
    # Add custom headers
    response.headers["X-Process-Time"] = str(duration)
    response.headers["X-API-Version"] = settings.APP_VERSION
    
    return response

# Exception handlers
@app.exception_handler(StockAPIException)
async def stock_api_exception_handler(request: Request, exc: StockAPIException):
    logger.error(
        f"Stock API Exception: {exc.detail}",
        extra={"status_code": exc.status_code}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            detail=exc.detail
        ).model_dump(mode='json')
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="ValidationError",
            detail=str(exc.errors())
        ).model_dump(mode='json')
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={"exception_type": type(exc).__name__},
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="InternalServerError",
            detail="An unexpected error occurred. Please try again later."
        ).model_dump(mode='json')
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(
        f"Starting {settings.APP_NAME} v{settings.APP_VERSION}",
        extra={"debug": settings.DEBUG}
    )

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")

# Include routers
app.include_router(predict.router, prefix="/api/v1", tags=["Predictions"])
app.include_router(health.router, tags=["Health"])
app.include_router(metrics.router, tags=["Metrics"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }