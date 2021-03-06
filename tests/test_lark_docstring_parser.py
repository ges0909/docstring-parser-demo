import pytest

from src.lark_docstring_parser import DocstringParser, Docstring


def assert_doctsring(docstring: Docstring):
    assert docstring.summary == "Summary line."
    assert docstring.description == "Extended description of function. 2nd line. 3rd line."
    assert docstring.args == [
        ("arg1", None, "Description of arg1"),
        ("arg2", "str", "Description of arg2"),
        ("arg3", None, "The [JMESpath](https://jmespath.org) query."),
        ("*args", None, "variable length argument list"),
        ("**kwargs", None, "arbitrary keyword arguments"),
    ]
    assert docstring.returns == ("bool", "Description of return value")
    assert docstring.yields is None
    assert docstring.raises == [
        (
            "AttributeError",
            "The ``Raises`` section is a list of all exceptions that are relevant to the interface.",
        ),
        (
            "ValueError",
            "If `arg2` is equal to `arg1`.",
        ),
    ]
    assert docstring.alias == "whateveryouwanttocall"
    assert (
        docstring.examples
        == "Examples should be written in doctest format, and should illustrate how to use the function."
        " >>> a=1 >>> b=2 >>> func(a,b) True"
    )


@pytest.fixture(scope="module")
def parser():
    return DocstringParser()


@pytest.mark.repeat(1)
def test_parse_google_style(benchmark):
    """Summary line.

    Extended description of function.
    2nd line.
    3rd line.

    Args:
        arg1: Description of arg1
        arg2 (str): Description of arg2
        arg3: The [JMESpath](https://jmespath.org)
            query.
        *args: variable length argument list
        **kwargs: arbitrary keyword arguments

    Returns:
        bool: Description of return value

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `arg2` is equal to `arg1`.

    Alias:
        What ever you want to call

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> a=1
        >>> b=2
        >>> func(a,b)
        True

    """

    def parse(text):
        parser = DocstringParser()
        return parser.parse(text=text)

    # docstring, error = parse(text=google_sample)
    docstring, error = benchmark(parse, text=test_parse_google_style.__doc__)

    assert error is None, error
    assert docstring is not None

    assert_doctsring(docstring)


@pytest.mark.repeat(1)
def test_parse_google_style_initialized_parser(benchmark, parser):
    """Summary line.

    Extended description of function.
    2nd line.
    3rd line.

    Args:
        arg1: Description of arg1
        arg2 (str): Description of arg2
        arg3: The [JMESpath](https://jmespath.org)
            query.
        *args: variable length argument list
        **kwargs: arbitrary keyword arguments

    Returns:
        bool: Description of return value

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `arg2` is equal to `arg1`.

    Alias:
        What ever you want to call

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> a=1
        >>> b=2
        >>> func(a,b)
        True

    """
    # docstring, error = parser.parse(text=google_sample)
    docstring, error = benchmark(parser.parse, text=test_parse_google_style_initialized_parser.__doc__)

    assert error is None, error
    assert docstring is not None

    assert_doctsring(docstring)


def test_summary(parser):
    summary = r"""Summary line."""
    docstring, error = parser.parse(text=summary)

    assert error is None, error
    assert docstring is not None


def test_summary_newline(parser):
    summary = r"""Summary line.
"""
    docstring, error = parser.parse(text=summary)

    assert error is None, error
    assert docstring is not None
