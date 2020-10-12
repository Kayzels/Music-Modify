# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window_main.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(997, 902)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/music_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {border: 1px solid grey; border-radius: 15px}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setContentsMargins(9, -1, -1, 9)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.filesButtonsWidget = QtWidgets.QWidget(self.centralwidget)
        self.filesButtonsWidget.setStyleSheet("QPushButton {  \n"
"  border-width: 3px;\n"
"  border-style: outset;\n"
"  border-radius: 18px\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"  color:grey;\n"
"  background-color:lightgrey\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style: inset\n"
"}")
        self.filesButtonsWidget.setObjectName("filesButtonsWidget")
        self.filesButtonsHorizontalLayout = QtWidgets.QHBoxLayout(self.filesButtonsWidget)
        self.filesButtonsHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.filesButtonsHorizontalLayout.setObjectName("filesButtonsHorizontalLayout")
        self.addFilesButton = QtWidgets.QPushButton(self.filesButtonsWidget)
        self.addFilesButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addFilesButton.sizePolicy().hasHeightForWidth())
        self.addFilesButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.addFilesButton.setFont(font)
        self.addFilesButton.setStyleSheet("QPushButton:enabled {\n"
"  border-color:green;\n"
"  background: rgb(200,240,200);\n"
"  color:green;\n"
"  border-style: outset\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: rgb(120, 200, 120);\n"
"  border-style: inset\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/icons/plus_icon_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addFilesButton.setIcon(icon1)
        self.addFilesButton.setIconSize(QtCore.QSize(32, 32))
        self.addFilesButton.setObjectName("addFilesButton")
        self.filesButtonsHorizontalLayout.addWidget(self.addFilesButton)
        self.addFolderButton = QtWidgets.QPushButton(self.filesButtonsWidget)
        self.addFolderButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addFolderButton.sizePolicy().hasHeightForWidth())
        self.addFolderButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.addFolderButton.setFont(font)
        self.addFolderButton.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.addFolderButton.setAutoFillBackground(False)
        self.addFolderButton.setStyleSheet("QPushButton:enabled {\n"
"  border-color:rgb(250,100,50);\n"
"  background: navajowhite;\n"
"  color:rgb(250,100,50)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: rgb(255, 200, 120)\n"
"}")
        self.addFolderButton.setText("ADD FOLDER")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/resources/icons/folder_icon_circle_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addFolderButton.setIcon(icon2)
        self.addFolderButton.setIconSize(QtCore.QSize(32, 32))
        self.addFolderButton.setObjectName("addFolderButton")
        self.filesButtonsHorizontalLayout.addWidget(self.addFolderButton)
        self.clearFilesButton = QtWidgets.QPushButton(self.filesButtonsWidget)
        self.clearFilesButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearFilesButton.sizePolicy().hasHeightForWidth())
        self.clearFilesButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.clearFilesButton.setFont(font)
        self.clearFilesButton.setStyleSheet("QPushButton:enabled {\n"
"  border-color:red;\n"
"  background:pink;\n"
"  color:darkred\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: rgb(255, 160, 180)\n"
"}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/resources/icons/minus_icon_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearFilesButton.setIcon(icon3)
        self.clearFilesButton.setIconSize(QtCore.QSize(32, 32))
        self.clearFilesButton.setObjectName("clearFilesButton")
        self.filesButtonsHorizontalLayout.addWidget(self.clearFilesButton)
        self.refreshButton = QtWidgets.QPushButton(self.filesButtonsWidget)
        self.refreshButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.refreshButton.setFont(font)
        self.refreshButton.setStyleSheet("QPushButton:enabled {\n"
"  border-color:rgb(0,115,150);\n"
"  background: lightblue;\n"
"  color: rgb(0,115,150)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: lightsteelblue\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/resources/icons/refresh_icon_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon4)
        self.refreshButton.setIconSize(QtCore.QSize(32, 32))
        self.refreshButton.setObjectName("refreshButton")
        self.filesButtonsHorizontalLayout.addWidget(self.refreshButton)
        self.filesButtonsHorizontalLayout.setStretch(0, 1)
        self.filesButtonsHorizontalLayout.setStretch(1, 1)
        self.filesButtonsHorizontalLayout.setStretch(2, 1)
        self.filesButtonsHorizontalLayout.setStretch(3, 1)
        self.verticalLayout.addWidget(self.filesButtonsWidget)
        self.filesTableView = QtWidgets.QTableView(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.filesTableView.setFont(font)
        self.filesTableView.setStyleSheet("QTableView QTableCornerButton::section {\n"
"  background-color: lavender;\n"
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
"  background-color: lavender;\n"
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
"  background-color: lavender;\n"
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
"  margin-top:3px;\n"
"  margin-bottom:3px;\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 15px;\n"
"  background-color:white;\n"
"  alternate-background-color: rgb(245, 245, 255);\n"
"  gridline-color: lavender\n"
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
        self.filesTableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.filesTableView.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.filesTableView.setAlternatingRowColors(True)
        self.filesTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.filesTableView.setObjectName("filesTableView")
        self.filesTableView.verticalHeader().setCascadingSectionResizes(True)
        self.verticalLayout.addWidget(self.filesTableView)
        self.selectionButtonsWidget = QtWidgets.QWidget(self.centralwidget)
        self.selectionButtonsWidget.setStyleSheet("QPushButton  {\n"
"  border-width: 2px;\n"
"  border-style: outset;\n"
"  border-radius: 9px\n"
"}\n"
"QPushButton:disabled {\n"
"  color:grey;\n"
"  background-color:lightgrey\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style:inset\n"
"}")
        self.selectionButtonsWidget.setObjectName("selectionButtonsWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.selectionButtonsWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.selectAllFilesButton = QtWidgets.QPushButton(self.selectionButtonsWidget)
        self.selectAllFilesButton.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectAllFilesButton.setFont(font)
        self.selectAllFilesButton.setStyleSheet("QPushButton:enabled {\n"
"  border-color:rgb(0,115,150);\n"
"  background: lightblue;\n"
"  color:rgb(0,115,150)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: lightsteelblue\n"
"}")
        self.selectAllFilesButton.setObjectName("selectAllFilesButton")
        self.horizontalLayout.addWidget(self.selectAllFilesButton)
        self.selectNoFilesButton = QtWidgets.QPushButton(self.selectionButtonsWidget)
        self.selectNoFilesButton.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectNoFilesButton.setFont(font)
        self.selectNoFilesButton.setStyleSheet("QPushButton:enabled {\n"
"  border-color:rgb(0,115,150);\n"
"  background: lightblue;\n"
"  color:rgb(0,115,150)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: lightsteelblue\n"
"}")
        self.selectNoFilesButton.setObjectName("selectNoFilesButton")
        self.horizontalLayout.addWidget(self.selectNoFilesButton)
        self.removeSelectedButton = QtWidgets.QPushButton(self.selectionButtonsWidget)
        self.removeSelectedButton.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.removeSelectedButton.setFont(font)
        self.removeSelectedButton.setStyleSheet("QPushButton:enabled {\n"
"  border-color:red;\n"
"  background:pink;\n"
"  color:darkred\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: rgb(255, 160, 180)\n"
"}")
        self.removeSelectedButton.setObjectName("removeSelectedButton")
        self.horizontalLayout.addWidget(self.removeSelectedButton)
        self.verticalLayout.addWidget(self.selectionButtonsWidget)
        self.jobPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.jobPushButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.jobPushButton.sizePolicy().hasHeightForWidth())
        self.jobPushButton.setSizePolicy(sizePolicy)
        self.jobPushButton.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.jobPushButton.setFont(font)
        self.jobPushButton.setStyleSheet("QPushButton {\n"
"  border-radius:14px;\n"
"  border-width: 3px;\n"
"  border-style: outset;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"  color:grey;\n"
"  background-color:lightgrey\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style:inset;\n"
"  background: rgb(170, 170, 255)\n"
"}\n"
"\n"
"QPushButton:enabled {\n"
"  border-color:rgb(100,100,215);\n"
"  background: rgb(200,200,250);\n"
"  color: rgb(100,100,215);\n"
"}\n"
"QPushButton::menu-indicator {\n"
"  image: url(:/icons/icons/down_icon.png);\n"
"  width:20px;\n"
"  height:20px;\n"
"  subcontrol-position: right center\n"
"}\n"
"QPushButton QMenu {\n"
"  font-size:14pt;\n"
"  border-color:rgb(100,100,215);\n"
"  border-width: 2px;        \n"
"  border-style: solid;\n"
"  background-color:rgb(240,230,255);\n"
"  color:rgb(100,100,215);\n"
"  margin:2px;\n"
"}\n"
"QPushButton QMenu::item {\n"
"  background:transparent\n"
"}\n"
"QPushButton QMenu::item::selected{\n"
"  background-color:rgb(200,200,250)\n"
"}")
        self.jobPushButton.setObjectName("jobPushButton")
        self.verticalLayout.addWidget(self.jobPushButton)
        self.verticalLayout_6.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 997, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuSelection = QtWidgets.QMenu(self.menubar)
        self.menuSelection.setObjectName("menuSelection")
        self.menuJobs = QtWidgets.QMenu(self.menubar)
        self.menuJobs.setObjectName("menuJobs")
        MainWindow.setMenuBar(self.menubar)
        self.mainStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.mainStatusBar.setObjectName("mainStatusBar")
        MainWindow.setStatusBar(self.mainStatusBar)
        self.actionAdd_Folder = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../../Music Modify 2/icons/folder_icon_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Folder.setIcon(icon5)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.actionAdd_Folder.setFont(font)
        self.actionAdd_Folder.setObjectName("actionAdd_Folder")
        self.actionClear_Files = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../../Music Modify 2/icons/minus_icon_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClear_Files.setIcon(icon6)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.actionClear_Files.setFont(font)
        self.actionClear_Files.setObjectName("actionClear_Files")
        self.actionAdd_Files = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../../Music Modify 2/icons/plus_icon_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Files.setIcon(icon7)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.actionAdd_Files.setFont(font)
        self.actionAdd_Files.setObjectName("actionAdd_Files")
        self.actionRefresh_Files = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../../Music Modify 2/icons/refresh_icon_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh_Files.setIcon(icon8)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.actionRefresh_Files.setFont(font)
        self.actionRefresh_Files.setObjectName("actionRefresh_Files")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionCurrent_Jobs = QtWidgets.QAction(MainWindow)
        self.actionCurrent_Jobs.setCheckable(True)
        self.actionCurrent_Jobs.setObjectName("actionCurrent_Jobs")
        self.actionSelect_All = QtWidgets.QAction(MainWindow)
        self.actionSelect_All.setObjectName("actionSelect_All")
        self.actionSelect_None = QtWidgets.QAction(MainWindow)
        self.actionSelect_None.setObjectName("actionSelect_None")
        self.actionNew_Job = QtWidgets.QAction(MainWindow)
        self.actionNew_Job.setObjectName("actionNew_Job")
        self.actionRemove_Selected_Files = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.actionRemove_Selected_Files.setFont(font)
        self.actionRemove_Selected_Files.setObjectName("actionRemove_Selected_Files")
        self.actionManual_Editing = QtWidgets.QAction(MainWindow)
        self.actionManual_Editing.setObjectName("actionManual_Editing")
        self.actionDownload_Data = QtWidgets.QAction(MainWindow)
        self.actionDownload_Data.setObjectName("actionDownload_Data")
        self.actionOrganise_Artwork = QtWidgets.QAction(MainWindow)
        self.actionOrganise_Artwork.setObjectName("actionOrganise_Artwork")
        self.actionImport_Replace_Sheet = QtWidgets.QAction(MainWindow)
        self.actionImport_Replace_Sheet.setObjectName("actionImport_Replace_Sheet")
        self.actionCreate_New_Job = QtWidgets.QAction(MainWindow)
        self.actionCreate_New_Job.setObjectName("actionCreate_New_Job")
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionAdd_Files)
        self.menuFile.addAction(self.actionAdd_Folder)
        self.menuFile.addAction(self.actionClear_Files)
        self.menuFile.addAction(self.actionRefresh_Files)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRemove_Selected_Files)
        self.menuView.addAction(self.actionCurrent_Jobs)
        self.menuSelection.addAction(self.actionSelect_All)
        self.menuSelection.addAction(self.actionSelect_None)
        self.menuJobs.addAction(self.actionCreate_New_Job)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSelection.menuAction())
        self.menubar.addAction(self.menuJobs.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Music Modify"))
        self.addFilesButton.setText(_translate("MainWindow", "ADD FILES"))
        self.clearFilesButton.setText(_translate("MainWindow", "CLEAR FILES"))
        self.refreshButton.setText(_translate("MainWindow", "REFRESH"))
        self.selectAllFilesButton.setText(_translate("MainWindow", "SELECT ALL"))
        self.selectNoFilesButton.setText(_translate("MainWindow", "SELECT NONE"))
        self.removeSelectedButton.setText(_translate("MainWindow", "REMOVE SELECTED FILES"))
        self.jobPushButton.setText(_translate("MainWindow", "NEW JOB"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuSelection.setTitle(_translate("MainWindow", "Selection"))
        self.menuJobs.setTitle(_translate("MainWindow", "Jobs"))
        self.actionAdd_Folder.setText(_translate("MainWindow", "Add Folder"))
        self.actionClear_Files.setText(_translate("MainWindow", "Clear Files"))
        self.actionAdd_Files.setText(_translate("MainWindow", "Add Files"))
        self.actionRefresh_Files.setText(_translate("MainWindow", "Refresh Files"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionCurrent_Jobs.setText(_translate("MainWindow", "Current Jobs"))
        self.actionSelect_All.setText(_translate("MainWindow", "Select All"))
        self.actionSelect_None.setText(_translate("MainWindow", "Select None"))
        self.actionNew_Job.setText(_translate("MainWindow", "New Job"))
        self.actionRemove_Selected_Files.setText(_translate("MainWindow", "Remove Selected Files"))
        self.actionManual_Editing.setText(_translate("MainWindow", "Manual Editing"))
        self.actionDownload_Data.setText(_translate("MainWindow", "Download Data"))
        self.actionOrganise_Artwork.setText(_translate("MainWindow", "Organise Artwork"))
        self.actionImport_Replace_Sheet.setText(_translate("MainWindow", "Import Replace Sheet"))
        self.actionCreate_New_Job.setText(_translate("MainWindow", "Create New Job"))
import resources_rc
