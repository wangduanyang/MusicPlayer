# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(758, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton_play = QtGui.QPushButton(self.centralwidget)
        self.pushButton_play.setGeometry(QtCore.QRect(480, 490, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_play.setFont(font)
        self.pushButton_play.setObjectName(_fromUtf8("pushButton_play"))
        self.pushButton_open_files = QtGui.QPushButton(self.centralwidget)
        self.pushButton_open_files.setGeometry(QtCore.QRect(0, 500, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_open_files.setFont(font)
        self.pushButton_open_files.setObjectName(_fromUtf8("pushButton_open_files"))
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 51, 341, 451))
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.pushButton_remove = QtGui.QPushButton(self.centralwidget)
        self.pushButton_remove.setGeometry(QtCore.QRect(170, 500, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_remove.setFont(font)
        self.pushButton_remove.setObjectName(_fromUtf8("pushButton_remove"))
        self.pushButton_open_dir = QtGui.QPushButton(self.centralwidget)
        self.pushButton_open_dir.setGeometry(QtCore.QRect(90, 500, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_open_dir.setFont(font)
        self.pushButton_open_dir.setObjectName(_fromUtf8("pushButton_open_dir"))
        self.volumeSlider = phonon.Phonon.VolumeSlider(self.centralwidget)
        self.volumeSlider.setGeometry(QtCore.QRect(100, 10, 241, 32))
        self.volumeSlider.setMouseTracking(False)
        self.volumeSlider.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.volumeSlider.setAcceptDrops(False)
        self.volumeSlider.setMaximumVolume(10.0)
        self.volumeSlider.setPageStep(3)
        self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))
        self.pushButton_sort = QtGui.QPushButton(self.centralwidget)
        self.pushButton_sort.setGeometry(QtCore.QRect(260, 500, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_sort.setFont(font)
        self.pushButton_sort.setObjectName(_fromUtf8("pushButton_sort"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 6, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(360, 490, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.listWidget_lrc = QtGui.QListWidget(self.centralwidget)
        self.listWidget_lrc.setGeometry(QtCore.QRect(350, 50, 401, 431))
        self.listWidget_lrc.setMouseTracking(True)
        self.listWidget_lrc.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.listWidget_lrc.setObjectName(_fromUtf8("listWidget_lrc"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 0, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(0, 550, 791, 17))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.seekSlider2 = phonon.Phonon.SeekSlider(self.splitter)
        self.seekSlider2.setEnabled(True)
        self.seekSlider2.setIconVisible(False)
        self.seekSlider2.setObjectName(_fromUtf8("seekSlider2"))
        self.label_time = QtGui.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.label_time.setFont(font)
        self.label_time.setObjectName(_fromUtf8("label_time"))
        self.pushButton_play.raise_()
        self.label_time.raise_()
        self.pushButton_open_files.raise_()
        self.listWidget.raise_()
        self.seekSlider2.raise_()
        self.label_time.raise_()
        self.seekSlider2.raise_()
        self.pushButton_remove.raise_()
        self.pushButton_open_dir.raise_()
        self.volumeSlider.raise_()
        self.pushButton_sort.raise_()
        self.label.raise_()
        self.comboBox.raise_()
        self.listWidget_lrc.raise_()
        self.label_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_play.setText(_translate("MainWindow", "Play", None))
        self.pushButton_open_files.setText(_translate("MainWindow", "Open Files", None))
        self.pushButton_remove.setText(_translate("MainWindow", "Remove", None))
        self.pushButton_open_dir.setText(_translate("MainWindow", "Open Dir", None))
        self.pushButton_sort.setText(_translate("MainWindow", "Sort", None))
        self.label.setText(_translate("MainWindow", "Playlist", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "Play Once", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "Single Cycle", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "List Loop", None))
        self.label_2.setText(_translate("MainWindow", "Lrc", None))
        self.label_time.setText(_translate("MainWindow", "0", None))

from PyQt4 import phonon