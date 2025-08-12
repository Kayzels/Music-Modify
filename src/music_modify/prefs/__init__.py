"""Package for managing the preferences stored for the application.

To use the settings, use the global `settings` object. Note that this
*must not* be done in the import, but at run time.

For example:
```python
from music_modify.prefs import prefs
# some other code

val = prefs.settings.some_attribute
```
"""
