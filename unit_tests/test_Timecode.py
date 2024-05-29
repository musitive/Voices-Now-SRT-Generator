import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator")

import unittest
from ProToolsData.Timecode import Timecode

class TestTimecode(unittest.TestCase):
    def setUp(self):
        self.timecode1 = Timecode(1, 0, 3, 23, frame_rate=24.0)
        self.timecode2 = Timecode.from_frames(89356, 24.0)
        self.timecode3 = Timecode.from_frames("11:12:13:14", 24.0)
        self.timecode4 = Timecode.from_frames(89357, 24.0)
        return

    def test_init_valid(self):
        self.assertEqual(self.timecode1.hours, 1)
        self.assertEqual(self.timecode1.minutes, 0)
        self.assertEqual(self.timecode1.seconds, 3)
        self.assertEqual(self.timecode1.frames, 23)
        self.assertEqual(self.timecode1.frame_rate, 24.0)

    def test_init_invalid(self):
        self.assertRaises(AssertionError, Timecode, -1, 0, 0, 0, 24.0)
        self.assertRaises(AssertionError, Timecode, 0, -1, 0, 0, 24.0)
        self.assertRaises(AssertionError, Timecode, 0, 61, 0, 0, 24.0)
        self.assertRaises(AssertionError, Timecode, 0, 0, -1, 0, 24.0)
        self.assertRaises(AssertionError, Timecode, 0, 0, 61, 0, 24.0)
        self.assertRaises(AssertionError, Timecode, 0, 0, 0, -1, 24.0)
        self.assertRaises(AssertionError, Timecode, 0, 0, 0, 25, 24.0)
        self.assertRaises(AssertionError, Timecode, 0, 0, 0, 0, -1.0)

    def test_from_frames_int_valid(self):
        self.assertEqual(self.timecode2.hours, 1)
        self.assertEqual(self.timecode2.minutes, 2)
        self.assertEqual(self.timecode2.seconds, 3)
        self.assertEqual(self.timecode2.frames, 4)
        self.assertEqual(self.timecode2.frame_rate, 24.0)

    def test_from_frames_str_valid(self):
        self.assertEqual(self.timecode3.hours, 11)
        self.assertEqual(self.timecode3.minutes, 12)
        self.assertEqual(self.timecode3.seconds, 13)
        self.assertEqual(self.timecode3.frames, 14)
        self.assertEqual(self.timecode3.frame_rate, 24.0)

    def test_from_frames_invalid(self):
        self.assertRaises(AssertionError, Timecode.from_frames, -1, 24.0)
        self.assertRaises(AssertionError, Timecode.from_frames, "fdsa", 24.0)
        self.assertRaises(AssertionError, Timecode.from_frames, "11:12:13:14:15", 24.0)
        self.assertRaises(AssertionError, Timecode.from_frames, "11;12;13;14", 24.0)
        self.assertRaises(TypeError, Timecode.from_frames, None, 24.0)

    def test_get_total_frames(self):
        self.assertEqual(self.timecode2.get_total_frames(), 89356)

    def test_get_timecode_in_frames(self):
        self.assertEqual(self.timecode2.get_timecode_in_frames(), "01:02:03:04")

    def test_get_timecode_in_ms(self):
        self.assertEqual(self.timecode2.get_timecode_in_ms(), "01:02:03,167")

    def test_comparators(self):
        timecode_cmp = Timecode.from_frames(89356, 24.0)

        self.assertEqual(self.timecode2, timecode_cmp)
        self.assertNotEqual(self.timecode2, self.timecode4)
        self.assertLess(self.timecode2, self.timecode4)
        self.assertLessEqual(self.timecode2, self.timecode4)
        self.assertGreater(self.timecode4, self.timecode2)
        self.assertGreaterEqual(self.timecode4, self.timecode2)

    def test_add_timecode(self):
        timecode4 = self.timecode2 + self.timecode4
        self.assertEqual(timecode4.get_total_frames(), 178713)

    def test_add_int(self):
        timecode4 = self.timecode2 + 2
        self.assertEqual(timecode4.get_total_frames(), 89358)

    def test_sub_timecode(self):
        timecode4 = self.timecode4 - self.timecode2
        self.assertEqual(timecode4.get_total_frames(), 1)

    def test_sub_int(self):
        timecode4 = self.timecode2 - 2
        self.assertEqual(timecode4.get_total_frames(), 89354)

    def test_mul_int(self):
        timecode4 = self.timecode2 * 3
        self.assertEqual(timecode4.get_total_frames(), 268068)

    def test_div_int(self):
        timecode4 = self.timecode2 / 3
        self.assertEqual(timecode4.get_total_frames(), 29785)

    def test_floordiv_int(self):
        timecode4 = self.timecode2 // 3
        self.assertEqual(timecode4.get_total_frames(), 29785)

    def test_mod_int(self):
        timecode4 = self.timecode2 % 3
        self.assertEqual(timecode4.get_total_frames(), 1)

    def test_ops_invalid(self):
        self.assertRaises(TypeError, self.timecode2.__add__, "test")
        self.assertRaises(TypeError, self.timecode2.__sub__, "test")
        self.assertRaises(TypeError, self.timecode2.__mul__, "test")
        self.assertRaises(TypeError, self.timecode2.__truediv__, "test")
        self.assertRaises(TypeError, self.timecode2.__floordiv__, "test")
        self.assertRaises(TypeError, self.timecode2.__mod__, "test")

if __name__ == '__main__':
    unittest.main()