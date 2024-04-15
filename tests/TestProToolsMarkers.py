import unittest
import sys

# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/RichardsonJ/Documents/Python Scripts/Word Doc Experiment/')

from ProToolsMarkerManager import ProToolsMarkerManager
from ProToolsMarker import Marker

class TestProToolsMarkers(unittest.TestCase):
    def setUp(self) -> None:
        self.markers_01 = ProToolsMarkerManager("test_01.txt")
        self.markers_02 = ProToolsMarkerManager("test_02.txt")

    def test_init(self):
        self.assertEqual(self.markers_01.FRAME_RATE, 23.976)
        self.assertEqual(self.markers_02.FRAME_RATE, 23.976)

    def test_getMarker_fail(self):
        self.assertRaises(Exception, lambda: self.markers_01.get_marker(-1))

    def test_getMarker_pass_01(self):
        m = Marker("1", "01:00:01:02", "533760", "Samples", "1", 23.976)
        self.assertEqual(self.markers_01.get_marker(0), m)

        m = Marker("2", "01:00:15:10", "1222656", "Samples", "2", 23.976)
        self.assertEqual(self.markers_01.get_marker(1), m)

    def test_getMarker_pass_02(self):
        m = Marker("1", "01:00:21:09", "1171170", "Samples", "1", 23.976)
        self.assertEqual(self.markers_02.get_marker(0), m)

        m = Marker("2", "01:00:33:05", "1739738", "Samples", "2", 23.976)
        self.assertEqual(self.markers_02.get_marker(1), m)

if __name__ == '__main__':
    unittest.main()