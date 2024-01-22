import unittest
import sys

# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/RichardsonJ/Documents/Python Scripts/Word Doc Experiment/')

from ProToolsMarkers import ProToolsMarkers
from Marker import Marker

class TestProToolsMarkers(unittest.TestCase):
    def setUp(self) -> None:
        self.markers = ProToolsMarkers("test_01.txt")

    def test_init(self):
        self.assertEqual(self.markers.FRAME_RATE, 23.976)

    def test_getMarker_fail(self):
        self.assertRaises(Exception, lambda: self.markers.get_marker(-1))

    def test_getMarker_pass(self):
        m = Marker("1", "01:00:01:02", "533760", "Samples", "1", 23.976)
        self.assertEqual(self.markers.get_marker(0), m)

        m = Marker("2", "01:00:15:10", "1222656", "Samples", "2", 23.976)
        self.assertEqual(self.markers.get_marker(1), m)

if __name__ == '__main__':
    unittest.main()