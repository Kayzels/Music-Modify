from datetime import datetime
import logging
import platform

import mutagen
import PySide6
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QDialog, QWidget

from .ui_dialog_about import Ui_AboutDialog

logger = logging.getLogger(__name__)


class AboutDialog(QDialog, Ui_AboutDialog):
    """Dialog that displays the meta information about the app,
    such as the name, version, and tools used."""

    def __init__(self, parent: QWidget | None = None) -> None:
        QDialog.__init__(self, parent)
        self.setupUi(self)
        text = self.generateText()
        if text:
            self.textEdit.setHtml(text)

    @staticmethod
    def generateText() -> str:
        """Constructs the html content that should be displayed in the dialog"""
        instance: QCoreApplication | None = QApplication.instance()
        if instance is None:
            logger.warning("Application instance was None when calling generateText")
            return ""
        app_name = instance.applicationName()
        app_version = instance.applicationVersion()
        app_description = "A music tag editor written using PySide6 and Qt."
        author = "Kyzan Hartwig"
        year: int = datetime.now().year
        python_version: str = platform.python_version()
        pyside_version: str = PySide6.__version__
        mutagen_version: str = mutagen.version_string

        return f"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "https://www.w3.org/TR/REC-html40/strict.dtd">
<html>
    <head>
        <meta name="qrichtext" content="1"/>
        <meta charset="utf-8"/>
        <style>
            p, h1 {{text-align: center; text-indent: 0;}}
            h1 {{margin: 0;}}
        </style>
    </head>
    <body>
        <h1>{app_name}</h1>
        <p>Version {app_version}</p>
        <p>{app_description}</p>
        <p>Copyright © {year} {author}</p>
        <h2>Tools Used</h2>
        <ul>
            <li>Python {python_version}</li>
            <li>PySide {pyside_version}</li>
            <li>Qt {pyside_version}</li>
            <li>mutagen {mutagen_version}</li>
        </ul>
    </body>
</html>
"""
