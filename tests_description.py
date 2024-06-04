import unittest

import description

class TestTasks(unittest.TestCase):
    def test_get_all_locations(self):
        locations = description.get_all_locations()
        self.assertEqual(len(locations), 161)
        self.assertEqual(locations[0][0], 1)
        self.assertEqual(locations[0][1], "New York, NY USA")
        self.assertEqual(locations[2][0], 3)
        self.assertEqual(locations[2][1], "Chicago, IL USA")
        
        