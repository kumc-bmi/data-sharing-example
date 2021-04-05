from all_questions import *
import unittest


class TestGenericApp(unittest.TestCase):
  def test_volume(self):
    self.assertAlmostEqual(cuboid(2),8)
    self.assertAlmostEqual(cuboid(1),1)
    self.assertAlmostEqual(cuboid(0),0)

  def test_input_value(self):
    self.assertRaises(TypeError, cuboid, True)

if __name__ == '__main__':
    unittest.main()