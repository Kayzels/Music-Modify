import logging
import sys

from PySide6.QtWidgets import QApplication

from music_modify.gui import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger()


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Kayzels")
    app.setApplicationName("Music Modify")
    app.setApplicationVersion("2.0.0")

    window = MainWindow()
    window.addStatusbarAppMessage(app.applicationName(), app.applicationVersion())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
