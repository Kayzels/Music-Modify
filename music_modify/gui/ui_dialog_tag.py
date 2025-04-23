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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHeaderView, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_TagDialog(object):
    def setupUi(self, TagDialog):
        if not TagDialog.objectName():
            TagDialog.setObjectName(u"TagDialog")
        TagDialog.resize(655, 434)
        self.verticalLayout = QVBoxLayout(TagDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tag_table = QTableView(TagDialog)
        self.tag_table.setObjectName(u"tag_table")

        self.verticalLayout.addWidget(self.tag_table)

        self.buttonBox = QDialogButtonBox(TagDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TagDialog)
        self.buttonBox.accepted.connect(TagDialog.accept)
        self.buttonBox.rejected.connect(TagDialog.reject)

        QMetaObject.connectSlotsByName(TagDialog)
    # setupUi

    def retranslateUi(self, TagDialog):
        TagDialog.setWindowTitle(QCoreApplication.translate("TagDialog", u"Dialog", None))
    # retranslateUi

