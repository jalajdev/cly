#    Copyright 2021 Jalaj Kumar
#    This file is part of cly.

#    cly is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    cly is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.

#    You should have received a copy of the GNU Lesser General Public License
#    along with cly.  If not, see <https://www.gnu.org/licenses/>

import unittest
from cly.parsers import Parser
from cly.errors import InvalidShortName, InvalidLongName


class StylesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        return super().setUp()

    def test_empty_long_name(self):

        # Empty Long name
        with self.assertRaises(ValueError):
            self.parser.add_argument("", "", dest="dest")

    def test_empty_short_name(self):

        # Empty short name
        with self.assertRaises(ValueError):
            self.parser.add_argument("--abcd", "", short_name="", dest="dest")

    def test_hyphen_is_valid_in_long_name(self):

        # Long name with '-' must not count as special character
        try:
            self.parser.add_argument("--ab-cd", "", dest="dest")
        except Exception:
            self.assertTrue(False)

    def test_hyphen_is_valid_in_short_name(self):

        # Short name with '-' must not count as special character
        try:
            self.parser.add_argument("--abcd", "", short_name="-c", dest="dest")
        except Exception:
            self.assertTrue(False)


# The above tests should also pass with strict mode
class StrictModeStylesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser(strict_mode=True)
        return super().setUp()

    def test_empty_long_name(self):

        # Empty Long name
        with self.assertRaises(ValueError):
            self.parser.add_argument("", "", dest="dest")

    def test_empty_short_name(self):

        # Empty short name
        with self.assertRaises(ValueError):
            self.parser.add_argument("--abcd", "", short_name="", dest="dest")

    def test_special_char_in_long_name(self):

        # Long name with special character
        with self.assertRaises(InvalidLongName):
            self.parser.add_argument("--$#as", "", dest="dest")

    def test_special_char_in_short_name(self):

        # Short name with special character
        with self.assertRaises(InvalidShortName):
            self.parser.add_argument("--abcd", "", short_name="-&", dest="dest")

    def test_hyphen_is_valid_in_long_name(self):

        # Long name with '-' must not count as special character
        try:
            self.parser.add_argument("--ab-cd", "", dest="dest")
        except Exception:
            self.assertTrue(False)

    def test_hyphen_is_valid_in_short_name(self):

        # Short name with '-' must not count as special character
        try:
            self.parser.add_argument("--abcd", "", short_name="-c", dest="dest")
        except Exception:
            self.assertTrue(False)

    def test_long_name_starts_with_double_hyphen(self):

        # Long name starting with something other than `--`.
        with self.assertRaises(InvalidLongName):
            self.parser.add_argument("abcd", "", short_name="-b", dest="dest")

    def test_short_name_starts_with_hyphen(self):

        # Short name starting with something other than `-`.
        with self.assertRaises(InvalidShortName):
            self.parser.add_argument("--abcd", "", short_name="cb", dest="dest")

    def test_fixed_length_short_name(self):

        # Short name too long.
        with self.assertRaises(InvalidShortName):
            self.parser.add_argument("--abcd", "", short_name="-cb", dest="dest")


class FunctionalityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        return super().setUp()

    def test_redundancy_error_in_long_name(self):
        self.parser.add_argument("--name1", "", dest="dest")
        with self.assertRaises(InvalidLongName):
            self.parser.add_argument("--name1", "", dest="dest")

    def test_redundancy_error_in_short_name(self):
        self.parser.add_argument("--name1", "", short_name="-n", dest="dest")
        with self.assertRaises(InvalidShortName):
            self.parser.add_argument("--name2", "", short_name="-n", dest="dest")
