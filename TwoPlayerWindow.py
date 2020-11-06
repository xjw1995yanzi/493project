from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette, QBrush, QPixmap, QRadialGradient
from PyQt5.QtCore import Qt, QPoint, QTimer
import traceback
from Game import Gomoku
from corner_widget import CornerWidget


def run_with_exc(f):
    """output error with messagebox"""

    def call(window, *args, **kwargs):
        try:
            return f(window, *args, **kwargs)
        except Exception:
            exc_info = traceback.format_exc()
            QMessageBox.about(window, 'Error', exc_info)
    return call

class Turnlabel(QLabel):

    def changeturn(self, turn):
        if turn == 0:
            self.setText("Player1 Turn")
            self.setStyleSheet("color:rgb(10,10,10,255);font-size:13px;font-weight:bold;font-family:Roman times;")
        elif turn == 1:
            self.setText("Player2 Turn")
            self.setStyleSheet("color:rgb(10,10,10,255);font-size:13px;font-weight:bold;font-family:Roman times;")



class TwoPlayerGomokuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.g = Gomoku()
        self.last_pos = (-1, -1)
        self.res = 0
        self.operate_status = 0
        self.flash_pieces = ((-1, -1),)
        self.turn = 0
        self.label = Turnlabel(self)
        self.label.changeturn(self.turn)
        self.label.show()

    def init_ui(self):
        """init game interface"""
        # 1. title,size,color
        self.setObjectName('MainWindow')
        self.setWindowTitle('Two Player Mode')
        self.setFixedSize(650, 650)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/wooden.jpg')))
        self.setPalette(palette)
        # 2. Open mouse track. mark the current position
        self.setMouseTracking(True)
        # 3. Mark the position of mouse
        self.corner_widget = CornerWidget(self)
        self.corner_widget.repaint()
        self.corner_widget.hide()
        # 4. Game over flash timer
        self.end_timer = QTimer(self)
        self.end_timer.timeout.connect(self.end_flash)
        self.flash_cnt = 0
        self.flash_pieces = ((-1, -1),)
        # 5. show init_game_interface
        self.show()

    @run_with_exc
    def paintEvent(self, e):

        def draw_map():
            qp.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidLine))
            # draw row
            for x in range(15):
                qp.drawLine(40 * (x+1), 40, 40 * (x+1), 600)
            # draw list
            for y in range(15):
                qp.drawLine(40, 40 * (y + 1), 600, 40 * (y + 1))
            # black point in Gomoku board
            qp.setBrush(QColor(0, 0, 0))
            key_points = [(4, 4), (12, 4), (4, 12), (12, 12), (8, 8)]
            for t in key_points:
                qp.drawEllipse(QPoint(40 * t[0], 40 * t[1]), 5, 5)

        def draw_pieces():
            """draw pieces"""
            # black pieces
            qp.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            for x in range(15):
                for y in range(15):
                    if self.g.g_map[x][y] == 1:
                        if self.flash_cnt % 2 == 1 and (x, y) in self.flash_pieces:
                            continue
                        radial = QRadialGradient(40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35)
                        radial.setColorAt(0, QColor(96, 96, 96))
                        radial.setColorAt(1, QColor(0, 0, 0))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(40 * (x + 1), 40 * (y + 1)), 15, 15)
            # white pieces
            qp.setPen(QPen(QColor(255, 255, 255), 1, Qt.SolidLine))
            for x in range(15):
                for y in range(15):
                    if self.g.g_map[x][y] == 2:
                        if self.flash_cnt % 2 == 1 and (x, y) in self.flash_pieces:
                            continue
                        radial = QRadialGradient(40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35)
                        radial.setColorAt(0, QColor(255, 255, 255))
                        radial.setColorAt(1, QColor(160, 160, 160))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(40 * (x + 1), 40 * (y + 1)), 15, 15)

        if hasattr(self, 'g'):
            qp = QPainter()
            qp.begin(self)
            draw_map()
            draw_pieces()
            qp.end()

    @run_with_exc
    def mouseMoveEvent(self, e):
        # 1. judge the corresponding position
        mouse_x = e.windowPos().x()
        mouse_y = e.windowPos().y()
        if 25 <= mouse_x <= 615 and 25 <= mouse_y <= 615 and (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (
                mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
            game_x = int((mouse_x + 15) // 40) - 1
            game_y = int((mouse_y + 15) // 40) - 1
        else:  # If mouse is not on the board, mark as (-1, -1)
            game_x = -1
            game_y = -1
        # 2. judge whether the position has changed or not
        pos_change = False
        if game_x != self.last_pos[0] or game_y != self.last_pos[1]:
            pos_change = True
        self.last_pos = (game_x, game_y)
        # 3. mark the position based on the change of mouse position
        if pos_change and game_x != -1:
            self.setCursor(Qt.PointingHandCursor)
        if pos_change and game_x == -1:
            self.setCursor(Qt.ArrowCursor)
        if pos_change and game_x != -1:
            self.corner_widget.move(25 + game_x * 40, 25 + game_y * 40)
            self.corner_widget.show()
        if pos_change and game_x == -1:
            self.corner_widget.hide()

    @run_with_exc
    def mousePressEvent(self, e):
        """get the position of mouse"""
        if not (hasattr(self, 'operate_status') and self.operate_status == 0):
            return
        if e.button() == Qt.LeftButton:
            mouse_x = e.windowPos().x()
            mouse_y = e.windowPos().y()
            if (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
                game_x = int((mouse_x + 15) // 40) - 1
                game_y = int((mouse_y + 15) // 40) - 1
            else:  # wrong place
                # QMessageBox.about(self, "error!", "wrong place")
                return
            if self.g.g_map[game_x][game_y] == 0:
                self.g.move_1step(True, game_x, game_y, self.turn)
                self.turn = (self.turn + 1) % 2
                self.label.changeturn(self.turn)
            elif self.g.g_map[game_x][game_y] != 0:
                QMessageBox.about(self, "error!", "wrong place")
            # exec game loop
            res, self.flash_pieces = self.g.game_result(show=True)
            if res != 0:
                self.repaint(0, 0, 650, 650)
                self.game_restart(res)
                return

    @run_with_exc
    def end_flash(self):
        # pieces flash at the end of game
        if self.flash_cnt <= 5:
            # flash
            self.flash_cnt += 1
            self.repaint()
        else:
            # after flash
            self.end_timer.stop()
            # 1. Display Game Over message
            if self.res == 1:
                QMessageBox.about(self, 'Game Over', 'Player1 Win!')
            elif self.res == 2:
                QMessageBox.about(self, 'Game Over', 'Player2 Win!')
            elif self.res == 3:
                QMessageBox.about(self, 'Game Over', 'Draw!')
            else:
                raise ValueError('result value should be 1 , 2 , 3')
            # 2. Game restart
            self.res = 0
            self.operate_status = 0
            self.flash_cnt = 0
            self.g = Gomoku()
            self.repaint(0, 0, 650, 650)

    @run_with_exc
    def game_restart(self, res):
        """Game restart"""
        self.res = res
        self.operate_status = 1
        self.end_timer.start(300)
        self.turn = 0
        self.label.changeturn(self.turn)
