import os
import sys

from qtpy.QtWidgets import QApplication
from src.application.calc_window import CalculatorWindow

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    app.setStyle('Fusion')

    wnd = CalculatorWindow()
    wnd.show()

    sys.exit(app.exec_())
