# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_selection.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileSelectionDialog(object):
    def setupUi(self, FileSelectionDialog):
        FileSelectionDialog.setObjectName("FileSelectionDialog")
        FileSelectionDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        FileSelectionDialog.resize(672, 540)
        FileSelectionDialog.setStyleSheet("")
        FileSelectionDialog.setSizeGripEnabled(True)
        FileSelectionDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(FileSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.selectAllPushButton = QtWidgets.QPushButton(FileSelectionDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectAllPushButton.setFont(font)
        self.selectAllPushButton.setStyleSheet("QPushButton {\n"
"  border-color:rgb(0,115,150);\n"
"  border-width: 2px;        \n"
"  border-style: outset;\n"
"  border-radius: 9px;\n"
"  background: lightblue;\n"
"  color:rgb(0,115,150)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style: inset;\n"
"  background: lightsteelblue\n"
"}")
        self.selectAllPushButton.setObjectName("selectAllPushButton")
        self.horizontalLayout.addWidget(self.selectAllPushButton)
        self.selectNonePushButton = QtWidgets.QPushButton(FileSelectionDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectNonePushButton.setFont(font)
        self.selectNonePushButton.setStyleSheet("QPushButton {\n"
"  border-color:rgb(0,115,150);\n"
"  border-width: 2px;        \n"
"  border-style: outset;\n"
"  border-radius: 9px;\n"
"  background: lightblue;\n"
"  color:rgb(0,115,150)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style: inset;\n"
"  background: lightsteelblue\n"
"}")
        self.selectNonePushButton.setObjectName("selectNonePushButton")
        self.horizontalLayout.addWidget(self.selectNonePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.changeSelectionTableView = QtWidgets.QTableView(FileSelectionDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.changeSelectionTableView.setFont(font)
        self.changeSelectionTableView.setStyleSheet("QTableView QTableCornerButton::section {\n"
"  background-color:lightblue;\n"
"  border: none;\n"
"  /* border-right: 1px solid rgb(100, 100, 215);\n"
"  border-bottom: 1px solid rgb(100, 100, 215);\n"
"  border-top: 0px;\n"
"  border-left: 0px;*/\n"
"  border-top-left-radius: 15px\n"
"}\n"
"\n"
"QHeaderView::section::horizontal {\n"
"  font-size:12pt;\n"
"  padding-bottom:6px;\n"
"  background-color: lightblue;\n"
"  border: none;\n"
"  /*border-right: 1px solid rgb(100, 100, 215);*/\n"
"  border-bottom: 1px solid rgb(100, 100, 215);\n"
" }\n"
"\n"
"QHeaderView::section::horizontal::last {\n"
"  border-right: 0px;\n"
"  border-top-right-radius: 15px\n"
"}\n"
"\n"
"QHeaderView::section::horizontal::only-one {\n"
"  background-color: transparent;\n"
"  border: none;\n"
"  border-left: 0px;\n"
"  border-top-left-radius: 15px;\n"
"  border-right: 0px;\n"
"  border-top-right-radius: 15px\n"
"}\n"
"\n"
"QHeaderView::section::vertical {\n"
"  background-color: lightblue;\n"
"  border: none;\n"
"  border-right: 1px solid rgb(100, 100, 215);\n"
"  /*border-bottom: 1px solid lightgrey;*/\n"
"  padding-left: 9px\n"
" }\n"
"\n"
"QHeaderView::section::vertical::last {\n"
"  border-bottom: 0px;\n"
"  border-bottom-left-radius: 15px\n"
"}\n"
"\n"
"QHeaderView {\n"
"  border:0px;\n"
"  background-color: transparent;\n"
"  border-radius: 15px\n"
"}\n"
"\n"
"QTableView {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 15px;\n"
"  background-color:white;\n"
"  alternate-background-color:rgb(215,245,255);\n"
"  gridline-color: lightblue\n"
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
" border: 1px solid lightblue;\n"
"  background:lightblue;\n"
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
        self.changeSelectionTableView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.changeSelectionTableView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.changeSelectionTableView.setTabKeyNavigation(False)
        self.changeSelectionTableView.setAlternatingRowColors(True)
        self.changeSelectionTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.changeSelectionTableView.setObjectName("changeSelectionTableView")
        self.changeSelectionTableView.verticalHeader().setCascadingSectionResizes(True)
        self.verticalLayout.addWidget(self.changeSelectionTableView)
        self.buttonBox = QtWidgets.QDialogButtonBox(FileSelectionDialog)
        self.buttonBox.setStyleSheet("QPushButton {\n"
"  min-width:70px;\n"
"  min-height:23px; \n"
"  border-width: 2px;        \n"
"  border-style: outset;\n"
"  border-radius: 9px;\n"
"  font-weight:bold;\n"
"  font-size:10pt\n"
"}\n"
"\n"
"QPushButton:enabled{\n"
"  background: lightblue;\n"
"  color:rgb(0,115,150);\n"
"  border-color:rgb(0,115,150);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style: inset;\n"
"  background: lightsteelblue\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"  color:grey;\n"
"  background:lightgrey;\n"
"  border-color:grey\n"
"}")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FileSelectionDialog)
        self.buttonBox.accepted.connect(FileSelectionDialog.accept)
        self.buttonBox.rejected.connect(FileSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FileSelectionDialog)

    def retranslateUi(self, FileSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        FileSelectionDialog.setWindowTitle(_translate("FileSelectionDialog", "Change Selected Files"))
        self.selectAllPushButton.setText(_translate("FileSelectionDialog", "SELECT ALL"))
        self.selectNonePushButton.setText(_translate("FileSelectionDialog", "SELECT NONE"))
