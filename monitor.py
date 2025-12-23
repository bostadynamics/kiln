# monitor.py
from fastapi import FastAPI
from src.routers.monitoring import router, get_kiln
from kiln_client import KilnClient
from src.core.config import KILN_SERVER_URL

app = FastAPI(title="Kiln Monitor Service (Standalone)")

# In standalone mode, we talk to the hardware server via KilnClient
client = KilnClient(KILN_SERVER_URL)

app.dependency_overrides[get_kiln] = lambda: client

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
