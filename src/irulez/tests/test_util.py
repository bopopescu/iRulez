import unittest
import src.irulez.util as util
import src.irulez.constants as constants


class TestIsArduinoTopic(unittest.TestCase):
    def test_empty_string(self):
        result = util.is_arduino_topic('')
        self.assertFalse(result)

    def test_valid_string(self):
        result = util.is_arduino_topic(constants.arduinoTopic + '/')
        self.assertTrue(result)

    def test_invalid_string(self):
        result = util.is_arduino_topic('blabla ')
        self.assertFalse(result)

    def test_not_startswith_arduino_topic(self):
        result = util.is_arduino_topic('blabla ' + constants.arduinoTopic)
        self.assertFalse(result)

    def test_none(self):
        result = util.is_arduino_topic(None)
        self.assertFalse(result)


class TestIsArduinoActionTopic(unittest.TestCase):
    def test_empty_string(self):
        self.assertFalse(util.is_arduino_action_topic(''))


if __name__ == '__main__':
    unittest.main(verbosity=2)