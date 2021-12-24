import sys
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget
from tddtgui.widgets import TDDTPreviewWindow,TDDTSidebarMenu

class TDDTGui:
    
    def __init__(self):
        self.app = QApplication([])
        self.window = TDDTMainWindow()
    
    def start(self):
        self.window.show()
        sys.exit(self.app.exec())
        
class TDDTMainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.configure()
        
    def configure(self):
        self.resize(1000,600)
        self.setWindowTitle("Tddt News Creator Tool")
        
        layout_frame = QHBoxLayout(self)
        self.setLayout(layout_frame)
        
        sidebar_widget = TDDTSidebarMenu()
        layout_frame.addWidget(sidebar_widget)
        
        preview_widget = TDDTPreviewWindow()
        layout_frame.addWidget(preview_widget)
        