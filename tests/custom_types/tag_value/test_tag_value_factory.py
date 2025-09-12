"""Tests for TagValueFactory."""

import logging
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

from mutagen import id3
import pytest

from music_modify.custom_types.tag_value.abstract_tag_value import AbstractTagValue
from music_modify.custom_types.tag_value.paired_text_tag_value import PairedTextTagValue
from music_modify.custom_types.tag_value.picture_tag_value import PictureTagValue
from music_modify.custom_types.tag_value.tag_value_factory import TagValueFactory
from music_modify.custom_types.tag_value.text_tag_value import TextTagValue


@pytest.mark.parametrize(
    ("frame", "expected_value"),
    [
        pytest.param(
            id3.TPE1(encoding=id3.Encoding.UTF8, text=[]),
            TextTagValue([]),
            id="text_tag_empty",
        ),
        pytest.param(
            id3.TIT2(encoding=id3.Encoding.UTF8, text=["Word"]),
            TextTagValue(["Word"]),
            id="text_tag_single",
        ),
        pytest.param(
            id3.TCOM(encoding=id3.Encoding.UTF8, text=["First", "Second"]),
            TextTagValue(["First", "Second"]),
            id="text_tag_multiple",
        ),
        pytest.param(
            id3.TXXX(encoding=id3.Encoding.UTF8, text=["Something"], desc="Test"),
            TextTagValue(["Something"]),
            id="text_tag_custom",
        ),
        pytest.param(
            id3.TDRC(encoding=id3.Encoding.UTF8, text=[id3.ID3TimeStamp("2000")]),
            TextTagValue(["2000"]),
            id="text_tag_timestamp",
        ),
        pytest.param(
            id3.TMCL(encoding=id3.Encoding.UTF8, people=[]),
            PairedTextTagValue([]),
            id="pair_tag_empty",
        ),
        pytest.param(
            id3.TIPL(encoding=id3.Encoding.UTF8, people=[["First", "Second"]]),
            PairedTextTagValue([["First", "Second"]]),
            id="pair_tag_single",
        ),
        pytest.param(
            id3.APIC(
                encoding=id3.Encoding.UTF8,
                mime="image/jpeg",
                type=id3.PictureType.COVER_FRONT,
                data=b"value",
            ),
            PictureTagValue(
                mime="image/jpeg",
                picture_type=id3.PictureType.COVER_FRONT,
                data=b"value",
            ),
            id="image_value",
        ),
        pytest.param(id3.AENC(), None, id="unsupported_tag_aenc"),
        pytest.param(id3.CHAP(), None, id="unsupported_tag_chap"),
    ],
)
def test_TagValueFactory_fromId3Frame(
    frame: id3.Frame, expected_value: AbstractTagValue | None
) -> None:
    """Tests that the correct TagValue types are created based on id3 frame.

    str, None -> None
    str, not APIC -> TextTagValue
    str, APIC -> PictureTagValue
    [], None -> None
    [], TIPL|TMCL -> PairedTextTagValue
    [], T... -> TextTagValue
    list[str] -> TextTagValue
    list[list[str]] -> PairedTextTagValue
    list[other] -> None
    """
    actual_value = TagValueFactory.fromId3Frame(frame)
    assert actual_value == expected_value


@pytest.mark.parametrize(
    ("value_input", "id3_key", "expected_value"),
    [
        pytest.param([], None, None, id="None_when_can_be_diff_types"),
        pytest.param("", None, TextTagValue([""]), id="text_when_empty_string"),
        pytest.param("Text", None, TextTagValue(["Text"]), id="text_when_string"),
        pytest.param(
            ["Text"], None, TextTagValue(["Text"]), id="text_when_single_text_list"
        ),
        pytest.param(
            ["Text", "More"],
            None,
            TextTagValue(["Text", "More"]),
            id="text_when_multiple_text_list",
        ),
        pytest.param([], "TIT2", TextTagValue([]), id="text_when_unknown_and_text_id3"),
        pytest.param(
            [], "TIPL", PairedTextTagValue([]), id="paired_when_unknown_and_paired_id3"
        ),
        pytest.param(
            ["Text"], "TIPL", TextTagValue(["Text"]), id="text_when_known_and_wrong_id3"
        ),
        pytest.param(
            [["First", "Second"]],
            "TIT2",
            PairedTextTagValue([["First", "Second"]]),
            id="pair_when_known_and_wrong_id3",
        ),
        pytest.param(None, None, None, id="None_when_passed_none_and_no_id3"),
        pytest.param(
            None,
            "TIPL",
            PairedTextTagValue([]),
            id="pair_when_passed_none_and_pair_id3",
        ),
        pytest.param(
            None, "TCOM", TextTagValue([]), id="text_when_passed_none_and_text_id3"
        ),
        pytest.param(2, "TCOM", None, id="none_returned_when_invalid_input_with_tag"),
        pytest.param(
            [0], "TCOM", None, id="none_returned_when_invalid_list_input_with_tag"
        ),
        pytest.param(2, None, None, id="none_returned_when_invalid_input_without_tag"),
        pytest.param([], "", None, id="none_returned_when_empty_input_empty_key"),
        pytest.param([], "CHAP", None, id="none_returned_when_empty_input_unknown_key"),
        pytest.param(
            None, "APIC", PictureTagValue(), id="image_when_passed_none_and_apic_id3"
        ),
    ],
)
def test_TagValueFactory_createTagValue(
    value_input: Any,  # noqa: ANN401
    id3_key: str | None,
    expected_value: AbstractTagValue | None,
) -> None:
    """Tests that the correct TagValue types are created based on input data."""
    actual_value = TagValueFactory.createTagValue(value_input, id3_key)
    assert actual_value == expected_value


def test_TagValueFactory_createTagValue_image_valid_path(
    image_path: Path, image_bytes: bytes
) -> None:
    """Tests that PictureTagValues are created correctly from valid image paths.

    This can't be parametrized: using lazy fixtures leads to different binary data.
    """
    actual_value: AbstractTagValue | None = TagValueFactory.createTagValue(
        image_path, "APIC"
    )
    expected_value = PictureTagValue(image_bytes, "image/jpeg")
    assert actual_value == expected_value

    actual_value = TagValueFactory.createTagValue(str(image_path), "APIC")
    assert actual_value == expected_value


def test_TagValueFactory_createTagValue_image_invalid_path(
    image_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Tests that None is returned when there is no file at the path sent."""
    edited_path = image_path.with_stem("png")
    with caplog.at_level(logging.ERROR):
        result = TagValueFactory.createTagValue(edited_path)

    assert result is None
    assert "No file existed at the path sent" in caplog.text
    assert caplog.records[0].levelname == "ERROR"


def test_TagValueFactory_createTagValue_image_path_no_extension(
    image_path_no_extension: Path, image_bytes: bytes, caplog: pytest.LogCaptureFixture
) -> None:
    """Tests creating a PictureTagValue with a valid path, without an extension."""
    with caplog.at_level(logging.WARNING):
        result = TagValueFactory.createTagValue(image_path_no_extension)

    assert result == PictureTagValue(image_bytes, "")
    assert "Could not guess mimetype" in caplog.text
    assert caplog.records[0].levelname == "WARNING"


def test_TagValueFactory_createTagValue_image_error_reading_logs_error(
    image_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests that an error is logged and None is returned when file can't be read."""
    mock_open = MagicMock(side_effect=IOError)
    monkeypatch.setattr("pathlib.Path.open", mock_open)
    with caplog.at_level(logging.ERROR):
        result = TagValueFactory.createTagValue(image_path)

    assert result is None
    assert f"Error reading image file '{image_path}' for APIC tag." in caplog.text
    assert caplog.records[0].levelname == "ERROR"
