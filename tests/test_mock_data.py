import unittest
import mock_data

# Write a test for return_relative_image_paths

class TestMockData(unittest.TestCase):
    def test_return_location_image_path(self):
        file_path = mock_data.return_location_image_path(1,'Test St. Francisco')
        self.assertEqual(file_path,'test_st_francisco_1')
