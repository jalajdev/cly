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

import re
import sys
from cly.utils import Argument, Flag
from typing import Any, Dict, List, Union
from cly.errors import InvalidLongName, InvalidShortName


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
        self.registry: Dict[str, Argument] = {}

    def parse(self, args: List[str] = sys.argv[1:]) -> None:
        """
        This is the function that performs the actual parsing of
        the args and internally builds up a tree of parsed args.
        """

    def add_argument(
        self,
        long_name: str,
        description: str,
        dest: str,
        short_name: Union[str, None] = None,
        metavar: Union[str, None] = None,
        indefinite: bool = False,
        default: Any = None,
    ) -> Argument:
        """
        Add an argument to the parser registry.

        Args:

        - long_name: [str]
            The longer name of the argument. Generally of the form
            `--<actual-name>`. For example: $ tsc --project file.

        - dest: [str]
            The name that will be used to access the value of this
            argument later in your program.

        - description: [str]
            The text to show in help menus for this argument.

        - short_name: [str, default: None]
            The short name of the argument. Generally of the form
            `-<a-single-char>`. Example: $ tsc -p file.

        - metavar: [str, default: None]
            The name used to reference to his variable in help
            messages.

        - indefinite: [bool, default: False]
            Does this accept indefinite number of values?

        - default: [Any, default: None]
            The value that the argument takes if none is supplied by
            the user.

        Returns: An instance of the `Argument` class.

        Raises:

        - ValueError: If the values of the arguments `indefinite`
            and `data_type` are incompatible.
        """
        if not len(long_name) > 0 or (
            short_name is not None and not len(short_name) > 0
        ):
            raise ValueError("Short name and/or Long names can't be empty strings.")

        # Redundancy checks
        if long_name in self.registry:
            raise InvalidLongName(
                f"The long name '{long_name}' is redundant."
                " It has been registered already."
            )

        if short_name and short_name in self.registry:
            raise InvalidShortName(
                f"The long name '{short_name}' is redundant."
                " It has been registered already."
            )

        # Check style if srict mode is enabled
        if self._options["strict_mode"]:
            if not long_name.startswith("--"):
                raise InvalidLongName(
                    f"Expected long name ('{long_name}') to start with a `-`"
                )

            if not long_name.replace("-", "").isalnum():
                raise InvalidLongName(
                    "Long name must be an alphanumeric string with "
                    "the exception of `-`."
                )

            if short_name:
                if not short_name.startswith("-"):
                    raise InvalidShortName(
                        f"Expected short name ('{short_name}') to start with a `-`"
                    )
                if len(short_name) != 2:
                    raise InvalidShortName(
                        "Exepcted short name of lengh 1 but instead "
                        f"got short name of length {len(short_name)-1}."
                    )
                if not short_name.replace("-", "").isalnum():
                    raise InvalidShortName(
                        "Short name must be an alphanumeric character."
                    )

        _obj = Argument(
            long_name=long_name,
            description=description,
            short_name=short_name,
            metavar=metavar,
            dest=dest,
            required=default is None,
            indefinite=indefinite,
            value=default,
        )

        self.registry[long_name] = _obj
        if short_name:
            self.registry[short_name] = _obj

        return _obj

    def add_arg(self, spec: str, dest: str) -> Argument:
        """
        Shorthand for the function `add_argument`. Instead of all the
        different parameters, you can provide just a singe string
        consisting the specification of the argument.

        Args:

        - spec: [str]
            The string that specifies the whole specification.
            It must be of this format:

            `"<long-name> <short-name> [<description>], <metavar>, <required>,
            <indefinite>"`

            Please take special care of the spaces present and that
            description must be enclosed within brackets (`[]`). If
            you have brackets in your description, you can escape
            it using a backslash (`\\`), like this: `\\[` or `\\]`.
        """
        SPEC_RE = (
            "(?P<long_name>[a-zA-Z0-9\\-_]+)( (?P<short_name>[a-zA-Z0-9\\-_]+))? "
            "(?P<description>\\[.+(?<!\\\\)\\])(, (?P<metavar>[\w\\-_]+))?"  # noqa: W605
            "(, (?P<indefinite>[a-zA-Z]+)(, (?P<default>.+))?)?"
        )
        _spec = re.match(SPEC_RE, spec)
        if _spec is None:
            # The Regex didn't match, program should go over finer
            # detatils of the provided spec and pin-point the problem.

            # TODO
            raise Exception("Invalid spec provided")

        _spec = _spec.groupdict()

        # Fallsback to False by default
        _spec["indefinite"] = str(_spec.get("indefinite")).lower() == "true"

        _spec["description"] = (
            _spec.get("description", "[]")[1:-1]  # Remove the enclosing brackets
            # Replace escaped brackets with good ones
            .replace("\\[", "[").replace("\\]", "]")
        )

        return self.add_argument(**_spec, dest=dest)

    def add_flag(
        self,
        long_name: str,
        description: str,
        dest: str,
        short_name: Union[str, None] = None,
    ) -> Flag:
        """
        Add a flag to the parser registry. A flag is just like an
        argument, the only difference being that an argument can take
        any value but a flag doesn't accept any values, rather it is
        either present or not. Kind of a boolean.

        Args:

        - long_name: [str]
            The longer name of the flag. Generally of the form
            `--<actual-name>`. For example: $ git add --all.

        - description: [str]
            The text to show in help menus for this flag.

        - dest: [str]
            The name that will be used to access the value of this
            argument later in your program.

        - short_name: [str, default: None]
            The short name of the flag. Generally of the form
            `-<a-single-char>`. Example: $ git add -A.

        Returns: An instance of the `Flag` class.
        """
        if not len(long_name) > 0 or (
            short_name is not None and not len(short_name) > 0
        ):
            raise ValueError("Short name and/or Long names can't be empty strings.")

        # Redundancy checks
        if long_name in self.registry:
            raise InvalidLongName(
                f"The long name '{long_name}' is redundant."
                " It has been registered already."
            )

        if short_name and short_name in self.registry:
            raise InvalidShortName(
                f"The long name '{short_name}' is redundant."
                " It has been registered already."
            )

        # Check style if srict mode is enabled
        if self._options["strict_mode"]:
            if not long_name.startswith("--"):
                raise InvalidLongName(
                    f"Expected long name ('{long_name}') to start with a `-`"
                )

            if not long_name.replace("-", "").isalnum():
                raise InvalidLongName(
                    "Long name must be an alphanumeric string with "
                    "the exception of `-`."
                )

            if short_name:
                if not short_name.startswith("-"):
                    raise InvalidShortName(
                        f"Expected short name ('{short_name}') to start with a `-`"
                    )
                if len(short_name) != 2:
                    raise InvalidShortName(
                        "Exepcted short name of lengh 1 but instead "
                        f"got short name of length {len(short_name)-1}."
                    )
                if not short_name.replace("-", "").isalnum():
                    raise InvalidShortName(
                        "Short name must be an alphanumeric character."
                    )

        _obj = Flag(
            long_name=long_name,
            description=description,
            short_name=short_name,
            dest=dest,
        )

        self.registry[long_name] = _obj
        if short_name:
            self.registry[short_name] = _obj

        return _obj

    def flag(self, spec: str, dest: str) -> Flag:
        """
        Shorthand for the function `add_flag`. Instead of all the
        different parameters, you can provide just a singe string
        consisting the specification of the argument.

        Args:

        - spec: [str]
            The string that specifies the whole specification.
            It must be of this format:

            `"<long-name> <short-name> [<description>]"`

            Please take special care of the spaces present and that
            description must be enclosed within brackets (`[]`). If
            you have brackets in your description, you can escape
            it using a backslash (`\\`), like this: `\\[` or `\\]`.
        """
        SPEC_RE = (
            "(?P<long_name>[a-zA-Z0-9\\-_]+)( (?P<short_name>[a-zA-Z0-9\\-_]+))? "
            "(?P<description>\\[.+(?<!\\\\)\\])"
        )
        _spec = re.match(SPEC_RE, spec)
        if _spec is None:
            # The Regex didn't match, program should go over finer
            # detatils of the provided spec and pin-point the problem.

            # TODO
            raise Exception("Invalid spec provided")

        _spec = _spec.groupdict()

        _spec["description"] = (
            _spec.get("description", "[]")[1:-1]  # Remove the enclosing brackets
            # Replace escaped brackets with good ones
            .replace("\\[", "[").replace("\\]", "]")
        )

        return self.add_flag(**_spec, dest=dest)
