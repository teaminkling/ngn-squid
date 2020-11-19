"""The official Python >= 3.8 transpiler for the Squid narrative markup language!"""

from typing import List, Union

PREFIX_CHARACTERS: Collection[str] = " ->#!"
"""Characters that can be part of a prefix of a line."""


@dataclass
class Node:
    """Data representation of a node of information in a pseudo-abstract syntax tree."""

    mode: str
    """The mode of the node. TODO: Make this an enum since we know all the modes."""

    contents: Union[None, List[Node], str]
    """
    The contents of the node.
    
    Either this is a node composed of more nodes or it has a `str` value that makes sense given the mode.
    """


@dataclass
class Line:
    """Data representation of a line of text with a prefix and contents."""

    prefix: str
    """The prefix of the "command" unit. Can be empty (usually indicates a line break continuation)."""

    contents: str
    """The part after the prefix, stripped."""

    continuation: bool
    """Whether this line is a continuation of a previous one."""


class SquidSyntaxError(BaseException):
    """An indication of a syntax error found in the markup."""

    pass


def read_line(ast: Dict[str, Any], line_number: int, contents: str) -> Dict[str, Any]:
    return ast


def read_string(contents: str) -> Dict[str, Any]:
    ast: Dict[str, Any] = {}

    for index, line in enumerate(contents.split("\n")):
        read_line(ast, index + 1, line.rstrip())

    return ast

def combine_files(files: List[str]) -> str:
    # Function combines all the files in the manifest into a mega-string.

    # TODO: Consider that debugging might be a lot easier if the files are kept separate and instead the ASTs are
    #       combined.

    pass


def split_prefix_from_line(line_number: int, line: str) -> Optional[Tuple[str, str]]:
    # First ensure the line can actually be split or if it should just be ignored.

    if not line:
        return
    
    first_character: str = line[0]

    if len(line) == 1 and first_character != "#":
        # TODO: Pass through the file name and the 
        raise SyntaxError()

    prefix: str = ""
    contents: str = ""

    for index, character in enumerate(line):
        if character in PREFIX_CHARACTERS:
            prefix += character
        else:
            contents = line[index:].strip()
