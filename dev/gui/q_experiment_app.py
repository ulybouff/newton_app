from __future__ import annotations
import sys 

# -----------------------------------------------------------------------------
import PySide6
from __feature__ import snake_case, true_property # type: ignore[import-not-found]
# -----------------------------------------------------------------------------

from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QScrollBar, QGroupBox, QApplication

# -----------------------------------------------------------------------------
from shibokensupport import feature # type: ignore[import-not-found]
feature.set_selection(feature.snake_case | feature.true_property)
assert "snake_case" in feature.info() and "true_property" in feature.info()
# -----------------------------------------------------------------------------
from dev.gui.q_newton_visualization import QNewtonVisualization
from dev.gui.q_parameters_panel import ParametersPanel

class QExperimentApp(QWidget): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__parameters_panel = ParametersPanel()
        self.__visualization = QNewtonVisualization()

        main_layout = QHBoxLayout()
        main_layout.add_widget(self.__parameters_panel)
        main_layout.add_widget(self.__visualization)
        self.set_layout(main_layout)
        self.update()
    
    def update(self):
        self.__visualization.update(self.__parameters_panel.properties)