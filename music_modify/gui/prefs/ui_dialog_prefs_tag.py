# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_prefs_tag.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHBoxLayout, QHeaderView, QSizePolicy,
    QTableView, QToolButton, QVBoxLayout, QWidget)

class Ui_PrefsTagDialog(object):
    def setupUi(self, PrefsTagDialog):
        if not PrefsTagDialog.objectName():
            PrefsTagDialog.setObjectName(u"PrefsTagDialog")
        PrefsTagDialog.resize(510, 434)
        self.verticalLayout_2 = QVBoxLayout(PrefsTagDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tag_table = QTableView(PrefsTagDialog)
        self.tag_table.setObjectName(u"tag_table")
        self.tag_table.setAlternatingRowColors(True)
        self.tag_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tag_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tag_table.setShowGrid(True)
        self.tag_table.horizontalHeader().setStretchLastSection(True)
        self.tag_table.verticalHeader().setVisible(False)

        self.horizontalLayout.addWidget(self.tag_table)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.up_toolbutton = QToolButton(PrefsTagDialog)
        self.up_toolbutton.setObjectName(u"up_toolbutton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.up_toolbutton.setIcon(icon)

        self.verticalLayout.addWidget(self.up_toolbutton)

        self.add_toolbutton = QToolButton(PrefsTagDialog)
        self.add_toolbutton.setObjectName(u"add_toolbutton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.add_toolbutton.setIcon(icon1)

        self.verticalLayout.addWidget(self.add_toolbutton)

        self.remove_toolbutton = QToolButton(PrefsTagDialog)
        self.remove_toolbutton.setObjectName(u"remove_toolbutton")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.remove_toolbutton.setIcon(icon2)

        self.verticalLayout.addWidget(self.remove_toolbutton)

        self.down_toolbutton = QToolButton(PrefsTagDialog)
        self.down_toolbutton.setObjectName(u"down_toolbutton")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        self.down_toolbutton.setIcon(icon3)

        self.verticalLayout.addWidget(self.down_toolbutton)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.button_box = QDialogButtonBox(PrefsTagDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Reset|QDialogButtonBox.StandardButton.RestoreDefaults)

        self.verticalLayout_2.addWidget(self.button_box)

        self.verticalLayout_2.setStretch(0, 10)

        self.retranslateUi(PrefsTagDialog)
        self.button_box.accepted.connect(PrefsTagDialog.accept)
        self.button_box.rejected.connect(PrefsTagDialog.reject)

        QMetaObject.connectSlotsByName(PrefsTagDialog)
    # setupUi

    def retranslateUi(self, PrefsTagDialog):
        PrefsTagDialog.setWindowTitle(QCoreApplication.translate("PrefsTagDialog", u"Dialog", None))
        self.up_toolbutton.setText(QCoreApplication.translate("PrefsTagDialog", u"Move Up", None))
        self.add_toolbutton.setText(QCoreApplication.translate("PrefsTagDialog", u"Add Tag", None))
        self.remove_toolbutton.setText(QCoreApplication.translate("PrefsTagDialog", u"Remove Tag", None))
        self.down_toolbutton.setText(QCoreApplication.translate("PrefsTagDialog", u"Move Down", None))
    # retranslateUi

