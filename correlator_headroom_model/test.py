import unittest

from .model import HeadroomModel, Scale, Limit

# cells, exception, R, values
TESTS = [
    [[Scale(1)], True, None, None],
    [[Limit(1)], True, None, None],
    [[Limit(1), Scale(10)], True, None, None],
    [[Limit(10), Scale(2), Limit(1), Limit(2)], False, 0.5, [0.5, 0.5, 1, 1, 1]],
    [[Limit(0.1), Scale(2), Limit(1), Limit(2)], False, 0.1, [0.1, 0.1, 0.2, 0.2, 0.2]],
    [[Limit(10), Scale(2), Limit(1), Limit(0.2)], False, 0.1, [0.1, 0.1, 0.2, 0.2, 0.2]],
    [[Limit(10), Scale(0.5), Limit(1), Limit(0.2)], False, 0.4, [0.4, 0.4, 0.2, 0.2, 0.2]],
]


class HeadroomModelTest(unittest.TestCase):

    def test_values(self):

        for cells, is_exception, R_ref, values_ref in TESTS:
            try:
                m = HeadroomModel(cells)
            except Exception as e:
                self.assertTrue(is_exception)
                continue
            self.assertEqual(m.R, R_ref)
            self.assertEqual(m.values, values_ref)


if __name__ == '__main__':
    unittest.main()