from __future__ import annotations
import numpy as np 
import sys 

# -----------------------------------------------------------------------------
import PySide6
from __feature__ import snake_case, true_property # type: ignore[import-not-found]
# -----------------------------------------------------------------------------

from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QScrollBar, QGroupBox, QApplication
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
# -----------------------------------------------------------------------------
from shibokensupport import feature # type: ignore[import-not-found]
feature.set_selection(feature.snake_case | feature.true_property)
assert "snake_case" in feature.info() and "true_property" in feature.info()
# -----------------------------------------------------------------------------
from dev.physics.newton_solver import NewtonSolver

class QNewtonVisualization(QWidget): 
    def __init__(self, parent=None):
        super().__init__(parent)
        min_val, max_val = -0.005, 0.005
        self.__solver = NewtonSolver()
        self.y_array = np.linspace(min_val, max_val, 1000) # zoom a integrer peut etre 
        self.__I = None
        self.__I_diff = None
        self.__I_inter = None
        self.__V = None
        self.__axis = QValueAxis()
        self.__axis.set_range(min_val, max_val)
        self.__axis.tick_count = 5
        self.__axis.label_format = "{value:.4f}"
        self.__chart = QChart()
        self.__chart.add_axis(self.__axis)



    def update(self, properties):
        self.__solver.assign_parameters(*properties)
        self.__I_diff, self.__I_inter, self.__V, self.__I = self.__solver.calculate(self.y_array)