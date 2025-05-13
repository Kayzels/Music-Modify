# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_prefs.ui'
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
    QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        if not PrefsDialog.objectName():
            PrefsDialog.setObjectName(u"PrefsDialog")
        PrefsDialog.resize(361, 139)
        self.verticalLayout = QVBoxLayout(PrefsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_edit_tags = QPushButton(PrefsDialog)
        self.button_edit_tags.setObjectName(u"button_edit_tags")

        self.horizontalLayout.addWidget(self.button_edit_tags)

        self.button_edit_split = QPushButton(PrefsDialog)
        self.button_edit_split.setObjectName(u"button_edit_split")

        self.horizontalLayout.addWidget(self.button_edit_split)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.button_box = QDialogButtonBox(PrefsDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Close)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(PrefsDialog)
        self.button_box.accepted.connect(PrefsDialog.accept)
        self.button_box.rejected.connect(PrefsDialog.reject)

        QMetaObject.connectSlotsByName(PrefsDialog)
    # setupUi

    def retranslateUi(self, PrefsDialog):
        PrefsDialog.setWindowTitle(QCoreApplication.translate("PrefsDialog", u"Preferences", None))
#if QT_CONFIG(tooltip)
        self.button_edit_tags.setToolTip(QCoreApplication.translate("PrefsDialog", u"<html><head/><body><p>The tags shown in the main table.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.button_edit_tags.setText(QCoreApplication.translate("PrefsDialog", u"Edit Tags...", None))
        self.button_edit_split.setText(QCoreApplication.translate("PrefsDialog", u"Edit Split Characters...", None))
    # retranslateUi

