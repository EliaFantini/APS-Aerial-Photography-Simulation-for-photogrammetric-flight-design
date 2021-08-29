from PyQt5 import QtCore, QtWidgets


class CustomSettingsGUI(object):
    def setup_ui(self, Dialog):
        '''
                instantiates dialog window's visual elements and sets preset choices, values range and stylesheets.
                Connects elements' events to specific class functions.
        '''
        Dialog.setObjectName("Dialog")
        Dialog.resize(421, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 40, 381, 151))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sensor_size_label = QtWidgets.QLabel(self.widget)
        self.sensor_size_label.setMinimumSize(QtCore.QSize(0, 30))
        self.sensor_size_label.setObjectName("sensor_size_label")
        self.horizontalLayout.addWidget(self.sensor_size_label)
        self.x_sensor_size_spinBox = QtWidgets.QDoubleSpinBox(self.widget)
        self.x_sensor_size_spinBox.setMinimumSize(QtCore.QSize(100, 30))
        self.x_sensor_size_spinBox.setObjectName("x_sensor_size_spinBox")
        self.horizontalLayout.addWidget(self.x_sensor_size_spinBox)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMaximumSize(QtCore.QSize(10, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.y_sensor_size_spinBox = QtWidgets.QDoubleSpinBox(self.widget)
        self.y_sensor_size_spinBox.setMinimumSize(QtCore.QSize(100, 30))
        self.y_sensor_size_spinBox.setObjectName("y_sensor_size_spinBox")
        self.horizontalLayout.addWidget(self.y_sensor_size_spinBox)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.resolution_label = QtWidgets.QLabel(self.widget)
        self.resolution_label.setMinimumSize(QtCore.QSize(210, 0))
        self.resolution_label.setObjectName("resolution_label")
        self.horizontalLayout_2.addWidget(self.resolution_label)
        self.x_resolution_spinBox = QtWidgets.QSpinBox(self.widget)
        self.x_resolution_spinBox.setMinimumSize(QtCore.QSize(100, 30))
        self.x_resolution_spinBox.setObjectName("x_resolution_spinBox")
        self.horizontalLayout_2.addWidget(self.x_resolution_spinBox)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setMaximumSize(QtCore.QSize(10, 16777215))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.y_resolution_spinBox = QtWidgets.QSpinBox(self.widget)
        self.y_resolution_spinBox.setMinimumSize(QtCore.QSize(100, 30))
        self.y_resolution_spinBox.setObjectName("y_resolution_spinBox")
        self.horizontalLayout_2.addWidget(self.y_resolution_spinBox)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslate_ui(Dialog)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.x_sensor_size_spinBox.setRange(0.01, 99999999.0)
        self.y_sensor_size_spinBox.setRange(0.01, 99999999.0)
        self.x_resolution_spinBox.setRange(1, 99999999)
        self.y_resolution_spinBox.setRange(1, 99999999)

    def retranslate_ui(self, Dialog):
        '''
                initializes window's textual content
        '''
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select custom settings"))
        self.sensor_size_label.setText(_translate("Dialog", "Sensor size:"))
        self.label_2.setText(_translate("Dialog", "x"))
        self.label_3.setText(_translate("Dialog", "mm"))
        self.resolution_label.setText(_translate("Dialog", "Resolution:"))
        self.label_5.setText(_translate("Dialog", "x"))
        self.label_6.setText(_translate("Dialog", "pixel"))

    def reject(self):
        '''
                if reject button is pressed, the dialog window is closed and
                current dialog window's custom settings ignored.
        '''
        self.main_window.reject_customized_settings()

    def accept(self):
        '''
                if accept button is pressed, the dialog window is closed and
                current dialog window's custom settings are saved in MainWindowGUI's instance.
        '''
        self.main_window.customized_settings(self.x_sensor_size_spinBox.value() / 1000, self.y_sensor_size_spinBox.value() / 1000, self.x_resolution_spinBox.value(), self.y_resolution_spinBox.value())

    def set_main_window(self, main_window):
        '''
                saves a reference of the MainWindowGUI's instance.
        '''
        self.main_window = main_window



