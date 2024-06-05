import unittest
from ProToolsData.ProToolsMarker import ProToolsMarker
from ProToolsData.Timecode import Timecode

"""
EXAMPLE PRO TOOLS MARKER 1

#   	LOCATION     	TIME REFERENCE    	UNITS    	NAME                             	COMMENTS
1   	01:00:39:12  	2043360           	Samples  	1                                	
2   	01:00:48:19  	2490480           	Samples  	2 this one has a weird name	
3   	01:00:56:22  	2879280           	Samples  	3                                	fdsa fdsa fdsa fdsa
"""

class TestTimecode(unittest.TestCase):
    def setUp(self):
        self.marker1 = ProToolsMarker("1", "01:00:39:12", "2043360", "Samples", "1", 24.0)
        self.marker2 = ProToolsMarker("2", "01:00:48:19", "2490480", "Samples", "2 this one has a weird name", 24.0, "")
        self.marker3 = ProToolsMarker("3", "01:00:56:22", "2879280", "Samples", "3", 24.0, "fdsa fdsa fdsa fdsa")
        return

    def test_init_valid(self):
        self.assertEqual(self.marker1.marker_id, "1")
        self.assertEqual(self.marker1.timecode, Timecode.from_frames("00:00:39:12", 24.0))
        self.assertEqual(self.marker1.time_reference, "2043360")
        self.assertEqual(self.marker1.units, "Samples")
        self.assertEqual(self.marker1.loop_id, "1")
        self.assertEqual(self.marker1.comments, "")

        self.assertEqual(self.marker2.marker_id, "2")
        self.assertEqual(self.marker2.timecode, Timecode.from_frames("00:00:48:19", 24.0))
        self.assertEqual(self.marker2.time_reference, "2490480")
        self.assertEqual(self.marker2.units, "Samples")
        self.assertEqual(self.marker2.loop_id, "2 this one has a weird name")
        self.assertEqual(self.marker2.comments, "")

        self.assertEqual(self.marker3.marker_id, "3")
        self.assertEqual(self.marker3.timecode, Timecode.from_frames("00:00:56:22", 24.0))
        self.assertEqual(self.marker3.time_reference, "2879280")
        self.assertEqual(self.marker3.units, "Samples")
        self.assertEqual(self.marker3.loop_id, "3")
        self.assertEqual(self.marker3.comments, "fdsa fdsa fdsa fdsa")

    def test_init_invalid(self):
        self.assertRaises(AssertionError, ProToolsMarker, "", "01:00:39:12", "2043360", "Samples", "1", 24.0)
        self.assertRaises(AssertionError, ProToolsMarker, "-1", "01:00:39:12", "2043360", "Samples", "1", 24.0)
        self.assertRaises(AssertionError, ProToolsMarker, "1", "01:00", "2043360", "Samples", "1", 24.0)
        self.assertRaises(AssertionError, ProToolsMarker, "1", "01:00:39;12", "2043360", "Samples", "1", 24.0)
        self.assertRaises(AssertionError, ProToolsMarker, "1", "01:00:39:12", "-1", "Samples", "1", 24.0)
        self.assertRaises(AssertionError, ProToolsMarker, "1", "01:00:39:12", "2043360", "Ticks", "1", 24.0)
        self.assertRaises(AssertionError, ProToolsMarker, "1", "01:00:39:12", "2043360", "Samples", "", 24.0)
        self.assertRaises(AssertionError, ProToolsMarker, "1", "01:00:39:12", "2043360", "Samples", "1", -1)

    def test_eq(self):
        marker_cmp = ProToolsMarker("1", "01:00:39:12", "2043360", "Samples", "1", 24.0)
        self.assertEqual(self.marker1, marker_cmp)
        self.assertFalse(self.marker2 == marker_cmp)

    def test_neq(self):
        marker_cmp = ProToolsMarker("1", "01:00:39:12", "2043360", "Samples", "1", 24.0)
        self.assertNotEqual(self.marker2, marker_cmp)
        self.assertFalse(self.marker1 != marker_cmp)

if __name__ == '__main__':
    unittest.main()