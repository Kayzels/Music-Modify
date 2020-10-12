# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_progress_subaction.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_subactionProgressWidget(object):
    def setupUi(self, subactionProgressWidget):
        subactionProgressWidget.setObjectName("subactionProgressWidget")
        subactionProgressWidget.resize(462, 99)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(subactionProgressWidget.sizePolicy().hasHeightForWidth())
        subactionProgressWidget.setSizePolicy(sizePolicy)
        subactionProgressWidget.setStyleSheet("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(subactionProgressWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.subactionProgressWidget_All = QtWidgets.QWidget(subactionProgressWidget)
        self.subactionProgressWidget_All.setStyleSheet("QWidget#subactionProgressWidget_All {\n"
"  border: 1px solid black;\n"
"  border-radius: 15px;\n"
"  background: rgb(255, 235, 245)\n"
"}")
        self.subactionProgressWidget_All.setObjectName("subactionProgressWidget_All")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.subactionProgressWidget_All)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headingWidget = QtWidgets.QWidget(self.subactionProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headingWidget.sizePolicy().hasHeightForWidth())
        self.headingWidget.setSizePolicy(sizePolicy)
        self.headingWidget.setObjectName("headingWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.headingWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.subactionLabel = QtWidgets.QLabel(self.headingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.subactionLabel.sizePolicy().hasHeightForWidth())
        self.subactionLabel.setSizePolicy(sizePolicy)
        self.subactionLabel.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.subactionLabel.setFont(font)
        self.subactionLabel.setStyleSheet("QLabel {\n"
"  border-color:black;\n"
"  border-width: 2px;        \n"
"  border-style: solid;\n"
"  border-radius: 25px;\n"
"  margin:0px;\n"
"  padding:0px;\n"
"  color:black;\n"
"  background: white\n"
"}")
        self.subactionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.subactionLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.subactionLabel.setObjectName("subactionLabel")
        self.horizontalLayout.addWidget(self.subactionLabel)
        self.subactionName = QtWidgets.QLineEdit(self.headingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subactionName.sizePolicy().hasHeightForWidth())
        self.subactionName.setSizePolicy(sizePolicy)
        self.subactionName.setMinimumSize(QtCore.QSize(105, 37))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.subactionName.setFont(font)
        self.subactionName.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  padding:3px;\n"
"  margin:0px\n"
"}")
        self.subactionName.setMaxLength(100)
        self.subactionName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.subactionName.setReadOnly(True)
        self.subactionName.setObjectName("subactionName")
        self.horizontalLayout.addWidget(self.subactionName)
        self.verticalLayout.addWidget(self.headingWidget)
        self.subactionProgressBar = QtWidgets.QProgressBar(self.subactionProgressWidget_All)
        self.subactionProgressBar.setStyleSheet("QProgressBar {\n"
"  border: 2px solid dimgrey;\n"
"  border-radius: 12px;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"  border-radius: 10px;\n"
"  background-color: plum;\n"
"  border-color: plum;\n"
"}\n"
"")
        self.subactionProgressBar.setProperty("value", 0)
        self.subactionProgressBar.setInvertedAppearance(False)
        self.subactionProgressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.subactionProgressBar.setObjectName("subactionProgressBar")
        self.verticalLayout.addWidget(self.subactionProgressBar)
        self.verticalLayout_2.addWidget(self.subactionProgressWidget_All)

        self.retranslateUi(subactionProgressWidget)
        QtCore.QMetaObject.connectSlotsByName(subactionProgressWidget)

    def retranslateUi(self, subactionProgressWidget):
        _translate = QtCore.QCoreApplication.translate
        subactionProgressWidget.setWindowTitle(_translate("subactionProgressWidget", "Form"))
        self.subactionLabel.setText(_translate("subactionProgressWidget", "SUBACTION"))
        self.subactionName.setText(_translate("subactionProgressWidget", "No Action"))
