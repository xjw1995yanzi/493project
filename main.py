from PyQt5.QtWidgets import QApplication
from Windows import GomokuWindow
from Game import Gomoku
import sys

def main():
    # game = Gomoku()
    # game.play()
    app = QApplication(sys.argv)
    ex = GomokuWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()