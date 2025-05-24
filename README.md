# Music Modify

Welcome to Music Modify -- an app designed to allow you to have greater control over the tags in your music files.

## Screenshots

[The main dialog with no songs](./docs/main_screen.png)

[The main dialog with songs added](./docs/main_with_songs.png)

[Bulk edit dialog](./docs/edit_dialog.png)

## How to Use

You can drag any mp3 files onto the main table, or add files and folders using the buttons.

You can then select any of the songs displayed. To edit them, select the Edit button from the menu bar, or right click and select Edit.

The tags that are displayed can be configured. They follow the convention defined for ID3 tags, where title is TIT2, for example.
Custom tags are defined with TXXX and then the specific name, for example TXXX:KEYWORDS.
A significant limitation of custom tags is that they can only store a single line of text, unlike the default tags,
where more can be stored, depending on the type.

To configure the tags, open the Settings menu, and then select Tags.
Tags have a display name, the ID3 key that's stored in the file itself, and a checkbox for whether this tag should be displayed
in the main table or not.

## Building

Requires Python 3.13, PySide6, and mutagen. More instructions should be coming soon.

---
