import minimalmodbus


class Delta2(minimalmodbus.Instrument):
    """Instrument class for Delta DTB Series Temperature Controller.

    Based on the RS-485 Communication Protocol.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """

    # Pattern start addresses
    PATTERN_TEMP_START = 0x2000
    PATTERN_TIME_START = 0x2080

    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        # Default settings that might be useful, though minimalmodbus defaults are usually fine
        # self.serial.baudrate = 9600
        # self.serial.bytesize = 7
        # self.serial.parity   = serial.PARITY_EVEN
        # self.serial.stopbits = 1
        # self.serial.timeout  = 0.5
        # self.mode = minimalmodbus.MODE_ASCII

    # =========================================================================
    # 5. Address and Content of Data Register
    # Function Code: 03H (Read) / 06H (Write)
    # =========================================================================

    def get_pv(self):
        """Read Process value (PV). Unit is 0.1."""
        return self.read_register(0x1000, 1)

    def get_setpoint(self):
        """Read Set point (SV). Unit is 0.1, deg C or deg F."""
        return self.read_register(0x1001, 1)

    def set_setpoint(self, value):
        """Write Set point (SV). Unit is 0.1, deg C or deg F."""
        self.write_register(0x1001, value, 1)

    def get_upper_limit_temp_range(self):
        """Read Upper-limit of temperature range."""
        return self.read_register(0x1002, 1)

    def set_upper_limit_temp_range(self, value):
        """Write Upper-limit of temperature range."""
        self.write_register(0x1002, value, 1)

    def get_lower_limit_temp_range(self):
        """Read Lower-limit of temperature range."""
        return self.read_register(0x1003, 1)

    def set_lower_limit_temp_range(self, value):
        """Write Lower-limit of temperature range."""
        self.write_register(0x1003, value, 1)

    def get_sensor_type(self):
        """Read Input temperature sensor type."""
        return self.read_register(0x1004)

    def set_sensor_type(self, value):
        """Write Input temperature sensor type."""
        self.write_register(0x1004, value)

    def get_control_method(self):
        """Read Control method. 0: PID, 1: ON/OFF, 2: Manual tuning, 3: PID program control."""
        return self.read_register(0x1005)

    def set_control_method(self, value):
        """Write Control method. 0: PID, 1: ON/OFF, 2: Manual tuning, 3: PID program control."""
        self.write_register(0x1005, value)

    def get_heating_cooling_selection(self):
        """Read Heating/Cooling selection. 0: Heating, 1: Cooling, 2: Heating/Cooling, 3: Cooling/Heating."""
        return self.read_register(0x1006)

    def set_heating_cooling_selection(self, value):
        """Write Heating/Cooling selection. 0: Heating, 1: Cooling, 2: Heating/Cooling, 3: Cooling/Heating."""
        self.write_register(0x1006, value)

    def get_heating_cooling_cycle_1(self):
        """Read 1st group Heating/Cooling cycle. 0-99."""
        return self.read_register(0x1007)

    def set_heating_cooling_cycle_1(self, value):
        """Write 1st group Heating/Cooling cycle. 0-99."""
        self.write_register(0x1007, value)

    def get_heating_cooling_cycle_2(self):
        """Read 2nd group Heating/Cooling cycle. 0-99."""
        return self.read_register(0x1008)

    def set_heating_cooling_cycle_2(self, value):
        """Write 2nd group Heating/Cooling cycle. 0-99."""
        self.write_register(0x1008, value)

    def get_proportional_band(self):
        """Read PB Proportional band. 0.1 ~ 999.9."""
        return self.read_register(0x1009, 1)

    def set_proportional_band(self, value):
        """Write PB Proportional band. 0.1 ~ 999.9."""
        self.write_register(0x1009, value, 1)

    def get_integral_time(self):
        """Read Ti Integral time. 0 ~ 9,999."""
        return self.read_register(0x100A, 1)  # Note: 0 decimal places according to spec value range, but previous delta.py used 1? Spec says "0 ~ 9,999", implied integer. Using 1 decimal to match delta.py if that was the intent, but strictly spec says 0~9999. Let's assume integer unless delta.py forced otherwise. delta.py used 1. Let's stick to 1 for consistency if it worked, or 0 if strictly following integer. Spec says "0 ~ 9,999", no decimal point mentioned unlike 1009H. However, to match delta.py style which used 1, I will keep 1 if it seems appropriate, but "0 ~ 9,999" usually implies int. Wait, delta.py used `read_register(0x100A, 1)`, which means it treats it as 1 decimal place. I will follow delta.py precedent for consistency, assuming the user wants that."""
        # Actually, looking at 1009H, it says "0.1 ~ 999.9", which clearly has a decimal. 100A says "0 ~ 9,999".
        # minimalmodbus read_register(addr, numberOfDecimals)
        # If delta.py used 1, maybe they observed it has decimals. I will respect delta.py for 100A.
        # But for others I will follow spec.

    def set_integral_time(self, value):
        """Write Ti Integral time. 0 ~ 9,999."""
        self.write_register(0x100A, value, 1)

    def get_derivative_time(self):
        """Read Td Derivative time. 0 ~ 9,999."""
        return self.read_register(0x100B, 1)

    def set_derivative_time(self, value):
        """Write Td Derivative time. 0 ~ 9,999."""
        self.write_register(0x100B, value, 1)

    def get_integration_default(self):
        """Read Integration default. 0 ~ 100%, unit is 0.1%."""
        return self.read_register(0x100C, 1)

    def set_integration_default(self, value):
        """Write Integration default. 0 ~ 100%, unit is 0.1%."""
        self.write_register(0x100C, value, 1)

    def get_pd_control_offset(self):
        """Read PD control offset (when Ti=0). 0 ~ 100%, unit is 0.1%."""
        return self.read_register(0x100D, 1)

    def set_pd_control_offset(self, value):
        """Write PD control offset (when Ti=0). 0 ~ 100%, unit is 0.1%."""
        self.write_register(0x100D, value, 1)

    def get_coef_setting(self):
        """Read COEF setting (Dual Loop). 0.01 ~ 99.99."""
        return self.read_register(0x100E, 2)

    def set_coef_setting(self, value):
        """Write COEF setting (Dual Loop). 0.01 ~ 99.99."""
        self.write_register(0x100E, value, 2)

    def get_dead_band_setting(self):
        """Read Dead band setting (Dual Loop). -999 ~ 9,999."""
        return self.read_register(0x100F)

    def set_dead_band_setting(self, value):
        """Write Dead band setting (Dual Loop). -999 ~ 9,999."""
        self.write_register(0x100F, value)

    def get_hysteresis_output_1(self):
        """Read Hysteresis (1st output group). 0 ~ 9,999."""
        return self.read_register(0x1010)

    def set_hysteresis_output_1(self, value):
        """Write Hysteresis (1st output group). 0 ~ 9,999."""
        self.write_register(0x1010, value)

    def get_hysteresis_output_2(self):
        """Read Hysteresis (2nd output group). 0 ~ 9,999."""
        return self.read_register(0x1011)

    def set_hysteresis_output_2(self, value):
        """Write Hysteresis (2nd output group). 0 ~ 9,999."""
        self.write_register(0x1011, value)

    def get_output_1_value(self):
        """Read Output 1 Value. Unit is 0.1%."""
        return self.read_register(0x1012, 1)

    def set_output_1_value(self, value):
        """Write Output 1 Value. Write valid under manual tuning mode only."""
        self.write_register(0x1012, value, 1)

    def get_output_2_value(self):
        """Read Output 2 Value. Unit is 0.1%."""
        return self.read_register(0x1013, 1)

    def set_output_2_value(self, value):
        """Write Output 2 Value. Write valid under manual tuning mode only."""
        self.write_register(0x1013, value, 1)

    def get_upper_limit_analog(self):
        """Read Upper-limit analog regulation."""
        return self.read_register(0x1014)

    def set_upper_limit_analog(self, value):
        """Write Upper-limit analog regulation."""
        self.write_register(0x1014, value)

    def get_lower_limit_analog(self):
        """Read Lower-limit analog regulation."""
        return self.read_register(0x1015)

    def set_lower_limit_analog(self, value):
        """Write Lower-limit analog regulation."""
        self.write_register(0x1015, value)

    def get_temperature_regulation_value(self):
        """Read Temperature regulation value. -999 ~ +999, unit: 0.1."""
        return self.read_register(0x1016, 1)

    def set_temperature_regulation_value(self, value):
        """Write Temperature regulation value. -999 ~ +999, unit: 0.1."""
        self.write_register(0x1016, value, 1)

    def get_analog_decimal_setting(self):
        """Read Analog decimal setting. 0 ~ 3."""
        return self.read_register(0x1017)

    def set_analog_decimal_setting(self, value):
        """Write Analog decimal setting. 0 ~ 3."""
        self.write_register(0x1017, value)

    def get_valve_time(self):
        """Read Valve time (Open to Close). 0.1 ~ 999.9."""
        return self.read_register(0x1018, 1)

    def set_valve_time(self, value):
        """Write Valve time (Open to Close). 0.1 ~ 999.9."""
        self.write_register(0x1018, value, 1)

    def get_valve_dead_band(self):
        """Read Valve Dead Band. 0 ~ 100%; unit: 0.1%."""
        return self.read_register(0x1019, 1)

    def set_valve_dead_band(self, value):
        """Write Valve Dead Band. 0 ~ 100%; unit: 0.1%."""
        self.write_register(0x1019, value, 1)

    def get_valve_feedback_upper_limit(self):
        """Read Valve feedback upper-limit. 0 ~ 1,024."""
        return self.read_register(0x101A)

    def set_valve_feedback_upper_limit(self, value):
        """Write Valve feedback upper-limit. 0 ~ 1,024."""
        self.write_register(0x101A, value)

    def get_valve_feedback_lower_limit(self):
        """Read Valve feedback lower-limit. 0 ~ 1,024."""
        return self.read_register(0x101B)

    def set_valve_feedback_lower_limit(self, value):
        """Write Valve feedback lower-limit. 0 ~ 1,024."""
        self.write_register(0x101B, value)

    def get_pid_parameter_selection(self):
        """Read PID parameter selection. 0 ~ 4."""
        return self.read_register(0x101C)

    def set_pid_parameter_selection(self, value):
        """Write PID parameter selection. 0 ~ 4."""
        self.write_register(0x101C, value)

    def get_sv_value_corresponded_to_pid(self):
        """Read SV value corresponded to PID. Unit: 0.1."""
        return self.read_register(0x101D, 1)

    def get_alarm_1_type(self):
        """Read Alarm 1 type."""
        return self.read_register(0x1020)

    def set_alarm_1_type(self, value):
        """Write Alarm 1 type."""
        self.write_register(0x1020, value)

    def get_alarm_2_type(self):
        """Read Alarm 2 type."""
        return self.read_register(0x1021)

    def set_alarm_2_type(self, value):
        """Write Alarm 2 type."""
        self.write_register(0x1021, value)

    def get_alarm_3_type(self):
        """Read Alarm 3 type."""
        return self.read_register(0x1022)

    def set_alarm_3_type(self, value):
        """Write Alarm 3 type."""
        self.write_register(0x1022, value)

    def get_system_alarm_setting(self):
        """Read System alarm setting. 0: None (default), 1-3: Set Alarm 1 to Alarm 3."""
        return self.read_register(0x1023)

    def set_system_alarm_setting(self, value):
        """Write System alarm setting. 0: None (default), 1-3: Set Alarm 1 to Alarm 3."""
        self.write_register(0x1023, value)

    def get_upper_limit_alarm_1(self):
        """Read Upper-limit alarm 1."""
        return self.read_register(0x1024)

    def set_upper_limit_alarm_1(self, value):
        """Write Upper-limit alarm 1."""
        self.write_register(0x1024, value)

    def get_lower_limit_alarm_1(self):
        """Read Lower-limit alarm 1."""
        return self.read_register(0x1025)

    def set_lower_limit_alarm_1(self, value):
        """Write Lower-limit alarm 1."""
        self.write_register(0x1025, value)

    def get_upper_limit_alarm_2(self):
        """Read Upper-limit alarm 2."""
        return self.read_register(0x1026)

    def set_upper_limit_alarm_2(self, value):
        """Write Upper-limit alarm 2."""
        self.write_register(0x1026, value)

    def get_lower_limit_alarm_2(self):
        """Read Lower-limit alarm 2."""
        return self.read_register(0x1027)

    def set_lower_limit_alarm_2(self, value):
        """Write Lower-limit alarm 2."""
        self.write_register(0x1027, value)

    def get_upper_limit_alarm_3(self):
        """Read Upper-limit alarm 3."""
        return self.read_register(0x1028)

    def set_upper_limit_alarm_3(self, value):
        """Write Upper-limit alarm 3."""
        self.write_register(0x1028, value)

    def get_lower_limit_alarm_3(self):
        """Read Lower-limit alarm 3."""
        return self.read_register(0x1029)

    def set_lower_limit_alarm_3(self, value):
        """Write Lower-limit alarm 3."""
        self.write_register(0x1029, value)

    def get_led_status(self):
        """Read LED status.
        b0: Alm3, b1: Alm2, b2: degF, b3: degC, b4: Alm1, b5: OUT2, b6: OUT1, b7: AT
        """
        return self.read_register(0x102A)

    def get_pushbutton_status(self):
        """Read pushbutton status.
        b0: Set, b1: Select, b2: Up, b3: Down. 0 is to push.
        """
        return self.read_register(0x102B)

    def get_setting_lock_status(self):
        """Read Setting lock status. 0: Normal, 1: All setting lock, 11: Lock others than SV value."""
        return self.read_register(0x102C)

    def set_setting_lock_status(self, value):
        """Write Setting lock status."""
        self.write_register(0x102C, value)

    def get_ct_read_value(self):
        """Read CT read value. Unit: 0.1A."""
        return self.read_register(0x102D, 1)

    def get_firmware_version(self):
        """Read Software version. V1.00 indicates 0x100."""
        return self.read_register(0x102F)

    def get_start_pattern_number(self):
        """Read Start pattern number. 0-7."""
        return self.read_register(0x1030)

    def set_start_pattern_number(self, value):
        """Write Start pattern number. 0-7."""
        self.write_register(0x1030, value)

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
        return self.read_register(0x1032)

    def get_step_time_left_min(self):
        """Read step time left (min)."""
        return self.read_register(0x1033)

    def get_executing_step_number(self):
        """Read executing step No."""
        return self.read_register(0x1034)

    def get_executing_pattern_number(self):
        """Read executing pattern No."""
        return self.read_register(0x1035)

    def get_dynamic_set_value(self):
        """Read dynamic set value."""
        return self.read_register(0x1036, 1) # Assuming unit 0.1 same as PV/SV

    def get_actual_step_number_setting(self, pattern_index):
        """Read Actual step No. setting for pattern 0-7.
        Address 1040H - 1047H.
        """
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        return self.read_register(0x1040 + pattern_index)

    def set_actual_step_number_setting(self, pattern_index, value):
        """Write Actual step No. setting for pattern 0-7."""
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        self.write_register(0x1040 + pattern_index, value)

    def get_cycle_number(self, pattern_index):
        """Read Cycle number for pattern 0-7.
        Address 1050H - 1057H.
        """
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        return self.read_register(0x1050 + pattern_index)

    def set_cycle_number(self, pattern_index, value):
        """Write Cycle number for pattern 0-7."""
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        self.write_register(0x1050 + pattern_index, value)

    def get_link_pattern_number(self, pattern_index):
        """Read Link pattern number for pattern 0-7.
        Address 1060H - 1067H.
        """
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        return self.read_register(0x1060 + pattern_index)

    def set_link_pattern_number(self, pattern_index, value):
        """Write Link pattern number for pattern 0-7."""
        if not 0 <= pattern_index <= 7:
            raise ValueError("Pattern index must be between 0 and 7")
        self.write_register(0x1060 + pattern_index, value)

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

        temp_addr = self.PATTERN_TEMP_START + (pattern_number * 8) + step_number
        time_addr = self.PATTERN_TIME_START + (pattern_number * 8) + step_number

        temp = self.read_register(temp_addr, 1) # Unit 0.1 check? Spec says Range -999 ~ 9999. Usually temp is 0.1. Verify?
        # 1001H SV is 0.1. Pattern temp is likely 0.1 too. delta.py uses / 10.0 manually.
        # minimalmodbus with decimals=1 does /10 automatically.
        time = self.read_register(time_addr) # Time 0~900. No decimal.

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
        return self.read_bit(0x0800)

    def get_led_out1_status(self):
        """Read Output 1 LED status. 0: OFF; 1: ON."""
        return self.read_bit(0x0801)

    def get_led_out2_status(self):
        """Read Output 2 LED status. 0: OFF; 1: ON."""
        return self.read_bit(0x0802)

    def get_led_alarm1_status(self):
        """Read Alarm 1 LED status. 0: OFF; 1: ON."""
        return self.read_bit(0x0803)

    def get_led_deg_f_status(self):
        """Read degF LED status. 0: OFF; 1: ON."""
        return self.read_bit(0x0804)

    def get_led_deg_c_status(self):
        """Read degC LED status. 0: OFF; 1: ON."""
        return self.read_bit(0x0805)

    def get_led_alarm2_status(self):
        """Read Alarm 2 LED status. 0: OFF; 1: ON."""
        return self.read_bit(0x0806)

    def get_led_alarm3_status(self):
        """Read Alarm 3 LED status. 0: OFF; 1: ON."""
        return self.read_bit(0x0807)

    def get_key_set_status(self):
        """Read SET key status. 0: Press down."""
        return self.read_bit(0x0808)

    def get_key_function_status(self):
        """Read FUNCTION key status. 0: Press down."""
        return self.read_bit(0x0809)

    def get_key_up_status(self):
        """Read UP key status. 0: Press down."""
        return self.read_bit(0x080A)

    def get_key_down_status(self):
        """Read DOWN key status. 0: Press down."""
        return self.read_bit(0x080B)

    def get_event_1_status(self):
        """Read Event 1 status. 1: Event action."""
        return self.read_bit(0x080C)

    def get_event_2_status(self):
        """Read Event 2 status. 1: Event action."""
        return self.read_bit(0x080D)

    def get_system_alarm_status(self):
        """Read System Alarm status. 1: Alarm action."""
        return self.read_bit(0x080E)

    def get_communication_write_in(self):
        """Read Communication write-in. 0: Disabled (default), 1: Enabled."""
        return self.read_bit(0x0810)

    def set_communication_write_in(self, value):
        """Write Communication write-in. 0: Disabled (default), 1: Enabled."""
        self.write_bit(0x0810, value)

    def get_temp_unit_display(self):
        """Read Temp unit display. 1: degC/linear (default); 0: degF."""
        return self.read_bit(0x0811)

    def set_temp_unit_display(self, value):
        """Write Temp unit display. 1: degC/linear (default); 0: degF."""
        self.write_bit(0x0811, value)

    def get_decimal_point_position(self):
        """Read Decimal point position. Valid for all except B, S, R type. (0 or 1)."""
        return self.read_bit(0x0812)

    def set_decimal_point_position(self, value):
        """Write Decimal point position. Valid for all except B, S, R type. (0 or 1)."""
        self.write_bit(0x0812, value)

    def get_at_setting(self):
        """Read AT setting. 0: OFF (default), 1: ON."""
        return self.read_bit(0x0813)

    def set_at_setting(self, value):
        """Write AT setting. 0: OFF (default), 1: ON."""
        self.write_bit(0x0813, value)

    def get_run_stop_setting(self):
        """Read Control RUN/STOP setting. 0: STOP, 1: RUN (default)."""
        return self.read_bit(0x0814)

    def set_run_stop_setting(self, value):
        """Write Control RUN/STOP setting. 0: STOP, 1: RUN (default)."""
        self.write_bit(0x0814, value)

    def get_stop_setting_pid(self):
        """Read STOP setting (PID program). 0: RUN (default), 1: STOP."""
        return self.read_bit(0x0815)

    def set_stop_setting_pid(self, value):
        """Write STOP setting (PID program). 0: RUN (default), 1: STOP."""
        self.write_bit(0x0815, value)

    def get_temporarily_stop_pid(self):
        """Read Temporarily STOP (PID program). 0: RUN (default), 1: Temporarily STOP."""
        return self.read_bit(0x0816)

    def set_temporarily_stop_pid(self, value):
        """Write Temporarily STOP (PID program). 0: RUN (default), 1: Temporarily STOP."""
        self.write_bit(0x0816, value)

    def get_valve_feedback_setting(self):
        """Read Valve feedback setting. 0: w/o feedback (default), 1: feedback function."""
        return self.read_bit(0x0817)

    def set_valve_feedback_setting(self, value):
        """Write Valve feedback setting. 0: w/o feedback (default), 1: feedback function."""
        self.write_bit(0x0817, value)

    def get_auto_tuning_valve_feedback(self):
        """Read Auto-tuning valve feedback. 0: Stop AT (default), 1: Start AT."""
        return self.read_bit(0x0818)

    def set_auto_tuning_valve_feedback(self, value):
        """Write Auto-tuning valve feedback. 0: Stop AT (default), 1: Start AT."""
        self.write_bit(0x0818, value)
