"""12/08/2016 my colleague Leela reported getting a weird error.

She was trying to perform an equivalent of the following string interpolation:
`" a {0}, b {1}".format(some_dict["key"], ["key2"])`

She had forgotten to type `some_dict` for the second argument of `format`.
However the error she got was unrelated to that. She was namely told that list
indices must be integers, not strings.

At the time I was pretty certain


Unfortunately I didn't get a chance to check her Python interpreter version, so
I have to test this in both 3 and 2.
"""
import pytest


def test_format_insert_list():
    """I think what Leela was indexing as a dictionary was in fact a list.

    This test clearly demonstrates that .format can handle raw lists as arguments.
    """
    tpl = "a {0}, b {1}"
    d = {4: 3}

    assert tpl.format(d[4], [3]) == 'a 3, b [3]'
    assert tpl.format(d[4], ["3"]) == "a 3, b ['3']"


def test_format_insert_list_str_indx():
    """Confirming that we should get the error Leela and I saw if we in fact
    index a list as if it were a dictionary.
    """
    tpl = "a {0}, b {1}"
    l = [2, 3]

    with pytest.raises(TypeError) as exc_info:
        assert tpl.format(l["4"], ["5"]) == 'a 3, b ["5"]'

    assert str(exc_info.value) == "list indices must be integers or slices, not str"
