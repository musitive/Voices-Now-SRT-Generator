import unittest
from ProToolsMarkers.Timecode import Timecode

class TestTimecode(unittest.TestCase):
    def setUp(self):
        return

    def test_init(self):
        timecode = Timecode(1, 0, 3, 23, frame_rate=24.0)
        with self.subTest(f"Valid __init__ call {str(timecode)}"):
            self.assertEqual(timecode.hours, 1)
            self.assertEqual(timecode.minutes, 0)
            self.assertEqual(timecode.seconds, 3)
            self.assertEqual(timecode.frames, 23)
            self.assertEqual(timecode.frame_rate, 24.0)

        with self.subTest("Invalid __init__ calls"):
            self.assertRaises(AssertionError, Timecode, -1, 0, 0, 0, 24.0)
            self.assertRaises(AssertionError, Timecode, 0, -1, 0, 0, 24.0)
            self.assertRaises(AssertionError, Timecode, 0, 61, 0, 0, 24.0)
            self.assertRaises(AssertionError, Timecode, 0, 0, -1, 0, 24.0)
            self.assertRaises(AssertionError, Timecode, 0, 0, 61, 0, 24.0)
            self.assertRaises(AssertionError, Timecode, 0, 0, 0, -1, 24.0)
            self.assertRaises(AssertionError, Timecode, 0, 0, 0, 25, 24.0)
            self.assertRaises(AssertionError, Timecode, 0, 0, 0, 0, -1.0)

    def test_from_frames(self):
        timecode = Timecode.from_frames(89356, 24.0)

        with self.subTest(f"Valid from_frames call {str(timecode)}"):
            self.assertEqual(timecode.hours, 1)
            self.assertEqual(timecode.minutes, 2)
            self.assertEqual(timecode.seconds, 3)
            self.assertEqual(timecode.frames, 4)
            self.assertEqual(timecode.frame_rate, 24.0)

        timecode = Timecode.from_frames("11:12:13:14", 24.0)

        with self.subTest(f"Valid from_frames call {str(timecode)}"):
            self.assertEqual(timecode.hours, 11)
            self.assertEqual(timecode.minutes, 12)
            self.assertEqual(timecode.seconds, 13)
            self.assertEqual(timecode.frames, 14)
            self.assertEqual(timecode.frame_rate, 24.0)

        with self.subTest(f"Invalid from_frames call"):
            self.assertRaises(AssertionError, Timecode.from_frames, -1, 24.0)
            self.assertRaises(AssertionError, Timecode.from_frames, "fdsa", 24.0)
            self.assertRaises(AssertionError, Timecode.from_frames, "11:12:13:14:15", 24.0)
            self.assertRaises(AssertionError, Timecode.from_frames, "11;12;13;14", 24.0)
            self.assertRaises(TypeError, Timecode.from_frames, None, 24.0)

    def test_get_total_frames(self):
        timecode = Timecode.from_frames(89356, 24.0)
        self.assertEqual(timecode.get_total_frames(), 89356)

    def test_get_timecode_in_frames(self):
        timecode = Timecode.from_frames(89356, 24.0)
        self.assertEqual(timecode.get_timecode_in_frames(), "01:02:03:04")

    def test_get_timecode_in_ms(self):
        timecode = Timecode.from_frames(89356, 24.0)
        self.assertEqual(timecode.get_timecode_in_ms(), "01:02:03,167")

    def test_comparators(self):
        timecode1 = Timecode.from_frames(89356, 24.0)
        timecode2 = Timecode.from_frames(89356, 24.0)
        timecode3 = Timecode.from_frames(89357, 24.0)

        self.assertEqual(timecode1, timecode2)
        self.assertNotEqual(timecode1, timecode3)
        self.assertLess(timecode1, timecode3)
        self.assertLessEqual(timecode1, timecode3)
        self.assertGreater(timecode3, timecode1)
        self.assertGreaterEqual(timecode3, timecode1)

    def test_operators(self):
        timecode1 = Timecode.from_frames(89356, 24.0)
        timecode2 = Timecode.from_frames(89356, 24.0)
        timecode3 = Timecode.from_frames(89357, 24.0)

        with self.subTest("Addition with Timecode"):
            timecode4 = timecode1 + timecode2
            self.assertEqual(timecode4.get_total_frames(), 178712)

        with self.subTest("Subtraction with Timecode"):
            timecode4 = timecode3 - timecode1
            self.assertEqual(timecode4.get_total_frames(), 1)

        with self.subTest("Addition with integer"):
            timecode4 = timecode1 + 2
            self.assertEqual(timecode4.get_total_frames(), 89358)

        with self.subTest("Subtraction with integer"):
            timecode4 = timecode1 - 2
            self.assertEqual(timecode4.get_total_frames(), 89354)

        with self.subTest("Multiplication with integer"):
            timecode4 = timecode1 * 3
            self.assertEqual(timecode4.get_total_frames(), 268068)

        with self.subTest("Division with integer"):
            timecode4 = timecode1 / 3
            self.assertEqual(timecode4.get_total_frames(), 29785)

        with self.subTest("Floor division with integer"):
            timecode4 = timecode1 // 3
            self.assertEqual(timecode4.get_total_frames(), 29785)

        with self.subTest("Modulus with integer"):
            timecode4 = timecode1 % 3
            self.assertEqual(timecode4.get_total_frames(), 1)

        with self.subTest("Invalid operations"):
            self.assertRaises(TypeError, timecode1.__add__, "test")
            self.assertRaises(TypeError, timecode1.__sub__, "test")
            self.assertRaises(TypeError, timecode1.__mul__, "test")
            self.assertRaises(TypeError, timecode1.__truediv__, "test")
            self.assertRaises(TypeError, timecode1.__floordiv__, "test")
            self.assertRaises(TypeError, timecode1.__mod__, "test")

if __name__ == '__main__':
    unittest.main()