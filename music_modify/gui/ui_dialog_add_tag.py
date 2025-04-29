# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_add_tag.ui'
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
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_AddTagDialog(object):
    def setupUi(self, AddTagDialog):
        if not AddTagDialog.objectName():
            AddTagDialog.setObjectName(u"AddTagDialog")
        AddTagDialog.resize(280, 138)
        self.verticalLayout = QVBoxLayout(AddTagDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_id3 = QLabel(AddTagDialog)
        self.label_id3.setObjectName(u"label_id3")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_id3)

        self.id3_line_edit = QLineEdit(AddTagDialog)
        self.id3_line_edit.setObjectName(u"id3_line_edit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.id3_line_edit)

        self.label_display = QLabel(AddTagDialog)
        self.label_display.setObjectName(u"label_display")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_display)

        self.display_name_line_edit = QLineEdit(AddTagDialog)
        self.display_name_line_edit.setObjectName(u"display_name_line_edit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.display_name_line_edit)

        self.show_checkbox = QCheckBox(AddTagDialog)
        self.show_checkbox.setObjectName(u"show_checkbox")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.show_checkbox)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(AddTagDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.label_id3.setBuddy(self.id3_line_edit)
        self.label_display.setBuddy(self.display_name_line_edit)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(AddTagDialog)
        self.buttonBox.accepted.connect(AddTagDialog.accept)
        self.buttonBox.rejected.connect(AddTagDialog.reject)

        QMetaObject.connectSlotsByName(AddTagDialog)
    # setupUi

    def retranslateUi(self, AddTagDialog):
        AddTagDialog.setWindowTitle(QCoreApplication.translate("AddTagDialog", u"Dialog", None))
        self.label_id3.setText(QCoreApplication.translate("AddTagDialog", u"ID3 Key", None))
        self.label_display.setText(QCoreApplication.translate("AddTagDialog", u"Display Name", None))
        self.show_checkbox.setText(QCoreApplication.translate("AddTagDialog", u"Show in Table", None))
    # retranslateUi

