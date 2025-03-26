import unittest
from config import config

class ConfigTestCase(unittest.TestCase):
    def test_testing_config(self):
        self.assertEqual(config['testing'].TESTING, True)
        self.assertEqual(config['testing'].SQLALCHEMY_TRACK_MODIFICATIONS, False)

if __name__ == '__main__':
    unittest.main()
import unittest
from config import config

class ConfigTestCase(unittest.TestCase):
    def test_testing_config(self):
        self.assertEqual(config['testing'].TESTING, True)
        self.assertEqual(config['testing'].SQLALCHEMY_TRACK_MODIFICATIONS, False)

if __name__ == '__main__':
    unittest.main()
import unittest
from config import config

class ConfigTestCase(unittest.TestCase):
    def test_testing_config(self):
        self.assertEqual(config['testing'].TESTING, True)
        self.assertEqual(config['testing'].SQLALCHEMY_TRACK_MODIFICATIONS, False)

if __name__ == '__main__':
    unittest.main()

