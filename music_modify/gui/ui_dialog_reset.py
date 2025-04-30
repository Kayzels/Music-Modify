# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_reset.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGroupBox, QHBoxLayout, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ResetDialog(object):
    def setupUi(self, ResetDialog):
        if not ResetDialog.objectName():
            ResetDialog.setObjectName(u"ResetDialog")
        ResetDialog.resize(282, 153)
        self.verticalLayout = QVBoxLayout(ResetDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(ResetDialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tags_check_box = QCheckBox(self.groupBox)
        self.tags_check_box.setObjectName(u"tags_check_box")

        self.horizontalLayout.addWidget(self.tags_check_box)

        self.split_check_box = QCheckBox(self.groupBox)
        self.split_check_box.setObjectName(u"split_check_box")

        self.horizontalLayout.addWidget(self.split_check_box)


        self.verticalLayout.addWidget(self.groupBox)

        self.button_box = QDialogButtonBox(ResetDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(ResetDialog)
        self.button_box.accepted.connect(ResetDialog.accept)
        self.button_box.rejected.connect(ResetDialog.reject)

        QMetaObject.connectSlotsByName(ResetDialog)
    # setupUi

    def retranslateUi(self, ResetDialog):
        ResetDialog.setWindowTitle(QCoreApplication.translate("ResetDialog", u"Restore Defaults", None))
        self.groupBox.setTitle(QCoreApplication.translate("ResetDialog", u"Restore to Default:", None))
        self.tags_check_box.setText(QCoreApplication.translate("ResetDialog", u"Tags", None))
        self.split_check_box.setText(QCoreApplication.translate("ResetDialog", u"Split", None))
    # retranslateUi

