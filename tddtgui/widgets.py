from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget 
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import pyqtSignal as Signal
from enum import Enum

from emailcreator.emailRender import emailRender

class ActionTypes(Enum):
    UPDATECALENDAR = 1,
    CREATEEVENT = 2,
    HOSTIMAGE = 3,
    PUBLISH = 4
    
class TDDTPreviewWindow(QWidget):
    
    def __init__(self, template="liondancebeat"):
        super().__init__()
        self.renderer = emailRender(template + ".jinja")
        self.configure()
        self.show()
    
    def configure(self):
        
        # set layout
        layout_preview = QVBoxLayout()
        self.setLayout(layout_preview)
        
        # add html viewer
        self.browser = QWebEngineView()
        self.browser.setHtml(self.renderer.render())
        layout_preview.addWidget(self.browser)

    def update(self):
        self.renderer.update()
        self.browser.setHtml(self.renderer.render())
    
    def add_new_event(self, event : dict) -> bool:
        result = self.renderer.add_news(event)
        self.browser.setHtml(self.renderer.render())
        return result
        
    def remove_event(self, title : str) -> bool:
        result = self.renderer.remove_news(title)
        self.browser.setHtml(self.renderer.render())
        return result
    
    def get_publish_info(self) -> dict:
        self.update()   
        return {
            "volume": self.renderer.volume, 
            "number": self.renderer.number,
            "html": self.renderer.render()
        }
        
        
class TDDTSidebarMenu(QWidget):
    
    update_calendar_signal = Signal(ActionTypes)
    add_event_signal = Signal(ActionTypes)
    host_image_signal = Signal(ActionTypes)
    publish_signal = Signal(ActionTypes)
        
    def __init__(self):
        super().__init__()
        self.configure()
        
    def configure(self):
        layout_sidebar = QVBoxLayout()
        self.setLayout(layout_sidebar)
        
        # update calendar
        updatecalendar = QPushButton("Update Calendar")
        layout_sidebar.addWidget(updatecalendar)
        updatecalendar.clicked.connect(lambda : self.update_calendar_signal.emit(ActionTypes.UPDATECALENDAR))
        
        # add new event
        createevent = QPushButton("Add New Event")
        layout_sidebar.addWidget(createevent)
        createevent.clicked.connect(lambda : self.add_event_signal.emit(ActionTypes.CREATEEVENT))
        
        # host image
        hostimage = QPushButton("Host New Image")
        layout_sidebar.addWidget(hostimage)
        hostimage.clicked.connect(lambda: self.host_image_signal.emit(ActionTypes.HOSTIMAGE))
        
        # publishes document -> publish
        publish = QPushButton("Publish NewsLetter")
        layout_sidebar.addWidget(publish)
        publish.clicked.connect(lambda: self.publish_signal.emit(ActionTypes.PUBLISH))