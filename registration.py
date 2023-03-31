import sys, amcam
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox
import numpy as np
import cv2

prevImgArray = None # use this to store the previous frame's image

# crop to 510x510 square at center of image
def cropImage(img):
    k = 510
    x = (img.width() // 2) - (k // 2)
    y = (img.height() // 2) - (k // 2)
    croppedImg = QImage.copy(img, x, y, k, k)
    return croppedImg

# converts a QImage into an OpenCV MAT format
def QImageToCvMat(incomingImage):
    # incomingImage = incomingImage.convertToFormat(QImage.Format_RGB888)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr

# run registration algorithm using opencv
def runRegistration(currImgArray):
    # do registration stuff





    # save this frame's array data for the next frame of registration
    prevImgArray = currImgArray

class MainWin(QWidget):
    eventImage = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.hcam = None
        self.buf = None      # video buffer
        self.w = 0           # video width
        self.h = 0           # video height
        self.total = 0
        self.setFixedSize(800, 600)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.initUI()
        self.initCamera()

    def initUI(self):
        self.cb = QCheckBox('Auto Exposure', self)
        self.cb.stateChanged.connect(self.changeAutoExposure)
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.move(0, 30)
        self.label.resize(self.geometry().width(), self.geometry().height())

# the vast majority of callbacks come from amcam.dll/so/dylib internal threads, so we use qt signal to post this event to the UI thread  
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == amcam.AMCAM_EVENT_IMAGE:
            ctx.eventImage.emit()

# run in the UI thread
    @pyqtSlot()
    def eventImageSignal(self):
        if self.hcam is not None:
            try:
                self.hcam.PullImageV2(self.buf, 24, None)
                self.total += 1
            except amcam.HRESULTException as ex:
                QMessageBox.warning(self, '', 'pull image failed, hr=0x{:x}'.format(ex.hr), QMessageBox.Ok)
            else:
                self.setWindowTitle('{}: {}'.format(self.camname, self.total))
                img = QImage(self.buf, self.w, self.h, (self.w * 24 + 31) // 32 * 4, QImage.Format_RGB888)
                img = cropImage(img) # now that we have a new image, crop it to a square
                self.label.setPixmap(QPixmap.fromImage(img))
                imgMat = QImageToCvMat(img) # convert from img to numpy format
                runRegistration(imgMat) # run registration algorithm to compare to previous frame

    def initCamera(self):
        a = amcam.Amcam.EnumV2()
        if len(a) <= 0:
            self.setWindowTitle('No camera found')
            self.cb.setEnabled(False)
        else:
            self.camname = a[0].displayname
            self.setWindowTitle(self.camname)
            self.eventImage.connect(self.eventImageSignal)
            try:
                self.hcam = amcam.Amcam.Open(a[0].id)
            except amcam.HRESULTException as ex:
                QMessageBox.warning(self, '', 'failed to open camera, hr=0x{:x}'.format(ex.hr), QMessageBox.Ok)
            else:
                self.w, self.h = self.hcam.get_Size()
                bufsize = ((self.w * 24 + 31) // 32 * 4) * self.h
                self.buf = bytes(bufsize)
                self.cb.setChecked(self.hcam.get_AutoExpoEnable())            
                try:
                    if sys.platform == 'win32':
                        self.hcam.put_Option(amcam.AMCAM_OPTION_BYTEORDER, 0) # QImage.Format_RGB888
                    self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
                except amcam.HRESULTException as ex:
                    QMessageBox.warning(self, '', 'failed to start camera, hr=0x{:x}'.format(ex.hr), QMessageBox.Ok)

    def changeAutoExposure(self, state):
        if self.hcam is not None:
            self.hcam.put_AutoExpoEnable(state == Qt.Checked)

    def closeEvent(self, event):
        if self.hcam is not None:
            self.hcam.Close()
            self.hcam = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())