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
#from ..physics import NewtonSolver # comment import?

class ParametersPanel(QWidget): 
    valueChanged = Signal()            # reste a voir comment connecter sans trop repeter de code

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__wave_length_area, self.__wave_length_sb = self.create_parameter_area("Longueur d'onde", 380, 780, 500, 1, "nm")
        self.__central_intensity_area, self.__central_intensity_sb = self.create_parameter_area("Intensité au centre", 0, 100, 1, 1)
        self.__source_width_area, self.__source_width_sb = self.create_parameter_area("Largeur de la source", 0, 100, 0, 100, "mm") # x100
        self.__slit_count_area, self.__slit_count_sb = self.create_parameter_area("Nombre de fentes", 1, 20, 2, 1)
        self.__slit_width_area, self.__slit_width_sb = self.create_parameter_area("Largeur de fente", 1, 1000, 40, 1, "μm")
        # gerer lorsque 1 seule fente pour la separation
        self.__slit_interval_area, self.__slit_interval_sb = self.create_parameter_area("Largeur entre fentes", 10, 5000, 250, 1, "μm")
        self.__screen_distance_area, self.__screen_distance_sb = self.create_parameter_area("Distance fentes-écran", 1, 50, 10, 10, "m") # x10
        self.__medium_index_area, self.__medium_index_sb = self.create_parameter_area("Indice de réfraction", 100, 200, 100, 100) # x100
        self.__source_distance_area, self.__source_distance_sb = self.create_parameter_area("Distance source-fentes", 1, 20 , 10, 10) # x10

        self.__source_layout = QVBoxLayout()
        self.__source_layout.add_layout(self.__wave_length_area)
        self.__source_layout.add_layout(self.__central_intensity_area)
        self.__source_layout.add_layout(self.__source_width_area)
        self.__source_box = QGroupBox("Paramètres de la source")
        self.__source_box.set_layout(self.__source_layout)

        self.__geometry_layout = QVBoxLayout()
        self.__geometry_layout.add_layout(self.__slit_count_area)
        self.__geometry_layout.add_layout(self.__slit_width_area)
        self.__geometry_layout.add_layout(self.__slit_interval_area)
        self.__geometry_layout.add_layout(self.__screen_distance_area)
        self.__geometry_layout.add_layout(self.__medium_index_area)
        self.__geometry_box = QGroupBox("Paramètres de la géométrie et du milieu")
        self.__geometry_box.set_layout(self.__geometry_layout)

        final_layout = QVBoxLayout()
        final_layout.add_widget(self.__source_box)
        final_layout.add_widget(self.__geometry_box)
        self.set_layout(final_layout)

    @property
    def wave_length(self):
        return self.__wave_length_sb.value / 1e9
    
    @property
    def central_intensity(self):
        return self.__central_intensity_sb.value
    
    @property
    def source_width(self):
        return self.__source_width_sb.value / 1e5

    @property
    def slit_count(self):
        return self.__slit_count_sb.value

    @property
    def slit_width(self):
        return self.__slit_width_sb.value / 1e6

    @property
    def slit_interval(self):
        return self.__slit_interval_sb.value / 1e6

    @property
    def screen_distance(self):
        return self.__screen_distance_sb.value / 10

    @property
    def medium_index(self):
        return self.__medium_index_sb.value / 100
    
    @property
    def source_distance(self):
        return self.__source_distance_sb.value / 10

    @property
    def properties(self):
        return (self.wave_length, self.central_intensity, self.source_width, self.slit_count, self.slit_width, self.slit_interval, self.screen_distance, self.medium_index, self.source_distance)

    def create_parameter_area(self, name, min_val, max_val, default, scale, unit=""):
        name_label = QLabel(name)
        unit_label = QLabel(unit)
        value_label = QLabel()
        scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        scrollbar.set_range(min_val, max_val)
        scrollbar.value = default
        layout = QHBoxLayout()
        layout.add_widget(name_label)
        layout.add_widget(scrollbar)
        layout.add_widget(value_label)
        layout.add_widget(unit_label)
        # reste a connecter le value_label et le scrollbar 
        def change_value(val):
            value_label.text = str(val/scale)
            self.valueChanged.emit()
        value_label.text = str(default)
        scrollbar.valueChanged.connect(change_value)
        return layout, scrollbar

    
def main():
    app = QApplication(sys.argv)
    window = ParametersPanel()
    window.show()   
    app.exec()

if __name__ == "__main__":    main()