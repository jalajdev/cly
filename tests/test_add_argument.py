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


class AddArgumentMethodStylesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        return super().setUp()

    def test_empty_long_name(self):

        # Empty Long name
        with self.assertRaises(ValueError):
            self.parser.add_argument("", "")

    def test_empty_short_name(self):

        # Empty short name
        with self.assertRaises(ValueError):
            self.parser.add_argument("abcd", "", short_name="")

    def test_special_char_in_long_name(self):

        # Long name with special character
        with self.assertRaises(ValueError):
            self.parser.add_argument("$#as", "")

    def test_special_char_in_short_name(self):

        # Short name with special character
        with self.assertRaises(ValueError):
            self.parser.add_argument("abcd", "", "^&")

    def test_hyphen_is_valid_in_long_name(self):

        # Long name with '-' must not count as special character
        try:
            self.parser.add_argument("--ab-cd", "")
        except ValueError:
            self.assertTrue(False)

    def test_hyphen_is_valid_in_short_name(self):

        # Short name with '-' must not count as special character
        try:
            self.parser.add_argument("--abcd", "", short_name="-c")
        except ValueError:
            self.assertTrue(False)
