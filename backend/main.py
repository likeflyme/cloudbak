import uvicorn
from app.application import create_app
from config.app_config import settings


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.server_host, port=settings.server_port)
