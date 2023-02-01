import sys

import numpy as np
from PyQt5 import QtWidgets, uic, QtGui
import cv2
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene


class Cv(QThread):
    cap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.cap_signal.emit(frame)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi('ui/MainWindow.ui', self)
        self.pushButton_start.clicked.connect(self.start)
        self.cap_thread = Cv()
        self.cap_thread.cap_signal.connect(self.update_frame)
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.zoom = 1
        self.show()

    def start(self):
        self.cap_thread.start()

    @pyqtSlot(np.ndarray)
    def update_frame(self, frame):
        qt_img = self.convertCvQt(frame)
        self.scene.addPixmap(qt_img)
        # self.graphicsView
        # self.label.setPixmap(qt_img)

    def convertCvQt(self, cvimg):
        rgbimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        
        h, w, c = rgbimg.shape
        bpl = c * w
        qimg = QImage(rgbimg.data, w, h, bpl, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        self.zoom += a0.angleDelta().y() / 2800
        self.graphicsView.scale(self.zoom, self.zoom)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
