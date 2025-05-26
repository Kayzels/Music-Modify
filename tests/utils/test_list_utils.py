from music_modify.utils.list_utils import (
    getUniqueOrdered,
    toPairs,
    addValues,
    removePairs,
    removeMatchingSublistPairs,
    remapMatchingSublistPairs,
)


def test_getUniqueOrdered():
    text = "First, Second, Third, First"
    separator = ","
    assert getUniqueOrdered(text, separator) == ["First", "Second", "Third"]


def test_toPairs():
    values = ["role1: Person1", "role2: Person2"]
    separator = ": "
    assert toPairs(values, separator) == [["role1", "Person1"], ["role2", "Person2"]]


def test_addValues():
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


def test_removePairs():
    pairs = {("role1", "Person1"), ("role2", "Person2")}
    original = [["role1", "Person1"], ["role2", "Person2"], ["role3", "Person3"]]
    assert removePairs(pairs, original) == [["role3", "Person3"]]


def test_removeMatchingSublistPairs():
    roles = {"role1"}
    people = {"Person2"}
    original = [
        ["role1", "Person1"],
        ["role1", "Person2"],
        ["role2", "Person3"],
        ["role3", "Person2"],
    ]
    assert removeMatchingSublistPairs(roles, original, 0) == [
        ["role2", "Person3"],
        ["role3", "Person2"],
    ]
    assert removeMatchingSublistPairs(people, original, 1) == [
        ["role1", "Person1"],
        ["role2", "Person3"],
    ]


def test_remapMatchingSublistPairs():
    role_replacements = {"role1": "role_new"}
    people_replacements = {"Person1": "Person_New", "Person2": "Another_Person"}
    original = [
        ["role1", "Person1"],
        ["role1", "Person2"],
        ["role2", "Person3"],
        ["role3", "Person2"],
    ]
    assert remapMatchingSublistPairs(role_replacements, original, 0) == [
        ["role_new", "Person1"],
        ["role_new", "Person2"],
        ["role2", "Person3"],
        ["role3", "Person2"],
    ]
    assert remapMatchingSublistPairs(people_replacements, original, 1) == [
        ["role1", "Person_New"],
        ["role1", "Another_Person"],
        ["role2", "Person3"],
        ["role3", "Another_Person"],
    ]

