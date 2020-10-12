# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_tag.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tagWidget(object):
    def setupUi(self, tagWidget):
        tagWidget.setObjectName("tagWidget")
        tagWidget.resize(871, 58)
        self.verticalLayout = QtWidgets.QVBoxLayout(tagWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tagsComboBox = QtWidgets.QComboBox(tagWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsComboBox.sizePolicy().hasHeightForWidth())
        self.tagsComboBox.setSizePolicy(sizePolicy)
        self.tagsComboBox.setMinimumSize(QtCore.QSize(0, 23))
        self.tagsComboBox.setBaseSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tagsComboBox.setFont(font)
        self.tagsComboBox.setStyleSheet("QComboBox {\n"
"  background:rgb(240,230,255);\n"
"  border-color:rgb(100,100,215);\n"
"  border-width: 3px;        \n"
"  border-style: outset;\n"
"  border-radius: 9px;\n"
"  color:rgb(100,100,215);\n"
"  padding-left:6px\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"border:none;\n"
"width:24px\n"
"}\n"
"\n"
"QComboBox::down-arrow{\n"
"image:url(:/icons/resources/icons/down_icon.png);\n"
"width:20px;\n"
"height:20px;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"  border-style:inset;\n"
"  background: lavender\n"
"}\n"
"QListView {\n"
"  font-size:12pt;\n"
"  /*border-color:rgb(100,100,215);\n"
"  border-width: 2px;        \n"
"  border-style: solid;*/\n"
"  border: none;\n"
"  background-color:rgb(248,248,255);\n"
"  color:rgb(100,100,215);\n"
"  margin:2px;\n"
"  outline: 0px\n"
"}\n"
"QListView::item {\n"
"  background: transparent;\n"
"  border: 0px\n"
"}\n"
"\n"
"QListView::item::selected{\n"
"  background-color:lavender;\n"
"  color:rgb(100, 100, 215);\n"
"  /*border: 1px solid lavender;\n"
"  border-color:lavender;*/\n"
"}\n"
"\n"
"QAbstractScrollArea::corner {\n"
"  background: transparent\n"
"}\n"
"\n"
"QScrollBar {\n"
"  border: 1px solid black;\n"
"  background: white;\n"
"  border-radius: 12px;\n"
"  margin: 0px\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
" border: 1px solid lavender;\n"
"  background:lavender;\n"
"  border-radius: 9px;\n"
"}\n"
"\n"
"QScrollBar::sub-line, QScrollBar::add-line {\n"
"  background:transparent;\n"
"  subcontrol-origin:margin;\n"
"}\n"
"\n"
"QScrollBar::left-arrow, QScrollBar::right-arrow,\n"
"QScrollBar::add-page, \n"
"QScrollBar::sub-page {\n"
"  background:transparent\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"  height:25px\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"  width: 25px\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"  width: 0px;\n"
"  subcontrol-position:left\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"  width: 0px;\n"
"  subcontrol-position:right\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"  height: 0px;\n"
"  subcontrol-position: top\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"  height: 0px;\n"
"  subcontrol-position: bottom\n"
"}")
        self.tagsComboBox.setFrame(True)
        self.tagsComboBox.setObjectName("tagsComboBox")
        self.tagsComboBox.addItem("")
        self.horizontalLayout.addWidget(self.tagsComboBox)
        self.copyTagsComboBox = QtWidgets.QComboBox(tagWidget)
        self.copyTagsComboBox.setMinimumSize(QtCore.QSize(0, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.copyTagsComboBox.setFont(font)
        self.copyTagsComboBox.setStyleSheet("QComboBox {\n"
"  background:rgb(240,230,255);\n"
"  border-color:rgb(100,100,215);\n"
"  border-width: 3px;        \n"
"  border-style: outset;\n"
"  border-radius: 9px;\n"
"  color:rgb(100,100,215);\n"
"  padding-left:6px\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"border:none;\n"
"width:24px\n"
"}\n"
"\n"
"QComboBox::down-arrow{\n"
"image:url(:/icons/resources/icons/down_icon.png);\n"
"width:20px;\n"
"height:20px;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"  border-style:inset;\n"
"  background: lavender\n"
"}\n"
"QListView {\n"
"  font-size:12pt;\n"
"  /*border-color:rgb(100,100,215);\n"
"  border-width: 2px;        \n"
"  border-style: solid;*/\n"
"  border: none;\n"
"  background-color:rgb(248,248,255);\n"
"  color:rgb(100,100,215);\n"
"  margin:2px;\n"
"  outline: 0px\n"
"}\n"
"QListView::item {\n"
"  background: transparent;\n"
"  border: 0px\n"
"}\n"
"\n"
"QListView::item::selected{\n"
"  background-color:lavender;\n"
"  color:rgb(100, 100, 215);\n"
"  /*border: 1px solid lavender;\n"
"  border-color:lavender;*/\n"
"}\n"
"\n"
"QAbstractScrollArea::corner {\n"
"  background: transparent\n"
"}\n"
"\n"
"QScrollBar {\n"
"  border: 1px solid black;\n"
"  background: white;\n"
"  border-radius: 12px;\n"
"  margin: 0px\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
" border: 1px solid lavender;\n"
"  background:lavender;\n"
"  border-radius: 9px;\n"
"}\n"
"\n"
"QScrollBar::sub-line, QScrollBar::add-line {\n"
"  background:transparent;\n"
"  subcontrol-origin:margin;\n"
"}\n"
"\n"
"QScrollBar::left-arrow, QScrollBar::right-arrow,\n"
"QScrollBar::add-page, \n"
"QScrollBar::sub-page {\n"
"  background:transparent\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"  height:25px\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"  width: 25px\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"  width: 0px;\n"
"  subcontrol-position:left\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"  width: 0px;\n"
"  subcontrol-position:right\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"  height: 0px;\n"
"  subcontrol-position: top\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"  height: 0px;\n"
"  subcontrol-position: bottom\n"
"}")
        self.copyTagsComboBox.setObjectName("copyTagsComboBox")
        self.copyTagsComboBox.addItem("")
        self.horizontalLayout.addWidget(self.copyTagsComboBox)
        self.addButton = QtWidgets.QPushButton(tagWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setMinimumSize(QtCore.QSize(40, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.addButton.setFont(font)
        self.addButton.setStyleSheet("QPushButton {\n"
"  border-color:green;\n"
"  border-width: 2px;        \n"
"  border-style: outset;\n"
"  border-radius:9px;\n"
"  background: lightgreen;\n"
"  color: green;\n"
"  margin: 1px\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: limegreen;\n"
"  border-style: inset\n"
"}\n"
"")
        self.addButton.setText("+")
        self.addButton.setShortcut("")
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.removeButton = QtWidgets.QPushButton(tagWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy)
        self.removeButton.setMinimumSize(QtCore.QSize(40, 0))
        self.removeButton.setBaseSize(QtCore.QSize(15, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.removeButton.setFont(font)
        self.removeButton.setStyleSheet("QPushButton {\n"
"  border-color:darkred;\n"
"  border-width: 2px;        \n"
"  border-style: outset;\n"
"  background: pink;\n"
"  color: darkred;\n"
"  margin:1px;\n"
"  border-radius:9px\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style: inset;\n"
"  background: rgb(255, 160, 180)\n"
"}")
        self.removeButton.setText("-")
        self.removeButton.setShortcut("")
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout.addWidget(self.removeButton)
        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout.setStretch(1, 10)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.roleWidget = QtWidgets.QWidget(tagWidget)
        self.roleWidget.setObjectName("roleWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.roleWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.roleLabel = QtWidgets.QLabel(self.roleWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.roleLabel.setFont(font)
        self.roleLabel.setStyleSheet("color:rgb(80,80,180)")
        self.roleLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roleLabel.setObjectName("roleLabel")
        self.horizontalLayout_2.addWidget(self.roleLabel)
        self.roleLineEdit = QtWidgets.QLineEdit(self.roleWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.roleLineEdit.setFont(font)
        self.roleLineEdit.setStyleSheet("color:rgb(100,100,215);\n"
"border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 9px;\n"
"  padding-left: 4px")
        self.roleLineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.roleLineEdit.setObjectName("roleLineEdit")
        self.horizontalLayout_2.addWidget(self.roleLineEdit)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.verticalLayout.addWidget(self.roleWidget)

        self.retranslateUi(tagWidget)
        self.copyTagsComboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(tagWidget)

    def retranslateUi(self, tagWidget):
        _translate = QtCore.QCoreApplication.translate
        tagWidget.setWindowTitle(_translate("tagWidget", "Form"))
        self.tagsComboBox.setItemText(0, _translate("tagWidget", "Select Tag"))
        self.copyTagsComboBox.setCurrentText(_translate("tagWidget", "Select Copy Tag"))
        self.copyTagsComboBox.setItemText(0, _translate("tagWidget", "Select Copy Tag"))
        self.roleLabel.setText(_translate("tagWidget", "Role:"))
        self.roleLineEdit.setPlaceholderText(_translate("tagWidget", "Incompatible Tags. Type the role for the Paired Tag."))
import resources_rc
