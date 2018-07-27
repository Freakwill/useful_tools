# -*- coding: utf-8 -*-


import sys
import random

import matplotlib
# matplotlib.use("Qt5Agg")

from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """FigureCanvas"""
    def __init__(self, parent=None, *args, **kwargs):
        super(MplCanvas, self).__init__(*args, **kwargs)
        self.axes = self.figure.add_subplot(111)
        # self.axes.hold(False)

        self._initial_figure()
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def _initial_figure(self):
        pass

    def clear(self):
        del self.axes.lines[:]
        # self.canvas.draw_idle()



class DynamicMplCanvas(MplCanvas):
    """动态画布：每秒自动更新，更换一条折线。"""
    def __init__(self, *args, **kwargs):
        super(DynamicMplCanvas, self).__init__(*args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        pass

class LabeledLineEdit(QWidget):
    '''
    LineEdit with Label
    '''
    def __init__(self, label='', *args, **kwargs):
        super(LabeledLineEdit, self).__init__()
        self.label = label
        layout = QHBoxLayout()
        label = QLabel(label)
        self.lineEdit = QLineEdit(*args, **kwargs)
        layout.addWidget(label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def __getattr__(self, prop):
        return getattr(self.lineEdit, prop)


class CommandLine(LabeledLineEdit):
    '''CommandLine
    LineEdit with Label
    '''
    def __init__(self, executor=None, prompt='>>>', *args, **kwargs):
        super(CommandLine, self).__init__(label=prompt, *args, **kwargs)
        self.prompt = prompt
        self.executor = executor

    def __call__(self, *args, **kwargs):
        if self.executor:
            return self.executor(self.command, *args, **kwargs)

    def keyPressEvent(self, e):        
        if e.key() == QtCore.Qt.Key_Enter:
            self()
