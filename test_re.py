"""Testing behavior of python regular expressions"""
import re


def _re_search(needle, haystack):
    """helper function wraps access to re.MatchObject instance"""
    m = re.search(needle, haystack)
    if m is None:
        return ""
    return m.group(1)



def test_escape_chars():
    yes_match = "test = test"
    no_match = "test= test"
    expected_match = "test"

    # simplest case: regular string, slashes combine with following char
    assert _re_search("\s+=\s+(\S+)", yes_match) == expected_match
    assert _re_search("\s+=\s+(\S+)", no_match) == ""
    # "raw" string version of above, should have the same effect
    # I think the docs recommend using this.
    assert _re_search(r"\s+=\s+(\S+)", yes_match) == expected_match
    assert _re_search(r"\s+=\s+(\S+)", no_match) == ""
    # "escaping" the slashes by using a double should have no additional effect
    assert _re_search("\\s+=\\s+(\\S+)", yes_match) == expected_match
    assert _re_search("\\s+=\\s+(\\S+)", no_match) == ""
    # escaping slashes and "raw" string don't play nice and the slashes no longer
    # combine with the following char to acquire special meaning
    assert _re_search(r"\\s+=\\s+(\\S+)", yes_match) == ""
    assert _re_search(r"\\s+=\\s+(\\S+)", no_match) == ""
