# web.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from kiln_client import KilnClient
from src.core.config import KILN_SERVER_URL
from src.routers.monitoring import get_kiln
from src.routers.ui import router

app = FastAPI(title="Kiln Web UI (Standalone)")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# In standalone mode, we talk to the hardware server via KilnClient
client = KilnClient(KILN_SERVER_URL)
app.dependency_overrides[get_kiln] = lambda: client

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
