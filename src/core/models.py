# src/core/models.py
from pydantic import BaseModel
from .delta_2 import (
    ControlMethod,
    HeatingCoolingSelection,
    TempUnit,
    RunStopSetting,
    SettingLockStatus,
    PIDParameterSelection,
    AnalogDecimalSetting,
    ValveFeedbackSetting,
    AutoTuningValveFeedback,
    DecimalPointPosition,
    ATSetting,
    StopSettingPID,
    TemporarilyStopPID,
    SystemAlarmSetting,
)


class SetpointRequest(BaseModel):
    value: float


class ControlMethodRequest(BaseModel):
    value: ControlMethod


class HeatingCoolingRequest(BaseModel):
    value: HeatingCoolingSelection


class TempUnitRequest(BaseModel):
    value: TempUnit


class PIDRequest(BaseModel):
    value: float


class OutputRequest(BaseModel):
    value: float


class AlarmTypeRequest(BaseModel):
    value: int


class AlarmLimitRequest(BaseModel):
    value: int


class PatternStepRequest(BaseModel):
    temp: float
    time: int


class RunStopRequest(BaseModel):
    value: RunStopSetting


class LockStatusRequest(BaseModel):
    value: SettingLockStatus


class PIDSelectionRequest(BaseModel):
    value: PIDParameterSelection


class AnalogDecimalRequest(BaseModel):
    value: AnalogDecimalSetting


class ValveFeedbackRequest(BaseModel):
    value: ValveFeedbackSetting


class ATValveFeedbackRequest(BaseModel):
    value: AutoTuningValveFeedback


class DecimalPointRequest(BaseModel):
    value: DecimalPointPosition


class ATSettingRequest(BaseModel):
    value: ATSetting


class StopSettingPIDRequest(BaseModel):
    value: StopSettingPID


class TempStopPIDRequest(BaseModel):
    value: TemporarilyStopPID


class SystemAlarmRequest(BaseModel):
    value: SystemAlarmSetting


class SensorTypeRequest(BaseModel):
    value: int


class IntValueRequest(BaseModel):
    value: int
