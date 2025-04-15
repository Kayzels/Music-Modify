# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window_main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTableView, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_add_files = QAction(MainWindow)
        self.action_add_files.setObjectName(u"action_add_files")
        icon = QIcon(QIcon.fromTheme(u"document-new"))
        self.action_add_files.setIcon(icon)
        self.action_add_files.setMenuRole(QAction.MenuRole.NoRole)
        self.action_add_folder = QAction(MainWindow)
        self.action_add_folder.setObjectName(u"action_add_folder")
        icon1 = QIcon(QIcon.fromTheme(u"folder-new"))
        self.action_add_folder.setIcon(icon1)
        self.action_add_folder.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.files_table_view = QTableView(self.centralwidget)
        self.files_table_view.setObjectName(u"files_table_view")
        self.files_table_view.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.files_table_view.setAlternatingRowColors(True)
        self.files_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.files_table_view.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.files_table_view)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName(u"menu_view")
        self.menu_edit = QMenu(self.menubar)
        self.menu_edit.setObjectName(u"menu_edit")
        self.menu_settings = QMenu(self.menubar)
        self.menu_settings.setObjectName(u"menu_settings")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tool_bar = QToolBar(MainWindow)
        self.tool_bar.setObjectName(u"tool_bar")
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_add_files)
        self.menu_file.addAction(self.action_add_folder)
        self.tool_bar.addAction(self.action_add_files)
        self.tool_bar.addAction(self.action_add_folder)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Music Modify", None))
        self.action_add_files.setText(QCoreApplication.translate("MainWindow", u"Add Files", None))
#if QT_CONFIG(tooltip)
        self.action_add_files.setToolTip(QCoreApplication.translate("MainWindow", u"Import Files", None))
#endif // QT_CONFIG(tooltip)
        self.action_add_folder.setText(QCoreApplication.translate("MainWindow", u"Add Folder", None))
#if QT_CONFIG(tooltip)
        self.action_add_folder.setToolTip(QCoreApplication.translate("MainWindow", u"Add Folder", None))
#endif // QT_CONFIG(tooltip)
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menu_edit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menu_settings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.tool_bar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

