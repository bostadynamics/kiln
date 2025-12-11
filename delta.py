import minimalmodbus


class Delta(minimalmodbus.Instrument):
    """Instrument class for Eurotherm 3500 process controller.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """

    PATTERN_TEMP_START = 0x2000
    PATTERN_TIME_START = 0x2080

    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)

    def get_pv(self):
        return self.read_register(0x1000, 1)

    def get_setpoint(self):
        return self.read_register(0x1001, 1)

    def get_integral_time(self):
        return self.read_register(0x100A, 1)

    def get_derivative_time(self):
        return self.read_register(0x100B, 1)

    def get_current_pattern(self):
        return self.read_register(0x1030, 2)

    def get_current_step_left_sec(self):
        return self.read_register(0x1032, 1) * 10

    def get_current_step_left_min(self):
        return self.read_register(0x1033, 1) * 10

    def get_current_step(self):
        return self.read_register(0x1034)

    def get_current_program(self):
        return self.read_register(0x1035)

    def get_sensor_type(self):
        return self.read_register(0x1004)

    def get_heating_cooling_selection(self):
        return self.read_register(0x1006)

    def get_output_1_value(self):
        return self.read_register(0x1012, 1)

    def get_output_2_value(self):
        return self.read_register(0x1013, 1)

    def get_system_alarm_setting(self):
        return self.read_register(0x1023)

    def get_led_status(self):
        return self.read_register(0x102A)

    def get_pushbutton_status(self):
        return self.read_register(0x102B)

    def get_firmware_version(self):
        return self.read_register(0x102F)

    def get_led_at(self):
        return self.read_bit(0x0800)

    def get_led_out1(self):
        return self.read_bit(0x0801)

    def get_led_out2(self):
        return self.read_bit(0x0802)

    def get_led_deg_f(self):
        return self.read_bit(0x0804)

    def get_led_deg_c(self):
        return self.read_bit(0x0805)

    def get_run_stop_setting(self):
        return self.read_bit(0x0814)

    def get_pattern(self, pattern_number=0):
        pattern_temp_start_addr = self.PATTERN_TEMP_START + pattern_number * 8
        pattern_time_start_addr = self.PATTERN_TIME_START + pattern_number * 8
        for step in range(8):
            temp = self.read_register(pattern_temp_start_addr + step)
            temp = temp / 10.0
            time = self.read_register(pattern_time_start_addr + step)
            yield temp, time

    def get_all_patterns(self):
        patterns = []
        for pattern in range(8):
            patterns.append(list(self.get_pattern(pattern)))
        return patterns
