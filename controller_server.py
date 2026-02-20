# controller_server.py
import asyncio
import json
import time
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.kiln import kiln
from src.routers.hardware import _eval, router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Background task to update PV in Redis
    r = redis.Redis(host="localhost", port=6379, db=0)

    async def update_pv_loop():
        while True:
            try:
                # Use the helper logic to get PV regardless of sync/async kiln
                pv = await _eval(kiln, "get_pv")
                sp = await _eval(kiln, "get_setpoint")
                await r.set(
                    "kiln-snapshot",
                    json.dumps({"pv": pv, "sp": sp, "timestamp": time.time()}),
                )
            except Exception as e:
                print(f"Error updating Redis PV: {e}")

            await asyncio.sleep(0.5)

    task = asyncio.create_task(update_pv_loop())
    yield
    task.cancel()
    await r.aclose()


app = FastAPI(title="Delta DTB Controller API (Standalone)", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
