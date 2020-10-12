# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_progress_job.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_jobProgressWidget(object):
    def setupUi(self, jobProgressWidget):
        jobProgressWidget.setObjectName("jobProgressWidget")
        jobProgressWidget.resize(461, 412)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(jobProgressWidget.sizePolicy().hasHeightForWidth())
        jobProgressWidget.setSizePolicy(sizePolicy)
        jobProgressWidget.setMinimumSize(QtCore.QSize(0, 180))
        jobProgressWidget.setStyleSheet("")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(jobProgressWidget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.jobProgressWidget_All = QtWidgets.QWidget(jobProgressWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobProgressWidget_All.sizePolicy().hasHeightForWidth())
        self.jobProgressWidget_All.setSizePolicy(sizePolicy)
        self.jobProgressWidget_All.setStyleSheet("QWidget#jobProgressWidget_All {\n"
"  border: 5px solid black;\n"
"  border-radius: 15px;\n"
"  background: azure\n"
"}")
        self.jobProgressWidget_All.setObjectName("jobProgressWidget_All")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.jobProgressWidget_All)
        self.verticalLayout.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headinglLayout = QtWidgets.QHBoxLayout()
        self.headinglLayout.setObjectName("headinglLayout")
        self.jobLabel = QtWidgets.QLabel(self.jobProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobLabel.sizePolicy().hasHeightForWidth())
        self.jobLabel.setSizePolicy(sizePolicy)
        self.jobLabel.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.jobLabel.setFont(font)
        self.jobLabel.setStyleSheet("QLabel {\n"
"  border-color:black;\n"
"  border-width: 4px;        \n"
"  border-style: solid;\n"
"  border-radius: 25px;\n"
"  margin:0px;\n"
"  padding:0px;\n"
"  color:black;\n"
"  background: white\n"
"}")
        self.jobLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.jobLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.jobLabel.setObjectName("jobLabel")
        self.headinglLayout.addWidget(self.jobLabel)
        self.jobCount = QtWidgets.QLineEdit(self.jobProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobCount.sizePolicy().hasHeightForWidth())
        self.jobCount.setSizePolicy(sizePolicy)
        self.jobCount.setMinimumSize(QtCore.QSize(97, 37))
        self.jobCount.setBaseSize(QtCore.QSize(91, 37))
        font = QtGui.QFont()
        font.setFamily("Digital-7")
        font.setPointSize(24)
        self.jobCount.setFont(font)
        self.jobCount.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.jobCount.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.jobCount.setText("0")
        self.jobCount.setMaxLength(100)
        self.jobCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.jobCount.setReadOnly(True)
        self.jobCount.setObjectName("jobCount")
        self.headinglLayout.addWidget(self.jobCount)
        self.displayJobButton = QtWidgets.QPushButton(self.jobProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayJobButton.sizePolicy().hasHeightForWidth())
        self.displayJobButton.setSizePolicy(sizePolicy)
        self.displayJobButton.setMinimumSize(QtCore.QSize(50, 50))
        self.displayJobButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displayJobButton.setFont(font)
        self.displayJobButton.setStyleSheet("QPushButton {\n"
"  border-color: black;\n"
"  border-width: 3px;        \n"
"  border-style: solid;\n"
"  border-radius: 25px;\n"
"  margin:0px;\n"
"  padding:0px;\n"
"  background: white\n"
"}\n"
"QPushButton#displayActionPushButton {\n"
"    qproperty-iconSize: 48px 48px; /* space for the background image */\n"
"}")
        self.displayJobButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/down_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/up_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.displayJobButton.setIcon(icon)
        self.displayJobButton.setIconSize(QtCore.QSize(48, 48))
        self.displayJobButton.setCheckable(True)
        self.displayJobButton.setChecked(True)
        self.displayJobButton.setObjectName("displayJobButton")
        self.headinglLayout.addWidget(self.displayJobButton)
        self.removeJobButton = QtWidgets.QPushButton(self.jobProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeJobButton.sizePolicy().hasHeightForWidth())
        self.removeJobButton.setSizePolicy(sizePolicy)
        self.removeJobButton.setMinimumSize(QtCore.QSize(50, 50))
        self.removeJobButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.removeJobButton.setFont(font)
        self.removeJobButton.setStyleSheet("QPushButton {\n"
"  border-color: darkred;\n"
"  border-width: 3px;        \n"
"  border-style: outset;\n"
"  border-radius: 25px;\n"
"  margin:0px;\n"
"  padding:0px;\n"
"  background: pink\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style: inset;\n"
"  background: rgb(255,160,180)\n"
"}")
        self.removeJobButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/icons/remove_x_symbol_red.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeJobButton.setIcon(icon1)
        self.removeJobButton.setIconSize(QtCore.QSize(26, 26))
        self.removeJobButton.setCheckable(False)
        self.removeJobButton.setChecked(False)
        self.removeJobButton.setObjectName("removeJobButton")
        self.headinglLayout.addWidget(self.removeJobButton)
        self.headinglLayout.setStretch(0, 100)
        self.headinglLayout.setStretch(1, 2)
        self.headinglLayout.setStretch(2, 1)
        self.headinglLayout.setStretch(3, 1)
        self.verticalLayout.addLayout(self.headinglLayout)
        self.jobProgressBar = QtWidgets.QProgressBar(self.jobProgressWidget_All)
        self.jobProgressBar.setStyleSheet("QProgressBar {\n"
"  border: 2px solid grey;\n"
"  border-radius: 12px;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"  border-radius: 10px;\n"
"  background-color: lightseagreen;\n"
"  border-color: lightseagreen;\n"
"}\n"
"\n"
"QProgressBar::chunk:indeterminate {\n"
"  border-radius: 10px;\n"
"  background-color: blue\n"
"}\n"
"")
        self.jobProgressBar.setMaximum(100)
        self.jobProgressBar.setProperty("value", 0)
        self.jobProgressBar.setTextVisible(True)
        self.jobProgressBar.setObjectName("jobProgressBar")
        self.verticalLayout.addWidget(self.jobProgressBar)
        self.actionsScrollArea = QtWidgets.QScrollArea(self.jobProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionsScrollArea.sizePolicy().hasHeightForWidth())
        self.actionsScrollArea.setSizePolicy(sizePolicy)
        self.actionsScrollArea.setStyleSheet("QScrollArea#actionsScrollArea {\n"
"background: snow;\n"
"border: 1px solid black;\n"
"border-radius: 15px;\n"
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
"  border: 1px solid lightseagreen;\n"
"  background:lightseagreen;\n"
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
        self.actionsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.actionsScrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.actionsScrollArea.setWidgetResizable(True)
        self.actionsScrollArea.setObjectName("actionsScrollArea")
        self.actionsScrollAreaWidgetContents = QtWidgets.QWidget()
        self.actionsScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 441, 303))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionsScrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.actionsScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.actionsScrollAreaWidgetContents.setStyleSheet("QWidget#actionsScrollAreaWidgetContents {\n"
" /*  border: 1px solid black;\n"
"  border-radius: 15px; */\n"
"  background: transparent\n"
"}")
        self.actionsScrollAreaWidgetContents.setObjectName("actionsScrollAreaWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.actionsScrollAreaWidgetContents)
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.actionsScrollArea.setWidget(self.actionsScrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.actionsScrollArea)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 100)
        self.verticalLayout_6.addWidget(self.jobProgressWidget_All)

        self.retranslateUi(jobProgressWidget)
        self.displayJobButton.toggled['bool'].connect(self.actionsScrollArea.setVisible)
        QtCore.QMetaObject.connectSlotsByName(jobProgressWidget)

    def retranslateUi(self, jobProgressWidget):
        _translate = QtCore.QCoreApplication.translate
        jobProgressWidget.setWindowTitle(_translate("jobProgressWidget", "Form"))
        self.jobLabel.setText(_translate("jobProgressWidget", "JOB"))
import resources_rc
