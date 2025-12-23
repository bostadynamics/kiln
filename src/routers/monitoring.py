# src/routers/monitoring.py
import asyncio
import json
import time
from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends

from ..core.kiln import kiln as direct_kiln
from ..core.config import RECORDING_FILE

router = APIRouter(tags=["monitoring"])


# Helper to get kiln interface
def get_kiln():
    return direct_kiln


# Global State
recording_task: Optional[asyncio.Task] = None
start_time: Optional[float] = None


async def recorder(kiln: Any):
    global start_time
    print("Recording started...")
    try:
        with open(RECORDING_FILE, "a") as f:
            while True:
                try:
                    # Check if kiln is KilnClient (has async methods) or direct (sync)
                    if hasattr(kiln, "get_pv") and asyncio.iscoroutinefunction(
                        kiln.get_pv
                    ):
                        temperature = await kiln.get_pv()
                    else:
                        temperature = await asyncio.to_thread(kiln.get_pv)

                    now = datetime.now()
                    elapsed = time.time() - start_time

                    log_entry = {
                        "timestamp": now.isoformat(),
                        "time_passed": round(elapsed, 2),
                        "temperature": temperature,
                    }

                    f.write(json.dumps(log_entry) + "\n")
                    f.flush()
                except Exception as e:
                    print(f"Error querying temperature: {e}")

                await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Recording stopped.")
    except Exception as e:
        print(f"Recorder failed: {e}")


@router.get("/current_temperature")
async def get_current_temperature(kiln: Any = Depends(get_kiln)):
    try:
        if hasattr(kiln, "get_pv") and asyncio.iscoroutinefunction(kiln.get_pv):
            temp = await kiln.get_pv()
        else:
            temp = await asyncio.to_thread(kiln.get_pv)
        return {"temperature": temp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start_recording")
async def start_recording(kiln: Any = Depends(get_kiln)):
    global recording_task, start_time

    if recording_task and not recording_task.done():
        return {"status": "error", "message": "Recording is already in progress"}

    # Reset file
    with open(RECORDING_FILE, "w"):
        pass

    start_time = time.time()
    recording_task = asyncio.create_task(recorder(kiln))

    return {"status": "ok", "message": "Recording started"}


@router.post("/stop_recording")
async def stop_recording():
    global recording_task

    if not recording_task or recording_task.done():
        return {"status": "error", "message": "No recording in progress"}

    recording_task.cancel()
    try:
        await recording_task
    except asyncio.CancelledError:
        pass

    recording_task = None
    return {"status": "ok", "message": "Recording stopped"}


@router.get("/current_recording")
async def get_current_recording() -> List[dict]:
    try:
        recordings = []
        with open(RECORDING_FILE, "r") as f:
            for line in f:
                if line.strip():
                    recordings.append(json.loads(line))
        return recordings
    except FileNotFoundError:
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    global recording_task
    return {"is_recording": recording_task is not None and not recording_task.done()}


async def shutdown_monitoring():
    global recording_task
    if recording_task:
        recording_task.cancel()
        try:
            await recording_task
        except asyncio.CancelledError:
            pass
