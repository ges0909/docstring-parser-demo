import re
from typing import Optional

import pdoc
import pytest


def function_google_style(arg1: int, arg2: str, arg3: str) -> list:
    """Summary line.

    Extended description of function.

    Args:
        arg1 (int, default 5): Description of arg1
        arg2 (str): Description of arg2
        arg3 (str): The [JMESpath](https://jmespath.org) query.

    Returns:
        bool: Description of return value

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `arg2` is equal to `arg1`.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >> a=1
        >> b=2
        >> func(a,b)
        True

    Alias:
        Give the function an alias name.
    """


def test_pdoc3():
    modules = ["test_pdoc3_docstring_parser"]
    context = pdoc.Context()
    modules = [pdoc.Module(mod, context=context) for mod in modules]
    pdoc.link_inheritance(context)
    #
    for module in modules:
        for function in module.functions():
            na = function.name
            mo = function.module
            ob = function.obj
            do = function.docstring
            ih = function.inherits
            fd = function.funcdef()
            pa = function.params(annotate=True)
            ra = function.return_annotation()
            pass
        html = module.html()


# --


def get_alias(docstring: str) -> Optional[str]:
    lines = docstring.split("\n")
    lines = [line.strip() for line in lines if line]  # remove leading and trailing spaces in each line
    lines = [line for line in lines if line]  # remove empty lines
    for index, line in enumerate(lines):
        if match := re.search(pattern=r"Alias:\s*(.+)\s*", string=line):
            return match.group(1)
        elif _ := re.search(pattern=r"Alias:", string=line):
            if index < len(lines) - 1:
                return lines[index + 1]
            else:
                return None
    return None


@pytest.mark.parametrize(
    ("docstring",),
    (
        (r"""Alias: Give the function an alias name.""",),
        (r"""Alias:Give the function an alias name.""",),
        (r"""Alias:     Give the function an alias name.""",),
        (r"""Alias: Give the function an alias name.     """,),
        (r"""Alias:     Give the function an alias name.     """,),
        (r"""     Alias:     Give the function an alias name.     """,),
        (
            r"""
            Alias:     Give the function an alias name.     """,
        ),
        (
            r"""Alias:
            Give the function an alias name.""",
        ),
        (
            r"""Alias:
                Give the function an alias name.
                """,
        ),
        (
            r"""
                Alias:
                    Give the function an alias name.
                    """,
        ),
    ),
)
def test_alias(docstring: str):
    alias = get_alias(docstring=docstring)
    # match = re.search(pattern=r"Alias:\s*(\S+(?:\s+\S+)*)\s*", string=docstring)
    # alias = match.group(1)
    assert alias == "Give the function an alias name."


def test_docstring_alias(benchmark):
    # alias = get_alias(docstring=function_google_style.__doc__)
    alias = benchmark(get_alias, docstring=function_google_style.__doc__)
    assert alias == "Give the function an alias name."


def test_docstring_single_regex(benchmark):
    # match = re.search(pattern=r"Alias:\s*(\S+(?:\s+\S+)*)\s*", string=function_google_style.__doc__)
    match = benchmark(re.search, pattern=r"Alias:\s*(\S+(?:\s+\S+)*)\s*", string=function_google_style.__doc__)
    assert match is not None
    alias = match.group(1)
    assert alias == "Give the function an alias name."
    alias = alias.casefold()
    assert alias == "give the function an alias name."
    alias = re.sub(pattern=r"\s+", repl="", string=alias)
    assert alias == "givethefunctionanaliasname."


def test_docstring_single_regex_compile(benchmark):
    regex = re.compile(pattern=r"Alias:\s*(\S+(?:\s+\S+)*)\s*")
    # match = regex.search(string=function_google_style.__doc__)
    match = benchmark(regex.search, string=function_google_style.__doc__)
    assert match is not None
    alias = match.group(1)
    assert alias == "Give the function an alias name."
