# SPDX-License-Identifier: Apache-2.0
import unittest
from vex.enrich_metadata import Version, parse_version


class TestVersion(unittest.TestCase):
    def test_comparisons(self):
        versions = [
            Version(1, 0, 0, 'alpha'),
            Version(1, 0,0),
            Version(1, 2, 0),
            Version(1, 2, 3)
        ]
        for i in range(len(versions) - 1):
            self.assertLess(versions[i], versions[i + 1])
            self.assertGreater(versions[i + 1], versions[i])

    def test_parse_version(self):
        cases: list[InputAndVersion] = [
            InputAndVersion('1.2.3', 1, 2, 3),
            InputAndVersion('1.2.3-alpha', 1, 2, 3, 'alpha'),
            InputAndVersion('2.0', 2, 0)
        ]
        for case in cases:
            v = parse_version(case.input_str)
            self.assertIsInstance(v, Version)
            self.assertEqual(v.major, case.major)
            self.assertEqual(v.minor, case.minor)
            self.assertEqual(v.patch, case.patch)
            self.assertEqual(v.pre_release, case.pre_release)


class InputAndVersion(Version):
    def __init__(self, input_str: str, *args):
        super().__init__(*args)
        self.input_str = input_str


if __name__ == '__main__':
    unittest.main()
