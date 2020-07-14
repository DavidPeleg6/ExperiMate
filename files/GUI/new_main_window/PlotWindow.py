from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import pandas as pd


class PlotWindow(QWidget):
    """
    this is a class representing the plot, gets a pandas dataframe and plots it in a window
    """
    # interval = 0 means that the graph is static
    # gets an
    def __init__(self, name, icon, data_observer=None, live=False):
        super(PlotWindow, self).__init__()
        # TODO this should be in a toolbar
        self.name, self.df = name, data_observer
        self.setWindowIcon(icon)
        self.setWindowTitle(name)
        self.setup_UI(live)

    def setup_UI(self, live):
        self.layout = QtWidgets.QVBoxLayout()
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.zoom_in_btn = QtWidgets.QPushButton('Zoom in')
        self.zoom_out_btn = QtWidgets.QPushButton('Zoom out')
        self.canvas = Canvas(plot_observer=self.df, parent=self, live=live)
        self.layout.addWidget(self.canvas)
        self.btn_layout.addWidget(self.zoom_in_btn)
        self.btn_layout.addWidget(self.zoom_out_btn)
        self.layout.addItem(self.btn_layout)
        self.setLayout(self.layout)
        self.resize(800, 600)
        self.show()


class Canvas(FigureCanvas):
    def __init__(self, plot_observer, parent=None, width=5, height=5, dpi=100, live=False):
        self.observer = plot_observer
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.ax = self.figure.add_subplot(1, 1, 1)
        if live:
            self.ani = animation.FuncAnimation(self.figure, self.live_plot, interval=100)
        else:
            self.plot()

    def live_plot(self, i):
        df = self.observer.get_dataframe()
        if df is None:
            if self.observer.started:
                self.ani.event_source.stop()
            return
        self.ax.clear()
        self.ax.plot(pd.to_numeric(df.iloc[:, 1]), pd.to_numeric(df.iloc[:, 0]))
        self.ax.set_xlabel(df.columns[1])
        self.ax.set_ylabel(df.columns[0])
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator())
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator())

    def plot(self):
        df = self.observer.get_dataframe()
        if df is None:
            raise SystemError("no data to plot")
        self.ax.plot(pd.to_numeric(df.iloc[:, 1]), pd.to_numeric(df.iloc[:, 0]))
        self.ax.set_xlabel(df.columns[1])
        self.ax.set_ylabel(df.columns[0])
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator())
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator())



"""
app = QApplication(sys.argv)
icont = QtGui.QIcon()
icont.addPixmap(QtGui.QPixmap("images/index.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
window = PlotWindow('plot', loc='', icon=icont)
app.exec()
"""
"""
df = pd.read_csv('../../results/rgerge.csv')

fig, ax = plt.subplots()
ax.plot(df.iloc[:, 1], df.iloc[:, 0])
ax.set_xlabel(df.columns[1])
ax.set_ylabel(df.columns[0])
ax.xaxis.set_major_locator(ticker.MaxNLocator())
ax.yaxis.set_major_locator(ticker.MaxNLocator())
# ax.tick_params(axis='both', which='both', pad=10)
plt.show()

"""