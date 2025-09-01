"""Tests for list utilities."""

import pytest

from music_modify.custom_types.enums import PairIndex
from music_modify.utils.list_utils import (
    addValues,
    getUnique,
    remapMatchingSublistPairs,
    removeMatchingSublistPairs,
    removePairs,
    toPairs,
)


@pytest.mark.parametrize(
    ("text", "separator", "expected"),
    [
        pytest.param(
            "First, Second, Third", ",", ["First", "Second", "Third"], id="normal"
        ),
        pytest.param(
            "First, Second, Third, First",
            ",",
            ["First", "Second", "Third"],
            id="duplicate",
        ),
        pytest.param(
            "First; Second; ; Third; First",
            ";",
            ["First", "Second", "Third"],
            id="removes_empty",
        ),
    ],
)
def test_getUnique(text: str, separator: str, expected: list[str]) -> None:
    """Tests get unique with different text and separators."""
    assert getUnique(text, separator) == expected


@pytest.mark.parametrize(
    ("values", "separator", "expected"),
    [
        pytest.param(
            ["role1: Person1", "role2: Person2"],
            ": ",
            [["role1", "Person1"], ["role2", "Person2"]],
            id="normal",
        ),
        pytest.param(
            ["role1: Person1", "role2: Person2"], ".", [], id="no_pairs_with_sep"
        ),
        pytest.param(
            ["role1: Person1", "role2.Person2"],
            ": ",
            [["role1", "Person1"]],
            id="mixed_sep_with_colon",
        ),
        pytest.param(
            ["role1: Person1", "role2.Person2"],
            ".",
            [["role2", "Person2"]],
            id="mixed_sep_with_dot",
        ),
        pytest.param(
            ["role1: Person1", "role2: Person2: another"],
            ": ",
            [["role1", "Person1"], ["role2", "Person2: another"]],
            id="extra_sep",
        ),
    ],
)
def test_toPairs(values: list[str], separator: str, expected: list[list[str]]) -> None:
    """Test that lists of strings are converted into pairs."""
    assert toPairs(values, separator) == expected


@pytest.mark.parametrize(
    ("new", "original", "expected"),
    [
        pytest.param(
            ["Value 4"],
            ["Value 1", "Value 2", "Value 3"],
            ["Value 1", "Value 2", "Value 3", "Value 4"],
            id="str_list_normal_add",
        ),
        pytest.param(
            [["role3", "Person3"]],
            [["role1", "Person1"], ["role2", "Person2"]],
            [["role1", "Person1"], ["role2", "Person2"], ["role3", "Person3"]],
            id="nested_list_normal_add",
        ),
        pytest.param(
            ["Value 3", "Value 4"],
            ["Value 1", "Value 2", "Value 3"],
            ["Value 1", "Value 2", "Value 3", "Value 4"],
            id="str_list_duplicate_not_added",
        ),
        pytest.param(
            [["role1", "Person1"], ["role3", "Person3"]],
            [["role1", "Person1"], ["role2", "Person2"]],
            [["role1", "Person1"], ["role2", "Person2"], ["role3", "Person3"]],
            id="nested_list_duplicate_not_added",
        ),
        pytest.param(
            None,
            [1, 2, 3],
            [1, 2, 3],
            id="new_is_None",
        ),
        pytest.param(
            [],
            [1, 2, 3],
            [1, 2, 3],
            id="new_is_empty",
        ),
    ],
)
def test_addValues[T](
    new: list[T] | None, original: list[T], expected: list[T]
) -> None:
    """Tests the addValues function with various scenarios."""
    assert addValues(new, original) == expected


@pytest.mark.parametrize(
    ("pairs", "original", "expected"),
    [
        pytest.param(
            {("role1", "Person1"), ("role2", "Person2")},
            [["role1", "Person1"], ["role2", "Person2"], ["role3", "Person3"]],
            [["role3", "Person3"]],
            id="normal_with_values",
        ),
        pytest.param(
            set(),
            [["role1", "Person1"], ["role2", "Person2"], ["role3", "Person3"]],
            [["role1", "Person1"], ["role2", "Person2"], ["role3", "Person3"]],
            id="normal_no_remove_values",
        ),
        pytest.param(
            {("role1", "Person1"), ("role2", "Person2")},
            [["role3", "Person3"], ["role4", "Person4"], ["role5", "Person5"]],
            [["role3", "Person3"], ["role4", "Person4"], ["role5", "Person5"]],
            id="values_not_present",
        ),
    ],
)
def test_removePairs(
    pairs: set[tuple[str, ...]], original: list[list[str]], expected: list[list[str]]
) -> None:
    """Tests that removing pairs works with various scenarios."""
    assert removePairs(pairs, original) == expected


_original_list = [
    ["role1", "Person1"],
    ["role1", "Person2"],
    ["role2", "Person3"],
    ["role3", "Person2"],
]


@pytest.mark.parametrize(
    ("remove_values", "original", "index", "expected"),
    [
        pytest.param(
            {"role1"},
            _original_list,
            PairIndex.Role.value,
            [["role2", "Person3"], ["role3", "Person2"]],
            id="remove_role1_matching",
        ),
        pytest.param(
            {"Person2"},
            _original_list,
            PairIndex.Person.value,
            [["role1", "Person1"], ["role2", "Person3"]],
            id="remove_person2_matching",
        ),
        pytest.param(
            set(),
            _original_list,
            PairIndex.Role.value,
            _original_list,
            id="empty_set_role_index_no_op",
        ),
        pytest.param(
            set(),
            _original_list,
            PairIndex.Person.value,
            _original_list,
            id="empty_set_person_index_no_op",
        ),
        pytest.param(
            {"role1"},
            _original_list,
            len(PairIndex) + 1,
            _original_list,
            id="invalid_high_index_no_op",
        ),
        pytest.param(
            {"role1"},
            _original_list,
            -1,
            _original_list,
            id="invalid_low_index_no_op",
        ),
        pytest.param(
            {"Person2"},
            _original_list,
            PairIndex.Role.value,
            _original_list,
            id="not_present_role_no_removal",
        ),
        pytest.param(
            {"role1"},
            _original_list,
            PairIndex.Person.value,
            _original_list,
            id="not_present_person_no_removal",
        ),
    ],
)
def test_removeMatchingSublistPairs(
    remove_values: set[str],
    original: list[list[str]],
    index: int,
    expected: list[list[str]],
) -> None:
    """Test that removing sublist pairs works correctly under various conditions.

    Also ensures that the original lists aren't changed.
    """
    original_before_change = list(original)
    assert removeMatchingSublistPairs(remove_values, original, index) == expected
    assert original == original_before_change


@pytest.mark.parametrize(
    ("replacements", "original", "index", "expected"),
    [
        pytest.param(
            {"role1": "role_new"},
            _original_list,
            PairIndex.Role.value,
            [
                ["role_new", "Person1"],
                ["role_new", "Person2"],
                ["role2", "Person3"],
                ["role3", "Person2"],
            ],
            id="remap_role_normal",
        ),
        pytest.param(
            {"Person1": "Person New", "Person2": "Another Person"},
            _original_list,
            PairIndex.Person.value,
            [
                ["role1", "Person New"],
                ["role1", "Another Person"],
                ["role2", "Person3"],
                ["role3", "Another Person"],
            ],
            id="remap_person_normal",
        ),
        pytest.param(
            {"role1": "role_new"},
            _original_list,
            PairIndex.Person.value,
            _original_list,
            id="not_present_person_no_removal",
        ),
        pytest.param(
            {"Person1": "Person New", "Person2": "Another Person"},
            _original_list,
            PairIndex.Role.value,
            _original_list,
            id="not_present_role_no_removal",
        ),
        pytest.param(
            {},
            _original_list,
            PairIndex.Role.value,
            _original_list,
            id="empty_dict_role_index_no_op",
        ),
        pytest.param(
            {},
            _original_list,
            PairIndex.Person.value,
            _original_list,
            id="empty_dict_role_index_no_op",
        ),
        pytest.param(
            {"role1": "role_new"},
            _original_list,
            len(PairIndex) + 1,
            _original_list,
            id="invalid_high_index_no_op",
        ),
        pytest.param(
            {"role1": "role_new"},
            _original_list,
            -1,
            _original_list,
            id="invalid_low_index_no_op",
        ),
    ],
)
def test_remapMatchingSublistPairs(
    replacements: dict[str, str],
    original: list[list[str]],
    index: int,
    expected: list[list[str]],
) -> None:
    """Test that remapping sublist pairs works correctly under various conditions.

    Also ensures that the original lists aren't changed.
    """
    original_before_change = list(original)
    assert remapMatchingSublistPairs(replacements, original, index) == expected
    assert original == original_before_change
