# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_tag.ui'
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

class Ui_TagDialog(object):
    def setupUi(self, TagDialog):
        if not TagDialog.objectName():
            TagDialog.setObjectName(u"TagDialog")
        TagDialog.resize(389, 434)
        self.verticalLayout_2 = QVBoxLayout(TagDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tag_table = QTableView(TagDialog)
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
        self.up_toolbutton = QToolButton(TagDialog)
        self.up_toolbutton.setObjectName(u"up_toolbutton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.up_toolbutton.setIcon(icon)

        self.verticalLayout.addWidget(self.up_toolbutton)

        self.add_toolbutton = QToolButton(TagDialog)
        self.add_toolbutton.setObjectName(u"add_toolbutton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.add_toolbutton.setIcon(icon1)

        self.verticalLayout.addWidget(self.add_toolbutton)

        self.remove_toolbutton = QToolButton(TagDialog)
        self.remove_toolbutton.setObjectName(u"remove_toolbutton")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.remove_toolbutton.setIcon(icon2)

        self.verticalLayout.addWidget(self.remove_toolbutton)

        self.down_toolbutton = QToolButton(TagDialog)
        self.down_toolbutton.setObjectName(u"down_toolbutton")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        self.down_toolbutton.setIcon(icon3)

        self.verticalLayout.addWidget(self.down_toolbutton)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(TagDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(TagDialog)
        self.buttonBox.accepted.connect(TagDialog.accept)
        self.buttonBox.rejected.connect(TagDialog.reject)

        QMetaObject.connectSlotsByName(TagDialog)
    # setupUi

    def retranslateUi(self, TagDialog):
        TagDialog.setWindowTitle(QCoreApplication.translate("TagDialog", u"Dialog", None))
        self.up_toolbutton.setText(QCoreApplication.translate("TagDialog", u"Move Up", None))
        self.add_toolbutton.setText(QCoreApplication.translate("TagDialog", u"Add Tag", None))
        self.remove_toolbutton.setText(QCoreApplication.translate("TagDialog", u"Remove Tag", None))
        self.down_toolbutton.setText(QCoreApplication.translate("TagDialog", u"Move Down", None))
    # retranslateUi

