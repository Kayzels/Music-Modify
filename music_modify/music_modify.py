import sys

from PySide6.QtWidgets import QApplication

from music_modify.gui import MainWindow


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
