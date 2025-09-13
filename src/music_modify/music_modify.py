"""Entry point for running Music Modify."""

import logging
import sys
from typing import Never

from PySide6.QtWidgets import QApplication

from music_modify.gui import MainWindow
from music_modify.prefs import prefs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger()


def main() -> Never:
    """The entry point function for running the app."""
    app = QApplication(sys.argv)
    app.setOrganizationName("Kayzels")
    app.setApplicationName("Music Modify")
    app.setApplicationVersion("2.0.0")

    settings = prefs.Settings()
    settings.configureForApplication()

    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
