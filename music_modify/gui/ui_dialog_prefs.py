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
    QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        if not PrefsDialog.objectName():
            PrefsDialog.setObjectName(u"PrefsDialog")
        PrefsDialog.resize(361, 227)
        self.verticalLayout = QVBoxLayout(PrefsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_split_text_entered = QLabel(PrefsDialog)
        self.label_split_text_entered.setObjectName(u"label_split_text_entered")
        self.label_split_text_entered.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_split_text_entered.setWordWrap(True)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_split_text_entered)

        self.line_edit_split_text_entered = QLineEdit(PrefsDialog)
        self.line_edit_split_text_entered.setObjectName(u"line_edit_split_text_entered")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.line_edit_split_text_entered)

        self.label_split_values_display = QLabel(PrefsDialog)
        self.label_split_values_display.setObjectName(u"label_split_values_display")
        self.label_split_values_display.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_split_values_display.setWordWrap(True)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_split_values_display)

        self.line_edit_split_values_display = QLineEdit(PrefsDialog)
        self.line_edit_split_values_display.setObjectName(u"line_edit_split_values_display")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.line_edit_split_values_display)

        self.label_split_values_at = QLabel(PrefsDialog)
        self.label_split_values_at.setObjectName(u"label_split_values_at")
        self.label_split_values_at.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_split_values_at.setWordWrap(True)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_split_values_at)

        self.line_edit_split_values_at = QLineEdit(PrefsDialog)
        self.line_edit_split_values_at.setObjectName(u"line_edit_split_values_at")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.line_edit_split_values_at)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_edit_tags = QPushButton(PrefsDialog)
        self.button_edit_tags.setObjectName(u"button_edit_tags")

        self.horizontalLayout.addWidget(self.button_edit_tags)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.button_box = QDialogButtonBox(PrefsDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.RestoreDefaults)

        self.verticalLayout.addWidget(self.button_box)

#if QT_CONFIG(shortcut)
        self.label_split_text_entered.setBuddy(self.line_edit_split_text_entered)
        self.label_split_values_display.setBuddy(self.line_edit_split_values_display)
        self.label_split_values_at.setBuddy(self.line_edit_split_values_at)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(PrefsDialog)
        self.button_box.accepted.connect(PrefsDialog.accept)
        self.button_box.rejected.connect(PrefsDialog.reject)

        QMetaObject.connectSlotsByName(PrefsDialog)
    # setupUi

    def retranslateUi(self, PrefsDialog):
        PrefsDialog.setWindowTitle(QCoreApplication.translate("PrefsDialog", u"Preferences", None))
#if QT_CONFIG(tooltip)
        self.label_split_text_entered.setToolTip(QCoreApplication.translate("PrefsDialog", u"<html><head/><body><p>The symbol that should split the data typed in. For example, with it set to be &quot;,&quot;, John Smith, Jane Doe should be understood as two separate values.</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_split_text_entered.setText(QCoreApplication.translate("PrefsDialog", u"Split Text Entered", None))
#if QT_CONFIG(tooltip)
        self.label_split_values_display.setToolTip(QCoreApplication.translate("PrefsDialog", u"<html><head/><body><p>The symbol that should be used in the table to show when there are multiple items in a field. If set to \\\\, John Smith, Jane Doe would be shown as John Smith\\\\Jane Doe</p><p/></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_split_values_display.setText(QCoreApplication.translate("PrefsDialog", u"Split Values Display", None))
#if QT_CONFIG(tooltip)
        self.label_split_values_at.setToolTip(QCoreApplication.translate("PrefsDialog", u"<html><head/><body><p>The symbol used when existing values should be split. For example, if an existing field is John Smith; Jane Doe, this should split it into separate values.</p><p/></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_split_values_at.setText(QCoreApplication.translate("PrefsDialog", u"Split Values At", None))
#if QT_CONFIG(tooltip)
        self.button_edit_tags.setToolTip(QCoreApplication.translate("PrefsDialog", u"<html><head/><body><p>The tags shown in the main table.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.button_edit_tags.setText(QCoreApplication.translate("PrefsDialog", u"Edit Tags...", None))
    # retranslateUi

