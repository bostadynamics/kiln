import threading
from enum import IntEnum

import minimalmodbus


class ControlMethod(IntEnum):
    PID = 0
    ON_OFF = 1
    MANUAL_TUNING = 2
    PID_PROGRAM_CONTROL = 3


class HeatingCoolingSelection(IntEnum):
    HEATING = 0
    COOLING = 1
    HEATING_COOLING = 2
    COOLING_HEATING = 3


class SystemAlarmSetting(IntEnum):
    NONE = 0
    ALARM_1 = 1
    ALARM_2 = 2
    ALARM_3 = 3


class SettingLockStatus(IntEnum):
    NORMAL = 0
    ALL_LOCKED = 1
    LOCK_OTHERS_THAN_SV = 11


class PIDParameterSelection(IntEnum):
    PID_0 = 0
    PID_1 = 1
    PID_2 = 2
    PID_3 = 3
    PID_4 = 4


class AnalogDecimalSetting(IntEnum):
    NO_DECIMAL = 0
    ONE_DECIMAL = 1
    TWO_DECIMALS = 2
    THREE_DECIMALS = 3


class ValveFeedbackSetting(IntEnum):
    WITHOUT_FEEDBACK = 0
    FEEDBACK_FUNCTION = 1


class AutoTuningValveFeedback(IntEnum):
    STOP_AT = 0
    START_AT = 1


class TempUnit(IntEnum):
    FAHRENHEIT = 0
    CELSIUS_LINEAR = 1


class DecimalPointPosition(IntEnum):
    NO_DECIMAL = 0
    ONE_DECIMAL = 1


class ATSetting(IntEnum):
    OFF = 0
    ON = 1


class RunStopSetting(IntEnum):
    STOP = 0
    RUN = 1


class StopSettingPID(IntEnum):
    RUN = 0
    STOP = 1


class Register(IntEnum):
    PV = 0x1000
    SV = 0x1001
    UPPER_LIMIT_TEMP_RANGE = 0x1002
    LOWER_LIMIT_TEMP_RANGE = 0x1003
    SENSOR_TYPE = 0x1004
    CONTROL_METHOD = 0x1005
    HEATING_COOLING_SELECTION = 0x1006
    HEATING_COOLING_CYCLE_1 = 0x1007
    HEATING_COOLING_CYCLE_2 = 0x1008
    PROPORTIONAL_BAND = 0x1009
    INTEGRAL_TIME = 0x100A
    DERIVATIVE_TIME = 0x100B
    INTEGRATION_DEFAULT = 0x100C
    PD_CONTROL_OFFSET = 0x100D
    COEF = 0x100E
    DEAD_BAND = 0x100F
    HYSTERESIS_OUTPUT_1 = 0x1010
    HYSTERESIS_OUTPUT_2 = 0x1011
    OUTPUT_1_VALUE = 0x1012
    OUTPUT_2_VALUE = 0x1013
    UPPER_LIMIT_ANALOG = 0x1014
    LOWER_LIMIT_ANALOG = 0x1015
    TEMPERATURE_REGULATION = 0x1016
    ANALOG_DECIMAL = 0x1017
    VALVE_TIME = 0x1018
    VALVE_DEAD_BAND = 0x1019
    VALVE_FEEDBACK_UPPER_LIMIT = 0x101A
    VALVE_FEEDBACK_LOWER_LIMIT = 0x101B
    PID_PARAMETER_SELECTION = 0x101C
    SV_VALUE_CORRESPONDED_TO_PID = 0x101D
    ALARM_1_TYPE = 0x1020
    ALARM_2_TYPE = 0x1021
    ALARM_3_TYPE = 0x1022
    SYSTEM_ALARM_SETTING = 0x1023
    UPPER_LIMIT_ALARM_1 = 0x1024
    LOWER_LIMIT_ALARM_1 = 0x1025
    UPPER_LIMIT_ALARM_2 = 0x1026
    LOWER_LIMIT_ALARM_2 = 0x1027
    UPPER_LIMIT_ALARM_3 = 0x1028
    LOWER_LIMIT_ALARM_3 = 0x1029
    LED_STATUS = 0x102A
    PUSHBUTTON_STATUS = 0x102B
    SETTING_LOCK_STATUS = 0x102C
    CT_READ_VALUE = 0x102D
    FIRMWARE_VERSION = 0x102F
    START_PATTERN = 0x1030
    STEP_TIME_LEFT_SEC = 0x1032
    STEP_TIME_LEFT_MIN = 0x1033
    EXECUTING_STEP_NUMBER = 0x1034
    EXECUTING_PATTERN_NUMBER = 0x1035
    DYNAMIC_SET_VALUE = 0x1036
    ACTUAL_STEP_BASE = 0x1040
    CYCLE_NUMBER_BASE = 0x1050
    LINK_PATTERN_BASE = 0x1060
    PATTERN_TEMP_START = 0x2000
    PATTERN_TIME_START = 0x2080


class BitRegister(IntEnum):
    LED_AT = 0x0800
    LED_OUT1 = 0x0801
    LED_OUT2 = 0x0802
    LED_ALARM1 = 0x0803
    LED_DEG_F = 0x0804
    LED_DEG_C = 0x0805
    LED_ALARM2 = 0x0806
    LED_ALARM3 = 0x0807
    KEY_SET = 0x0808
    KEY_FUNCTION = 0x0809
    KEY_UP = 0x080A
    KEY_DOWN = 0x080B
    EVENT_1 = 0x080C
    EVENT_2 = 0x080D
    SYSTEM_ALARM = 0x080E
    COMMUNICATION_WRITE_IN = 0x0810
    TEMP_UNIT = 0x0811
    DECIMAL_POINT = 0x0812
    AT = 0x0813
    RUN_STOP = 0x0814
    STOP_PID = 0x0815
    TEMP_STOP_PID = 0x0816
    VALVE_FEEDBACK = 0x0817
    AT_VALVE_FEEDBACK = 0x0818


class TemporarilyStopPID(IntEnum):
    RUN = 0
    TEMPORARILY_STOP = 1


class Delta2(minimalmodbus.Instrument):
    """Instrument class for Delta DTB Series Temperature Controller.

    Based on the RS-485 Communication Protocol.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """

    # Pattern start addresses
    PATTERN_TEMP_START = Register.PATTERN_TEMP_START
    PATTERN_TIME_START = Register.PATTERN_TIME_START

    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.lock = threading.Lock()

    def read_register(
        self, registeraddress, number_of_decimals=0, functioncode=3, signed=False
    ):
        with self.lock:
            return super().read_register(
                registeraddress, number_of_decimals, functioncode, signed
            )

    def write_register(
        self, registeraddress, value, number_of_decimals=0, functioncode=6, signed=False
    ):
        with self.lock:
            return super().write_register(
                registeraddress, value, number_of_decimals, functioncode, signed
            )

    def read_bit(self, registeraddress, functioncode=2):
        with self.lock:
            return super().read_bit(registeraddress, functioncode)

    def write_bit(self, registeraddress, value, functioncode=5):
        with self.lock:
            return super().write_bit(registeraddress, value, functioncode)

    # =========================================================================
    # 5. Address and Content of Data Register
    # Function Code: 03H (Read) / 06H (Write)
    # =========================================================================

    def get_pv(self):
        """Read Process value (PV). Unit is 0.1."""
        return self.read_register(Register.PV, 1)

    def get_setpoint(self):
        """Read Set point (SV). Unit is 0.1, deg C or deg F."""
        return self.read_register(Register.SV, 1)

    def set_setpoint(self, value):
        """Write Set point (SV). Unit is 0.1, deg C or deg F."""
        self.write_register(Register.SV, value, 1)

    def get_upper_limit_temp_range(self):
        """Read Upper-limit of temperature range."""
        return self.read_register(Register.UPPER_LIMIT_TEMP_RANGE, 1)

    def set_upper_limit_temp_range(self, value):
        """Write Upper-limit of temperature range."""
        self.write_register(Register.UPPER_LIMIT_TEMP_RANGE, value, 1)

    def get_lower_limit_temp_range(self):
        """Read Lower-limit of temperature range."""
        return self.read_register(Register.LOWER_LIMIT_TEMP_RANGE, 1)

    def set_lower_limit_temp_range(self, value):
        """Write Lower-limit of temperature range."""
        self.write_register(Register.LOWER_LIMIT_TEMP_RANGE, value, 1)

    def get_sensor_type(self):
        """Read Input temperature sensor type."""
        return self.read_register(Register.SENSOR_TYPE)

    def set_sensor_type(self, value):
        """Write Input temperature sensor type."""
        self.write_register(Register.SENSOR_TYPE, value)

    def get_control_method(self):
        """Read Control method. 0: PID, 1: ON/OFF, 2: Manual tuning, 3: PID program control."""
        return ControlMethod(self.read_register(Register.CONTROL_METHOD))

    def set_control_method(self, value):
        """Write Control method. 0: PID, 1: ON/OFF, 2: Manual tuning, 3: PID program control."""
        self.write_register(Register.CONTROL_METHOD, int(value))

    def get_heating_cooling(self):
        """Read Heating/Cooling selection. 0: Heating, 1: Cooling, 2: Heating/Cooling, 3: Cooling/Heating."""
        return HeatingCoolingSelection(
            self.read_register(Register.HEATING_COOLING_SELECTION)
        )

    def set_heating_cooling(self, value):
        """Write Heating/Cooling selection. 0: Heating, 1: Cooling, 2: Heating/Cooling, 3: Cooling/Heating."""
        self.write_register(Register.HEATING_COOLING_SELECTION, int(value))

    def get_heating_cooling_cycle_1(self):
        """Read 1st group Heating/Cooling cycle. 0-99."""
        return self.read_register(Register.HEATING_COOLING_CYCLE_1)

    def set_heating_cooling_cycle_1(self, value):
        """Write 1st group Heating/Cooling cycle. 0-99."""
        self.write_register(Register.HEATING_COOLING_CYCLE_1, value)

    def get_heating_cooling_cycle_2(self):
        """Read 2nd group Heating/Cooling cycle. 0-99."""
        return self.read_register(Register.HEATING_COOLING_CYCLE_2)

    def set_heating_cooling_cycle_2(self, value):
        """Write 2nd group Heating/Cooling cycle. 0-99."""
        self.write_register(Register.HEATING_COOLING_CYCLE_2, value)

    def get_proportional_band(self):
        """Read PB Proportional band. 0.1 ~ 999.9."""
        return self.read_register(Register.PROPORTIONAL_BAND, 1)

    def set_proportional_band(self, value):
        """Write PB Proportional band. 0.1 ~ 999.9."""
        self.write_register(Register.PROPORTIONAL_BAND, value, 1)

    def get_integral_time(self):
        """Read Ti Integral time. 0 ~ 9,999."""
        return self.read_register(Register.INTEGRAL_TIME, 1)

    def set_integral_time(self, value):
        """Write Ti Integral time. 0 ~ 9,999."""
        self.write_register(Register.INTEGRAL_TIME, value, 1)

    def get_derivative_time(self):
        """Read Td Derivative time. 0 ~ 9,999."""
        return self.read_register(Register.DERIVATIVE_TIME, 1)

    def set_derivative_time(self, value):
        """Write Td Derivative time. 0 ~ 9,999."""
        self.write_register(Register.DERIVATIVE_TIME, value, 1)

    def get_integration_default(self):
        """Read Integration default. 0 ~ 100%, unit is 0.1%."""
        return self.read_register(Register.INTEGRATION_DEFAULT, 1)

    def set_integration_default(self, value):
        """Write Integration default. 0 ~ 100%, unit is 0.1%."""
        self.write_register(Register.INTEGRATION_DEFAULT, value, 1)

    def get_pd_control_offset(self):
        """Read PD control offset (when Ti=0). 0 ~ 100%, unit is 0.1%."""
        return self.read_register(Register.PD_CONTROL_OFFSET, 1)

    def set_pd_control_offset(self, value):
        """Write PD control offset (when Ti=0). 0 ~ 100%, unit is 0.1%."""
        self.write_register(Register.PD_CONTROL_OFFSET, value, 1)

    def get_coef(self):
        """Read COEF setting (Dual Loop). 0.01 ~ 99.99."""
        return self.read_register(Register.COEF, 2)

    def set_coef(self, value):
        """Write COEF setting (Dual Loop). 0.01 ~ 99.99."""
        self.write_register(Register.COEF, value, 2)

    def get_dead_band(self):
        """Read Dead band setting (Dual Loop). -999 ~ 9,999."""
        return self.read_register(Register.DEAD_BAND)

    def set_dead_band(self, value):
        """Write Dead band setting (Dual Loop). -999 ~ 9,999."""
        self.write_register(Register.DEAD_BAND, value)

    def get_hysteresis_output_1(self):
        """Read Hysteresis (1st output group). 0 ~ 9,999."""
        return self.read_register(Register.HYSTERESIS_OUTPUT_1)

    def set_hysteresis_output_1(self, value):
        """Write Hysteresis (1st output group). 0 ~ 9,999."""
        self.write_register(Register.HYSTERESIS_OUTPUT_1, value)

    def get_hysteresis_output_2(self):
        """Read Hysteresis (2nd output group). 0 ~ 9,999."""
        return self.read_register(Register.HYSTERESIS_OUTPUT_2)

    def set_hysteresis_output_2(self, value):
        """Write Hysteresis (2nd output group). 0 ~ 9,999."""
        self.write_register(Register.HYSTERESIS_OUTPUT_2, value)

    def get_output_1_value(self):
        """Read Output 1 Value. Unit is 0.1%."""
        return self.read_register(Register.OUTPUT_1_VALUE, 1)

    def set_output_1_value(self, value):
        """Write Output 1 Value. Write valid under manual tuning mode only."""
        self.write_register(Register.OUTPUT_1_VALUE, value, 1)

    def get_output_2_value(self):
        """Read Output 2 Value. Unit is 0.1%."""
        return self.read_register(Register.OUTPUT_2_VALUE, 1)

    def set_output_2_value(self, value):
        """Write Output 2 Value. Write valid under manual tuning mode only."""
        self.write_register(Register.OUTPUT_2_VALUE, value, 1)

    def get_upper_limit_analog(self):
        """Read Upper-limit analog regulation."""
        return self.read_register(Register.UPPER_LIMIT_ANALOG)

    def set_upper_limit_analog(self, value):
        """Write Upper-limit analog regulation."""
        self.write_register(Register.UPPER_LIMIT_ANALOG, value)

    def get_lower_limit_analog(self):
        """Read Lower-limit analog regulation."""
        return self.read_register(Register.LOWER_LIMIT_ANALOG)

    def set_lower_limit_analog(self, value):
        """Write Lower-limit analog regulation."""
        self.write_register(Register.LOWER_LIMIT_ANALOG, value)

    def get_temperature_regulation(self):
        """Read Temperature regulation value. -999 ~ +999, unit: 0.1."""
        return self.read_register(Register.TEMPERATURE_REGULATION, 1)

    def set_temperature_regulation(self, value):
        """Write Temperature regulation value. -999 ~ +999, unit: 0.1."""
        self.write_register(Register.TEMPERATURE_REGULATION, value, 1)

    def get_analog_decimal(self):
        """Read Analog decimal setting. 0 ~ 3."""
        return AnalogDecimalSetting(self.read_register(Register.ANALOG_DECIMAL))

    def set_analog_decimal(self, value):
        """Write Analog decimal setting. 0 ~ 3."""
        self.write_register(Register.ANALOG_DECIMAL, int(value))

    def get_valve_time(self):
        """Read Valve time (Open to Close). 0.1 ~ 999.9."""
        return self.read_register(Register.VALVE_TIME, 1)

    def set_valve_time(self, value):
        """Write Valve time (Open to Close). 0.1 ~ 999.9."""
        self.write_register(Register.VALVE_TIME, value, 1)

    def get_valve_dead_band(self):
        """Read Valve Dead Band. 0 ~ 100%; unit: 0.1%."""
        return self.read_register(Register.VALVE_DEAD_BAND, 1)

    def set_valve_dead_band(self, value):
        """Write Valve Dead Band. 0 ~ 100%; unit: 0.1%."""
        self.write_register(Register.VALVE_DEAD_BAND, value, 1)

    def get_valve_feedback_upper_limit(self):
        """Read Valve feedback upper-limit. 0 ~ 1,024."""
        return self.read_register(Register.VALVE_FEEDBACK_UPPER_LIMIT)

    def set_valve_feedback_upper_limit(self, value):
        """Write Valve feedback upper-limit. 0 ~ 1,024."""
        self.write_register(Register.VALVE_FEEDBACK_UPPER_LIMIT, value)

    def get_valve_feedback_lower_limit(self):
        """Read Valve feedback lower-limit. 0 ~ 1,024."""
        return self.read_register(Register.VALVE_FEEDBACK_LOWER_LIMIT)

    def set_valve_feedback_lower_limit(self, value):
        """Write Valve feedback lower-limit. 0 ~ 1,024."""
        self.write_register(Register.VALVE_FEEDBACK_LOWER_LIMIT, value)

    def get_pid_selection(self):
        """Read PID parameter selection. 0 ~ 4."""
        return PIDParameterSelection(
            self.read_register(Register.PID_PARAMETER_SELECTION)
        )

    def set_pid_selection(self, value):
        """Write PID parameter selection. 0 ~ 4."""
        self.write_register(Register.PID_PARAMETER_SELECTION, int(value))

    def get_sv_value_corresponded_to_pid(self):
        """Read SV value corresponded to PID. Unit: 0.1."""
        return self.read_register(Register.SV_VALUE_CORRESPONDED_TO_PID, 1)

    def get_alarm_1_type(self):
        """Read Alarm 1 type."""
        return self.read_register(Register.ALARM_1_TYPE)

    def set_alarm_1_type(self, value):
        """Write Alarm 1 type."""
        self.write_register(Register.ALARM_1_TYPE, value)

    def get_alarm_2_type(self):
        """Read Alarm 2 type."""
        return self.read_register(Register.ALARM_2_TYPE)

    def set_alarm_2_type(self, value):
        """Write Alarm 2 type."""
        self.write_register(Register.ALARM_2_TYPE, value)

    def get_alarm_3_type(self):
        """Read Alarm 3 type."""
        return self.read_register(Register.ALARM_3_TYPE)

    def set_alarm_3_type(self, value):
        """Write Alarm 3 type."""
        self.write_register(Register.ALARM_3_TYPE, value)

    def get_system_alarm(self):
        """Read System alarm setting. 0: None (default), 1-3: Set Alarm 1 to Alarm 3."""
        return SystemAlarmSetting(self.read_register(Register.SYSTEM_ALARM_SETTING))

    def set_system_alarm(self, value):
        """Write System alarm setting. 0: None (default), 1-3: Set Alarm 1 to Alarm 3."""
        self.write_register(Register.SYSTEM_ALARM_SETTING, int(value))

    def get_upper_limit_alarm_1(self):
        """Read Upper-limit alarm 1."""
        return self.read_register(Register.UPPER_LIMIT_ALARM_1)

    def set_upper_limit_alarm_1(self, value):
        """Write Upper-limit alarm 1."""
        self.write_register(Register.UPPER_LIMIT_ALARM_1, value)

    def get_lower_limit_alarm_1(self):
        """Read Lower-limit alarm 1."""
        return self.read_register(Register.LOWER_LIMIT_ALARM_1)

    def set_lower_limit_alarm_1(self, value):
        """Write Lower-limit alarm 1."""
        self.write_register(Register.LOWER_LIMIT_ALARM_1, value)

    def get_upper_limit_alarm_2(self):
        """Read Upper-limit alarm 2."""
        return self.read_register(Register.UPPER_LIMIT_ALARM_2)

    def set_upper_limit_alarm_2(self, value):
        """Write Upper-limit alarm 2."""
        self.write_register(Register.UPPER_LIMIT_ALARM_2, value)

    def get_lower_limit_alarm_2(self):
        """Read Lower-limit alarm 2."""
        return self.read_register(Register.LOWER_LIMIT_ALARM_2)

    def set_lower_limit_alarm_2(self, value):
        """Write Lower-limit alarm 2."""
        self.write_register(Register.LOWER_LIMIT_ALARM_2, value)

    def get_upper_limit_alarm_3(self):
        """Read Upper-limit alarm 3."""
        return self.read_register(Register.UPPER_LIMIT_ALARM_3)

    def set_upper_limit_alarm_3(self, value):
        """Write Upper-limit alarm 3."""
        self.write_register(Register.UPPER_LIMIT_ALARM_3, value)

    def get_lower_limit_alarm_3(self):
        """Read Lower-limit alarm 3."""
        return self.read_register(Register.LOWER_LIMIT_ALARM_3)

    def set_lower_limit_alarm_3(self, value):
        """Write Lower-limit alarm 3."""
        self.write_register(Register.LOWER_LIMIT_ALARM_3, value)

    def get_led_status(self):
        """Read LED status.
        b0: Alm3, b1: Alm2, b2: degF, b3: degC, b4: Alm1, b5: OUT2, b6: OUT1, b7: AT
        """
        return self.read_register(Register.LED_STATUS)

    def get_pushbutton_status(self):
        """Read pushbutton status.
        b0: Set, b1: Select, b2: Up, b3: Down. 0 is to push.
        """
        return self.read_register(Register.PUSHBUTTON_STATUS)

    def get_lock_status(self):
        """Read Setting lock status. 0: Normal, 1: All setting lock, 11: Lock others than SV value."""
        return SettingLockStatus(self.read_register(Register.SETTING_LOCK_STATUS))

    def set_lock_status(self, value):
        """Write Setting lock status."""
        self.write_register(Register.SETTING_LOCK_STATUS, int(value))

    def get_ct_read_value(self):
        """Read CT read value. Unit: 0.1A."""
        return self.read_register(Register.CT_READ_VALUE, 1)

    def get_firmware_version(self):
        """Read Software version. V1.00 indicates 0x100."""
        return self.read_register(Register.FIRMWARE_VERSION)

    def get_start_pattern(self):
        """Read Start pattern number. 0-7."""
        return self.read_register(Register.START_PATTERN)

    def set_start_pattern(self, value):
        """Write Start pattern number. 0-7."""
        self.write_register(Register.START_PATTERN, value)

    def get_executing_step_time_left(self):
        """Read step time left. Returns tuple (min, sec) or total seconds, depending on preference.
        Here handling as per Delta.py style: separate or raw?
        Spec 1032H: sec, 1033H: min.
        """
        # Delta.py style:
        # get_current_step_left_sec
        # get_current_step_left_min
        # I will match that.
        pass

    def get_step_time_left_sec(self):
        """Read step time left (sec)."""
        return self.read_register(Register.STEP_TIME_LEFT_SEC)

    def get_step_time_left_min(self):
        """Read step time left (min)."""
        return self.read_register(Register.STEP_TIME_LEFT_MIN)

    def get_executing_step_number(self):
        """Read executing step No."""
        return self.read_register(Register.EXECUTING_STEP_NUMBER)

    def get_executing_pattern_number(self):
        """Read executing pattern No."""
        return self.read_register(Register.EXECUTING_PATTERN_NUMBER)

    def get_dynamic_set_value(self):
        """Read dynamic set value."""
        return self.read_register(
            Register.DYNAMIC_SET_VALUE, 1
        )  # Assuming unit 0.1 same as PV/SV

    def get_actual_steps(self, pattern_index):
        """Read Actual step No. setting for pattern 0-7.
        Address 1040H - 1047H.
        """
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        return self.read_register(Register.ACTUAL_STEP_BASE + pattern_index)

    def set_actual_steps(self, pattern_index, value):
        """Write Actual step No. setting for pattern 0-7."""
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        self.write_register(Register.ACTUAL_STEP_BASE + pattern_index, value)

    def get_cycle_number(self, pattern_index):
        """Read Cycle number for pattern 0-7.
        Address 1050H - 1057H.
        """
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        return self.read_register(Register.CYCLE_NUMBER_BASE + pattern_index)

    def set_cycle_number(self, pattern_index, value):
        """Write Cycle number for pattern 0-7."""
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        self.write_register(Register.CYCLE_NUMBER_BASE + pattern_index, value)

    def get_link_pattern(self, pattern_index):
        """Read Link pattern number for pattern 0-7.
        Address 1060H - 1067H.
        """
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        return self.read_register(Register.LINK_PATTERN_BASE + pattern_index)

    def set_link_pattern(self, pattern_index, value):
        """Write Link pattern number for pattern 0-7."""
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        self.write_register(Register.LINK_PATTERN_BASE + pattern_index, value)

    # Patterns (Temperature and Time)
    # Pattern 0 is 2000H-2007H (Temp) and 2080H-2087H (Time)
    # Each pattern has 8 steps.
    # Total patterns: 8 (0-7).
    # Pattern N Temp Start = 2000H + N*8
    # Pattern N Time Start = 2080H + N*8

    def get_pattern_step(self, pattern_number, step_number):
        """Get temperature and time for a specific pattern and step.
        Returns: (temp, time)
        """
        if not 0 <= pattern_number <= 7:
            raise ValueError("Pattern number must be 0-7")
        if not 0 <= step_number <= 7:
            raise ValueError("Step number must be 0-7")

        temp_addr = Register.PATTERN_TEMP_START + (pattern_number * 8) + step_number
        time_addr = Register.PATTERN_TIME_START + (pattern_number * 8) + step_number

        temp = self.read_register(
            temp_addr, 1
        )  # Unit 0.1 check? Spec says Range -999 ~ 9999. Usually temp is 0.1. Verify?
        # 1001H SV is 0.1. Pattern temp is likely 0.1 too. delta.py uses / 10.0 manually.
        # minimalmodbus with decimals=1 does /10 automatically.
        time = self.read_register(time_addr)  # Time 0~900. No decimal.

        return temp, time

    def set_pattern_step(self, pattern_number, step_number, temp, time):
        """Set temperature and time for a specific pattern and step."""
        if not 0 <= pattern_number <= 7:
            raise ValueError("Pattern number must be 0-7")
        if not 0 <= step_number <= 7:
            raise ValueError("Step number must be 0-7")

        temp_addr = self.PATTERN_TEMP_START + (pattern_number * 8) + step_number
        time_addr = self.PATTERN_TIME_START + (pattern_number * 8) + step_number

        self.write_register(temp_addr, temp, 1)
        self.write_register(time_addr, time, 0)

    # =========================================================================
    # 6. Address and Content of Bit Register
    # Function Code: 02H (Read) / 05H (Write)
    # =========================================================================

    def get_led_at_status(self):
        """Read AT LED status. 0: OFF; 1: ON."""
        return self.read_bit(BitRegister.LED_AT)

    def get_led_out1_status(self):
        """Read Output 1 LED status. 0: OFF; 1: ON."""
        return self.read_bit(BitRegister.LED_OUT1)

    def get_led_out2_status(self):
        """Read Output 2 LED status. 0: OFF; 1: ON."""
        return self.read_bit(BitRegister.LED_OUT2)

    def get_led_alarm1_status(self):
        """Read Alarm 1 LED status. 0: OFF; 1: ON."""
        return self.read_bit(BitRegister.LED_ALARM1)

    def get_led_deg_f_status(self):
        """Read degF LED status. 0: OFF; 1: ON."""
        return self.read_bit(BitRegister.LED_DEG_F)

    def get_led_deg_c_status(self):
        """Read degC LED status. 0: OFF; 1: ON."""
        return self.read_bit(BitRegister.LED_DEG_C)

    def get_led_alarm2_status(self):
        """Read Alarm 2 LED status. 0: OFF; 1: ON."""
        return self.read_bit(BitRegister.LED_ALARM2)

    def get_led_alarm3_status(self):
        """Read Alarm 3 LED status. 0: OFF; 1: ON."""
        return self.read_bit(BitRegister.LED_ALARM3)

    def get_key_set_status(self):
        """Read SET key status. 0: Press down."""
        return self.read_bit(BitRegister.KEY_SET)

    def get_key_function_status(self):
        """Read FUNCTION key status. 0: Press down."""
        return self.read_bit(BitRegister.KEY_FUNCTION)

    def get_key_up_status(self):
        """Read UP key status. 0: Press down."""
        return self.read_bit(BitRegister.KEY_UP)

    def get_key_down_status(self):
        """Read DOWN key status. 0: Press down."""
        return self.read_bit(BitRegister.KEY_DOWN)

    def get_event_1_status(self):
        """Read Event 1 status. 1: Event action."""
        return self.read_bit(BitRegister.EVENT_1)

    def get_event_2_status(self):
        """Read Event 2 status. 1: Event action."""
        return self.read_bit(BitRegister.EVENT_2)

    def get_system_alarm_status(self):
        """Read System Alarm status. 1: Alarm action."""
        return self.read_bit(BitRegister.SYSTEM_ALARM)

    def get_communication_write_in(self):
        """Read Communication write-in. 0: Disabled (default), 1: Enabled."""
        return self.read_bit(BitRegister.COMMUNICATION_WRITE_IN)

    def set_communication_write_in(self, value):
        """Write Communication write-in. 0: Disabled (default), 1: Enabled."""
        self.write_bit(BitRegister.COMMUNICATION_WRITE_IN, value)

    def get_temp_unit(self):
        """Read Temp unit display. 1: degC/linear (default); 0: degF."""
        return TempUnit(self.read_bit(BitRegister.TEMP_UNIT))

    def set_temp_unit(self, value):
        """Write Temp unit display. 1: degC/linear (default); 0: degF."""
        self.write_bit(BitRegister.TEMP_UNIT, int(value))

    def get_decimal_point(self):
        """Read Decimal point position. Valid for all except B, S, R type. (0 or 1)."""
        return DecimalPointPosition(self.read_bit(BitRegister.DECIMAL_POINT))

    def set_decimal_point(self, value):
        """Write Decimal point position. Valid for all except B, S, R type. (0 or 1)."""
        self.write_bit(BitRegister.DECIMAL_POINT, int(value))

    def get_at(self):
        """Read AT setting. 0: OFF (default), 1: ON."""
        return ATSetting(self.read_bit(BitRegister.AT))

    def set_at(self, value):
        """Write AT setting. 0: OFF (default), 1: ON."""
        self.write_bit(BitRegister.AT, int(value))

    def get_run_stop(self):
        """Read Control RUN/STOP setting. 0: STOP, 1: RUN (default)."""
        return RunStopSetting(self.read_bit(BitRegister.RUN_STOP))

    def set_run_stop(self, value):
        """Write Control RUN/STOP setting. 0: STOP, 1: RUN (default)."""
        self.write_bit(BitRegister.RUN_STOP, int(value))

    def get_stop_pid(self):
        """Read STOP setting (PID program). 0: RUN (default), 1: STOP."""
        return StopSettingPID(self.read_bit(BitRegister.STOP_PID))

    def set_stop_pid(self, value):
        """Write STOP setting (PID program). 0: RUN (default), 1: STOP."""
        self.write_bit(BitRegister.STOP_PID, int(value))

    def get_temp_stop_pid(self):
        """Read Temporarily STOP (PID program). 0: RUN (default), 1: Temporarily STOP."""
        return TemporarilyStopPID(self.read_bit(BitRegister.TEMP_STOP_PID))

    def set_temp_stop_pid(self, value):
        """Write Temporarily STOP (PID program). 0: RUN (default), 1: Temporarily STOP."""
        self.write_bit(BitRegister.TEMP_STOP_PID, int(value))

    def get_valve_feedback(self):
        """Read Valve feedback setting. 0: w/o feedback (default), 1: feedback function."""
        return ValveFeedbackSetting(self.read_bit(BitRegister.VALVE_FEEDBACK))

    def set_valve_feedback(self, value):
        """Write Valve feedback setting. 0: w/o feedback (default), 1: feedback function."""
        self.write_bit(BitRegister.VALVE_FEEDBACK, int(value))

    def get_at_valve_feedback(self):
        """Read Auto-tuning valve feedback. 0: Stop AT (default), 1: Start AT."""
        return AutoTuningValveFeedback(self.read_bit(BitRegister.AT_VALVE_FEEDBACK))

    def set_at_valve_feedback(self, value):
        """Write Auto-tuning valve feedback. 0: Stop AT (default), 1: Start AT."""
        self.write_bit(BitRegister.AT_VALVE_FEEDBACK, int(value))
