# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyopqt.ui'
#
# Created by: PyQt5 UI code generator 5.15.0 and M0g1)
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# qtchooser -run-tool=designer -qt=5 to launch qt designer
# pyuic5 -x filename.ui -o python_file_name.py

from PyQt5 import QtCore, QtGui, QtWidgets

from view.opengl.pyqt.myopengl_widget import MyOpenGLWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # ===========openGL widget======================================
        self.openGLWidget = MyOpenGLWidget(self.centralwidget)
        self.openGLWidget.setMinimumSize(QtCore.QSize(780, 400))
        self.openGLWidget.setObjectName("openGLWidget")
        self.verticalLayout.addWidget(self.openGLWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        # =============layout and label============================================
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        # =============grid===========================================
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        # =============buttons===========================================
        self.btn_up = QtWidgets.QPushButton(self.centralwidget)
        self.btn_up.setObjectName("btn_up")
        self.gridLayout_2.addWidget(self.btn_up, 0, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_forward = QtWidgets.QPushButton(self.centralwidget)
        self.btn_forward.setObjectName("btn_forward")
        self.horizontalLayout_3.addWidget(self.btn_forward)
        self.btn_toward = QtWidgets.QPushButton(self.centralwidget)
        self.btn_toward.setObjectName("btn_toward")
        self.horizontalLayout_3.addWidget(self.btn_toward)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.btn_right = QtWidgets.QPushButton(self.centralwidget)
        self.btn_right.setObjectName("btn_right")
        self.gridLayout_2.addWidget(self.btn_right, 1, 2, 1, 1)
        self.btn_down = QtWidgets.QPushButton(self.centralwidget)
        self.btn_down.setObjectName("btn_down")
        self.gridLayout_2.addWidget(self.btn_down, 3, 1, 1, 1)
        self.btn_left = QtWidgets.QPushButton(self.centralwidget)
        self.btn_left.setObjectName("btn_left")
        self.gridLayout_2.addWidget(self.btn_left, 1, 0, 1, 1)
        self.btn_radio_wireframe = QtWidgets.QRadioButton(self.centralwidget)
        self.btn_radio_wireframe.setObjectName("radioButton_wireframe")
        self.gridLayout_2.addWidget(self.btn_radio_wireframe, 3, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_create_sphere = QtWidgets.QPushButton(self.centralwidget)
        self.btn_create_sphere.setObjectName("btn_create_sphere")
        self.horizontalLayout.addWidget(self.btn_create_sphere)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.set_btn_action()
        # ================upper menu==================================
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuedit = QtWidgets.QMenu(self.menubar)
        self.menuedit.setObjectName("menuedit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuedit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_btn_action(self):
        def btn_create_sphere() -> None:
            self.openGLWidget.is_draw ^= True
            self.openGLWidget.update()

        def btn_wireframe():
            self.openGLWidget.wireframe = self.btn_radio_wireframe.isChecked()
            self.openGLWidget.update()

        self.btn_create_sphere.clicked.connect(btn_create_sphere)
        self.btn_radio_wireframe.toggled.connect(btn_wireframe)
        self.btn_radio_wireframe.setChecked(True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Text Area"))
        self.btn_up.setText(_translate("MainWindow", "Up"))
        self.btn_forward.setText(_translate("MainWindow", "forward"))
        self.btn_toward.setText(_translate("MainWindow", "toward"))
        self.btn_right.setText(_translate("MainWindow", "right"))
        self.btn_down.setText(_translate("MainWindow", "down"))
        self.btn_left.setText(_translate("MainWindow", "left"))
        self.btn_radio_wireframe.setText(_translate("MainWindow", "lined wireframe"))
        self.btn_create_sphere.setText(_translate("MainWindow", "Create Sphere"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuedit.setTitle(_translate("MainWindow", "edit"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
