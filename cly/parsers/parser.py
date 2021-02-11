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

import sys
from typing import Any, List, Union
from dataclasses import dataclass


class Parser:
    def __init__(
        self,
        prog: str = sys.argv[0],
        desc: str = "",
        usage: str = "",
        help: str = "",
        help_flag: str = "-h, --help",
        allow_unknown_args: bool = False,
        strict_mode: bool = True,
    ) -> None:
        """
        The base class for parsing a given argument list and executing
        the tasks accordingly.

        Args:

        - prog: [str, default: sys.argv[0]]
            Name of the program. This is used to generate help messages
            and usage strings. Uses `sys.argv[0]` by default.

        - desc: [str, default: ""]
            Description of the program. Used in help strings along with
            other information.

        - usage: [str, default: ""]
            A string that describes the usage of the cli. If this is
            left empty, then one will be generated automatically when
            needed.

        - help: [str, default: ""]
            Help message to display when the user asks for it [See
            help_flag argument]. If it is left empty, the help
            message will be generated dynamically during runtime.

        - help_flag: [str, default: "-h, --help"]
            The flag that will trigger the dynamic generation and
            thereafter writing it to `stdout`. It must be of the form
            "<short-name>, <long-name>". For example: "-h, --help".

        - allow_unknown_args: [bool, default: False]
            Whether the program should silently ignore unknown
            arguments or not. By default, when an unknown argument is
            encountered an error will be printed to the console along
            with a message showing correct usage [The usage string].

        - strict_mode: [bool, default: True]
            Whether to use strict mode or not. In strict mode, the
            `long_name` of all arguments and flags *must* start with a
            `--` and all `short_name`s must start with a `-`. All short
            names can only be a single character alphanumeric string.

            Disabling `strict_mode` also disables some other functions.
            For example, when strict mode is enabled, the user can
            cluster multiple flags together. Clustering flags, allows
            user to simply type:

                $ your_script -abcd

            instead of:

                $ your_script -a -b -c -d

            Moreover, it _enforces_ a style in your program with which
            most users are already familiar.
        """
        self._options = {
            "prog": prog,
            "desc": desc,
            "usage": usage,
            "help": help,
            "help_flag": help_flag,
            "allow_unknown_args": allow_unknown_args,
            "strict_mode": strict_mode,
        }
        self.argtree = []
        self.registry: List = []

    def parse(self, args: List[str] = sys.argv[1:]) -> None:
        """
        This is the function that performs the actual parsing of
        the args and internally builds up a tree of parsed args.
        """

    def add_argument(
        self,
        long_name: str,
        description: str,
        short_name: Union[str, None] = None,
        required: bool = True,
        indefinite: bool = False,
        data_type: Union[list, tuple, str, int] = str,
        default: Any = None,
    ) -> None:
        """
        Add an argument to the parser registry.

        Args:

        - long_name: [str]
            The longer name of the argument. Generally of the form
            `--<actual-name>`. For example: $ git add --all.

        - short_name: [str, default: None]
            The short name of the argument. Generally of the form
            `-<a-single-char>`. Example: $ git add -A.

        - description: [str]
            The text to show in help menus for this argument.

        - required: [bool, default: True]
            Whether this argument is required.

        - indefinite: [bool, default: False]
            Does this accept indefinite number of values?

        - data_type: [Union[str, int, tuple, list], default: str]
            The data type to convert the provided value into. The
            only supported types are str, int, list and tuple. Note
            that list/tuple can be used only if `indefinite` is set
            to True

        - default: [Any, default: None]
            The value that the argument takes if none is supplied by
            the user. This argument will have effect only if `argument`
            is set to False.

        Returns: None

        Raises:

        - ValueError: If the values of the arguments `indefinite`
            and `data_type` are incompatible.
        """

        # Some basic checks
        if (data_type == tuple or data_type == list) and not indefinite:
            raise ValueError(
                "Invalid combination in argument. "
                + f"Cannot use data type {data_type} when indefinite is False."
            )

        if not len(long_name) > 0 or (
            short_name is not None and not len(short_name) > 0
        ):
            raise ValueError("Short name and Long names can't be empty strings.")

        if not long_name.replace("-", "").isalnum():
            raise ValueError(
                "Long name must be an alphanumeric string with " "the exception of `-`."
            )
        if short_name and not short_name.replace("-", "").isalnum():
            raise ValueError("Short name must be an alphanumeric character.")

        # Check style if srict mode is enabled
        if self._options["strict_mode"]:
            if not long_name.startswith("--"):
                raise ValueError(
                    f"Expected long name ('{long_name}') to start with a `-`"
                )

            if short_name:
                if not long_name.startswith("-"):
                    raise ValueError(
                        f"Expected short name ('{short_name}') to start with a `-`"
                    )
                if len(short_name) != 2:
                    raise ValueError(
                        "Exepcted short name of lengh 1 but instead "
                        f"got short name of length {len(short_name)-1}."
                    )

        self.registry.append(
            Argument(
                long_name,
                short_name,
                description,
                required,
                indefinite,
                data_type,
                (None if required else default),
            )
        )

    def arg(spec: str) -> None:
        """
        Shorthand for the function `add_argument`. Instead of all the
        different parameters, you can provide just a singe string
        consisting the specification of the argument.

        Args:

        - spec: [str]
            The string that specifies the whole specification.
            It must be of this format:

            `"<short-name> <long-name> [<description>] <required>
            <indefinite> <data_type>"`

            Please take special care of the spaces present and that
            description must be enclosed within brackets (`[]`). If
            you have brackets in your description, you can escape
            it using a backslash (`\\`), like this: `\\[` or `\\]`.
            Just like the `add_argument` function, the `required`,
            `indefinite` and `data_type` values are optional and
            have default values `True`, `False` and `str`
            respectively.
        """


@dataclass
class Argument:
    """
    The base data class to represent an argument
    """

    long_name: str
    short_name: str
    description: str
    required: bool = True
    indefinite: bool = False
    data_type: Union[list, tuple, str, int] = str

    # This is the value of the argumen as supplied by the user
    # It will be set once parsing is complete.
    value: Any = None
