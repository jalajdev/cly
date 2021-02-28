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
from typing import Any, Union
from dataclasses import dataclass


@dataclass
class Argument:
    """
    The base data class to represent an argument
    """

    long_name: str
    description: str
    dest: str
    short_name: Union[str, None] = None
    metavar: Union[str, None] = None
    required: bool = True
    indefinite: bool = False

    # This is the value of the argument as supplied by the user
    # It will be set once parsing is complete.
    value: Any = None


@dataclass
class Flag:
    """
    The base data class to represent an argument
    """

    long_name: str
    description: str
    dest: str
    short_name: Union[str, None] = None
    metavar: Union[str, None] = None
    value: bool = False


def gen_help(
    inst: Union[Argument, Flag], left_width: int = 0, right_width: int = 0
) -> str:
    """
    Generates help for a given instance of `Argument` or `Flag`.
    The help is generated in two columns:

    - The left column is the long-name and short-name of the given flag
    or argument.
    - The right column is its description.
    """

    left_width = round(left_width or os.get_terminal_size().columns * 0.3)
    right_width = round(
        right_width or (os.get_terminal_size().columns - left_width - 2)
    )

    help_str = ""
    s_name = (inst.short_name and (", " + inst.short_name)) or ""
    left_column = inst.long_name + s_name
    right_column = inst.description

    if type(inst) == Argument and inst.metavar:
        if inst.indefinite:
            left_column += (
                f"  <{inst.metavar}1> <{inst.metavar}2> ... <{inst.metavar}n>"
            )
        else:
            left_column += f" <{inst.metavar}>"

    while left_column != "" or right_column != "":
        # Handle left column
        if len(left_column) <= left_width:
            padding = (left_width - len(left_column)) * " "
            help_str += left_column + padding
            left_column = ""
        else:
            help_str += left_column[:left_width]
            left_column = left_column[left_width:]

        # A minimum padding of 2 spaces between left and
        # right column
        help_str += "  "

        # Handle right column
        if len(right_column) <= right_width:
            help_str += right_column
            right_column = ""
        else:
            help_str += right_column[:right_width]
            right_column = right_column[right_width:]

        # Next line
        help_str += "\n"

    return help_str
