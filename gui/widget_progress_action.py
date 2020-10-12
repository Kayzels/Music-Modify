# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_progress_action.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_actionProgressWidget(object):
    def setupUi(self, actionProgressWidget):
        actionProgressWidget.setObjectName("actionProgressWidget")
        actionProgressWidget.resize(606, 364)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(actionProgressWidget.sizePolicy().hasHeightForWidth())
        actionProgressWidget.setSizePolicy(sizePolicy)
        actionProgressWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(actionProgressWidget)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.actionProgressWidget_All = QtWidgets.QWidget(actionProgressWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionProgressWidget_All.sizePolicy().hasHeightForWidth())
        self.actionProgressWidget_All.setSizePolicy(sizePolicy)
        self.actionProgressWidget_All.setMinimumSize(QtCore.QSize(0, 0))
        self.actionProgressWidget_All.setStyleSheet("QWidget#actionProgressWidget_All {\n"
"  border: 3px solid black;\n"
"  border-radius: 15px; \n"
"  background: rgb(245,245,255)\n"
"}")
        self.actionProgressWidget_All.setObjectName("actionProgressWidget_All")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.actionProgressWidget_All)
        self.verticalLayout.setObjectName("verticalLayout")
        self.actionHeading = QtWidgets.QWidget(self.actionProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionHeading.sizePolicy().hasHeightForWidth())
        self.actionHeading.setSizePolicy(sizePolicy)
        self.actionHeading.setMinimumSize(QtCore.QSize(0, 58))
        self.actionHeading.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.actionHeading.setObjectName("actionHeading")
        self.headingHLayout = QtWidgets.QHBoxLayout(self.actionHeading)
        self.headingHLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.headingHLayout.setContentsMargins(1, 4, 1, 4)
        self.headingHLayout.setObjectName("headingHLayout")
        self.actionLabel = QtWidgets.QLabel(self.actionHeading)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionLabel.sizePolicy().hasHeightForWidth())
        self.actionLabel.setSizePolicy(sizePolicy)
        self.actionLabel.setMinimumSize(QtCore.QSize(0, 50))
        self.actionLabel.setMaximumSize(QtCore.QSize(16777215, 50))
        self.actionLabel.setBaseSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.actionLabel.setFont(font)
        self.actionLabel.setStyleSheet("QLabel {\n"
"  border-color:black;\n"
"  border-width: 4px;        \n"
"  border-style: solid;\n"
"  border-radius: 25px;\n"
"  margin:0px;\n"
"  padding:0px;\n"
"  color:black;\n"
"  background: white\n"
"}")
        self.actionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.actionLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.actionLabel.setObjectName("actionLabel")
        self.headingHLayout.addWidget(self.actionLabel)
        self.displayActionPushButton = QtWidgets.QPushButton(self.actionHeading)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayActionPushButton.sizePolicy().hasHeightForWidth())
        self.displayActionPushButton.setSizePolicy(sizePolicy)
        self.displayActionPushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.displayActionPushButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displayActionPushButton.setFont(font)
        self.displayActionPushButton.setStyleSheet("QPushButton {\n"
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
        self.displayActionPushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/down_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/up_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.displayActionPushButton.setIcon(icon)
        self.displayActionPushButton.setIconSize(QtCore.QSize(48, 48))
        self.displayActionPushButton.setCheckable(True)
        self.displayActionPushButton.setChecked(True)
        self.displayActionPushButton.setObjectName("displayActionPushButton")
        self.headingHLayout.addWidget(self.displayActionPushButton)
        self.headingHLayout.setStretch(1, 1)
        self.verticalLayout.addWidget(self.actionHeading)
        self.actionProgressBar = QtWidgets.QProgressBar(self.actionProgressWidget_All)
        self.actionProgressBar.setStyleSheet("QProgressBar {\n"
"  border: 2px solid grey;\n"
"  border-radius: 12px;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"  border-radius: 10px;\n"
"  background-color: rgb(200, 200, 250);\n"
"  border-color: rgb(200, 200, 250);\n"
"}\n"
"")
        self.actionProgressBar.setProperty("value", 0)
        self.actionProgressBar.setObjectName("actionProgressBar")
        self.verticalLayout.addWidget(self.actionProgressBar)
        self.summaryWidget = QtWidgets.QWidget(self.actionProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.summaryWidget.sizePolicy().hasHeightForWidth())
        self.summaryWidget.setSizePolicy(sizePolicy)
        self.summaryWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.summaryWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.summaryWidget.setObjectName("summaryWidget")
        self.summaryHLayout_2 = QtWidgets.QHBoxLayout(self.summaryWidget)
        self.summaryHLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.summaryHLayout_2.setContentsMargins(1, 1, 1, 1)
        self.summaryHLayout_2.setSpacing(4)
        self.summaryHLayout_2.setObjectName("summaryHLayout_2")
        self.actionSummaryInfo = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionSummaryInfo.sizePolicy().hasHeightForWidth())
        self.actionSummaryInfo.setSizePolicy(sizePolicy)
        self.actionSummaryInfo.setMinimumSize(QtCore.QSize(125, 0))
        self.actionSummaryInfo.setObjectName("actionSummaryInfo")
        self.summaryActionVLayout_2 = QtWidgets.QVBoxLayout(self.actionSummaryInfo)
        self.summaryActionVLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.summaryActionVLayout_2.setContentsMargins(0, 0, 0, 0)
        self.summaryActionVLayout_2.setSpacing(4)
        self.summaryActionVLayout_2.setObjectName("summaryActionVLayout_2")
        self.actionInfoLabel = QtWidgets.QLabel(self.actionSummaryInfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionInfoLabel.sizePolicy().hasHeightForWidth())
        self.actionInfoLabel.setSizePolicy(sizePolicy)
        self.actionInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.actionInfoLabel.setObjectName("actionInfoLabel")
        self.summaryActionVLayout_2.addWidget(self.actionInfoLabel)
        self.actionInfo_Main = QtWidgets.QTextEdit(self.actionSummaryInfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionInfo_Main.sizePolicy().hasHeightForWidth())
        self.actionInfo_Main.setSizePolicy(sizePolicy)
        self.actionInfo_Main.setMinimumSize(QtCore.QSize(105, 37))
        self.actionInfo_Main.setMaximumSize(QtCore.QSize(16777215, 78))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.actionInfo_Main.setFont(font)
        self.actionInfo_Main.setStyleSheet("QTextEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  padding:3px;\n"
"  margin:0px\n"
"}")
        self.actionInfo_Main.setObjectName("actionInfo_Main")
        self.summaryActionVLayout_2.addWidget(self.actionInfo_Main)
        self.summaryHLayout_2.addWidget(self.actionSummaryInfo)
        self.tagsSummary = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsSummary.sizePolicy().hasHeightForWidth())
        self.tagsSummary.setSizePolicy(sizePolicy)
        self.tagsSummary.setMinimumSize(QtCore.QSize(91, 0))
        self.tagsSummary.setMaximumSize(QtCore.QSize(91, 16777215))
        self.tagsSummary.setObjectName("tagsSummary")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tagsSummary)
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tagsLabel = QtWidgets.QLabel(self.tagsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsLabel.sizePolicy().hasHeightForWidth())
        self.tagsLabel.setSizePolicy(sizePolicy)
        self.tagsLabel.setMinimumSize(QtCore.QSize(91, 0))
        self.tagsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tagsLabel.setObjectName("tagsLabel")
        self.verticalLayout_5.addWidget(self.tagsLabel)
        self.tagInfo_Main = QtWidgets.QTextEdit(self.tagsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagInfo_Main.sizePolicy().hasHeightForWidth())
        self.tagInfo_Main.setSizePolicy(sizePolicy)
        self.tagInfo_Main.setMinimumSize(QtCore.QSize(91, 37))
        self.tagInfo_Main.setMaximumSize(QtCore.QSize(16777215, 78))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tagInfo_Main.setFont(font)
        self.tagInfo_Main.setStyleSheet("QTextEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  padding:3px;\n"
"  margin:0px\n"
"}")
        self.tagInfo_Main.setObjectName("tagInfo_Main")
        self.verticalLayout_5.addWidget(self.tagInfo_Main)
        self.summaryHLayout_2.addWidget(self.tagsSummary)
        self.songsSummary = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songsSummary.sizePolicy().hasHeightForWidth())
        self.songsSummary.setSizePolicy(sizePolicy)
        self.songsSummary.setMinimumSize(QtCore.QSize(91, 0))
        self.songsSummary.setMaximumSize(QtCore.QSize(91, 16777215))
        self.songsSummary.setObjectName("songsSummary")
        self.summarySongsVLayout_2 = QtWidgets.QVBoxLayout(self.songsSummary)
        self.summarySongsVLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.summarySongsVLayout_2.setContentsMargins(0, 0, 0, 0)
        self.summarySongsVLayout_2.setSpacing(4)
        self.summarySongsVLayout_2.setObjectName("summarySongsVLayout_2")
        self.songsLabel = QtWidgets.QLabel(self.songsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songsLabel.sizePolicy().hasHeightForWidth())
        self.songsLabel.setSizePolicy(sizePolicy)
        self.songsLabel.setMinimumSize(QtCore.QSize(91, 0))
        self.songsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.songsLabel.setObjectName("songsLabel")
        self.summarySongsVLayout_2.addWidget(self.songsLabel)
        self.songCount_Main = QtWidgets.QLineEdit(self.songsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songCount_Main.sizePolicy().hasHeightForWidth())
        self.songCount_Main.setSizePolicy(sizePolicy)
        self.songCount_Main.setMinimumSize(QtCore.QSize(91, 37))
        self.songCount_Main.setMaximumSize(QtCore.QSize(91, 37))
        self.songCount_Main.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.songCount_Main.setFont(font)
        self.songCount_Main.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.songCount_Main.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.songCount_Main.setText("0")
        self.songCount_Main.setMaxLength(100)
        self.songCount_Main.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.songCount_Main.setReadOnly(True)
        self.songCount_Main.setObjectName("songCount_Main")
        self.summarySongsVLayout_2.addWidget(self.songCount_Main)
        self.songsCustomName_Main = QtWidgets.QLineEdit(self.songsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songsCustomName_Main.sizePolicy().hasHeightForWidth())
        self.songsCustomName_Main.setSizePolicy(sizePolicy)
        self.songsCustomName_Main.setMinimumSize(QtCore.QSize(91, 37))
        self.songsCustomName_Main.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.songsCustomName_Main.setFont(font)
        self.songsCustomName_Main.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.songsCustomName_Main.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.songsCustomName_Main.setText("")
        self.songsCustomName_Main.setMaxLength(103)
        self.songsCustomName_Main.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.songsCustomName_Main.setReadOnly(False)
        self.songsCustomName_Main.setObjectName("songsCustomName_Main")
        self.summarySongsVLayout_2.addWidget(self.songsCustomName_Main)
        self.summaryHLayout_2.addWidget(self.songsSummary)
        self.valuesSummary = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valuesSummary.sizePolicy().hasHeightForWidth())
        self.valuesSummary.setSizePolicy(sizePolicy)
        self.valuesSummary.setMinimumSize(QtCore.QSize(91, 0))
        self.valuesSummary.setMaximumSize(QtCore.QSize(91, 16777215))
        self.valuesSummary.setBaseSize(QtCore.QSize(265, 0))
        self.valuesSummary.setObjectName("valuesSummary")
        self.summaryValuesVLayout_2 = QtWidgets.QVBoxLayout(self.valuesSummary)
        self.summaryValuesVLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.summaryValuesVLayout_2.setContentsMargins(0, 0, 0, 0)
        self.summaryValuesVLayout_2.setSpacing(4)
        self.summaryValuesVLayout_2.setObjectName("summaryValuesVLayout_2")
        self.valuesLabel = QtWidgets.QLabel(self.valuesSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valuesLabel.sizePolicy().hasHeightForWidth())
        self.valuesLabel.setSizePolicy(sizePolicy)
        self.valuesLabel.setMinimumSize(QtCore.QSize(91, 0))
        self.valuesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.valuesLabel.setObjectName("valuesLabel")
        self.summaryValuesVLayout_2.addWidget(self.valuesLabel)
        self.valueCount_Main = QtWidgets.QLineEdit(self.valuesSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valueCount_Main.sizePolicy().hasHeightForWidth())
        self.valueCount_Main.setSizePolicy(sizePolicy)
        self.valueCount_Main.setMinimumSize(QtCore.QSize(91, 37))
        self.valueCount_Main.setMaximumSize(QtCore.QSize(91, 37))
        self.valueCount_Main.setBaseSize(QtCore.QSize(91, 37))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.valueCount_Main.setFont(font)
        self.valueCount_Main.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.valueCount_Main.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.valueCount_Main.setText("0")
        self.valueCount_Main.setMaxLength(100)
        self.valueCount_Main.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.valueCount_Main.setReadOnly(True)
        self.valueCount_Main.setObjectName("valueCount_Main")
        self.summaryValuesVLayout_2.addWidget(self.valueCount_Main)
        self.valuesCustomName_Main = QtWidgets.QLineEdit(self.valuesSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valuesCustomName_Main.sizePolicy().hasHeightForWidth())
        self.valuesCustomName_Main.setSizePolicy(sizePolicy)
        self.valuesCustomName_Main.setMinimumSize(QtCore.QSize(91, 37))
        self.valuesCustomName_Main.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.valuesCustomName_Main.setFont(font)
        self.valuesCustomName_Main.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.valuesCustomName_Main.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.valuesCustomName_Main.setText("")
        self.valuesCustomName_Main.setMaxLength(103)
        self.valuesCustomName_Main.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.valuesCustomName_Main.setReadOnly(False)
        self.valuesCustomName_Main.setObjectName("valuesCustomName_Main")
        self.summaryValuesVLayout_2.addWidget(self.valuesCustomName_Main)
        self.summaryHLayout_2.addWidget(self.valuesSummary)
        self.discogsSummary = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsSummary.sizePolicy().hasHeightForWidth())
        self.discogsSummary.setSizePolicy(sizePolicy)
        self.discogsSummary.setMinimumSize(QtCore.QSize(125, 0))
        self.discogsSummary.setObjectName("discogsSummary")
        self.summaryActionVLayout_3 = QtWidgets.QVBoxLayout(self.discogsSummary)
        self.summaryActionVLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.summaryActionVLayout_3.setContentsMargins(0, 0, 0, 0)
        self.summaryActionVLayout_3.setSpacing(4)
        self.summaryActionVLayout_3.setObjectName("summaryActionVLayout_3")
        self.discogsReleaseIDLabel = QtWidgets.QLabel(self.discogsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsReleaseIDLabel.sizePolicy().hasHeightForWidth())
        self.discogsReleaseIDLabel.setSizePolicy(sizePolicy)
        self.discogsReleaseIDLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.discogsReleaseIDLabel.setObjectName("discogsReleaseIDLabel")
        self.summaryActionVLayout_3.addWidget(self.discogsReleaseIDLabel)
        self.discogsReleaseID_Main = QtWidgets.QTextEdit(self.discogsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsReleaseID_Main.sizePolicy().hasHeightForWidth())
        self.discogsReleaseID_Main.setSizePolicy(sizePolicy)
        self.discogsReleaseID_Main.setMinimumSize(QtCore.QSize(105, 37))
        self.discogsReleaseID_Main.setMaximumSize(QtCore.QSize(16777215, 78))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.discogsReleaseID_Main.setFont(font)
        self.discogsReleaseID_Main.setStyleSheet("QTextEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  padding:3px;\n"
"  margin:0px\n"
"}")
        self.discogsReleaseID_Main.setObjectName("discogsReleaseID_Main")
        self.summaryActionVLayout_3.addWidget(self.discogsReleaseID_Main)
        self.summaryHLayout_2.addWidget(self.discogsSummary)
        self.verticalLayout.addWidget(self.summaryWidget)
        self.subactionsHeadingWidget = QtWidgets.QWidget(self.actionProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subactionsHeadingWidget.sizePolicy().hasHeightForWidth())
        self.subactionsHeadingWidget.setSizePolicy(sizePolicy)
        self.subactionsHeadingWidget.setMinimumSize(QtCore.QSize(0, 59))
        self.subactionsHeadingWidget.setMaximumSize(QtCore.QSize(16777215, 59))
        self.subactionsHeadingWidget.setObjectName("subactionsHeadingWidget")
        self.subactionsHeadingLayout = QtWidgets.QHBoxLayout(self.subactionsHeadingWidget)
        self.subactionsHeadingLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.subactionsHeadingLayout.setContentsMargins(0, 9, 0, 0)
        self.subactionsHeadingLayout.setObjectName("subactionsHeadingLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.subactionsHeadingLayout.addItem(spacerItem)
        self.subactionsLabel = QtWidgets.QLabel(self.subactionsHeadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subactionsLabel.sizePolicy().hasHeightForWidth())
        self.subactionsLabel.setSizePolicy(sizePolicy)
        self.subactionsLabel.setMinimumSize(QtCore.QSize(0, 50))
        self.subactionsLabel.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.subactionsLabel.setFont(font)
        self.subactionsLabel.setStyleSheet("QLabel {\n"
"  border-color:black;\n"
"  border-width: 2px;        \n"
"  border-style: solid;\n"
"  border-radius: 25px;\n"
"  margin:0px;\n"
"  padding:0px;\n"
"  color:black;\n"
"  background: white\n"
"}")
        self.subactionsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.subactionsLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.subactionsLabel.setObjectName("subactionsLabel")
        self.subactionsHeadingLayout.addWidget(self.subactionsLabel)
        self.displaySubactionsPushButton = QtWidgets.QPushButton(self.subactionsHeadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displaySubactionsPushButton.sizePolicy().hasHeightForWidth())
        self.displaySubactionsPushButton.setSizePolicy(sizePolicy)
        self.displaySubactionsPushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.displaySubactionsPushButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displaySubactionsPushButton.setFont(font)
        self.displaySubactionsPushButton.setStyleSheet("QPushButton {\n"
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
        self.displaySubactionsPushButton.setText("")
        self.displaySubactionsPushButton.setIcon(icon)
        self.displaySubactionsPushButton.setIconSize(QtCore.QSize(48, 48))
        self.displaySubactionsPushButton.setCheckable(True)
        self.displaySubactionsPushButton.setChecked(True)
        self.displaySubactionsPushButton.setObjectName("displaySubactionsPushButton")
        self.subactionsHeadingLayout.addWidget(self.displaySubactionsPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.subactionsHeadingLayout.addItem(spacerItem1)
        self.subactionsHeadingLayout.setStretch(1, 8)
        self.subactionsHeadingLayout.setStretch(2, 1)
        self.verticalLayout.addWidget(self.subactionsHeadingWidget)
        self.subactionsScrollArea = QtWidgets.QScrollArea(self.actionProgressWidget_All)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subactionsScrollArea.sizePolicy().hasHeightForWidth())
        self.subactionsScrollArea.setSizePolicy(sizePolicy)
        self.subactionsScrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.subactionsScrollArea.setStyleSheet("QScrollArea#subactionsScrollArea {\n"
"background: snow;\n"
"border-radius: 15px;\n"
"border: 1px solid black\n"
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
"  border: 1px solid rgb(200,200,250);\n"
"  background-color: rgb(200, 200, 250);\n"
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
        self.subactionsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.subactionsScrollArea.setWidgetResizable(True)
        self.subactionsScrollArea.setObjectName("subactionsScrollArea")
        self.subactionsScrollAreaWidgetContents = QtWidgets.QWidget()
        self.subactionsScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 586, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subactionsScrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.subactionsScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.subactionsScrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.subactionsScrollAreaWidgetContents.setStyleSheet("QWidget#subactionsScrollAreaWidgetContents {\n"
"  /*border: 1px solid black;\n"
"  border-radius: 15px;*/\n"
"  background: transparent\n"
"}")
        self.subactionsScrollAreaWidgetContents.setObjectName("subactionsScrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.subactionsScrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.subactionsScrollArea.setWidget(self.subactionsScrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.subactionsScrollArea)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 10)
        self.verticalLayout_4.addWidget(self.actionProgressWidget_All)

        self.retranslateUi(actionProgressWidget)
        self.displaySubactionsPushButton.toggled['bool'].connect(self.subactionsScrollArea.setVisible)
        self.displayActionPushButton.toggled['bool'].connect(self.summaryWidget.setVisible)
        QtCore.QMetaObject.connectSlotsByName(actionProgressWidget)

    def retranslateUi(self, actionProgressWidget):
        _translate = QtCore.QCoreApplication.translate
        actionProgressWidget.setWindowTitle(_translate("actionProgressWidget", "Form"))
        self.actionLabel.setText(_translate("actionProgressWidget", "ACTION"))
        self.actionInfoLabel.setText(_translate("actionProgressWidget", "Action"))
        self.actionInfo_Main.setHtml(_translate("actionProgressWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No Action</p></body></html>"))
        self.tagsLabel.setText(_translate("actionProgressWidget", "Tags"))
        self.tagInfo_Main.setHtml(_translate("actionProgressWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No Tags</p></body></html>"))
        self.songsLabel.setText(_translate("actionProgressWidget", "Songs"))
        self.songsCustomName_Main.setPlaceholderText(_translate("actionProgressWidget", "Label"))
        self.valuesLabel.setText(_translate("actionProgressWidget", "Values"))
        self.valuesCustomName_Main.setPlaceholderText(_translate("actionProgressWidget", "Label"))
        self.discogsReleaseIDLabel.setText(_translate("actionProgressWidget", "Discogs"))
        self.discogsReleaseID_Main.setHtml(_translate("actionProgressWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No ID</p></body></html>"))
        self.subactionsLabel.setText(_translate("actionProgressWidget", "SUBACTIONS"))
import resources_rc
