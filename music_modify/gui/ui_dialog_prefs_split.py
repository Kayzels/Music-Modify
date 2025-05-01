# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_prefs_split.ui'
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
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_PrefsSplitDialog(object):
    def setupUi(self, PrefsSplitDialog):
        if not PrefsSplitDialog.objectName():
            PrefsSplitDialog.setObjectName(u"PrefsSplitDialog")
        PrefsSplitDialog.resize(400, 186)
        self.verticalLayout = QVBoxLayout(PrefsSplitDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_split_text_entered = QLabel(PrefsSplitDialog)
        self.label_split_text_entered.setObjectName(u"label_split_text_entered")
        self.label_split_text_entered.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_split_text_entered.setWordWrap(True)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_split_text_entered)

        self.line_edit_split_text_entered = QLineEdit(PrefsSplitDialog)
        self.line_edit_split_text_entered.setObjectName(u"line_edit_split_text_entered")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.line_edit_split_text_entered)

        self.label_split_values_display = QLabel(PrefsSplitDialog)
        self.label_split_values_display.setObjectName(u"label_split_values_display")
        self.label_split_values_display.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_split_values_display.setWordWrap(True)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_split_values_display)

        self.line_edit_split_values_display = QLineEdit(PrefsSplitDialog)
        self.line_edit_split_values_display.setObjectName(u"line_edit_split_values_display")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.line_edit_split_values_display)

        self.label_split_values_at = QLabel(PrefsSplitDialog)
        self.label_split_values_at.setObjectName(u"label_split_values_at")
        self.label_split_values_at.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_split_values_at.setWordWrap(True)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_split_values_at)

        self.line_edit_split_values_at = QLineEdit(PrefsSplitDialog)
        self.line_edit_split_values_at.setObjectName(u"line_edit_split_values_at")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.line_edit_split_values_at)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.button_box = QDialogButtonBox(PrefsSplitDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.RestoreDefaults)

        self.verticalLayout.addWidget(self.button_box)

#if QT_CONFIG(shortcut)
        self.label_split_text_entered.setBuddy(self.line_edit_split_text_entered)
        self.label_split_values_display.setBuddy(self.line_edit_split_values_display)
        self.label_split_values_at.setBuddy(self.line_edit_split_values_at)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(PrefsSplitDialog)
        self.button_box.accepted.connect(PrefsSplitDialog.accept)
        self.button_box.rejected.connect(PrefsSplitDialog.reject)

        QMetaObject.connectSlotsByName(PrefsSplitDialog)
    # setupUi

    def retranslateUi(self, PrefsSplitDialog):
        PrefsSplitDialog.setWindowTitle(QCoreApplication.translate("PrefsSplitDialog", u"Edit Split Characters", None))
#if QT_CONFIG(tooltip)
        self.label_split_text_entered.setToolTip(QCoreApplication.translate("PrefsSplitDialog", u"<html><head/><body><p>The symbol that should split the data typed in. For example, with it set to be &quot;,&quot;, John Smith, Jane Doe should be understood as two separate values.</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_split_text_entered.setText(QCoreApplication.translate("PrefsSplitDialog", u"Split Text Entered", None))
#if QT_CONFIG(tooltip)
        self.label_split_values_display.setToolTip(QCoreApplication.translate("PrefsSplitDialog", u"<html><head/><body><p>The symbol that should be used in the table to show when there are multiple items in a field. If set to \\\\, John Smith, Jane Doe would be shown as John Smith\\\\Jane Doe</p><p/></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_split_values_display.setText(QCoreApplication.translate("PrefsSplitDialog", u"Split Values Display", None))
#if QT_CONFIG(tooltip)
        self.label_split_values_at.setToolTip(QCoreApplication.translate("PrefsSplitDialog", u"<html><head/><body><p>The symbol used when existing values should be split. For example, if an existing field is John Smith; Jane Doe, this should split it into separate values.</p><p/></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_split_values_at.setText(QCoreApplication.translate("PrefsSplitDialog", u"Split Values At", None))
    # retranslateUi

