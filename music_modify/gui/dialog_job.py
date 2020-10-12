# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_job.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_JobDialog(object):
    def setupUi(self, JobDialog):
        JobDialog.setObjectName("JobDialog")
        JobDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        JobDialog.resize(1018, 645)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(JobDialog.sizePolicy().hasHeightForWidth())
        JobDialog.setSizePolicy(sizePolicy)
        JobDialog.setStyleSheet("QScrollBar {\n"
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
"QScrollBar::sub-line, \n"
"QScrollBar::add-line {\n"
"  background:transparent;\n"
"  subcontrol-origin:margin;\n"
"}\n"
"\n"
"QScrollBar::left-arrow,\n"
"QScrollBar::right-arrow,\n"
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
"}\n"
"\n"
"QScrollBar::vertical {\n"
"  margin-left: 4px\n"
"}")
        JobDialog.setSizeGripEnabled(True)
        JobDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(JobDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.actionsScrollArea = QtWidgets.QScrollArea(JobDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionsScrollArea.sizePolicy().hasHeightForWidth())
        self.actionsScrollArea.setSizePolicy(sizePolicy)
        self.actionsScrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.actionsScrollArea.setStyleSheet("QScrollBar {\n"
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
"QScrollBar::sub-line, \n"
"QScrollBar::add-line {\n"
"  background:transparent;\n"
"  subcontrol-origin:margin;\n"
"}\n"
"\n"
"QScrollBar::left-arrow,\n"
"QScrollBar::right-arrow,\n"
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
        self.actionsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.actionsScrollArea.setLineWidth(0)
        self.actionsScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.actionsScrollArea.setWidgetResizable(True)
        self.actionsScrollArea.setObjectName("actionsScrollArea")
        self.actionsScrollAreaWidgetContents = QtWidgets.QWidget()
        self.actionsScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1000, 594))
        self.actionsScrollAreaWidgetContents.setStyleSheet("QWidget#actionsScrollAreaWidgetContents {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 15px;\n"
"}")
        self.actionsScrollAreaWidgetContents.setObjectName("actionsScrollAreaWidgetContents")
        self.actionsScrollAreaContentsVerticalLayout = QtWidgets.QVBoxLayout(self.actionsScrollAreaWidgetContents)
        self.actionsScrollAreaContentsVerticalLayout.setObjectName("actionsScrollAreaContentsVerticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.actionsScrollAreaContentsVerticalLayout.addItem(spacerItem)
        self.actionsScrollArea.setWidget(self.actionsScrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.actionsScrollArea)
        self.buttonBox = QtWidgets.QDialogButtonBox(JobDialog)
        self.buttonBox.setStyleSheet("QPushButton {\n"
"  background: lightblue;\n"
"  color:rgb(0,115,150);\n"
"  min-width:70px;\n"
"  min-height:23px;\n"
"  border-color:rgb(0,115,150);\n"
"  border-width: 2px;        \n"
"  border-style: outset;\n"
"  border-radius: 9px;\n"
"  font-weight:bold;\n"
"  font-size:10pt\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style: inset;\n"
"  background: lightsteelblue\n"
"}")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(JobDialog)
        self.buttonBox.accepted.connect(JobDialog.accept)
        self.buttonBox.rejected.connect(JobDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(JobDialog)

    def retranslateUi(self, JobDialog):
        _translate = QtCore.QCoreApplication.translate
        JobDialog.setWindowTitle(_translate("JobDialog", "Job Dialog"))
