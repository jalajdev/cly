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


class TestArgMethodRegExps(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        return super().setUp()

    def test_basic_sample(self):
        arg = self.parser.add_arg("--long-name -s [description]")
        self.assertEquals(arg.long_name, "--long-name")
        self.assertEquals(arg.short_name, "-s")
        self.assertEquals(arg.description, "description")
        self.assertEquals(arg.required, True)
        self.assertEquals(arg.indefinite, False)

    def test_ommitted_short_name(self):
        arg = self.parser.add_arg("--long-name [description]")
        self.assertEquals(arg.long_name, "--long-name")
        self.assertEquals(arg.short_name, None)
        self.assertEquals(arg.description, "description")
        self.assertEquals(arg.required, True)
        self.assertEquals(arg.indefinite, False)

    def test_complex_description(self):
        arg = self.parser.add_arg(
            "--long-name -s "
            "[This is a big description, with \\[brackets\\] and spaces]"
        )
        self.assertEquals(arg.long_name, "--long-name")
        self.assertEquals(arg.short_name, "-s")
        self.assertEquals(
            arg.description, "This is a big description, with [brackets] and spaces"
        )
        self.assertEquals(arg.required, True)
        self.assertEquals(arg.indefinite, False)

    def test_required_parameter(self):
        arg = self.parser.add_arg("--long-name -s [description], False")
        self.assertEquals(arg.long_name, "--long-name")
        self.assertEquals(arg.short_name, "-s")
        self.assertEquals(arg.description, "description")
        self.assertEquals(arg.required, False)
        self.assertEquals(arg.indefinite, False)

    def test_required_parameter_case_insensitive(self):
        arg = self.parser.add_arg("--long-name -s [description], false")
        self.assertEquals(arg.indefinite, False)

    def test_indefinite_parameter(self):
        arg = self.parser.add_arg("--long-name -s [description], true, True")
        self.assertEquals(arg.long_name, "--long-name")
        self.assertEquals(arg.short_name, "-s")
        self.assertEquals(arg.description, "description")
        self.assertEquals(arg.required, True)
        self.assertEquals(arg.indefinite, True)

    def test_indefinite_parameter_case_insensitive(self):
        arg = self.parser.add_arg("--long-name -s [description], true, true")
        self.assertEquals(arg.indefinite, True)
