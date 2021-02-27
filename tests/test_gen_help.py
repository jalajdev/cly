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

import os
import unittest
from collections import namedtuple
from unittest.mock import MagicMock
from cly.utils import Argument, Flag, gen_help


class TestGenHelpFunction(unittest.TestCase):
    def test_gen_help_argument(self):

        # A very basic test with the Argument class
        long_name = "--name"
        short_name = "-n"
        description = "Some good description"
        self.assertEqual(
            gen_help(
                Argument(
                    long_name=long_name, short_name=short_name, description=description
                ),
                len(long_name) + len(short_name) + 2,
                len(description),
            ),
            "--name, -n  Some good description\n",
        )

    def test_gen_help_flag(self):

        # The same basic test with the Flag class
        long_name = "--name"
        short_name = "-n"
        description = "Some good description"
        self.assertEqual(
            gen_help(
                Flag(
                    long_name=long_name, short_name=short_name, description=description
                ),
                len(long_name) + len(short_name) + 2,
                len(description),
            ),
            "--name, -n  Some good description\n",
        )

    def test_omitted_short_name(self):
        # Tests for correct help string for Arguments/Flag without a
        # short name
        long_name = "--name"
        description = "Some good description"
        self.assertEqual(
            gen_help(
                Argument(long_name=long_name, description=description),
                len(long_name),
                len(description),
            ),
            "--name  Some good description\n",
        )
        self.assertEqual(
            gen_help(
                Flag(long_name=long_name, description=description),
                len(long_name),
                len(description),
            ),
            "--name  Some good description\n",
        )

    def test_padding(self):
        # Tests that correct padding is inserted between left and right
        # column of the final generated help
        long_name = "--name"
        short_name = "-n"
        description = "Some good description"
        extra_padding = 10
        self.assertEqual(
            gen_help(
                Argument(
                    long_name=long_name, short_name=short_name, description=description
                ),
                len(long_name) + len(short_name) + 2 + extra_padding,
                len(description),
            ),
            f"--name, -n{extra_padding*' '}  Some good description\n",
        )

    def test_right_column_word_wrap(self):
        # Tests that right column is wrapped at the right place and
        # that the final string is not longer than expected
        long_name = "--name"
        short_name = "-n"
        description = (
            "Some good description that is going to be very big"
            " and will not fit in one line"
        )
        self.assertEqual(
            gen_help(
                Argument(
                    long_name=long_name, short_name=short_name, description=description
                ),
                len(long_name) + len(short_name) + 2,
                20,  # Any arbitrary number
            ),
            (
                "--name, -n  Some good descriptio\n"
                "            n that is going to b\n"
                "            e very big and will \n"
                "            not fit in one line\n"
            ),
        )

    def test_left_column_word_wrap(self):
        # Tests that left column is wrapped at the right place and
        # that the final string is not longer than expected
        long_name = "--very-big-long-name"
        short_name = "-n"
        description = (
            "Some good description that is going to be very big"
            " and will not fit in one line"
        )
        self.assertEqual(
            gen_help(
                Argument(
                    long_name=long_name, short_name=short_name, description=description
                ),
                12,
                20,
            ),
            (
                # This looks ugly but in practice, no one's going to
                # have a screen just 34 characters wide and no user
                # friendly program will have an argument that big.
                "--very-big-l  Some good descriptio\n"
                "ong-name, -n  n that is going to b\n"
                "              e very big and will \n"
                "              not fit in one line\n"
            ),
        )

    def test_decimals_rounded_off(self):
        # Tests that decimal widths are rounded off and the
        # padding is still correct
        long_name = "--very-big-long-name"
        short_name = "-n"
        description = (
            "Some good description that is going to be very big"
            " and will not fit in one line"
        )
        self.assertEqual(
            gen_help(
                Argument(
                    long_name=long_name, short_name=short_name, description=description
                ),
                12.4,
                19.8,
            ),
            (
                "--very-big-l  Some good descriptio\n"
                "ong-name, -n  n that is going to b\n"
                "              e very big and will \n"
                "              not fit in one line\n"
            ),
        )

    def test_default_parameters(self):
        # Tests that left column is wrapped at the right place and
        # that the final string is not longer than expected

        os.get_terminal_size = MagicMock(
            return_value=namedtuple("terminal_size", ["columns", "lines"])(50, 12)
        )

        long_name = "--very-big-long-name"
        short_name = "-n"
        description = (
            "Some good description that is going to be very big"
            " and will not fit in one line"
        )
        self.assertEqual(
            gen_help(
                Argument(
                    long_name=long_name, short_name=short_name, description=description
                ),
            ),
            (
                "--very-big-long  Some good description that is goi\n"
                "-name, -n        ng to be very big and will not fi\n"
                "                 t in one line\n"
            ),
        )

    def test_with_metavar(self):
        long_name = "--file"
        short_name = "-f"
        description = (
            "Some good description that is going to be very big"
            " and will not fit in one line"
        )
        self.assertEqual(
            gen_help(
                Argument(
                    long_name=long_name,
                    short_name=short_name,
                    description=description,
                    metavar="filename",
                ),
                25,
                40
            ),
            (
                "--file, -f <filename>      Some good description that is going to b\n"
                "                           e very big and will not fit in one line\n"
            ),
        )

    def test_indefinite_with_metavar(self):
        long_name = "--file"
        short_name = "-f"
        description = (
            "Some good description that is going to be very big"
            " and will not fit in one line"
        )
        self.assertEqual(
            gen_help(
                Argument(
                    long_name=long_name,
                    short_name=short_name,
                    description=description,
                    metavar="FILE",
                    indefinite=True
                ),
                25,
                40
            ),
            (
                "--file, -f  <FILE1> <FILE  Some good description that is going to b\n"
                "2> ... <FILEn>             e very big and will not fit in one line\n"
            ),
        )
