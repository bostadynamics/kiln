import unittest

from src.core.mock_delta_2 import MockDelta2
from src.core.delta_2 import ControlMethod


class TestMockDelta2(unittest.TestCase):
    def setUp(self):
        self.mock = MockDelta2()

    def test_initial_values(self):
        # Default PV should be 25.0
        self.assertEqual(self.mock.get_pv(), 25.0)
        # Default SV should be 25.0
        self.assertEqual(self.mock.get_setpoint(), 25.0)

    def test_set_get_setpoint(self):
        # Set to 100.5
        self.mock.set_setpoint(100.5)
        self.assertEqual(self.mock.get_setpoint(), 100.5)

        # Check raw register storage
        # 0x1001 should be 1005
        self.assertEqual(self.mock.registers[0x1001], 1005)

    def test_control_method_enum(self):
        # Default 0 -> PID
        self.assertEqual(self.mock.get_control_method(), ControlMethod.PID)

        # Set to ON_OFF
        self.mock.set_control_method(ControlMethod.ON_OFF)
        self.assertEqual(self.mock.get_control_method(), ControlMethod.ON_OFF)
        self.assertEqual(self.mock.registers[0x1005], 1)

    def test_bits(self):
        # Test generic bit
        self.assertEqual(self.mock.get_at(), 0)  # Default OFF

        self.mock.set_at(1)
        self.assertEqual(self.mock.get_at(), 1)  # ON
        self.assertEqual(self.mock.bits[0x0813], 1)

    def test_defaults(self):
        # Unset register should return 0
        self.assertEqual(self.mock.get_valve_time(), 0.0)


if __name__ == "__main__":
    unittest.main()
