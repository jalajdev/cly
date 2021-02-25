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


class TestFlagMethodRegExps(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        return super().setUp()

    def test_basic_sample(self):
        flg = self.parser.flag("--long-name -s [description]")
        self.assertEquals(flg.long_name, "--long-name")
        self.assertEquals(flg.short_name, "-s")
        self.assertEquals(flg.description, "description")

    def test_ommitted_short_name(self):
        flg = self.parser.flag("--long-name [description]")
        self.assertEquals(flg.long_name, "--long-name")
        self.assertEquals(flg.short_name, None)
        self.assertEquals(flg.description, "description")

    def test_complex_description(self):
        flg = self.parser.flag(
            "--long-name -s "
            "[This is a big description, with \\[brackets\\] and spaces]"
        )
        self.assertEquals(flg.long_name, "--long-name")
        self.assertEquals(flg.short_name, "-s")
        self.assertEquals(
            flg.description, "This is a big description, with [brackets] and spaces"
        )
