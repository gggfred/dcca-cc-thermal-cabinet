import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtCore import QTimer, Slot

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from mainwindow_ui import Ui_MainWindow

import api

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.canvas = FigureCanvas(Figure(figsize=(5, 4), dpi=100))
        self.plt = self.canvas.figure.add_subplot(111)
        self.plt.set(xlim=(0, 120), ylim=(20, 50))
        self.plt.set_xlabel("tiempo")
        self.plt.set_ylabel("temperatura")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.frame_plt.setLayout(self.layout)

        self.plot_ref = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.refreshStates)
        self.timer.start(10000)

        self.refreshStates()
        self.pushButton.clicked.connect(self.refreshStates)

    def refreshStates(self):
        self.getTemp()
        self.getDoorState()
        self.refresh()

    def getTemp(self):
        temp = api.getTemperature()
        self.lcdNumber.display(temp)

    def getDoorState(self):
        state = api.getDoorState()
        self.lineEdit.setText(state)

    def refresh(self):
        tt = []
        temperatures = []

        datalog = api.getHistory("1", 12)

        for i,m in enumerate(datalog):
            tt.append(12 - i)
            tempval = m.get('temperature')
            temperatures.append(tempval)

        # if self.plot_ref is None:
        #     plot_refs = self.plt.plot(tt, vc, '-')

        #     self.plot_ref = plot_refs[0]

        #     pass
        # else:
        #     self.plot_ref.set_ydata(vc)

        self.plt.clear()

        self.plt.plot(tt, temperatures, '-')

        self.canvas.draw()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

