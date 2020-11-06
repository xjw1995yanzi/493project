from PyQt5.Qt import *
from TwoPlayerWindow import TwoPlayerGomokuWindow
from Windows import GomokuWindow
import traceback
import sys

def run_with_exc(f):
    """output error with messagebox"""

    def call(window, *args, **kwargs):
        try:
            return f(window, *args, **kwargs)
        except Exception:
            exc_info = traceback.format_exc()
            QMessageBox.about(window, 'Error', exc_info)
    return call


class SingleModeLabel(QLabel):

    def enterEvent(self, *args, **kwargs):
        #print("mouse in")
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, *args, **kwargs):
        #print("mouse out")
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)

    @run_with_exc
    def mousePressEvent(self, *args, **kwargs):
        self.singleplayermode = GomokuWindow()

class TwoModeLabel(QLabel):

    def enterEvent(self, *args, **kwargs):
        #print("mouse in")
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, *args, **kwargs):
       # print("mouse out")
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)

    @run_with_exc
    def mousePressEvent(self, *args, **kwargs):
        self.twoplayersmode = TwoPlayerGomokuWindow()


class ExitLabel(QLabel):

    def enterEvent(self, *args, **kwargs):
        #print("mouse in")
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, *args, **kwargs):
        #print("mouse out")
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)

    @run_with_exc
    def mousePressEvent(self, *args, **kwargs):
        sys.exit()


class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def paintEvent(self, e):
        qp = QPainter()
        qp.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidLine))
        qp.begin(self)
        qp.drawRect(25, 25, 550, 750)
        qp.end()

    def init_ui(self):
        self.setObjectName('MainWindow')
        self.setWindowTitle('Gomoku')
        self.setFixedSize(600, 800)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/wooden.jpg')))
        self.setPalette(palette)

        label = QLabel(self)
        label.setText("GOMOKU")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        label.move(250, 100)
        print(label.size())

        label1 = SingleModeLabel(self)
        label1.setText("Single Player Mode")
        label1.move(175, 200)
        label1.resize(250, 50)
        label1.setStyleSheet("color:rgb(10,10,10,255);font-size:20px;font-weight:bold;font-family:Roman times;")
        label1.setAlignment(Qt.AlignCenter)
        label1.setFrameStyle(QFrame.Panel | QFrame.Raised)


        label2 = TwoModeLabel(self)
        label2.setText("Two Player Mode")
        label2.move(175, 300)
        label2.resize(250, 50)
        label2.setStyleSheet("color:rgb(10,10,10,255);font-size:20px;font-weight:bold;font-family:Roman times;")
        label2.setAlignment(Qt.AlignCenter)
        label2.setFrameStyle(QFrame.Panel | QFrame.Raised)

        label3 = ExitLabel(self)
        label3.setText("Exit")
        label3.move(200, 400)
        label3.resize(200, 50)
        label3.setStyleSheet("color:rgb(10,10,10,255);font-size:20px;font-weight:bold;font-family:Roman times;")
        label3.setAlignment(Qt.AlignCenter)
        label3.setFrameStyle(QFrame.Panel | QFrame.Raised)

        self.show()