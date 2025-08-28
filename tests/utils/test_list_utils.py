"""Tests for list utilities."""

from music_modify.custom_types.enums import PairIndex
from music_modify.utils.list_utils import (
    addValues,
    getUnique,
    remapMatchingSublistPairs,
    removeMatchingSublistPairs,
    removePairs,
    toPairs,
)


def test_getUnique_normal() -> None:
    """Test that when given a normal already ordered list, it returns it."""
    text = "First, Second, Third"
    separator = ","
    assert getUnique(text, separator) == ["First", "Second", "Third"]


def test_getUnique_duplicate() -> None:
    """Test that duplicates are removed from an already ordered list."""
    text = "First, Second, Third, First"
    separator = ","
    assert getUnique(text, separator) == ["First", "Second", "Third"]


def test_getUnique_removes_empty() -> None:
    """Test that empty strings are removed from an already ordered list."""
    text = "First; Second; ; Third; First"
    separator = ";"
    assert getUnique(text, separator) == ["First", "Second", "Third"]


def test_toPairs() -> None:
    """Test that lists of strings are converted into pairs."""
    values: list[str] = ["role1: Person1", "role2: Person2"]
    separator = ": "
    assert toPairs(values, separator) == [["role1", "Person1"], ["role2", "Person2"]]
    # If no pairs found, that are separated, should be empty
    assert toPairs(values, ".") == []
    values2: list[str] = ["role1: Person1", "role2.Person2"]
    assert toPairs(values2, separator) == [["role1", "Person1"]]
    assert toPairs(values2, ".") == [["role2", "Person2"]]
    values3 = ["role1: Person1", "role2: Person2: another"]
    assert toPairs(values3, ": ") == [
        ["role1", "Person1"],
        ["role2", "Person2: another"],
    ]


def test_addValues_normal() -> None:
    """Test that adding values to a list works."""
    original = ["Value 1", "Value 2", "Value 3"]
    new = ["Value 4"]
    assert addValues(new, original) == ["Value 1", "Value 2", "Value 3", "Value 4"]

    original = [["role1", "Person1"], ["role2", "Person2"]]
    new = [["role3", "Person3"]]
    assert addValues(new, original) == [
        ["role1", "Person1"],
        ["role2", "Person2"],
        ["role3", "Person3"],
    ]


def test_addValues_present_not_added() -> None:
    """Test that adding a value already present doesn't add it."""
    original = ["Value 1", "Value 2", "Value 3"]
    new = ["Value 3", "Value 4"]
    assert addValues(new, original) == ["Value 1", "Value 2", "Value 3", "Value 4"]

    original = [["role1", "Person1"], ["role2", "Person2"]]
    new = [["role1", "Person1"], ["role3", "Person3"]]
    assert addValues(new, original) == [
        ["role1", "Person1"],
        ["role2", "Person2"],
        ["role3", "Person3"],
    ]


def test_addValues_new_None() -> None:
    """Test that when new is None or empty, the original is returned."""
    original = [1, 2, 3]
    assert addValues(None, original) == [1, 2, 3]
    assert addValues([], original) == [1, 2, 3]


def test_removePairs_normal() -> None:
    """Test that removing pairs removes values that appear."""
    pairs = {("role1", "Person1"), ("role2", "Person2")}
    original = [["role1", "Person1"], ["role2", "Person2"], ["role3", "Person3"]]
    assert removePairs(pairs, original) == [["role3", "Person3"]]
    assert removePairs(set(), original) == original


def test_removePairs_none_in_list() -> None:
    """Test that removing pairs that don't exist doesn't do anything."""
    pairs = {("role1", "Person1"), ("role2", "Person2")}
    original = [["role3", "Person3"], ["role4", "Person4"], ["role5", "Person5"]]
    assert removePairs(pairs, original) == original


def test_removeMatchingSublistPairs_normal() -> None:
    """Test that removing pairs based on role or person removes all instances."""
    roles = {"role1"}
    people = {"Person2"}
    original = [
        ["role1", "Person1"],
        ["role1", "Person2"],
        ["role2", "Person3"],
        ["role3", "Person2"],
    ]
    assert removeMatchingSublistPairs(roles, original, PairIndex.Role.value) == [
        ["role2", "Person3"],
        ["role3", "Person2"],
    ]
    assert removeMatchingSublistPairs(people, original, PairIndex.Person.value) == [
        ["role1", "Person1"],
        ["role2", "Person3"],
    ]

    # Ensure the original lists aren't changed.
    assert removeMatchingSublistPairs(set(), original, PairIndex.Role.value) == original
    assert (
        removeMatchingSublistPairs(set(), original, PairIndex.Person.value) == original
    )
    assert removeMatchingSublistPairs(roles, original, 2) == original
    assert removeMatchingSublistPairs(roles, original, -1) == original


def test_removeMatchingSublistPairs_not_present() -> None:
    """Test that removing pairs doesn't remove when not present, or in other type."""
    roles = {"first"}
    people = {"second"}
    original = [["second", "first"], ["other", "other"]]

    assert removeMatchingSublistPairs(roles, original, PairIndex.Role.value) == original
    assert (
        removeMatchingSublistPairs(people, original, PairIndex.Person.value) == original
    )


def test_remapMatchingSublistPairs_normal() -> None:
    """Test that replacements change the correct values."""
    role_replacements = {"role1": "role_new"}
    people_replacements = {"Person1": "Person_New", "Person2": "Another_Person"}
    original = [
        ["role1", "Person1"],
        ["role1", "Person2"],
        ["role2", "Person3"],
        ["role3", "Person2"],
    ]
    assert remapMatchingSublistPairs(
        role_replacements,
        original,
        PairIndex.Role.value,
    ) == [
        ["role_new", "Person1"],
        ["role_new", "Person2"],
        ["role2", "Person3"],
        ["role3", "Person2"],
    ]
    assert remapMatchingSublistPairs(
        people_replacements,
        original,
        PairIndex.Person.value,
    ) == [
        ["role1", "Person_New"],
        ["role1", "Another_Person"],
        ["role2", "Person3"],
        ["role3", "Another_Person"],
    ]
    assert remapMatchingSublistPairs({}, original, PairIndex.Role.value) == original
    assert remapMatchingSublistPairs({}, original, PairIndex.Person.value) == original
    assert remapMatchingSublistPairs(role_replacements, original, 2) == original
    assert remapMatchingSublistPairs(people_replacements, original, -1) == original


def test_remapMatchingSublistPairs_not_present() -> None:
    """Test that replacements don't change values that aren't present."""
    role_replacements = {"role1": "role_new"}
    people_replacements = {"Person1": "Person_New", "Person2": "Another_Person"}
    original = [["role2", "Person New"], ["role3", "Person New"]]
    assert (
        remapMatchingSublistPairs(role_replacements, original, PairIndex.Role.value)
        == original
    )
    assert (
        remapMatchingSublistPairs(people_replacements, original, PairIndex.Person.value)
        == original
    )
