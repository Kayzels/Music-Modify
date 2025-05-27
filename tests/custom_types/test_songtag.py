from mutagen.id3 import ID3
from music_modify.custom_types.enums import TagType
from music_modify.custom_types.songtag import SongTag

single_tag = SongTag(id3_key="TIT2", display_name="Title")
multiple_tag = SongTag(id3_key="TCOM", display_name="Composer")
people_tag = SongTag(id3_key="TIPL", display_name="Involved People")
miss_tag = SongTag(id3_key="TPE2", display_name="Artist")

single_word = "Some Title"
single_value = [single_word]
multiple_value = ["Some Person", "Another Person"]
people_value = [["role1", "Person 1"], ["role2", "Person 2"]]


def test_id3_key():
    assert single_tag.id3_key == "TIT2"


def test_display_name():
    assert single_tag.display_name == "Title"


def test_frame_type():
    assert single_tag.frame_type == TagType.Text
    assert multiple_tag.frame_type == TagType.Text
    assert people_tag.frame_type == TagType.People


def test_allow_multiple():
    assert not single_tag.allow_multiple
    assert multiple_tag.allow_multiple
    assert not people_tag.allow_multiple


def test_len():
    assert len(single_tag) == 1
    assert len(multiple_tag) == 1
    assert len(people_tag) == 2


def test_hasTag():
    song = ID3()
    assert not single_tag.hasTag(song)
    assert not multiple_tag.hasTag(song)
    assert not people_tag.hasTag(song)


def test_generateFrame_hasTag():
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.generateFrame(song)
    assert single_tag.hasTag(song)


def test_setTag():
    song = ID3()
    single_tag.setTag(song, single_value)
    assert single_tag.getTag(song) == single_value
    multiple_tag.setTag(song, multiple_value)
    assert multiple_tag.getTag(song) == multiple_value
    people_tag.setTag(song, people_value)
    assert people_tag.getTag(song) == people_value


def test_removeTag():
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.hasTag(song)
    single_tag.removeTag(song)
    assert not single_tag.hasTag(song)


def test_getTag():
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.getTag(song) == single_value
    assert not multiple_tag.hasTag(song)
    assert multiple_tag.getTag(song) is None


def test_getValue():
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.getValue(song) == single_word

    multiple_tag.setTag(song, multiple_value)
    assert multiple_tag.getValue(song) == multiple_value

    people_tag.setTag(song, people_value)
    assert people_tag.getValue(song) == people_value
