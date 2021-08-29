import os
import rasterio as rs
from PyQt5.QtCore import QObject
import sys

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QStackedWidget

import CustomSettingsGUI
from rasterio.warp import Resampling
from PyQt5 import QtCore, QtWidgets, QtGui
import ProgressBarGUI


class StackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        QStackedWidget.__init__(self, parent=parent)

    def paintEvent(self, event):
        '''
                overrides method of class PyQt5.QtWidgets.QWidget changing  window's background.
        '''
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap("background.png"))
        QStackedWidget.paintEvent(self, event)


class MainWindowGUI(QObject):
    def setup_ui(self, MainWindow):
        '''
                instantiates window's visual elements and sets preset choices, values range and stylesheets.
                Connects elements' events to specific class functions.
        '''

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(979, 710)
        self.centralwidget = StackedWidget()

        self.centralwidget.setObjectName("centralwidget")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(830, 600, 100, 30))
        self.start_button.setObjectName("start_button")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 901, 461))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.select_dem_label = QtWidgets.QLabel(self.layoutWidget)
        self.select_dem_label.setObjectName("select_dem_label")
        self.horizontalLayout.addWidget(self.select_dem_label)
        self.dem_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.dem_lineEdit.setObjectName("dem_lineEdit")
        self.horizontalLayout.addWidget(self.dem_lineEdit)
        self.select_dem_button = QtWidgets.QPushButton(self.layoutWidget)
        self.select_dem_button.setObjectName("select_dem_button")
        self.horizontalLayout.addWidget(self.select_dem_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.select_orthophoto_label = QtWidgets.QLabel(self.layoutWidget)
        self.select_orthophoto_label.setObjectName("select_orthophoto_label")
        self.horizontalLayout_2.addWidget(self.select_orthophoto_label)
        self.orthophoto_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.orthophoto_lineEdit.setObjectName("orthophoto_lineEdit")
        self.horizontalLayout_2.addWidget(self.orthophoto_lineEdit)
        self.select_orthophoto_button = QtWidgets.QPushButton(self.layoutWidget)
        self.select_orthophoto_button.setObjectName("select_orthophoto_button")
        self.horizontalLayout_2.addWidget(self.select_orthophoto_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.select_pc_label = QtWidgets.QLabel(self.layoutWidget)
        self.select_pc_label.setObjectName("select_pc_label")
        self.horizontalLayout_3.addWidget(self.select_pc_label)
        self.pc_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.pc_lineEdit.setObjectName("pc_lineEdit")
        self.horizontalLayout_3.addWidget(self.pc_lineEdit)
        self.select_pc_button = QtWidgets.QPushButton(self.layoutWidget)
        self.select_pc_button.setObjectName("select_pc_button")
        self.horizontalLayout_3.addWidget(self.select_pc_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.select_saving_folder_label = QtWidgets.QLabel(self.layoutWidget)
        self.select_saving_folder_label.setObjectName("select_saving_folder_label")
        self.horizontalLayout_4.addWidget(self.select_saving_folder_label)
        self.save_folder_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.save_folder_lineEdit.setObjectName("save_folder_lineEdit")
        self.horizontalLayout_4.addWidget(self.save_folder_lineEdit)
        self.select_saving_folder_button = QtWidgets.QPushButton(self.layoutWidget)
        self.select_saving_folder_button.setObjectName("select_saving_folder_button")
        self.horizontalLayout_4.addWidget(self.select_saving_folder_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.preset_or_custom_label = QtWidgets.QLabel(self.layoutWidget)
        self.preset_or_custom_label.setObjectName("preset_or_custom_label")
        self.verticalLayout.addWidget(self.preset_or_custom_label)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.image_sensor_label = QtWidgets.QLabel(self.layoutWidget)
        self.image_sensor_label.setObjectName("image_sensor_label")
        self.horizontalLayout_7.addWidget(self.image_sensor_label)
        self.sensor_size_comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.sensor_size_comboBox.setObjectName("sensor_size_comboBox")
        self.horizontalLayout_7.addWidget(self.sensor_size_comboBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.image_resolution_label = QtWidgets.QLabel(self.layoutWidget)
        self.image_resolution_label.setObjectName("image_resolution_label")
        self.horizontalLayout_8.addWidget(self.image_resolution_label)
        self.image_resolution_comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.image_resolution_comboBox.setObjectName("image_resolution_comboBox")
        self.horizontalLayout_8.addWidget(self.image_resolution_comboBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9.addLayout(self.verticalLayout_3)
        self.custom_settings_button = QtWidgets.QToolButton(self.layoutWidget)
        self.custom_settings_button.setObjectName("custom_settings_button")
        self.horizontalLayout_9.addWidget(self.custom_settings_button)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.focal_length_label = QtWidgets.QLabel(self.layoutWidget)
        self.focal_length_label.setObjectName("focal_length_label")
        self.horizontalLayout_12.addWidget(self.focal_length_label)
        self.focal_length_spinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.focal_length_spinBox.setObjectName("focal_length_spinBox")
        self.horizontalLayout_12.addWidget(self.focal_length_spinBox)
        self.pp_coordinates_label = QtWidgets.QLabel(self.layoutWidget)
        self.pp_coordinates_label.setObjectName("pp_coordinates_label")
        self.horizontalLayout_12.addWidget(self.pp_coordinates_label)
        self.pp_xi_offset_spinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.pp_xi_offset_spinBox.setObjectName("pp_xi_offset_spinBox")
        self.horizontalLayout_12.addWidget(self.pp_xi_offset_spinBox)
        self.pp_eta_offset_spinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.pp_eta_offset_spinBox.setObjectName("pp_eta_offset_spinBox")
        self.horizontalLayout_12.addWidget(self.pp_eta_offset_spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.resampling_algorithm_dem_label = QtWidgets.QLabel(self.layoutWidget)
        self.resampling_algorithm_dem_label.setObjectName("resampling_algorithm_dem_label")
        self.horizontalLayout_14.addWidget(self.resampling_algorithm_dem_label)
        self.dem_resampling_algorithm_comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.dem_resampling_algorithm_comboBox.setObjectName("dem_resampling_algorithm_comboBox")
        self.horizontalLayout_14.addWidget(self.dem_resampling_algorithm_comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.resampling_algorithm_image_label = QtWidgets.QLabel(self.layoutWidget)
        self.resampling_algorithm_image_label.setObjectName("resampling_algorithm_image_label")
        self.horizontalLayout_13.addWidget(self.resampling_algorithm_image_label)
        self.image_resampling_algorithm_comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.image_resampling_algorithm_comboBox.setObjectName("image_resampling_algorithm_comboBox")
        self.horizontalLayout_13.addWidget(self.image_resampling_algorithm_comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 979, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslate_ui(MainWindow)

        self.custom = False
        self.start_button.setEnabled(False)

        self.pc_lineEdit.editingFinished.connect(self.editing_finished_slot)
        self.dem_lineEdit.editingFinished.connect(self.editing_finished_slot)
        self.orthophoto_lineEdit.editingFinished.connect(self.editing_finished_slot)
        self.save_folder_lineEdit.editingFinished.connect(self.editing_finished_slot)
        self.select_orthophoto_button.clicked.connect(self.browse_slot)
        self.select_pc_button.clicked.connect(self.browse_slot)
        self.select_dem_button.clicked.connect(self.browse_slot)
        self.select_saving_folder_button.clicked.connect(self.browse_slot)
        self.start_button.clicked.connect(self.on_next_button_pressed)
        self.start_button.clicked.connect(MainWindow.close)
        self.custom_settings_button.clicked.connect(self.on_custom_settings_button_pressed)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sensor_size_comboBox.setCurrentIndex(0)
        self.sensor_size_comboBox.addItem("Full-frame (36 x 24 mm)", [0.036, 0.024])
        self.sensor_size_comboBox.addItem("APS- Canon (28.7 x 19 mm)", [0.0287, 0.019])
        self.sensor_size_comboBox.addItem("APS-C (23.5 x 15.6 mm)", [0.0235, 0.0156])
        self.sensor_size_comboBox.addItem("APS-C Canon (22.2 x 14.8 mm)", [0.0222, 0.0148])
        self.sensor_size_comboBox.addItem("Foveon Sigma (20.7 x 13.8 mm)", [0.0207, 0.0138])
        self.sensor_size_comboBox.addItem("M4/3 (17.3 x 13 mm)", [0.0173, 0.013])
        self.sensor_size_comboBox.addItem("1\" (13.2 x 8.8 mm)", [0.0132, 0.0088])
        self.sensor_size_comboBox.addItem("2/3\" (8.6 x 6.6 mm)", [0.0086, 0.0066])
        self.sensor_size_comboBox.addItem("1/1.8\" (7.18 x 5.32 mm)", [0.00718, 0.00532])
        self.sensor_size_comboBox.addItem("1/2.3\" (6.17 x 4.55 mm)", [0.00617, 0.00455])
        self.sensor_size_comboBox.addItem("1/2.5\" (5.8 x 4.3 mm)", [0.0058, 0.0043])

        self.image_resolution_comboBox.setCurrentIndex(0)
        self.image_resolution_comboBox.addItem("3.456x2.304 3:2 aspect ratio 8Mpx", [3456, 2304])
        self.image_resolution_comboBox.addItem("3.264x2.448 4:3 aspect ratio 8Mpx", [3264, 2448])
        self.image_resolution_comboBox.addItem("3.504x2.336 3:2 aspect ratio 8,2Mpx", [3504, 2336])
        self.image_resolution_comboBox.addItem("3.520x2.344 3:2 aspect ratio 8,25", [3520, 2344])
        self.image_resolution_comboBox.addItem("3.648x2.736 4:3 aspect ratio 10Mpx", [3648, 2736])
        self.image_resolution_comboBox.addItem("3.872x2.592 3:2 aspect ratio 10Mpx", [3872, 2592])
        self.image_resolution_comboBox.addItem("13.888x2.592 3:2 aspect ratio 10,1Mpx", [13888, 2592])
        self.image_resolution_comboBox.addItem("4.064x2.704 3:2 aspect ratio 11Mpx", [4064, 2704])
        self.image_resolution_comboBox.addItem("4.000x3.000 4:3 aspect ratio 12Mpx", [4000, 3000])
        self.image_resolution_comboBox.addItem("4.256x2.834 3:2 aspect ratio 12,1Mpx", [4256, 2834])
        self.image_resolution_comboBox.addItem("4.272x2.848 3:2 aspect ratio 12,2Mpx", [4272, 2848])
        self.image_resolution_comboBox.addItem("4.288x2.848 3:2 aspect ratio 12,2Mpx", [4288, 2848])
        self.image_resolution_comboBox.addItem("4.368x2.912 3:2 aspect ratio 12,7Mpx", [4368, 2912])
        self.image_resolution_comboBox.addItem("4.672x3.104 3:2 aspect ratio 14,5Mpx", [4672, 3104])
        self.image_resolution_comboBox.addItem("4.928x3.264 3:2 aspect ratio 16,3Mpx", [4928, 3264])
        self.image_resolution_comboBox.addItem("4.992x3.328 3:2 aspect ratio 16,6Mpx", [4992, 3328])
        self.image_resolution_comboBox.addItem("5.184x3.456 3:2 aspect ratio 18Mpx", [5184, 3456])
        self.image_resolution_comboBox.addItem("5.616x3.744 3:2 aspect ratio 21Mpx", [5616, 3744])
        self.image_resolution_comboBox.addItem("6.048x4.032 3:2 aspect ratio 24,4Mpx", [6048, 4032])
        self.image_resolution_comboBox.addItem("7.360x4.912 4:3 aspect ratio 36,2Mpx", [7360, 4912])
        self.image_resolution_comboBox.addItem("7.212x5.142 4:3 aspect ratio 39Mpx", [7212, 5142])
        self.image_resolution_comboBox.addItem("7.264x5.440 4:3 aspect ratio 40Mpx", [7264, 5440])
        self.image_resolution_comboBox.addItem("7.952x5.304 4:3 aspect ratio 42,4Mpx", [7952, 5304])
        self.image_resolution_comboBox.addItem("8.176x6.132 4:3 aspect ratio 50,1Mpx", [8176, 6132])
        self.image_resolution_comboBox.addItem("8.984x6.732 4:3 aspect ratio 60,5Mpx", [8984, 6732])

        self.dem_resampling_algorithm_comboBox.setCurrentIndex(0)
        self.dem_resampling_algorithm_comboBox.addItem("nearest", Resampling.nearest)
        self.dem_resampling_algorithm_comboBox.addItem("bilinear", Resampling.bilinear)
        self.dem_resampling_algorithm_comboBox.addItem("cubic", Resampling.cubic)
        self.dem_resampling_algorithm_comboBox.addItem("cubic_spline", Resampling.cubic_spline)
        self.dem_resampling_algorithm_comboBox.addItem("lanczos", Resampling.lanczos)
        self.dem_resampling_algorithm_comboBox.addItem("average", Resampling.average)
        self.dem_resampling_algorithm_comboBox.addItem("mode", Resampling.mode)
        self.dem_resampling_algorithm_comboBox.addItem("max", Resampling.max)
        self.dem_resampling_algorithm_comboBox.addItem("min", Resampling.min)
        self.dem_resampling_algorithm_comboBox.addItem("med", Resampling.med)
        self.dem_resampling_algorithm_comboBox.addItem("q1", Resampling.q1)
        self.dem_resampling_algorithm_comboBox.addItem("q3", Resampling.q3)

        self.image_resampling_algorithm_comboBox.setCurrentIndex(0)
        self.image_resampling_algorithm_comboBox.addItem("nearest")
        self.image_resampling_algorithm_comboBox.addItem("linear")
        self.image_resampling_algorithm_comboBox.addItem("cubic")

        self.focal_length_spinBox.setRange((15 * (self.sensor_size_comboBox.currentData()[0] / 0.036)),
                                           (90 * (self.sensor_size_comboBox.currentData()[0] / 0.036)))
        self.pp_xi_offset_spinBox.setRange(0.0, 99999999.0)
        self.pp_eta_offset_spinBox.setRange(0.0, 99999999.0)
        self.sensor_size_comboBox.currentIndexChanged.connect(self.update_focal_length_range)

        self.select_dem_button.setStyleSheet("background: white;")
        self.select_orthophoto_button.setStyleSheet("background: white;")
        self.select_pc_button.setStyleSheet("background: white;")
        self.select_saving_folder_button.setStyleSheet("background: white;")
        self.start_button.setStyleSheet("background: white;")
        self.custom_settings_button.setStyleSheet("background: white;")
        self.sensor_size_comboBox.setStyleSheet("background: white;")
        self.image_resolution_comboBox.setStyleSheet("background: white;")
        self.dem_resampling_algorithm_comboBox.setStyleSheet("background: white;")
        self.image_resampling_algorithm_comboBox.setStyleSheet("background: white;")

        self.statusbar.hide()

    def retranslate_ui(self, MainWindow):
        '''
                initializes window's textual content
        '''
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aerial Photography Simulation"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.select_dem_label.setText(_translate("MainWindow", "Select DEM file (.tif):"))
        self.select_dem_button.setText(_translate("MainWindow", "Browse"))
        self.select_orthophoto_label.setText(_translate("MainWindow", "Select orthophoto file (.tif):"))
        self.select_orthophoto_button.setText(_translate("MainWindow", "Browse"))
        self.select_pc_label.setText(_translate("MainWindow", "Select projections\' centers parameters file (.txt):"))
        self.select_pc_button.setText(_translate("MainWindow", "Browse"))
        self.select_saving_folder_label.setText(_translate("MainWindow", "Select saving folder path:"))
        self.select_saving_folder_button.setText(_translate("MainWindow", "Browse"))
        self.preset_or_custom_label.setText(_translate("MainWindow",
                                                       "Select a camera parameters\'s preset or click the button to choose customized camera settings:"))
        self.image_sensor_label.setText(_translate("MainWindow", "Image sensor format(mm x mm):"))
        self.image_resolution_label.setText(_translate("MainWindow", "Image resolution (Megapixel):"))
        self.custom_settings_button.setText(_translate("MainWindow", "..."))
        self.focal_length_label.setText(_translate("MainWindow", "Focal lenght (mm)"))
        self.pp_coordinates_label.setText(_translate("MainWindow", "Principal point coordinates in mm (ξ,η):"))
        self.resampling_algorithm_dem_label.setText(
            _translate("MainWindow", "Resampling algorithm for DEM to orthophoto reprojection:"))
        self.resampling_algorithm_image_label.setText(
            _translate("MainWindow", "Resampling algorithm for simulated image:"))

    def update_focal_length_range(self):
        '''
                updates focal length spinbox's max/min values according to the chosen sensor size preset.
        '''
        self.focal_length_spinBox.setRange((15 * (self.sensor_size_comboBox.currentData()[0] / 0.036)),
                                           (90 * (self.sensor_size_comboBox.currentData()[0] / 0.036)))

    def editing_finished_slot(self):
        '''
                opens up the file/folder in the path contained in the sender (editLine) .
                If the chosen file/folder isn't correct or doesn't exist,
                the editLine's text is replaced with  a blank line.
        '''
        sender = self.sender()
        if sender == self.dem_lineEdit:
            arg = 'dem'
            lineText = self.dem_lineEdit
        if sender == self.orthophoto_lineEdit:
            arg = 'ortho'
            lineText = self.orthophoto_lineEdit
        if sender == self.pc_lineEdit:
            arg = 'pcf'
            lineText = self.pc_lineEdit
        if sender == self.save_folder_lineEdit:
            arg = 'save'
            lineText = self.save_folder_lineEdit
        if not self.is_valid(lineText.text(), arg):
            lineText.setText("")
        if self.dem_lineEdit.text() != "" and self.orthophoto_lineEdit.text() != "" and self.pc_lineEdit.text() != "" and self.save_folder_lineEdit.text() != "":
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def browse_slot(self):
        '''
                opens up a search file/folder window with the correct file'
                 suffix filter depending on the button pressed.
                If the chosen file/folder is correct, the button's corresponding
                editLine is filled with the path.
        '''
        sender = self.sender()
        if sender == self.select_dem_button:
            caption = "Select DEM"
            filter = "Tif files(*.tif)"
            arg = 'dem'
            lineText = self.dem_lineEdit
        if sender == self.select_orthophoto_button:
            caption = "Select orthophoto"
            filter = "Tif files(*.tif)"
            arg = 'ortho'
            lineText = self.orthophoto_lineEdit
        if sender == self.select_pc_button:
            caption = "Select projections' centers' file"
            filter = "Txt files(*.txt)"
            arg = 'pcf'
            lineText = self.pc_lineEdit
        if sender == self.select_saving_folder_button:
            caption = "Select saving folder"
            options = QtWidgets.QFileDialog.Options()
            directoryName = QtWidgets.QFileDialog.getExistingDirectory(
                None,
                caption=caption,
                directory="",
                options=options)
            if directoryName:
                self.set_file_name(directoryName, 'save', self.save_folder_lineEdit)
            if self.dem_lineEdit.text() != "" and self.orthophoto_lineEdit.text() != "" and self.pc_lineEdit.text() != "" and self.save_folder_lineEdit.text() != "":
                self.start_button.setEnabled(True)
            else:
                self.start_button.setEnabled(False)
            return
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            caption,
            "",
            filter,
            options=options)
        if fileName:
            self.set_file_name(fileName, arg, lineText)
        if self.dem_lineEdit.text() != "" and self.orthophoto_lineEdit.text() != "" and self.pc_lineEdit.text() != "" and self.save_folder_lineEdit.text() != "":
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def on_custom_settings_button_pressed(self):
        '''
                opens up CustomSettingsGUI's dialog window
        '''
        self.window = QtWidgets.QDialog()
        self.ui = CustomSettingsGUI.CustomSettingsGUI()
        self.ui.setup_ui(self.window)
        self.ui.set_main_window(self)
        self.window.show()

    def reject_customized_settings(self):
        '''
                sets custom variable to False and enables
                preset choices.
        '''
        self.sensor_size_comboBox.setEnabled(True)
        self.image_resolution_comboBox.setEnabled(True)
        self.custom = False

    def customized_settings(self, sensor_width, sensor_heigth, x_pix_num,
                            y_pix_num):
        '''
                sets custom variable to True and saves
                all custom settings values to be used as parameters.
                Disables preset choices.
        '''
        self.sensor_width = sensor_width
        self.sensor_heigth = sensor_heigth
        self.x_pix_num = x_pix_num
        self.y_pix_num = y_pix_num
        self.sensor_size_comboBox.setEnabled(False)
        self.image_resolution_comboBox.setEnabled(False)
        self.focal_length_spinBox.setRange(0.0, 9999999.0)
        self.custom = True

    def on_next_button_pressed(self):
        '''
                changes the interface with the progress bar window (ProgressBarGUI) and calls its method "start" passing all spinBox,ComboBox,
                and editLine's values as parameters. It chooses between custom and preset settings depending on user's choice.
        '''
        if self.dem_lineEdit.text() != "" and self.orthophoto_lineEdit.text() != "" and self.pc_lineEdit.text() != "" and self.save_folder_lineEdit.text() != "":
            self.window = QtWidgets.QMainWindow()
            self.ui = ProgressBarGUI.ProgressBarGUI()
            self.ui.setup_ui(self.window)
            self.window.show()
            if self.custom:
                self.ui.start(self.orthophoto_lineEdit.text(), self.dem_lineEdit.text(), self.pc_lineEdit.text(),
                              self.save_folder_lineEdit.text() + "/",
                              self.dem_resampling_algorithm_comboBox.currentData(),
                              self.image_resampling_algorithm_comboBox.currentText(),
                              self.sensor_width, self.sensor_heigth,
                              self.x_pix_num, self.y_pix_num, self.pp_xi_offset_spinBox.value() / 1000,
                              self.pp_eta_offset_spinBox.value() / 1000,
                              self.focal_length_spinBox.value() / 1000)
            else:
                self.ui.start(self.orthophoto_lineEdit.text(), self.dem_lineEdit.text(), self.pc_lineEdit.text(),
                              self.save_folder_lineEdit.text() + "/",
                              self.dem_resampling_algorithm_comboBox.currentData(),
                              self.image_resampling_algorithm_comboBox.currentText(),
                              self.sensor_size_comboBox.currentData()[0], self.sensor_size_comboBox.currentData()[1],
                              self.image_resolution_comboBox.currentData()[0],
                              self.image_resolution_comboBox.currentData()[1], self.pp_xi_offset_spinBox.value() / 1000,
                              self.pp_eta_offset_spinBox.value() / 1000,
                              self.focal_length_spinBox.value() / 1000)

    def is_valid(self, fileName, type):
        '''
        returns True if the file in fileName's path exists and can be
        opened.  Returns False otherwise. If fileName is a folder, checks whether
        the folder actually exists
        '''
        if type == "ortho" or type == "dem":
            try:
                file = rs.open(fileName)
                file.close()
                return True
            except:
                return False
        if type == "pcf":
            try:
                file = open(fileName, 'r')
                file.close()
                return True
            except:
                return False
        if type == "save":
            return os.path.isdir(fileName)

    def set_file_name(self, fileName, type, editLine):
        '''
                sets editLine's text content to the folder/file path contained in fileName
        '''
        if self.is_valid(fileName, type):
            editLine.setText(fileName)
        else:
            editLine.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowGUI()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
