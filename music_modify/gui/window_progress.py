# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window_progress.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgressWindow(object):
    def setupUi(self, ProgressWindow):
        ProgressWindow.setObjectName("ProgressWindow")
        ProgressWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/music_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ProgressWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ProgressWindow)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {border: 1px solid grey; border-radius: 15px}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.jobCountHeadingWidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobCountHeadingWidget.sizePolicy().hasHeightForWidth())
        self.jobCountHeadingWidget.setSizePolicy(sizePolicy)
        self.jobCountHeadingWidget.setObjectName("jobCountHeadingWidget")
        self.headingHLayout = QtWidgets.QHBoxLayout(self.jobCountHeadingWidget)
        self.headingHLayout.setContentsMargins(4, 4, 4, 4)
        self.headingHLayout.setSpacing(6)
        self.headingHLayout.setObjectName("headingHLayout")
        self.jobLabel = QtWidgets.QLabel(self.jobCountHeadingWidget)
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
"  border-width: 6px;        \n"
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
        self.headingHLayout.addWidget(self.jobLabel)
        self.activeJobsSummary = QtWidgets.QWidget(self.jobCountHeadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.activeJobsSummary.sizePolicy().hasHeightForWidth())
        self.activeJobsSummary.setSizePolicy(sizePolicy)
        self.activeJobsSummary.setMinimumSize(QtCore.QSize(91, 0))
        self.activeJobsSummary.setBaseSize(QtCore.QSize(265, 0))
        self.activeJobsSummary.setObjectName("activeJobsSummary")
        self.summaryValuesVLayout_2 = QtWidgets.QVBoxLayout(self.activeJobsSummary)
        self.summaryValuesVLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.summaryValuesVLayout_2.setContentsMargins(0, 0, 0, 0)
        self.summaryValuesVLayout_2.setSpacing(4)
        self.summaryValuesVLayout_2.setObjectName("summaryValuesVLayout_2")
        self.activeJobsLabel = QtWidgets.QLabel(self.activeJobsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.activeJobsLabel.sizePolicy().hasHeightForWidth())
        self.activeJobsLabel.setSizePolicy(sizePolicy)
        self.activeJobsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.activeJobsLabel.setObjectName("activeJobsLabel")
        self.summaryValuesVLayout_2.addWidget(self.activeJobsLabel)
        self.activeJobsCount = QtWidgets.QLineEdit(self.activeJobsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.activeJobsCount.sizePolicy().hasHeightForWidth())
        self.activeJobsCount.setSizePolicy(sizePolicy)
        self.activeJobsCount.setMinimumSize(QtCore.QSize(91, 37))
        self.activeJobsCount.setBaseSize(QtCore.QSize(91, 37))
        font = QtGui.QFont()
        font.setFamily("Digital-7")
        font.setPointSize(24)
        self.activeJobsCount.setFont(font)
        self.activeJobsCount.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.activeJobsCount.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.activeJobsCount.setText("0")
        self.activeJobsCount.setMaxLength(100)
        self.activeJobsCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.activeJobsCount.setReadOnly(True)
        self.activeJobsCount.setObjectName("activeJobsCount")
        self.summaryValuesVLayout_2.addWidget(self.activeJobsCount)
        self.headingHLayout.addWidget(self.activeJobsSummary)
        self.jobsShownSummary = QtWidgets.QWidget(self.jobCountHeadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobsShownSummary.sizePolicy().hasHeightForWidth())
        self.jobsShownSummary.setSizePolicy(sizePolicy)
        self.jobsShownSummary.setMinimumSize(QtCore.QSize(91, 0))
        self.jobsShownSummary.setObjectName("jobsShownSummary")
        self.summarySongsVLayout_2 = QtWidgets.QVBoxLayout(self.jobsShownSummary)
        self.summarySongsVLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.summarySongsVLayout_2.setContentsMargins(0, 0, 0, 0)
        self.summarySongsVLayout_2.setSpacing(4)
        self.summarySongsVLayout_2.setObjectName("summarySongsVLayout_2")
        self.jobsShownLabel = QtWidgets.QLabel(self.jobsShownSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobsShownLabel.sizePolicy().hasHeightForWidth())
        self.jobsShownLabel.setSizePolicy(sizePolicy)
        self.jobsShownLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.jobsShownLabel.setObjectName("jobsShownLabel")
        self.summarySongsVLayout_2.addWidget(self.jobsShownLabel)
        self.jobsShownCount = QtWidgets.QLineEdit(self.jobsShownSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobsShownCount.sizePolicy().hasHeightForWidth())
        self.jobsShownCount.setSizePolicy(sizePolicy)
        self.jobsShownCount.setMinimumSize(QtCore.QSize(91, 37))
        self.jobsShownCount.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setFamily("Digital-7")
        font.setPointSize(24)
        self.jobsShownCount.setFont(font)
        self.jobsShownCount.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.jobsShownCount.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.jobsShownCount.setText("0")
        self.jobsShownCount.setMaxLength(100)
        self.jobsShownCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.jobsShownCount.setReadOnly(True)
        self.jobsShownCount.setObjectName("jobsShownCount")
        self.summarySongsVLayout_2.addWidget(self.jobsShownCount)
        self.headingHLayout.addWidget(self.jobsShownSummary)
        self.headingHLayout.setStretch(0, 10)
        self.headingHLayout.setStretch(1, 2)
        self.headingHLayout.setStretch(2, 2)
        self.verticalLayout.addWidget(self.jobCountHeadingWidget)
        self.jobsScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobsScrollArea.sizePolicy().hasHeightForWidth())
        self.jobsScrollArea.setSizePolicy(sizePolicy)
        self.jobsScrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.jobsScrollArea.setStyleSheet("QScrollArea#jobsScrollArea {\n"
"  border: 2px solid black;\n"
"  border-radius: 15px;\n"
"  background: snow\n"
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
        self.jobsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.jobsScrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.jobsScrollArea.setWidgetResizable(True)
        self.jobsScrollArea.setObjectName("jobsScrollArea")
        self.jobsScrollAreaWidgetContents = QtWidgets.QWidget()
        self.jobsScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 788, 433))
        self.jobsScrollAreaWidgetContents.setStyleSheet("QWidget#jobsScrollAreaWidgetContents {\n"
"  /*border: 2px solid black;\n"
"  border-radius: 15px;*/\n"
"  background: transparent\n"
"}")
        self.jobsScrollAreaWidgetContents.setObjectName("jobsScrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.jobsScrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.innerSpacerWidget = QtWidgets.QWidget(self.jobsScrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.innerSpacerWidget.sizePolicy().hasHeightForWidth())
        self.innerSpacerWidget.setSizePolicy(sizePolicy)
        self.innerSpacerWidget.setObjectName("innerSpacerWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.innerSpacerWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.innerSpacerWidget)
        self.jobsScrollArea.setWidget(self.jobsScrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.jobsScrollArea)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 100)
        ProgressWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ProgressWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuJobs = QtWidgets.QMenu(self.menubar)
        self.menuJobs.setObjectName("menuJobs")
        ProgressWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ProgressWindow)
        self.statusbar.setObjectName("statusbar")
        ProgressWindow.setStatusBar(self.statusbar)
        self.actionShow_Main_Window = QtWidgets.QAction(ProgressWindow)
        self.actionShow_Main_Window.setCheckable(True)
        self.actionShow_Main_Window.setChecked(True)
        self.actionShow_Main_Window.setObjectName("actionShow_Main_Window")
        self.actionClear_Jobs = QtWidgets.QAction(ProgressWindow)
        self.actionClear_Jobs.setObjectName("actionClear_Jobs")
        self.menuView.addAction(self.actionShow_Main_Window)
        self.menuJobs.addAction(self.actionClear_Jobs)
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuJobs.menuAction())

        self.retranslateUi(ProgressWindow)
        QtCore.QMetaObject.connectSlotsByName(ProgressWindow)

    def retranslateUi(self, ProgressWindow):
        _translate = QtCore.QCoreApplication.translate
        ProgressWindow.setWindowTitle(_translate("ProgressWindow", "Progress Window"))
        self.jobLabel.setText(_translate("ProgressWindow", "JOB COUNT"))
        self.activeJobsLabel.setText(_translate("ProgressWindow", "Active Jobs"))
        self.jobsShownLabel.setText(_translate("ProgressWindow", "Jobs Shown"))
        self.menuView.setTitle(_translate("ProgressWindow", "View"))
        self.menuJobs.setTitle(_translate("ProgressWindow", "Jobs"))
        self.actionShow_Main_Window.setText(_translate("ProgressWindow", "Show Main Window"))
        self.actionClear_Jobs.setText(_translate("ProgressWindow", "Clear Jobs"))
import resources_rc
