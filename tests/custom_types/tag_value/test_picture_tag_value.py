"""Tests for PictureTagValue."""

import logging
from typing import Any, TypedDict

from mutagen import id3
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.tag_value.picture_tag_value import PictureTagValue


class _PictureParams(TypedDict, total=False):
    data: bytes
    mime: str
    picture_type: id3.PictureType
    desc: str
    salt: str | None
    join_character: str


@pytest.mark.parametrize(
    ("params", "expected_frame"),
    [
        pytest.param(
            {},
            id3.APIC(
                encoding=id3.Encoding.UTF8,
                mime="",
                type=id3.PictureType.COVER_FRONT,
                desc="",
                data=b"",
            ),
            id="default_values",
        ),
        pytest.param(
            {"salt": " "},
            id3.APIC(
                encoding=id3.Encoding.UTF8,
                mime="",
                type=id3.PictureType.COVER_FRONT,
                desc="",
                data=b"",
                salt=" ",
            ),
            id="salt_and_default",
        ),
        pytest.param(
            {"data": b"word"},
            id3.APIC(
                encoding=id3.Encoding.UTF8,
                mime="",
                type=id3.PictureType.COVER_FRONT,
                desc="",
                data=b"word",
            ),
            id="default_changed_data",
        ),
        pytest.param(
            {
                "mime": "image/jpeg",
                "desc": "Artist",
                "picture_type": id3.PictureType.LEAD_ARTIST,
            },
            id3.APIC(
                encoding=id3.Encoding.UTF8,
                mime="image/jpeg",
                type=id3.PictureType.LEAD_ARTIST,
                desc="Artist",
                data=b"",
            ),
            id="set_desc_mime_type",
        ),
    ],
)
def test_PictureTagValue_toId3Frame(
    params: _PictureParams, expected_frame: id3.Frame
) -> None:
    """Tests that ID3 frames are created correctly."""
    created_value = PictureTagValue(**params)
    created_frame = created_value.toId3Frame("APIC")
    assert created_frame == expected_frame


def test_PictureTagValue_toId3Frame_logs_when_wrong_id3_key(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests warning is raised when calling toId3Frame with a key other than APIC."""
    created_value = PictureTagValue()
    with caplog.at_level(logging.WARNING):
        _ = created_value.toId3Frame("TIT2")

    assert "Sent an unexpected id3 key for a PictureTagValue: TIT2." in caplog.text
    assert caplog.records[0].levelname == "WARNING"


@pytest.mark.parametrize(
    ("params", "expected"),
    [
        pytest.param(
            {},
            "Attached Picture: Cover Front",
            id="default_values",
        ),
        pytest.param(
            {"desc": "Word"},
            "Attached Picture: Cover Front (Word)",
            id="set_desc",
        ),
        pytest.param(
            {"picture_type": id3.PictureType.LEAD_ARTIST},
            "Attached Picture: Lead Artist",
            id="set_type",
        ),
        pytest.param(
            {"mime": "image/jpeg"},
            "Attached Picture: Cover Front (image/jpeg)",
            id="set_mime",
        ),
        pytest.param(
            {
                "mime": "image/jpeg",
                "desc": "Word",
            },
            "Attached Picture: Cover Front (Word, image/jpeg)",
            id="set_desc_mime",
        ),
        pytest.param(
            {
                "mime": "image/jpeg",
                "picture_type": id3.PictureType.LEAD_ARTIST,
            },
            "Attached Picture: Lead Artist (image/jpeg)",
            id="set_mime_type",
        ),
        pytest.param(
            {
                "picture_type": id3.PictureType.LEAD_ARTIST,
                "desc": "Artist",
            },
            "Attached Picture: Lead Artist (Artist)",
            id="set_desc_type",
        ),
        pytest.param(
            {
                "mime": "image/jpeg",
                "picture_type": id3.PictureType.LEAD_ARTIST,
                "desc": "Artist",
                "join_character": "; ",
            },
            "Attached Picture: Lead Artist (Artist; image/jpeg)",
            id="set_mime_type_desc",
        ),
    ],
)
def test_PictureTagValue_getDisplayValue(params: _PictureParams, expected: str) -> None:
    """Tests that the display value is calculated correctly."""
    created_value = PictureTagValue(**params)
    assert created_value.getDisplayValue() == expected


@pytest.mark.parametrize(
    ("params", "other", "expected_result"),
    [
        pytest.param({}, [], False, id="empty_list_not_equal"),
        pytest.param({}, "value", False, id="string_not_equal"),
        pytest.param({"data": b"value"}, b"value", False, id="same_bytes_not_others"),
        pytest.param({}, PictureTagValue(), True, id="same_with_defaults"),
        pytest.param(
            {"data": b"value"},
            PictureTagValue(b"value"),
            True,
            id="same_with_defaults_and_value",
        ),
        pytest.param(
            {"salt": " "},
            PictureTagValue(
                salt=" ",
            ),
            True,
            id="salt_and_default",
        ),
        pytest.param(
            {
                "mime": "image/jpeg",
                "desc": "Artist",
                "picture_type": id3.PictureType.LEAD_ARTIST,
            },
            PictureTagValue(
                mime="image/jpeg",
                picture_type=id3.PictureType.LEAD_ARTIST,
                desc="Artist",
            ),
            True,
            id="set_desc_mime_type",
        ),
        pytest.param(
            {
                "mime": "image/jpeg",
                "desc": "Artist",
                "picture_type": id3.PictureType.LEAD_ARTIST,
            },
            PictureTagValue(
                mime="image/jpeg",
                picture_type=id3.PictureType.LEAD_ARTIST,
                desc="Artist1",
            ),
            False,
            id="diff_desc_same_others",
        ),
    ],
)
def test_TextTagValue_eq(
    params: _PictureParams,
    other: Any,  # noqa: ANN401
    expected_result: bool,
) -> None:
    """Tests that equality checks are correct."""
    created_value = PictureTagValue(**params)
    actual_result: bool = created_value == other
    assert actual_result == expected_result


def test_PictureTagValue_hash_raises_TypeError() -> None:
    """Tests that PictureTagValues aren't hashable."""
    created_value = PictureTagValue()
    with pytest.raises(TypeError, match="TagValue objects are not hashable."):
        hash(created_value)


def test_PictureTagValue_join_diff_char_update_and_signal(qtbot: QtBot) -> None:
    """Tests that the join character is updated when sent a different character.

    The value should be updated, it should reflect in getDisplayValue,
    and a signal should be emitted.
    """
    created_value = PictureTagValue(
        mime="image/jpeg", desc="Image", join_character=", "
    )
    with qtbot.waitSignal(created_value.join_character_changed, timeout=1000):
        created_value.join_character = "; "
    assert created_value.join_character == "; "
    assert (
        created_value.getDisplayValue()
        == "Attached Picture: Cover Front (Image; image/jpeg)"
    )


def test_PictureTagValue_join_same_char_no_signal(qtbot: QtBot) -> None:
    """Tests that the join character is not updated when sent the same character.

    The value should not be updated, getDisplayValue should not change,
    and a signal should not be emitted.
    """
    created_value = PictureTagValue(
        mime="image/jpeg", desc="Image", join_character=", "
    )
    with qtbot.assertNotEmitted(created_value.join_character_changed):
        created_value.join_character = ", "
    assert created_value.join_character == ", "
    assert (
        created_value.getDisplayValue()
        == "Attached Picture: Cover Front (Image, image/jpeg)"
    )
