import os
import random
import subprocess
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QStackedWidget

from ImageSimulator import ImageSimulator
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')


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


class ProgressBarGUI(QObject):
    def setup_ui(self, MainWindow):
        '''
                instantiates window's visual elements and sets preset choices, values range and stylesheets.
                Connects button's click event to a specific class function.
        '''
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)
        self.centralwidget = StackedWidget()

        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 210, 701, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.message_label = QtWidgets.QLabel(self.centralwidget)
        self.message_label.setGeometry(QtCore.QRect(50, 80, 691, 111))
        self.message_label.setAlignment(Qt.AlignBottom | Qt.AlignLeading | Qt.AlignLeft)
        self.message_label.setObjectName("message_label")
        self.finish_button = QtWidgets.QPushButton(self.centralwidget)
        self.finish_button.setEnabled(False)
        self.finish_button.setGeometry(QtCore.QRect(630, 500, 75, 23))
        self.finish_button.setObjectName("finish_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.finish_button.clicked.connect(self.on_finish_button_pressed)
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.progressBar.setStyleSheet("QProgressBar {"
                                       "text-align: center;"
                                       "}")
        self.finish_button.setStyleSheet("background: white;")
        self.statusbar.hide()

    def retranslate_ui(self, MainWindow):
        '''
                initializes window's textual content
        '''
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aerial Photography Simulation"))
        self.message_label.setText(_translate("MainWindow", "Wait for the process to end."))
        self.finish_button.setText(_translate("MainWindow", "Finish"))

    def start(self, orthophoto_path, dem_path, projection_centers_path, save_folder_path, dem_resampling_method,
              image_resampling_method,
              sensor_width, sensor_height, x_pix_num, y_pix_num, x_pc_offset, y_pc_offset, focal_length):
        '''
                counts the number of images to be simulated to count how many of them are completed during the process.
               It instantiates a thread, it instantiates and assigns a Worker to it and then it starts the thread.
               Connects worker's events' signals to thread and ProgressBarGUI functions.
        '''
        self.save_folder_path = save_folder_path
        lines_file = open(projection_centers_path, 'r')
        counter = 0
        for cam_parameters in lines_file:
            if cam_parameters[0] == '#' in cam_parameters:
                continue
            counter += 1
        lines_file.close()
        self.image_counter = 0
        self.number_of_images = counter
        message = "Wait for the process to end. Images processed: " + str(
            self.image_counter) + " out of " + str(
            self.number_of_images) + " .\nWhen an image simulation is completed the bar will change its color."
        self.message_label.setText(message)
        self.thread = QThread()
        self.worker = Worker(orthophoto_path, dem_path, projection_centers_path, save_folder_path,
                             dem_resampling_method, image_resampling_method,
                             sensor_width, sensor_height, x_pix_num, y_pix_num, x_pc_offset, y_pc_offset, focal_length)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.report_progress)
        self.worker.changeColor.connect(self.change_bar_color)
        self.thread.finished.connect(
            lambda: self.finish_button.setEnabled(True)
        )
        self.thread.start()

    def report_progress(self, n):
        '''
               updates progress bar's completion value
        '''
        self.progressBar.setValue(n)

    def change_bar_color(self):
        '''
               changes progress bar's color with a new randomly generated ones. It also updates
               the number of completed images' simulations.
        '''
        self.image_counter += 1
        message = "Wait for the process to end. Images processed: " + str(
            self.image_counter) + " out of " + str(
            self.number_of_images) + " .\nWhen an image simulation is completed the bar will change its color."
        self.message_label.setText(message)
        random_number = random.randint(0, 16777215)
        hex_number = str(hex(random_number))
        hex_number = '#' + hex_number[2:]
        self.progressBar.setStyleSheet("QProgressBar {"
                                       "text-align: center;"
                                       "}"
                                       "QProgressBar::chunk "
                                       "{"
                                       "background-color: " + hex_number + ";"
                                                                           "border : 1px"
                                                                           "}")

    def on_finish_button_pressed(self):
        '''
               closes the program and opens up file explorer's program on selected save folder.
        '''
        path = os.path.normpath(self.save_folder_path)
        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
        sys.exit()


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    changeColor = pyqtSignal()

    def __init__(self, orthophoto_path, dem_path, projection_centers_path,
                 save_folder_path, dem_resampling_method, image_resampling_method, sensor_width,
                 sensor_height, x_pix_num, y_pix_num, x_pc_offset, y_pc_offset,
                 focal_length):
        '''
               saves values for ImageSimulator
        '''
        super(QObject, self).__init__()
        self.orthophoto_path = orthophoto_path
        self.dem_path = dem_path
        self.projection_centers_path = projection_centers_path
        self.save_folder_path = save_folder_path
        self.dem_resampling_method = dem_resampling_method
        self.image_resampling_method = image_resampling_method
        self.sensor_width = sensor_width
        self.sensor_height = sensor_height
        self.x_pix_num = x_pix_num
        self.y_pix_num = y_pix_num
        self.x_pc_offset = x_pc_offset
        self.y_pc_offset = y_pc_offset
        self.focal_length = focal_length

    def run(self):
        '''
               instantiates ImageSimulator passing saved values, then starts it. Once the execution is complete,
               the finished signal is issued.
        '''
        image_simulator = ImageSimulator(self.orthophoto_path, self.dem_path, self.projection_centers_path,
                                         self.save_folder_path, self.dem_resampling_method,
                                         self.image_resampling_method, self.sensor_width,
                                         self.sensor_height, self.x_pix_num, self.y_pix_num, self.x_pc_offset,
                                         self.y_pc_offset,
                                         self.focal_length, self.progress, self.changeColor)
        image_simulator.start()
        self.finished.emit()
