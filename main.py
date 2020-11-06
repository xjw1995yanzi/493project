from PyQt5.QtWidgets import QApplication
from Windows import GomokuWindow
from TwoPlayerWindow import TwoPlayerGomokuWindow
from Game import Gomoku
from MainMenuWindow import MainMenu
import sys

def main():
    # game = Gomoku()
    # game.play()
    #while True:
    #    print("1. single_player mode\n2. two_player mode\n0. exit")
    #    chose = int(input("chose:"))
    #    if chose == 1:
    #        app = QApplication(sys.argv)
    #        ex = GomokuWindow()
    #        sys.exit(app.exec_())
    #        continue
    #    elif chose == 2:
    #        app = QApplication(sys.argv)
    #        ex = TwoPlayerGomokuWindow()
    #        sys.exit(app.exec_())
    #        continue
    #    elif chose == 0:
    #        return
    app = QApplication(sys.argv)
    ex = MainMenu()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()