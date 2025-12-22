from typing import Any, Dict

import httpx


class KilnClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def close(self):
        await self.client.aclose()

    async def get_pv(self) -> float:
        resp = await self.client.get("/pv")
        resp.raise_for_status()
        return resp.json()["pv"]

    async def get_setpoint(self) -> float:
        resp = await self.client.get("/setpoint")
        resp.raise_for_status()
        return resp.json()["setpoint"]

    async def set_setpoint(self, value: float) -> float:
        resp = await self.client.post("/setpoint", json={"value": value})
        resp.raise_for_status()
        return resp.json()["setpoint"]

    async def get_output1(self) -> float:
        resp = await self.client.get("/output/1")
        resp.raise_for_status()
        return resp.json()["output_1"]

    async def get_output2(self) -> float:
        resp = await self.client.get("/output/2")
        resp.raise_for_status()
        return resp.json()["output_2"]

    async def set_run_stop(self, run: bool) -> str:
        resp = await self.client.post("/run", json={"run": run})
        resp.raise_for_status()
        return resp.json()["status"]

    async def get_status_leds(self) -> Dict[str, bool]:
        resp = await self.client.get("/status/leds")
        resp.raise_for_status()
        return resp.json()

    async def get_temp_range(self) -> Dict[str, float]:
        resp = await self.client.get("/temp-range")
        resp.raise_for_status()
        return resp.json()

    async def get_sensor_type(self) -> Dict[str, int]:
        resp = await self.client.get("/sensor-type")
        resp.raise_for_status()
        return resp.json()

    async def get_control_method(self) -> Dict[str, int]:
        resp = await self.client.get("/control-method")
        resp.raise_for_status()
        return resp.json()

    async def set_control_method(self, value: int) -> Dict[str, Any]:
        resp = await self.client.post("/control-method", json={"value": value})
        resp.raise_for_status()
        return resp.json()

    async def get_heating_cooling(self) -> Dict[str, int]:
        resp = await self.client.get("/heating-cooling")
        resp.raise_for_status()
        return resp.json()

    async def set_heating_cooling(self, value: int) -> Dict[str, Any]:
        resp = await self.client.post("/heating-cooling", json={"value": value})
        resp.raise_for_status()
        return resp.json()

    async def get_temp_unit(self) -> Dict[str, str]:
        resp = await self.client.get("/temp-unit")
        resp.raise_for_status()
        return resp.json()

    async def set_temp_unit(self, value: int) -> Dict[str, Any]:
        resp = await self.client.post("/temp-unit", json={"value": value})
        resp.raise_for_status()
        return resp.json()

    # PID
    async def get_pid_p(self) -> float:
        resp = await self.client.get("/pid/p")
        resp.raise_for_status()
        return resp.json()["proportional_band"]

    async def set_pid_p(self, value: float) -> float:
        resp = await self.client.post("/pid/p", json={"value": value})
        resp.raise_for_status()
        return resp.json()["proportional_band"]

    async def get_pid_i(self) -> float:
        resp = await self.client.get("/pid/i")
        resp.raise_for_status()
        return resp.json()["integral_time"]

    async def set_pid_i(self, value: float) -> float:
        resp = await self.client.post("/pid/i", json={"value": value})
        resp.raise_for_status()
        return resp.json()["integral_time"]

    async def get_pid_d(self) -> float:
        resp = await self.client.get("/pid/d")
        resp.raise_for_status()
        return resp.json()["derivative_time"]

    async def set_pid_d(self, value: float) -> float:
        resp = await self.client.post("/pid/d", json={"value": value})
        resp.raise_for_status()
        return resp.json()["derivative_time"]

    async def set_output_value(self, index: int, value: float) -> Dict[str, Any]:
        resp = await self.client.post(f"/output/{index}", json={"value": value})
        resp.raise_for_status()
        return resp.json()

    # Alarms
    async def get_system_alarm(self) -> int:
        resp = await self.client.get("/alarm/system")
        resp.raise_for_status()
        return resp.json()["system_alarm"]

    async def get_alarm_type(self, index: int) -> int:
        resp = await self.client.get(f"/alarm/{index}/type")
        resp.raise_for_status()
        return resp.json()["type"]

    async def get_alarm_limits(self, index: int) -> Dict[str, int]:
        resp = await self.client.get(f"/alarm/{index}/limits")
        resp.raise_for_status()
        return resp.json()

    async def get_run_status(self) -> int:
        resp = await self.client.get("/run")
        resp.raise_for_status()
        return resp.json()["run_status"]

    async def get_key_status(self) -> Dict[str, bool]:
        resp = await self.client.get("/status/keys")
        resp.raise_for_status()
        return resp.json()

    # Pattern Status
    async def get_executing_program_status(self) -> Dict[str, Any]:
        resp = await self.client.get("/current/program")
        resp.raise_for_status()
        return resp.json()

    async def get_pattern(self, pattern_id: int) -> Dict[str, Any]:
        resp = await self.client.get(f"/pattern/{pattern_id}")
        resp.raise_for_status()
        return resp.json()

    async def set_pattern_step(
        self, pattern_id: int, step_id: int, temp: float, time: int
    ) -> Dict[str, Any]:
        resp = await self.client.post(
            f"/pattern/{pattern_id}/step/{step_id}", json={"temp": temp, "time": time}
        )
        resp.raise_for_status()
        return resp.json()

    # Generic Settings
    async def get_all_settings(self) -> Dict[str, Any]:
        resp = await self.client.get("/settings/all")
        resp.raise_for_status()
        return resp.json()

    async def get_setting(self, name: str) -> Any:
        # name should be like 'lock-status', 'pid-selection', etc.
        resp = await self.client.get(f"/setting/{name}")
        resp.raise_for_status()
        return resp.json()

    async def set_setting(self, name: str, value: Any) -> Dict[str, Any]:
        resp = await self.client.post(f"/setting/{name}", json={"value": value})
        resp.raise_for_status()
        return resp.json()

    async def set_system_alarm(self, value: int) -> Dict[str, Any]:
        resp = await self.client.post("/alarm/system", json={"value": value})
        resp.raise_for_status()
        return resp.json()

    async def set_sensor_type(self, value: int) -> Dict[str, Any]:
        resp = await self.client.post("/sensor-type", json={"value": value})
        resp.raise_for_status()
        return resp.json()
