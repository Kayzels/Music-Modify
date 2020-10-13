# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_action.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_actionWidget_Main(object):
    def setupUi(self, actionWidget_Main):
        actionWidget_Main.setObjectName("actionWidget_Main")
        actionWidget_Main.resize(851, 1696)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(actionWidget_Main)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.actionWidget = QtWidgets.QWidget(actionWidget_Main)
        self.actionWidget.setStyleSheet("QWidget#actionWidget {border-color: black; border-style:solid; border-width:9px; border-radius:15px; background-color:white}")
        self.actionWidget.setObjectName("actionWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.actionWidget)
        self.verticalLayout.setContentsMargins(18, 18, 18, 18)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainHeadingWidget = QtWidgets.QWidget(self.actionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainHeadingWidget.sizePolicy().hasHeightForWidth())
        self.mainHeadingWidget.setSizePolicy(sizePolicy)
        self.mainHeadingWidget.setObjectName("mainHeadingWidget")
        self.headingHLayout = QtWidgets.QHBoxLayout(self.mainHeadingWidget)
        self.headingHLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.headingHLayout.setContentsMargins(1, 1, 1, -1)
        self.headingHLayout.setSpacing(6)
        self.headingHLayout.setObjectName("headingHLayout")
        self.actionLabel = QtWidgets.QLabel(self.mainHeadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionLabel.sizePolicy().hasHeightForWidth())
        self.actionLabel.setSizePolicy(sizePolicy)
        self.actionLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.actionLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.actionLabel.setFont(font)
        self.actionLabel.setStyleSheet("QLabel {\n"
"  border-color:black;\n"
"  border-width: 6px;        \n"
"  border-style: solid;\n"
"  border-radius: 25px;\n"
"  margin:0px;\n"
"  padding:0px;\n"
"  color:black\n"
"}")
        self.actionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.actionLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.actionLabel.setObjectName("actionLabel")
        self.headingHLayout.addWidget(self.actionLabel)
        self.summaryWidget = QtWidgets.QWidget(self.mainHeadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.summaryWidget.sizePolicy().hasHeightForWidth())
        self.summaryWidget.setSizePolicy(sizePolicy)
        self.summaryWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.summaryWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.summaryWidget.setObjectName("summaryWidget")
        self.summaryHLayout = QtWidgets.QHBoxLayout(self.summaryWidget)
        self.summaryHLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.summaryHLayout.setContentsMargins(1, 1, 1, 1)
        self.summaryHLayout.setSpacing(4)
        self.summaryHLayout.setObjectName("summaryHLayout")
        self.actionSummary = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionSummary.sizePolicy().hasHeightForWidth())
        self.actionSummary.setSizePolicy(sizePolicy)
        self.actionSummary.setMinimumSize(QtCore.QSize(125, 0))
        self.actionSummary.setObjectName("actionSummary")
        self.summaryActionVLayout = QtWidgets.QVBoxLayout(self.actionSummary)
        self.summaryActionVLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.summaryActionVLayout.setContentsMargins(0, 0, 0, 0)
        self.summaryActionVLayout.setSpacing(4)
        self.summaryActionVLayout.setObjectName("summaryActionVLayout")
        self.actionInfoLabel = QtWidgets.QLabel(self.actionSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionInfoLabel.sizePolicy().hasHeightForWidth())
        self.actionInfoLabel.setSizePolicy(sizePolicy)
        self.actionInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.actionInfoLabel.setObjectName("actionInfoLabel")
        self.summaryActionVLayout.addWidget(self.actionInfoLabel)
        self.actionInfo_Main = QtWidgets.QTextEdit(self.actionSummary)
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
        self.summaryActionVLayout.addWidget(self.actionInfo_Main)
        self.summaryHLayout.addWidget(self.actionSummary)
        self.tagsSummary = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsSummary.sizePolicy().hasHeightForWidth())
        self.tagsSummary.setSizePolicy(sizePolicy)
        self.tagsSummary.setMinimumSize(QtCore.QSize(91, 0))
        self.tagsSummary.setMaximumSize(QtCore.QSize(91, 16777215))
        self.tagsSummary.setObjectName("tagsSummary")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tagsSummary)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tagsLabel = QtWidgets.QLabel(self.tagsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsLabel.sizePolicy().hasHeightForWidth())
        self.tagsLabel.setSizePolicy(sizePolicy)
        self.tagsLabel.setMinimumSize(QtCore.QSize(91, 0))
        self.tagsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tagsLabel.setObjectName("tagsLabel")
        self.verticalLayout_2.addWidget(self.tagsLabel)
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
        self.verticalLayout_2.addWidget(self.tagInfo_Main)
        self.summaryHLayout.addWidget(self.tagsSummary)
        self.songsSummary = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songsSummary.sizePolicy().hasHeightForWidth())
        self.songsSummary.setSizePolicy(sizePolicy)
        self.songsSummary.setMinimumSize(QtCore.QSize(91, 0))
        self.songsSummary.setMaximumSize(QtCore.QSize(91, 16777215))
        self.songsSummary.setObjectName("songsSummary")
        self.summarySongsVLayout = QtWidgets.QVBoxLayout(self.songsSummary)
        self.summarySongsVLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.summarySongsVLayout.setContentsMargins(0, 0, 0, 0)
        self.summarySongsVLayout.setSpacing(4)
        self.summarySongsVLayout.setObjectName("summarySongsVLayout")
        self.songsLabel = QtWidgets.QLabel(self.songsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songsLabel.sizePolicy().hasHeightForWidth())
        self.songsLabel.setSizePolicy(sizePolicy)
        self.songsLabel.setMinimumSize(QtCore.QSize(91, 0))
        self.songsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.songsLabel.setObjectName("songsLabel")
        self.summarySongsVLayout.addWidget(self.songsLabel)
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
        self.summarySongsVLayout.addWidget(self.songCount_Main)
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
        self.summarySongsVLayout.addWidget(self.songsCustomName_Main)
        self.summaryHLayout.addWidget(self.songsSummary)
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
        self.summaryValuesVLayout = QtWidgets.QVBoxLayout(self.valuesSummary)
        self.summaryValuesVLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.summaryValuesVLayout.setContentsMargins(0, 0, 0, 0)
        self.summaryValuesVLayout.setSpacing(4)
        self.summaryValuesVLayout.setObjectName("summaryValuesVLayout")
        self.valuesLabel = QtWidgets.QLabel(self.valuesSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valuesLabel.sizePolicy().hasHeightForWidth())
        self.valuesLabel.setSizePolicy(sizePolicy)
        self.valuesLabel.setMinimumSize(QtCore.QSize(91, 0))
        self.valuesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.valuesLabel.setObjectName("valuesLabel")
        self.summaryValuesVLayout.addWidget(self.valuesLabel)
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
        self.summaryValuesVLayout.addWidget(self.valueCount_Main)
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
        self.summaryValuesVLayout.addWidget(self.valuesCustomName_Main)
        self.summaryHLayout.addWidget(self.valuesSummary)
        self.discogsSummary = QtWidgets.QWidget(self.summaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsSummary.sizePolicy().hasHeightForWidth())
        self.discogsSummary.setSizePolicy(sizePolicy)
        self.discogsSummary.setMinimumSize(QtCore.QSize(125, 0))
        self.discogsSummary.setObjectName("discogsSummary")
        self.summaryActionVLayout_2 = QtWidgets.QVBoxLayout(self.discogsSummary)
        self.summaryActionVLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.summaryActionVLayout_2.setContentsMargins(0, 0, 0, 0)
        self.summaryActionVLayout_2.setSpacing(4)
        self.summaryActionVLayout_2.setObjectName("summaryActionVLayout_2")
        self.discogsReleaseIDLabel = QtWidgets.QLabel(self.discogsSummary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsReleaseIDLabel.sizePolicy().hasHeightForWidth())
        self.discogsReleaseIDLabel.setSizePolicy(sizePolicy)
        self.discogsReleaseIDLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.discogsReleaseIDLabel.setObjectName("discogsReleaseIDLabel")
        self.summaryActionVLayout_2.addWidget(self.discogsReleaseIDLabel)
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
        self.summaryActionVLayout_2.addWidget(self.discogsReleaseID_Main)
        self.summaryHLayout.addWidget(self.discogsSummary)
        self.headingHLayout.addWidget(self.summaryWidget)
        self.displayActionPushButton = QtWidgets.QPushButton(self.mainHeadingWidget)
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
"}\n"
"QPushButton#displayActionPushButton {\n"
"    qproperty-iconSize: 48px 48px; /* space for the background image */\n"
"}")
        self.displayActionPushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/up_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/down_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.displayActionPushButton.setIcon(icon)
        self.displayActionPushButton.setIconSize(QtCore.QSize(48, 48))
        self.displayActionPushButton.setCheckable(True)
        self.displayActionPushButton.setChecked(True)
        self.displayActionPushButton.setObjectName("displayActionPushButton")
        self.headingHLayout.addWidget(self.displayActionPushButton)
        self.headingHLayout.setStretch(0, 3)
        self.headingHLayout.setStretch(1, 10)
        self.headingHLayout.setStretch(2, 1)
        self.verticalLayout.addWidget(self.mainHeadingWidget)
        self.entireActionWidget = QtWidgets.QWidget(self.actionWidget)
        self.entireActionWidget.setStyleSheet("QFrame#actionSelectFrame, \n"
"QFrame#songsSelectFrame, \n"
"QFrame#tableValuesFrame,\n"
"QFrame#discogsReleaseFrame,\n"
"QFrame#copyTableFrame {\n"
"  border-width:7px; \n"
"  border-style:solid;\n"
"  border-radius:15px}\n"
"\n"
"QLabel#selectedActionHeading, \n"
"QLabel#selectedSongsHeading, \n"
"QLabel#valuesTableHeading, \n"
"QLabel#discogsReleaseHeading,\n"
"QLabel#copyTableHeading,\n"
"QPushButton#displaySelectedActionButton, QPushButton#displaySelectedSongsButton, QPushButton#displayValuesTableButton,\n"
"QPushButton#displayDiscogsReleaseButton,\n"
"QPushButton#changeSelectedSongsButton, \n"
"QPushButton#displayCopyTableButton,\n"
"QPushButton#saveValuesButton,\n"
"QPushButton#saveCopyValuesButton{\n"
"  border-width: 3px;\n"
"  border-style: solid;\n"
"  border-radius:15px;\n"
"  margin: 0px;\n"
"  padding: 0px\n"
"}\n"
"\n"
"QPushButton#downloadReleaseButton {\n"
"  border-width:2px;\n"
"  border-style: solid;\n"
"  border-radius: 13px\n"
"}\n"
"\n"
"QPushButton#syncButton,\n"
"QPushButton#autoMapButton {\n"
"  border-width: 2px;\n"
"  border-radius: 9px\n"
"}\n"
"\n"
"\n"
"QPushButton#downloadReleaseButton:disabled,\n"
"QPushButton#syncButton:disabled,\n"
"QPushButton#autoMapButton:disabled {\n"
"  color:grey;\n"
"  background-color:lightgrey;\n"
"  border-color:grey\n"
"}\n"
"\n"
"QPushButton#saveValuesButton,\n"
"QPushButton#saveCopyValuesButton,\n"
"QPushButton#changeSelectedSongsButton,\n"
"QPushButton#downloadReleaseButton,\n"
"QPushButton#autoMapButton,\n"
"QPushButton#syncButton {\n"
"  border-style:outset\n"
"}\n"
"\n"
"QPushButton#saveValuesButton:pressed,\n"
"QPushButton#changeSelectedSongsButton:pressed,\n"
"QPushButton#downloadReleaseButton:pressed,\n"
"QPushButton#autoMapButton:pressed,\n"
"QPushButton#syncButton:checked,\n"
"QPushButton#saveCopyValuesButton:pressed {\n"
"  border-style: inset\n"
"}")
        self.entireActionWidget.setObjectName("entireActionWidget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.entireActionWidget)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.discogsSplitter = QtWidgets.QSplitter(self.entireActionWidget)
        self.discogsSplitter.setOrientation(QtCore.Qt.Vertical)
        self.discogsSplitter.setObjectName("discogsSplitter")
        self.copySplitter = QtWidgets.QSplitter(self.discogsSplitter)
        self.copySplitter.setOrientation(QtCore.Qt.Vertical)
        self.copySplitter.setObjectName("copySplitter")
        self.valuesSplitter = QtWidgets.QSplitter(self.copySplitter)
        self.valuesSplitter.setOrientation(QtCore.Qt.Vertical)
        self.valuesSplitter.setObjectName("valuesSplitter")
        self.songsSplitter = QtWidgets.QSplitter(self.valuesSplitter)
        self.songsSplitter.setOrientation(QtCore.Qt.Vertical)
        self.songsSplitter.setObjectName("songsSplitter")
        self.actionSelectFrame = QtWidgets.QFrame(self.songsSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionSelectFrame.sizePolicy().hasHeightForWidth())
        self.actionSelectFrame.setSizePolicy(sizePolicy)
        self.actionSelectFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.actionSelectFrame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.actionSelectFrame.setBaseSize(QtCore.QSize(0, 80))
        self.actionSelectFrame.setStyleSheet("QFrame#actionSelectFrame {border-color:rgb(200,200,250)}")
        self.actionSelectFrame.setObjectName("actionSelectFrame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.actionSelectFrame)
        self.verticalLayout_6.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_6.setSpacing(4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.actionHeadingHLayoutToggle = QtWidgets.QHBoxLayout()
        self.actionHeadingHLayoutToggle.setObjectName("actionHeadingHLayoutToggle")
        self.actionHeadingHLayout = QtWidgets.QHBoxLayout()
        self.actionHeadingHLayout.setObjectName("actionHeadingHLayout")
        self.selectedActionHeading = QtWidgets.QLabel(self.actionSelectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedActionHeading.sizePolicy().hasHeightForWidth())
        self.selectedActionHeading.setSizePolicy(sizePolicy)
        self.selectedActionHeading.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.selectedActionHeading.setFont(font)
        self.selectedActionHeading.setStyleSheet("border-color:rgb(200,200,250);\n"
"color:rgb(100,100,215)")
        self.selectedActionHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.selectedActionHeading.setObjectName("selectedActionHeading")
        self.actionHeadingHLayout.addWidget(self.selectedActionHeading)
        self.actionInfo = QtWidgets.QTextEdit(self.actionSelectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionInfo.sizePolicy().hasHeightForWidth())
        self.actionInfo.setSizePolicy(sizePolicy)
        self.actionInfo.setMinimumSize(QtCore.QSize(105, 40))
        self.actionInfo.setMaximumSize(QtCore.QSize(16777215, 78))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.actionInfo.setFont(font)
        self.actionInfo.setStyleSheet("QTextEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  padding:3px;\n"
"  margin:0px\n"
"}")
        self.actionInfo.setObjectName("actionInfo")
        self.actionHeadingHLayout.addWidget(self.actionInfo)
        self.tagInfo = QtWidgets.QTextEdit(self.actionSelectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagInfo.sizePolicy().hasHeightForWidth())
        self.tagInfo.setSizePolicy(sizePolicy)
        self.tagInfo.setMinimumSize(QtCore.QSize(91, 40))
        self.tagInfo.setMaximumSize(QtCore.QSize(16777215, 78))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tagInfo.setFont(font)
        self.tagInfo.setStyleSheet("QTextEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  padding:3px;\n"
"  margin:0px\n"
"}")
        self.tagInfo.setObjectName("tagInfo")
        self.actionHeadingHLayout.addWidget(self.tagInfo)
        self.actionHeadingHLayout.setStretch(0, 4)
        self.actionHeadingHLayout.setStretch(1, 2)
        self.actionHeadingHLayout.setStretch(2, 1)
        self.actionHeadingHLayoutToggle.addLayout(self.actionHeadingHLayout)
        self.displaySelectedActionButton = QtWidgets.QPushButton(self.actionSelectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displaySelectedActionButton.sizePolicy().hasHeightForWidth())
        self.displaySelectedActionButton.setSizePolicy(sizePolicy)
        self.displaySelectedActionButton.setMinimumSize(QtCore.QSize(31, 31))
        self.displaySelectedActionButton.setMaximumSize(QtCore.QSize(31, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displaySelectedActionButton.setFont(font)
        self.displaySelectedActionButton.setStyleSheet("\n"
"  border-color:rgb(200,200,250);\n"
"  color:rgb(100,100,215)")
        self.displaySelectedActionButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/icons/down_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/icons/up_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.displaySelectedActionButton.setIcon(icon1)
        self.displaySelectedActionButton.setIconSize(QtCore.QSize(32, 32))
        self.displaySelectedActionButton.setCheckable(True)
        self.displaySelectedActionButton.setChecked(True)
        self.displaySelectedActionButton.setObjectName("displaySelectedActionButton")
        self.actionHeadingHLayoutToggle.addWidget(self.displaySelectedActionButton)
        self.verticalLayout_6.addLayout(self.actionHeadingHLayoutToggle)
        self.actionSelectWidget = QtWidgets.QWidget(self.actionSelectFrame)
        self.actionSelectWidget.setObjectName("actionSelectWidget")
        self.actionSelectWidgetVLayout = QtWidgets.QVBoxLayout(self.actionSelectWidget)
        self.actionSelectWidgetVLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.actionSelectWidgetVLayout.setContentsMargins(0, 0, 0, 0)
        self.actionSelectWidgetVLayout.setSpacing(4)
        self.actionSelectWidgetVLayout.setObjectName("actionSelectWidgetVLayout")
        self.actionsComboBox = QtWidgets.QComboBox(self.actionSelectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionsComboBox.sizePolicy().hasHeightForWidth())
        self.actionsComboBox.setSizePolicy(sizePolicy)
        self.actionsComboBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.actionsComboBox.setFont(font)
        self.actionsComboBox.setAutoFillBackground(False)
        self.actionsComboBox.setStyleSheet("QComboBox {\n"
"  background:rgb(200,200,250);\n"
"  padding:4px;\n"
"  border-color:rgb(100,100,215);\n"
"  border-width: 3px;        \n"
"  border-style: outset;\n"
"  border-radius: 10px;\n"
"color:rgb(100,100,215)\n"
"}\n"
"QComboBox::drop-down{\n"
"border:none;\n"
"width:24px\n"
"}\n"
"QComboBox::down-arrow{\n"
"image:url(:/icons/icons/down_icon.png);\n"
"width:20px;\n"
"height:20px;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"  border-style:inset;\n"
"  background: rgb(170, 170, 255)\n"
"}\n"
"\n"
"QListView {\n"
"  font-size:14pt;\n"
"  /*border-color:rgb(100,100,215);\n"
"  border-width: 2px;        \n"
"  border-style: solid;*/\n"
"  border: 0px;\n"
"  background-color:rgb(240,230,255);\n"
"  color:rgb(100,100,215);\n"
"  margin:2px;\n"
"  outline: 0px\n"
"}\n"
"QListView::item {\n"
"  background: transparent;\n"
"  /*border: 0px solid rgb(240, 230, 255)*/\n"
"}\n"
"\n"
"QListView::item::selected{\n"
"  background-color:rgb(200,200,250);\n"
"  /*border: 1px solid rgb(200, 200, 250);*/\n"
"  \n"
"  /*border-color:rgb(200,200,250)*/\n"
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
" border: 1px solid rgb(200, 200, 250);\n"
"  background:rgb(200, 200, 250);\n"
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
        self.actionsComboBox.setFrame(False)
        self.actionsComboBox.setModelColumn(0)
        self.actionsComboBox.setObjectName("actionsComboBox")
        self.actionsComboBox.addItem("")
        self.actionSelectWidgetVLayout.addWidget(self.actionsComboBox)
        self.tagsScrollArea = QtWidgets.QScrollArea(self.actionSelectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsScrollArea.sizePolicy().hasHeightForWidth())
        self.tagsScrollArea.setSizePolicy(sizePolicy)
        self.tagsScrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.tagsScrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tagsScrollArea.setBaseSize(QtCore.QSize(0, 72))
        self.tagsScrollArea.setAutoFillBackground(False)
        self.tagsScrollArea.setStyleSheet("QScrollArea#tagsScrollArea {background:transparent}")
        self.tagsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tagsScrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tagsScrollArea.setLineWidth(0)
        self.tagsScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tagsScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tagsScrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tagsScrollArea.setWidgetResizable(True)
        self.tagsScrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.tagsScrollArea.setObjectName("tagsScrollArea")
        self.tagsScrollAreaWidgetContents = QtWidgets.QWidget()
        self.tagsScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 793, 69))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsScrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.tagsScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.tagsScrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 36))
        self.tagsScrollAreaWidgetContents.setMaximumSize(QtCore.QSize(16777215, 72))
        self.tagsScrollAreaWidgetContents.setBaseSize(QtCore.QSize(0, 72))
        self.tagsScrollAreaWidgetContents.setAutoFillBackground(False)
        self.tagsScrollAreaWidgetContents.setStyleSheet("QWidget#tagsScrollAreaWidgetContents {background:transparent}")
        self.tagsScrollAreaWidgetContents.setObjectName("tagsScrollAreaWidgetContents")
        self.tagsScrollAreaContentsVerticalLayout = QtWidgets.QVBoxLayout(self.tagsScrollAreaWidgetContents)
        self.tagsScrollAreaContentsVerticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.tagsScrollAreaContentsVerticalLayout.setContentsMargins(0, 4, 0, 4)
        self.tagsScrollAreaContentsVerticalLayout.setSpacing(4)
        self.tagsScrollAreaContentsVerticalLayout.setObjectName("tagsScrollAreaContentsVerticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tagsScrollAreaContentsVerticalLayout.addItem(spacerItem)
        self.tagsScrollArea.setWidget(self.tagsScrollAreaWidgetContents)
        self.actionSelectWidgetVLayout.addWidget(self.tagsScrollArea)
        self.verticalLayout_6.addWidget(self.actionSelectWidget)
        self.songsSelectFrame = QtWidgets.QFrame(self.songsSplitter)
        self.songsSelectFrame.setAutoFillBackground(False)
        self.songsSelectFrame.setStyleSheet("QFrame#songsSelectFrame {border-color: lightblue}\n"
"")
        self.songsSelectFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.songsSelectFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.songsSelectFrame.setLineWidth(0)
        self.songsSelectFrame.setMidLineWidth(0)
        self.songsSelectFrame.setObjectName("songsSelectFrame")
        self.songsSelectedFrameVLayout = QtWidgets.QVBoxLayout(self.songsSelectFrame)
        self.songsSelectedFrameVLayout.setContentsMargins(4, 4, 4, 4)
        self.songsSelectedFrameVLayout.setSpacing(4)
        self.songsSelectedFrameVLayout.setObjectName("songsSelectedFrameVLayout")
        self.selectedSongsHLayoutToggle = QtWidgets.QHBoxLayout()
        self.selectedSongsHLayoutToggle.setSpacing(4)
        self.selectedSongsHLayoutToggle.setObjectName("selectedSongsHLayoutToggle")
        self.selectedSongsHeadingHLayout = QtWidgets.QHBoxLayout()
        self.selectedSongsHeadingHLayout.setSpacing(4)
        self.selectedSongsHeadingHLayout.setObjectName("selectedSongsHeadingHLayout")
        self.selectedSongsHeading = QtWidgets.QLabel(self.songsSelectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedSongsHeading.sizePolicy().hasHeightForWidth())
        self.selectedSongsHeading.setSizePolicy(sizePolicy)
        self.selectedSongsHeading.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.selectedSongsHeading.setFont(font)
        self.selectedSongsHeading.setStyleSheet("border-color: lightblue;\n"
"color: rgb(0,115,150)")
        self.selectedSongsHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.selectedSongsHeading.setObjectName("selectedSongsHeading")
        self.selectedSongsHeadingHLayout.addWidget(self.selectedSongsHeading)
        self.songsCustomName = QtWidgets.QLineEdit(self.songsSelectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songsCustomName.sizePolicy().hasHeightForWidth())
        self.songsCustomName.setSizePolicy(sizePolicy)
        self.songsCustomName.setMinimumSize(QtCore.QSize(91, 37))
        self.songsCustomName.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.songsCustomName.setFont(font)
        self.songsCustomName.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.songsCustomName.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.songsCustomName.setText("")
        self.songsCustomName.setMaxLength(103)
        self.songsCustomName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.songsCustomName.setReadOnly(False)
        self.songsCustomName.setObjectName("songsCustomName")
        self.selectedSongsHeadingHLayout.addWidget(self.songsCustomName)
        self.songCount = QtWidgets.QLineEdit(self.songsSelectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songCount.sizePolicy().hasHeightForWidth())
        self.songCount.setSizePolicy(sizePolicy)
        self.songCount.setMinimumSize(QtCore.QSize(91, 37))
        self.songCount.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.songCount.setFont(font)
        self.songCount.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.songCount.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.songCount.setText("0")
        self.songCount.setMaxLength(100)
        self.songCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.songCount.setReadOnly(True)
        self.songCount.setObjectName("songCount")
        self.selectedSongsHeadingHLayout.addWidget(self.songCount)
        self.selectedSongsHeadingHLayout.setStretch(0, 4)
        self.selectedSongsHeadingHLayout.setStretch(1, 2)
        self.selectedSongsHeadingHLayout.setStretch(2, 1)
        self.selectedSongsHLayoutToggle.addLayout(self.selectedSongsHeadingHLayout)
        self.displaySelectedSongsButton = QtWidgets.QPushButton(self.songsSelectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displaySelectedSongsButton.sizePolicy().hasHeightForWidth())
        self.displaySelectedSongsButton.setSizePolicy(sizePolicy)
        self.displaySelectedSongsButton.setMinimumSize(QtCore.QSize(31, 31))
        self.displaySelectedSongsButton.setMaximumSize(QtCore.QSize(31, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displaySelectedSongsButton.setFont(font)
        self.displaySelectedSongsButton.setStyleSheet("\n"
"  border-color: lightblue;\n"
"color: rgb(0,115,150)\n"
"")
        self.displaySelectedSongsButton.setText("")
        self.displaySelectedSongsButton.setIcon(icon)
        self.displaySelectedSongsButton.setIconSize(QtCore.QSize(32, 32))
        self.displaySelectedSongsButton.setCheckable(True)
        self.displaySelectedSongsButton.setChecked(True)
        self.displaySelectedSongsButton.setObjectName("displaySelectedSongsButton")
        self.selectedSongsHLayoutToggle.addWidget(self.displaySelectedSongsButton)
        self.songsSelectedFrameVLayout.addLayout(self.selectedSongsHLayoutToggle)
        self.songsSelectWidget = QtWidgets.QWidget(self.songsSelectFrame)
        self.songsSelectWidget.setObjectName("songsSelectWidget")
        self.songsSelectWidgetVLayout = QtWidgets.QVBoxLayout(self.songsSelectWidget)
        self.songsSelectWidgetVLayout.setContentsMargins(0, 0, 0, 0)
        self.songsSelectWidgetVLayout.setSpacing(4)
        self.songsSelectWidgetVLayout.setObjectName("songsSelectWidgetVLayout")
        self.selectedSongsTableView = QtWidgets.QTableView(self.songsSelectWidget)
        self.selectedSongsTableView.setMinimumSize(QtCore.QSize(0, 170))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.selectedSongsTableView.setFont(font)
        self.selectedSongsTableView.setStyleSheet("QTableView QTableCornerButton::section {\n"
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
        self.selectedSongsTableView.setAlternatingRowColors(True)
        self.selectedSongsTableView.setObjectName("selectedSongsTableView")
        self.selectedSongsTableView.horizontalHeader().setStretchLastSection(True)
        self.selectedSongsTableView.verticalHeader().setCascadingSectionResizes(True)
        self.selectedSongsTableView.verticalHeader().setMinimumSectionSize(30)
        self.selectedSongsTableView.verticalHeader().setStretchLastSection(False)
        self.songsSelectWidgetVLayout.addWidget(self.selectedSongsTableView)
        self.changeSelectedSongsButton = QtWidgets.QPushButton(self.songsSelectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.changeSelectedSongsButton.sizePolicy().hasHeightForWidth())
        self.changeSelectedSongsButton.setSizePolicy(sizePolicy)
        self.changeSelectedSongsButton.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.changeSelectedSongsButton.setFont(font)
        self.changeSelectedSongsButton.setStyleSheet("QPushButton {\n"
"  border-color:rgb(0,115,150);\n"
"  background: lightblue;\n"
"  color: rgb(0,115,150)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background:lightsteelblue;\n"
"  border-style: inset\n"
"}\n"
"\n"
"QPushButton::menu-indicator {\n"
"  image: url(:/icons/icons/down_icon.png);\n"
"  width:20px;\n"
"  height:20px;\n"
"  subcontrol-position: right center\n"
"}\n"
"QPushButton QMenu {\n"
"  font-size:14pt;\n"
"  background-color:lightblue;\n"
"  color: rgb(0,115,150)\n"
"}\n"
"QPushButton QMenu::item {\n"
"  background:transparent\n"
"}\n"
"QPushButton QMenu::item::selected{\n"
"  background-color:lightskyblue\n"
"}")
        self.changeSelectedSongsButton.setIconSize(QtCore.QSize(16, 23))
        self.changeSelectedSongsButton.setObjectName("changeSelectedSongsButton")
        self.songsSelectWidgetVLayout.addWidget(self.changeSelectedSongsButton)
        self.songsSelectedFrameVLayout.addWidget(self.songsSelectWidget)
        self.tableValuesFrame = QtWidgets.QFrame(self.valuesSplitter)
        self.tableValuesFrame.setAutoFillBackground(False)
        self.tableValuesFrame.setStyleSheet("QFrame#tableValuesFrame {border-color: pink}")
        self.tableValuesFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.tableValuesFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableValuesFrame.setLineWidth(0)
        self.tableValuesFrame.setMidLineWidth(0)
        self.tableValuesFrame.setObjectName("tableValuesFrame")
        self.songsSelectedFrameVLayout_2 = QtWidgets.QVBoxLayout(self.tableValuesFrame)
        self.songsSelectedFrameVLayout_2.setContentsMargins(4, 4, 4, 4)
        self.songsSelectedFrameVLayout_2.setSpacing(4)
        self.songsSelectedFrameVLayout_2.setObjectName("songsSelectedFrameVLayout_2")
        self.valuesTableHLayoutToggle = QtWidgets.QHBoxLayout()
        self.valuesTableHLayoutToggle.setSpacing(4)
        self.valuesTableHLayoutToggle.setObjectName("valuesTableHLayoutToggle")
        self.valuesTableHeadingHLayout = QtWidgets.QHBoxLayout()
        self.valuesTableHeadingHLayout.setSpacing(4)
        self.valuesTableHeadingHLayout.setObjectName("valuesTableHeadingHLayout")
        self.valuesTableHeading = QtWidgets.QLabel(self.tableValuesFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valuesTableHeading.sizePolicy().hasHeightForWidth())
        self.valuesTableHeading.setSizePolicy(sizePolicy)
        self.valuesTableHeading.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.valuesTableHeading.setFont(font)
        self.valuesTableHeading.setStyleSheet("border-color: pink;\n"
"color: rgb(150,0,150)")
        self.valuesTableHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.valuesTableHeading.setObjectName("valuesTableHeading")
        self.valuesTableHeadingHLayout.addWidget(self.valuesTableHeading)
        self.valuesCustomName = QtWidgets.QLineEdit(self.tableValuesFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valuesCustomName.sizePolicy().hasHeightForWidth())
        self.valuesCustomName.setSizePolicy(sizePolicy)
        self.valuesCustomName.setMinimumSize(QtCore.QSize(91, 37))
        self.valuesCustomName.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.valuesCustomName.setFont(font)
        self.valuesCustomName.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.valuesCustomName.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.valuesCustomName.setText("")
        self.valuesCustomName.setMaxLength(103)
        self.valuesCustomName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.valuesCustomName.setReadOnly(False)
        self.valuesCustomName.setObjectName("valuesCustomName")
        self.valuesTableHeadingHLayout.addWidget(self.valuesCustomName)
        self.valuesCount = QtWidgets.QLineEdit(self.tableValuesFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valuesCount.sizePolicy().hasHeightForWidth())
        self.valuesCount.setSizePolicy(sizePolicy)
        self.valuesCount.setMinimumSize(QtCore.QSize(91, 0))
        self.valuesCount.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.valuesCount.setFont(font)
        self.valuesCount.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.valuesCount.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.valuesCount.setText("0")
        self.valuesCount.setMaxLength(100)
        self.valuesCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.valuesCount.setReadOnly(True)
        self.valuesCount.setObjectName("valuesCount")
        self.valuesTableHeadingHLayout.addWidget(self.valuesCount)
        self.valuesTableHeadingHLayout.setStretch(0, 4)
        self.valuesTableHeadingHLayout.setStretch(1, 2)
        self.valuesTableHeadingHLayout.setStretch(2, 1)
        self.valuesTableHLayoutToggle.addLayout(self.valuesTableHeadingHLayout)
        self.displayValuesTableButton = QtWidgets.QPushButton(self.tableValuesFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayValuesTableButton.sizePolicy().hasHeightForWidth())
        self.displayValuesTableButton.setSizePolicy(sizePolicy)
        self.displayValuesTableButton.setMinimumSize(QtCore.QSize(31, 31))
        self.displayValuesTableButton.setMaximumSize(QtCore.QSize(31, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displayValuesTableButton.setFont(font)
        self.displayValuesTableButton.setStyleSheet("border-color: pink;\n"
"color: rgb(150,0,150)\n"
"")
        self.displayValuesTableButton.setText("")
        self.displayValuesTableButton.setIcon(icon1)
        self.displayValuesTableButton.setIconSize(QtCore.QSize(32, 32))
        self.displayValuesTableButton.setCheckable(True)
        self.displayValuesTableButton.setChecked(True)
        self.displayValuesTableButton.setObjectName("displayValuesTableButton")
        self.valuesTableHLayoutToggle.addWidget(self.displayValuesTableButton)
        self.songsSelectedFrameVLayout_2.addLayout(self.valuesTableHLayoutToggle)
        self.valuesSelectWidget = QtWidgets.QWidget(self.tableValuesFrame)
        self.valuesSelectWidget.setObjectName("valuesSelectWidget")
        self.songsSelectWidgetVLayout_2 = QtWidgets.QVBoxLayout(self.valuesSelectWidget)
        self.songsSelectWidgetVLayout_2.setContentsMargins(0, 0, 0, 0)
        self.songsSelectWidgetVLayout_2.setSpacing(4)
        self.songsSelectWidgetVLayout_2.setObjectName("songsSelectWidgetVLayout_2")
        self.newValuesTableWidget = QtWidgets.QTableWidget(self.valuesSelectWidget)
        self.newValuesTableWidget.setMinimumSize(QtCore.QSize(0, 170))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.newValuesTableWidget.setFont(font)
        self.newValuesTableWidget.setStyleSheet("QTableWidget QTableCornerButton::section {\n"
"  background-color:pink;\n"
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
"  background-color: pink;\n"
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
"QHeaderView::section::horizontal::first {\n"
"  border-left: 0px;\n"
"  border-top-left-radius: 15px\n"
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
"  background-color:pink;\n"
"  border: none;\n"
"  border-right: 1px solid rgb(100, 100, 215);\n"
"  /*border-bottom: 1px solid lightgrey;*/\n"
"  padding-left: 9px;\n"
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
"  alternate-background-color: lavenderblush;\n"
"  gridline-color:pink\n"
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
" border: 1px solid pink;\n"
"  background:pink;\n"
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
        self.newValuesTableWidget.setAlternatingRowColors(True)
        self.newValuesTableWidget.setObjectName("newValuesTableWidget")
        self.newValuesTableWidget.setColumnCount(1)
        self.newValuesTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(9)
        item.setFont(font)
        self.newValuesTableWidget.setHorizontalHeaderItem(0, item)
        self.newValuesTableWidget.horizontalHeader().setMinimumSectionSize(39)
        self.newValuesTableWidget.horizontalHeader().setStretchLastSection(True)
        self.newValuesTableWidget.verticalHeader().setVisible(False)
        self.newValuesTableWidget.verticalHeader().setDefaultSectionSize(30)
        self.newValuesTableWidget.verticalHeader().setMinimumSectionSize(50)
        self.newValuesTableWidget.verticalHeader().setStretchLastSection(False)
        self.songsSelectWidgetVLayout_2.addWidget(self.newValuesTableWidget)
        self.saveValuesButton = QtWidgets.QPushButton(self.valuesSelectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveValuesButton.sizePolicy().hasHeightForWidth())
        self.saveValuesButton.setSizePolicy(sizePolicy)
        self.saveValuesButton.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.saveValuesButton.setFont(font)
        self.saveValuesButton.setStyleSheet("QPushButton {\n"
"border-color:rgb(150,0,150);\n"
"background: pink;\n"
"color:rgb(150,0,150);\n"
"}\n"
"\n"
":pressed {\n"
"  background: rgb(255, 160,180)\n"
"}\n"
"")
        self.saveValuesButton.setIconSize(QtCore.QSize(16, 23))
        self.saveValuesButton.setObjectName("saveValuesButton")
        self.songsSelectWidgetVLayout_2.addWidget(self.saveValuesButton)
        self.songsSelectedFrameVLayout_2.addWidget(self.valuesSelectWidget)
        self.copyTableFrame = QtWidgets.QFrame(self.copySplitter)
        self.copyTableFrame.setStyleSheet("QFrame#copyTableFrame {border-color: pink}")
        self.copyTableFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.copyTableFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.copyTableFrame.setObjectName("copyTableFrame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.copyTableFrame)
        self.verticalLayout_8.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_8.setSpacing(4)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.copyTableHeadingToggle = QtWidgets.QHBoxLayout()
        self.copyTableHeadingToggle.setObjectName("copyTableHeadingToggle")
        self.copyTableHeadingHLayout = QtWidgets.QHBoxLayout()
        self.copyTableHeadingHLayout.setSpacing(4)
        self.copyTableHeadingHLayout.setObjectName("copyTableHeadingHLayout")
        self.copyTableHeading = QtWidgets.QLabel(self.copyTableFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyTableHeading.sizePolicy().hasHeightForWidth())
        self.copyTableHeading.setSizePolicy(sizePolicy)
        self.copyTableHeading.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.copyTableHeading.setFont(font)
        self.copyTableHeading.setStyleSheet("border-color: pink;\n"
"color: rgb(150,0,150)")
        self.copyTableHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.copyTableHeading.setObjectName("copyTableHeading")
        self.copyTableHeadingHLayout.addWidget(self.copyTableHeading)
        self.copyTableCystomName = QtWidgets.QLineEdit(self.copyTableFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyTableCystomName.sizePolicy().hasHeightForWidth())
        self.copyTableCystomName.setSizePolicy(sizePolicy)
        self.copyTableCystomName.setMinimumSize(QtCore.QSize(91, 37))
        self.copyTableCystomName.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.copyTableCystomName.setFont(font)
        self.copyTableCystomName.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.copyTableCystomName.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.copyTableCystomName.setText("")
        self.copyTableCystomName.setMaxLength(103)
        self.copyTableCystomName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.copyTableCystomName.setReadOnly(False)
        self.copyTableCystomName.setObjectName("copyTableCystomName")
        self.copyTableHeadingHLayout.addWidget(self.copyTableCystomName)
        self.copyTableCount = QtWidgets.QLineEdit(self.copyTableFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyTableCount.sizePolicy().hasHeightForWidth())
        self.copyTableCount.setSizePolicy(sizePolicy)
        self.copyTableCount.setMinimumSize(QtCore.QSize(91, 0))
        self.copyTableCount.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.copyTableCount.setFont(font)
        self.copyTableCount.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.copyTableCount.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.copyTableCount.setText("0")
        self.copyTableCount.setMaxLength(100)
        self.copyTableCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.copyTableCount.setReadOnly(True)
        self.copyTableCount.setObjectName("copyTableCount")
        self.copyTableHeadingHLayout.addWidget(self.copyTableCount)
        self.copyTableHeadingHLayout.setStretch(0, 4)
        self.copyTableHeadingHLayout.setStretch(1, 2)
        self.copyTableHeadingHLayout.setStretch(2, 1)
        self.copyTableHeadingToggle.addLayout(self.copyTableHeadingHLayout)
        self.displayCopyTableButton = QtWidgets.QPushButton(self.copyTableFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayCopyTableButton.sizePolicy().hasHeightForWidth())
        self.displayCopyTableButton.setSizePolicy(sizePolicy)
        self.displayCopyTableButton.setMinimumSize(QtCore.QSize(31, 31))
        self.displayCopyTableButton.setMaximumSize(QtCore.QSize(31, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displayCopyTableButton.setFont(font)
        self.displayCopyTableButton.setStyleSheet("border-color: pink;\n"
"color: rgb(150,0,150)\n"
"")
        self.displayCopyTableButton.setText("")
        self.displayCopyTableButton.setIcon(icon1)
        self.displayCopyTableButton.setIconSize(QtCore.QSize(32, 32))
        self.displayCopyTableButton.setCheckable(True)
        self.displayCopyTableButton.setChecked(True)
        self.displayCopyTableButton.setObjectName("displayCopyTableButton")
        self.copyTableHeadingToggle.addWidget(self.displayCopyTableButton)
        self.verticalLayout_8.addLayout(self.copyTableHeadingToggle)
        self.copyWidget = QtWidgets.QWidget(self.copyTableFrame)
        self.copyWidget.setObjectName("copyWidget")
        self.copyTableHLayout = QtWidgets.QHBoxLayout(self.copyWidget)
        self.copyTableHLayout.setContentsMargins(0, 0, 0, 0)
        self.copyTableHLayout.setObjectName("copyTableHLayout")
        self.copyTableIndexesTableWidget = QtWidgets.QTableWidget(self.copyWidget)
        self.copyTableIndexesTableWidget.setObjectName("copyTableIndexesTableWidget")
        self.copyTableIndexesTableWidget.setColumnCount(0)
        self.copyTableIndexesTableWidget.setRowCount(0)
        self.copyTableHLayout.addWidget(self.copyTableIndexesTableWidget)
        self.copyTableSelectedSongs = QtWidgets.QTableView(self.copyWidget)
        self.copyTableSelectedSongs.setMinimumSize(QtCore.QSize(0, 170))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.copyTableSelectedSongs.setFont(font)
        self.copyTableSelectedSongs.setStyleSheet("QTableWidget QTableCornerButton::section {\n"
"  background-color:pink;\n"
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
"  background-color: pink;\n"
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
"QHeaderView::section::horizontal::first {\n"
"  border-left: 0px;\n"
"  border-top-left-radius: 15px\n"
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
"  background-color:pink;\n"
"  border: none;\n"
"  border-right: 1px solid rgb(100, 100, 215);\n"
"  /*border-bottom: 1px solid lightgrey;*/\n"
"  padding-left: 9px;\n"
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
"  alternate-background-color: lavenderblush;\n"
"  gridline-color:pink\n"
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
" border: 1px solid pink;\n"
"  background:pink;\n"
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
        self.copyTableSelectedSongs.setAlternatingRowColors(True)
        self.copyTableSelectedSongs.setObjectName("copyTableSelectedSongs")
        self.copyTableSelectedSongs.horizontalHeader().setStretchLastSection(True)
        self.copyTableSelectedSongs.verticalHeader().setCascadingSectionResizes(True)
        self.copyTableSelectedSongs.verticalHeader().setDefaultSectionSize(0)
        self.copyTableSelectedSongs.verticalHeader().setMinimumSectionSize(30)
        self.copyTableSelectedSongs.verticalHeader().setStretchLastSection(True)
        self.copyTableHLayout.addWidget(self.copyTableSelectedSongs)
        self.copyTableHLayout.setStretch(0, 1)
        self.copyTableHLayout.setStretch(1, 10)
        self.verticalLayout_8.addWidget(self.copyWidget)
        self.saveCopyValuesButton = QtWidgets.QPushButton(self.copyTableFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveCopyValuesButton.sizePolicy().hasHeightForWidth())
        self.saveCopyValuesButton.setSizePolicy(sizePolicy)
        self.saveCopyValuesButton.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.saveCopyValuesButton.setFont(font)
        self.saveCopyValuesButton.setStyleSheet("QPushButton {\n"
"border-color:rgb(150,0,150);\n"
"background: pink;\n"
"color:rgb(150,0,150);\n"
"}\n"
"\n"
":pressed {\n"
"  background: rgb(255, 160,180)\n"
"}\n"
"")
        self.saveCopyValuesButton.setIconSize(QtCore.QSize(16, 23))
        self.saveCopyValuesButton.setObjectName("saveCopyValuesButton")
        self.verticalLayout_8.addWidget(self.saveCopyValuesButton)
        self.verticalLayout_8.setStretch(0, 1)
        self.verticalLayout_8.setStretch(2, 1)
        self.discogsReleaseFrame = QtWidgets.QFrame(self.discogsSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsReleaseFrame.sizePolicy().hasHeightForWidth())
        self.discogsReleaseFrame.setSizePolicy(sizePolicy)
        self.discogsReleaseFrame.setStyleSheet("QFrame#discogsReleaseFrame{border-color:pink}")
        self.discogsReleaseFrame.setObjectName("discogsReleaseFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.discogsReleaseFrame)
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.discogsHeadingHLayoutToggle = QtWidgets.QHBoxLayout()
        self.discogsHeadingHLayoutToggle.setObjectName("discogsHeadingHLayoutToggle")
        self.discogsHeadingHLayout = QtWidgets.QHBoxLayout()
        self.discogsHeadingHLayout.setObjectName("discogsHeadingHLayout")
        self.discogsReleaseHeading = QtWidgets.QLabel(self.discogsReleaseFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsReleaseHeading.sizePolicy().hasHeightForWidth())
        self.discogsReleaseHeading.setSizePolicy(sizePolicy)
        self.discogsReleaseHeading.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.discogsReleaseHeading.setFont(font)
        self.discogsReleaseHeading.setStyleSheet("border-color: pink;\n"
"color: rgb(150,0,150)")
        self.discogsReleaseHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.discogsReleaseHeading.setObjectName("discogsReleaseHeading")
        self.discogsHeadingHLayout.addWidget(self.discogsReleaseHeading)
        self.discogsReleaseID = QtWidgets.QLineEdit(self.discogsReleaseFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsReleaseID.sizePolicy().hasHeightForWidth())
        self.discogsReleaseID.setSizePolicy(sizePolicy)
        self.discogsReleaseID.setMinimumSize(QtCore.QSize(91, 0))
        self.discogsReleaseID.setBaseSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.discogsReleaseID.setFont(font)
        self.discogsReleaseID.setStyleSheet("QLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"  margin:0px;\n"
"  padding-right:4px\n"
"}")
        self.discogsReleaseID.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.discogsReleaseID.setText("")
        self.discogsReleaseID.setMaxLength(100)
        self.discogsReleaseID.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.discogsReleaseID.setReadOnly(True)
        self.discogsReleaseID.setObjectName("discogsReleaseID")
        self.discogsHeadingHLayout.addWidget(self.discogsReleaseID)
        self.discogsHeadingHLayout.setStretch(0, 4)
        self.discogsHeadingHLayout.setStretch(1, 3)
        self.discogsHeadingHLayoutToggle.addLayout(self.discogsHeadingHLayout)
        self.displayDiscogsReleaseButton = QtWidgets.QPushButton(self.discogsReleaseFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayDiscogsReleaseButton.sizePolicy().hasHeightForWidth())
        self.displayDiscogsReleaseButton.setSizePolicy(sizePolicy)
        self.displayDiscogsReleaseButton.setMinimumSize(QtCore.QSize(31, 31))
        self.displayDiscogsReleaseButton.setMaximumSize(QtCore.QSize(31, 31))
        self.displayDiscogsReleaseButton.setBaseSize(QtCore.QSize(31, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displayDiscogsReleaseButton.setFont(font)
        self.displayDiscogsReleaseButton.setStyleSheet("border-color: pink;")
        self.displayDiscogsReleaseButton.setText("")
        self.displayDiscogsReleaseButton.setIcon(icon1)
        self.displayDiscogsReleaseButton.setIconSize(QtCore.QSize(32, 32))
        self.displayDiscogsReleaseButton.setCheckable(True)
        self.displayDiscogsReleaseButton.setChecked(True)
        self.displayDiscogsReleaseButton.setObjectName("displayDiscogsReleaseButton")
        self.discogsHeadingHLayoutToggle.addWidget(self.displayDiscogsReleaseButton)
        self.verticalLayout_3.addLayout(self.discogsHeadingHLayoutToggle)
        self.discogsReleaseWidget = QtWidgets.QWidget(self.discogsReleaseFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsReleaseWidget.sizePolicy().hasHeightForWidth())
        self.discogsReleaseWidget.setSizePolicy(sizePolicy)
        self.discogsReleaseWidget.setObjectName("discogsReleaseWidget")
        self.DiscogsReleaseWidgetVLayout = QtWidgets.QVBoxLayout(self.discogsReleaseWidget)
        self.DiscogsReleaseWidgetVLayout.setContentsMargins(0, 0, 0, 0)
        self.DiscogsReleaseWidgetVLayout.setSpacing(4)
        self.DiscogsReleaseWidgetVLayout.setObjectName("DiscogsReleaseWidgetVLayout")
        self.downloadDataHLayout = QtWidgets.QHBoxLayout()
        self.downloadDataHLayout.setContentsMargins(-1, -1, -1, 0)
        self.downloadDataHLayout.setObjectName("downloadDataHLayout")
        self.releaseIDLabel = QtWidgets.QLabel(self.discogsReleaseWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.releaseIDLabel.setFont(font)
        self.releaseIDLabel.setStyleSheet("color:rgb(150,0,150)")
        self.releaseIDLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.releaseIDLabel.setIndent(5)
        self.releaseIDLabel.setObjectName("releaseIDLabel")
        self.downloadDataHLayout.addWidget(self.releaseIDLabel)
        self.releaseIDLineEdit = QtWidgets.QLineEdit(self.discogsReleaseWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.releaseIDLineEdit.setFont(font)
        self.releaseIDLineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.releaseIDLineEdit.setStyleSheet("QLineEdit#releaseIDLineEdit {\n"
"  border-color:black;\n"
"  border-width: 1px;        \n"
"  border-style: solid;\n"
"  border-radius: 10px;\n"
"  background:white;\n"
"padding:3px\n"
"}")
        self.releaseIDLineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.releaseIDLineEdit.setInputMask("")
        self.releaseIDLineEdit.setText("")
        self.releaseIDLineEdit.setMaxLength(11)
        self.releaseIDLineEdit.setCursorPosition(0)
        self.releaseIDLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.releaseIDLineEdit.setObjectName("releaseIDLineEdit")
        self.downloadDataHLayout.addWidget(self.releaseIDLineEdit)
        self.downloadReleaseButton = QtWidgets.QPushButton(self.discogsReleaseWidget)
        self.downloadReleaseButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadReleaseButton.sizePolicy().hasHeightForWidth())
        self.downloadReleaseButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.downloadReleaseButton.setFont(font)
        self.downloadReleaseButton.setStyleSheet(":enabled{\n"
"border-color:rgb(150,0,150);\n"
"background: pink;\n"
"color:rgb(150,0,150)\n"
"}\n"
"\n"
":pressed {\n"
"  background: rgb(255, 160,180)\n"
"}\n"
"\n"
"")
        self.downloadReleaseButton.setObjectName("downloadReleaseButton")
        self.downloadDataHLayout.addWidget(self.downloadReleaseButton)
        self.downloadDataHLayout.setStretch(0, 1)
        self.downloadDataHLayout.setStretch(1, 5)
        self.downloadDataHLayout.setStretch(2, 1)
        self.DiscogsReleaseWidgetVLayout.addLayout(self.downloadDataHLayout)
        self.songMappingsWidget = QtWidgets.QWidget(self.discogsReleaseWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songMappingsWidget.sizePolicy().hasHeightForWidth())
        self.songMappingsWidget.setSizePolicy(sizePolicy)
        self.songMappingsWidget.setMinimumSize(QtCore.QSize(0, 350))
        self.songMappingsWidget.setObjectName("songMappingsWidget")
        self.songMappingsHLayout = QtWidgets.QHBoxLayout(self.songMappingsWidget)
        self.songMappingsHLayout.setContentsMargins(0, 0, 0, 0)
        self.songMappingsHLayout.setObjectName("songMappingsHLayout")
        self.discogsReleaseVLayout = QtWidgets.QVBoxLayout()
        self.discogsReleaseVLayout.setContentsMargins(-1, 4, -1, -1)
        self.discogsReleaseVLayout.setObjectName("discogsReleaseVLayout")
        self.discogsLabel = QtWidgets.QLabel(self.songMappingsWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.discogsLabel.setFont(font)
        self.discogsLabel.setStyleSheet("color:rgb(150,0,150)")
        self.discogsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.discogsLabel.setObjectName("discogsLabel")
        self.discogsReleaseVLayout.addWidget(self.discogsLabel)
        self.discogsTableHLayout = QtWidgets.QHBoxLayout()
        self.discogsTableHLayout.setSpacing(0)
        self.discogsTableHLayout.setObjectName("discogsTableHLayout")
        self.discogsVerticalScrollBar = QtWidgets.QScrollBar(self.songMappingsWidget)
        self.discogsVerticalScrollBar.setStyleSheet("QScrollBar {\n"
"  border: 1px solid black;\n"
"  background: white;\n"
"  border-radius: 12px;\n"
"  margin: 0px;\n"
"  margin-bottom: 25px;\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
" border: 1px solid pink;\n"
"  background:pink;\n"
"  border-radius: 9px;\n"
"}\n"
"\n"
"QScrollBar::handle:first {\n"
"  border: 1px solid black;\n"
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
"QScrollBar:vertical {\n"
"  width: 25px\n"
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
        self.discogsVerticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.discogsVerticalScrollBar.setObjectName("discogsVerticalScrollBar")
        self.discogsTableHLayout.addWidget(self.discogsVerticalScrollBar)
        self.discogsTableWidget = QtWidgets.QTableWidget(self.songMappingsWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.discogsTableWidget.setFont(font)
        self.discogsTableWidget.setStyleSheet("QTableWidget QTableCornerButton::section {\n"
"  background-color:pink;\n"
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
"  background-color: pink;\n"
"  border: none;\n"
"  /*border-right: 1px solid rgb(100, 100, 215);*/\n"
"  border-bottom: 1px solid rgb(100, 100, 215);\n"
" }\n"
"\n"
"QHeaderView::section::vertical {\n"
"  background-color: pink;\n"
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
"  border-top-left-radius: 15px;\n"
"  border-bottom-left-radius: 15px;\n"
"  background-color:white;\n"
"  alternate-background-color:lavenderblush;\n"
"  gridline-color: pink\n"
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
" border: 1px solid pink;\n"
"  background:pink;\n"
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
        self.discogsTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.discogsTableWidget.setAlternatingRowColors(True)
        self.discogsTableWidget.setObjectName("discogsTableWidget")
        self.discogsTableWidget.setColumnCount(0)
        self.discogsTableWidget.setRowCount(0)
        self.discogsTableWidget.horizontalHeader().setStretchLastSection(True)
        self.discogsTableHLayout.addWidget(self.discogsTableWidget)
        self.discogsReleaseVLayout.addLayout(self.discogsTableHLayout)
        self.songMappingsHLayout.addLayout(self.discogsReleaseVLayout)
        self.discogsSelectionVLayout = QtWidgets.QVBoxLayout()
        self.discogsSelectionVLayout.setContentsMargins(-1, 4, -1, -1)
        self.discogsSelectionVLayout.setObjectName("discogsSelectionVLayout")
        self.selectedLabel = QtWidgets.QLabel(self.songMappingsWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectedLabel.setFont(font)
        self.selectedLabel.setStyleSheet("color:rgb(150,0,150)")
        self.selectedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.selectedLabel.setObjectName("selectedLabel")
        self.discogsSelectionVLayout.addWidget(self.selectedLabel)
        self.discogsSelectionTableHLayout = QtWidgets.QHBoxLayout()
        self.discogsSelectionTableHLayout.setSpacing(0)
        self.discogsSelectionTableHLayout.setObjectName("discogsSelectionTableHLayout")
        self.discogsSelectedSongsTableView = QtWidgets.QTableView(self.songMappingsWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.discogsSelectedSongsTableView.setFont(font)
        self.discogsSelectedSongsTableView.setStyleSheet("QTableView QTableCornerButton::section {\n"
"  background-color:pink;\n"
"  border: none;\n"
"  /* border-right: 1px solid rgb(100, 100, 215);\n"
"  border-bottom: 1px solid rgb(100, 100, 215);\n"
"  border-top: 0px;\n"
"  border-left: 0px;*/\n"
"}\n"
"\n"
"QHeaderView::section::horizontal {\n"
"  font-size:12pt;\n"
"  padding-bottom:6px;\n"
"  background-color: pink;\n"
"  border: none;\n"
"  /*border-right: 1px solid rgb(100, 100, 215);*/\n"
"  border-bottom: 1px solid rgb(100, 100, 215);\n"
" }\n"
"\n"
"QHeaderView::section::vertical {\n"
"  background-color: pink;\n"
"  border: none;\n"
"  border-right: 1px solid rgb(100, 100, 215);\n"
"  /*border-bottom: 1px solid lightgrey;*/\n"
"  padding-left: 9px\n"
" }\n"
"\n"
"QHeaderView::section::horizontal::last {\n"
"  border-right: 0px;\n"
"  border-top-right-radius: 15px\n"
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
"  border-top-right-radius: 15px;\n"
"  border-bottom-right-radius: 15px;\n"
"  background-color:white;\n"
"  alternate-background-color:lavenderblush;\n"
"  gridline-color: pink\n"
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
" border: 1px solid pink;\n"
"  background:pink;\n"
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
        self.discogsSelectedSongsTableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.discogsSelectedSongsTableView.setAlternatingRowColors(True)
        self.discogsSelectedSongsTableView.setObjectName("discogsSelectedSongsTableView")
        self.discogsSelectedSongsTableView.verticalHeader().setCascadingSectionResizes(True)
        self.discogsSelectionTableHLayout.addWidget(self.discogsSelectedSongsTableView)
        self.selectedSongsVerticalScrollBar = QtWidgets.QScrollBar(self.songMappingsWidget)
        self.selectedSongsVerticalScrollBar.setStyleSheet("QScrollBar {\n"
"  border: 1px solid black;\n"
"  background: white;\n"
"  border-radius: 12px;\n"
"  margin: 0px;\n"
"  margin-bottom: 25px\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
" border: 1px solid pink;\n"
"  background:pink;\n"
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
"QScrollBar:vertical {\n"
"  width: 25px\n"
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
        self.selectedSongsVerticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.selectedSongsVerticalScrollBar.setObjectName("selectedSongsVerticalScrollBar")
        self.discogsSelectionTableHLayout.addWidget(self.selectedSongsVerticalScrollBar)
        self.discogsSelectionVLayout.addLayout(self.discogsSelectionTableHLayout)
        self.songMappingsHLayout.addLayout(self.discogsSelectionVLayout)
        self.syncWidget = QtWidgets.QWidget(self.songMappingsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syncWidget.sizePolicy().hasHeightForWidth())
        self.syncWidget.setSizePolicy(sizePolicy)
        self.syncWidget.setMinimumSize(QtCore.QSize(75, 0))
        self.syncWidget.setMaximumSize(QtCore.QSize(75, 16777215))
        self.syncWidget.setObjectName("syncWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.syncWidget)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.syncButton = QtWidgets.QPushButton(self.syncWidget)
        self.syncButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syncButton.sizePolicy().hasHeightForWidth())
        self.syncButton.setSizePolicy(sizePolicy)
        self.syncButton.setMinimumSize(QtCore.QSize(40, 19))
        self.syncButton.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.syncButton.setFont(font)
        self.syncButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.syncButton.setStyleSheet(":enabled{\n"
"border-color:rgb(150,0,150);\n"
"background: pink;\n"
"color:rgb(150,0,150)\n"
"}\n"
"\n"
":checked {\n"
"  background: rgb(255, 160,180)\n"
"}")
        self.syncButton.setCheckable(True)
        self.syncButton.setChecked(False)
        self.syncButton.setObjectName("syncButton")
        self.verticalLayout_4.addWidget(self.syncButton)
        self.scrollbarHLayout = QtWidgets.QHBoxLayout()
        self.scrollbarHLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.scrollbarHLayout.setObjectName("scrollbarHLayout")
        self.discogsSyncScrollBar = QtWidgets.QScrollBar(self.syncWidget)
        self.discogsSyncScrollBar.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discogsSyncScrollBar.sizePolicy().hasHeightForWidth())
        self.discogsSyncScrollBar.setSizePolicy(sizePolicy)
        self.discogsSyncScrollBar.setMinimumSize(QtCore.QSize(25, 318))
        self.discogsSyncScrollBar.setMaximumSize(QtCore.QSize(25, 16777215))
        self.discogsSyncScrollBar.setStyleSheet("QScrollBar {\n"
"  border: 1px solid black;\n"
"  background: white;\n"
"  border-radius: 12px;\n"
"  margin: 0px\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
" border: 1px solid pink;\n"
"  background:pink;\n"
"  border-radius: 9px;\n"
"}\n"
"\n"
"QScrollBar::handle:!enabled {\n"
"  border-color:lightgrey;\n"
"  background:lightgrey;\n"
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
"QScrollBar:vertical {\n"
"  width: 25px\n"
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
        self.discogsSyncScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.discogsSyncScrollBar.setObjectName("discogsSyncScrollBar")
        self.scrollbarHLayout.addWidget(self.discogsSyncScrollBar)
        self.verticalLayout_4.addLayout(self.scrollbarHLayout)
        self.autoMapButton = QtWidgets.QPushButton(self.syncWidget)
        self.autoMapButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoMapButton.sizePolicy().hasHeightForWidth())
        self.autoMapButton.setSizePolicy(sizePolicy)
        self.autoMapButton.setMinimumSize(QtCore.QSize(75, 19))
        self.autoMapButton.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.autoMapButton.setFont(font)
        self.autoMapButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.autoMapButton.setStyleSheet(":enabled{\n"
"border-color:rgb(150,0,150);\n"
"background: pink;\n"
"color:rgb(150,0,150)\n"
"}\n"
"\n"
":pressed {\n"
"  background: rgb(255, 160,180)\n"
"}")
        self.autoMapButton.setCheckable(False)
        self.autoMapButton.setObjectName("autoMapButton")
        self.verticalLayout_4.addWidget(self.autoMapButton)
        self.songMappingsHLayout.addWidget(self.syncWidget)
        self.songMappingsHLayout.setStretch(0, 100)
        self.songMappingsHLayout.setStretch(1, 100)
        self.DiscogsReleaseWidgetVLayout.addWidget(self.songMappingsWidget)
        self.verticalLayout_3.addWidget(self.discogsReleaseWidget)
        self.verticalLayout_9.addWidget(self.discogsSplitter)
        self.verticalLayout.addWidget(self.entireActionWidget)
        self.actionsEditButtonsLayout = QtWidgets.QHBoxLayout()
        self.actionsEditButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.actionsEditButtonsLayout.setSpacing(4)
        self.actionsEditButtonsLayout.setObjectName("actionsEditButtonsLayout")
        self.addAnotherActionButton = QtWidgets.QPushButton(self.actionWidget)
        self.addAnotherActionButton.setMinimumSize(QtCore.QSize(0, 29))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.addAnotherActionButton.setFont(font)
        self.addAnotherActionButton.setAutoFillBackground(False)
        self.addAnotherActionButton.setStyleSheet("QPushButton {\n"
"  border-color:green;\n"
"  border-width: 3px;        \n"
"  border-style: outset;\n"
"  border-radius: 14px;\n"
"  background: lightgreen;\n"
"  color: green\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background: limegreen;\n"
"  border-style: inset\n"
"}\n"
"")
        self.addAnotherActionButton.setFlat(False)
        self.addAnotherActionButton.setObjectName("addAnotherActionButton")
        self.actionsEditButtonsLayout.addWidget(self.addAnotherActionButton)
        self.removeActionPushButton = QtWidgets.QPushButton(self.actionWidget)
        self.removeActionPushButton.setMinimumSize(QtCore.QSize(0, 29))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.removeActionPushButton.setFont(font)
        self.removeActionPushButton.setAutoFillBackground(False)
        self.removeActionPushButton.setStyleSheet("QPushButton {\n"
"  border-color:red;\n"
"  border-width: 3px;        \n"
"  border-style: outset;\n"
"  border-radius: 14px;\n"
"  background: pink;\n"
"  color: red\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  border-style: inset;\n"
"  background: rgb(255,160,180)\n"
"}")
        self.removeActionPushButton.setFlat(False)
        self.removeActionPushButton.setObjectName("removeActionPushButton")
        self.actionsEditButtonsLayout.addWidget(self.removeActionPushButton)
        self.verticalLayout.addLayout(self.actionsEditButtonsLayout)
        self.verticalLayout_5.addWidget(self.actionWidget)
        self.actionCurrentSelection = QtWidgets.QAction(actionWidget_Main)
        self.actionCurrentSelection.setObjectName("actionCurrentSelection")
        self.actionGlobalSongs = QtWidgets.QAction(actionWidget_Main)
        self.actionGlobalSongs.setObjectName("actionGlobalSongs")
        self.actionOriginalSelection = QtWidgets.QAction(actionWidget_Main)
        self.actionOriginalSelection.setObjectName("actionOriginalSelection")
        self.valuesTableHeading.setBuddy(self.newValuesTableWidget)
        self.copyTableHeading.setBuddy(self.newValuesTableWidget)
        self.releaseIDLabel.setBuddy(self.releaseIDLineEdit)
        self.discogsLabel.setBuddy(self.discogsTableWidget)
        self.selectedLabel.setBuddy(self.discogsSelectedSongsTableView)

        self.retranslateUi(actionWidget_Main)
        self.actionsComboBox.setCurrentIndex(0)
        self.songCount.textChanged['QString'].connect(self.songCount_Main.setText)
        self.valuesCount.textChanged['QString'].connect(self.valueCount_Main.setText)
        self.displayActionPushButton.toggled['bool'].connect(self.entireActionWidget.setVisible)
        self.displaySelectedActionButton.toggled['bool'].connect(self.actionSelectWidget.setVisible)
        self.displaySelectedSongsButton.toggled['bool'].connect(self.songsSelectWidget.setVisible)
        self.displayValuesTableButton.toggled['bool'].connect(self.valuesSelectWidget.setVisible)
        self.displayDiscogsReleaseButton.toggled['bool'].connect(self.discogsReleaseWidget.setVisible)
        self.releaseIDLineEdit.textChanged['QString'].connect(self.discogsReleaseID.setText)
        self.songsCustomName.textChanged['QString'].connect(self.songsCustomName_Main.setText)
        self.valuesCustomName.textChanged['QString'].connect(self.valuesCustomName_Main.setText)
        self.discogsReleaseID.textChanged['QString'].connect(self.discogsReleaseID_Main.setText)
        self.displayCopyTableButton.toggled['bool'].connect(self.copyWidget.setVisible)
        QtCore.QMetaObject.connectSlotsByName(actionWidget_Main)

    def retranslateUi(self, actionWidget_Main):
        _translate = QtCore.QCoreApplication.translate
        actionWidget_Main.setWindowTitle(_translate("actionWidget_Main", "Form"))
        self.actionLabel.setText(_translate("actionWidget_Main", "ACTION"))
        self.actionInfoLabel.setText(_translate("actionWidget_Main", "Action"))
        self.actionInfo_Main.setHtml(_translate("actionWidget_Main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No Action</p></body></html>"))
        self.tagsLabel.setText(_translate("actionWidget_Main", "Tags"))
        self.tagInfo_Main.setHtml(_translate("actionWidget_Main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No Tags</p></body></html>"))
        self.songsLabel.setText(_translate("actionWidget_Main", "Songs"))
        self.songsCustomName_Main.setPlaceholderText(_translate("actionWidget_Main", "Label"))
        self.valuesLabel.setText(_translate("actionWidget_Main", "Values"))
        self.valuesCustomName_Main.setPlaceholderText(_translate("actionWidget_Main", "Label"))
        self.discogsReleaseIDLabel.setText(_translate("actionWidget_Main", "Discogs"))
        self.discogsReleaseID_Main.setHtml(_translate("actionWidget_Main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No ID</p></body></html>"))
        self.selectedActionHeading.setText(_translate("actionWidget_Main", "SELECTED ACTION"))
        self.actionInfo.setHtml(_translate("actionWidget_Main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No Action</p></body></html>"))
        self.tagInfo.setHtml(_translate("actionWidget_Main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No Tags</p></body></html>"))
        self.actionsComboBox.setItemText(0, _translate("actionWidget_Main", "Select Action"))
        self.selectedSongsHeading.setText(_translate("actionWidget_Main", "SELECTED SONGS"))
        self.songsCustomName.setPlaceholderText(_translate("actionWidget_Main", "Label"))
        self.changeSelectedSongsButton.setText(_translate("actionWidget_Main", "CHANGE SELECTED SONGS"))
        self.valuesTableHeading.setText(_translate("actionWidget_Main", "VALUES TABLE"))
        self.valuesCustomName.setPlaceholderText(_translate("actionWidget_Main", "Label"))
        item = self.newValuesTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("actionWidget_Main", "New Values Will Be Typed Here"))
        self.saveValuesButton.setText(_translate("actionWidget_Main", "SAVE VALUES"))
        self.copyTableHeading.setText(_translate("actionWidget_Main", "COPY TABLE"))
        self.copyTableCystomName.setPlaceholderText(_translate("actionWidget_Main", "Label"))
        self.saveCopyValuesButton.setText(_translate("actionWidget_Main", "SAVE VALUES"))
        self.discogsReleaseHeading.setText(_translate("actionWidget_Main", "DISCOGS RELEASE"))
        self.releaseIDLabel.setText(_translate("actionWidget_Main", "RELEASE ID:"))
        self.releaseIDLineEdit.setPlaceholderText(_translate("actionWidget_Main", "Type a Release ID from Discogs"))
        self.downloadReleaseButton.setText(_translate("actionWidget_Main", "GET"))
        self.discogsLabel.setText(_translate("actionWidget_Main", "Discogs Release"))
        self.selectedLabel.setText(_translate("actionWidget_Main", "Selected Songs"))
        self.syncButton.setText(_translate("actionWidget_Main", "SYNC"))
        self.autoMapButton.setText(_translate("actionWidget_Main", "AUTO MAP"))
        self.addAnotherActionButton.setText(_translate("actionWidget_Main", "ADD ANOTHER ACTION"))
        self.removeActionPushButton.setText(_translate("actionWidget_Main", "REMOVE THIS ACTION"))
        self.actionCurrentSelection.setText(_translate("actionWidget_Main", "CURRENT SELECTION"))
        self.actionGlobalSongs.setText(_translate("actionWidget_Main", "GLOBAL SONGS"))
        self.actionOriginalSelection.setText(_translate("actionWidget_Main", "ORIGINAL SELECTION"))
import resources_rc
