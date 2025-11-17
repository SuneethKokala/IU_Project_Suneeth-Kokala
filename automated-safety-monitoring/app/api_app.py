from fastapi import FastAPI
from src.api.routes import router
import uvicorn

def create_app():
    app = FastAPI(
        title="Safety Monitoring API",
        description="PPE Detection and Face Recognition API",
        version="1.0.0"
    )
    
    app.include_router(router, prefix="/api/v1")
    
    @app.get("/")
    def root():
        return {
            "message": "Safety Monitoring API",
            "version": "1.0.0",
            "docs": "/docs"
        }
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)