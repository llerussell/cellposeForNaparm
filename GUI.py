# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(431, 251)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ImagesLoaded_label = QtWidgets.QLabel(self.groupBox)
        self.ImagesLoaded_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ImagesLoaded_label.setObjectName("ImagesLoaded_label")
        self.horizontalLayout_2.addWidget(self.ImagesLoaded_label)
        self.gridLayout_2.addWidget(self.groupBox, 0, 2, 1, 1)
        self.settings_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.settings_groupBox.setObjectName("settings_groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.settings_groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.useGPU_checkBox = QtWidgets.QCheckBox(self.settings_groupBox)
        self.useGPU_checkBox.setText("")
        self.useGPU_checkBox.setChecked(True)
        self.useGPU_checkBox.setObjectName("useGPU_checkBox")
        self.gridLayout.addWidget(self.useGPU_checkBox, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.settings_groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.modelType_comboBox = QtWidgets.QComboBox(self.settings_groupBox)
        self.modelType_comboBox.setObjectName("modelType_comboBox")
        self.modelType_comboBox.addItem("")
        self.modelType_comboBox.addItem("")
        self.gridLayout.addWidget(self.modelType_comboBox, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.settings_groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.cellSize_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.settings_groupBox)
        self.cellSize_doubleSpinBox.setDecimals(0)
        self.cellSize_doubleSpinBox.setProperty("value", 10.0)
        self.cellSize_doubleSpinBox.setObjectName("cellSize_doubleSpinBox")
        self.gridLayout.addWidget(self.cellSize_doubleSpinBox, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.settings_groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.threshold_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.settings_groupBox)
        self.threshold_doubleSpinBox.setProperty("value", 0.4)
        self.threshold_doubleSpinBox.setObjectName("threshold_doubleSpinBox")
        self.gridLayout.addWidget(self.threshold_doubleSpinBox, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.settings_groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.setDefaults_pushButton = QtWidgets.QPushButton(self.settings_groupBox)
        self.setDefaults_pushButton.setObjectName("setDefaults_pushButton")
        self.verticalLayout_2.addWidget(self.setDefaults_pushButton)
        self.gridLayout_2.addWidget(self.settings_groupBox, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.run_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.run_pushButton.setObjectName("run_pushButton")
        self.verticalLayout.addWidget(self.run_pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 431, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cellpose for Naparm"))
        self.groupBox.setTitle(_translate("MainWindow", "Loaded images"))
        self.ImagesLoaded_label.setText(_translate("MainWindow", "Drag images here"))
        self.settings_groupBox.setTitle(_translate("MainWindow", "Settings"))
        self.label_4.setText(_translate("MainWindow", "Use GPU"))
        self.modelType_comboBox.setItemText(0, _translate("MainWindow", "cyto"))
        self.modelType_comboBox.setItemText(1, _translate("MainWindow", "nuclei"))
        self.label_3.setText(_translate("MainWindow", "Threshold"))
        self.label_2.setText(_translate("MainWindow", "Size"))
        self.label.setText(_translate("MainWindow", "Model"))
        self.setDefaults_pushButton.setText(_translate("MainWindow", "Set defaults"))
        self.run_pushButton.setText(_translate("MainWindow", "Run"))
