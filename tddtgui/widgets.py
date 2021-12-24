from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget 
from PyQt6.QtWebEngineWidgets import QWebEngineView

from tddtgui.popups import CreateEventDialog

class TDDTPreviewWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.configure()
        self.show()
    
    def configure(self):
        
        # set layout
        layout_preview = QVBoxLayout()
        self.setLayout(layout_preview)
        
        # add html viewer
        browser = QWebEngineView()
        html = open(r"C:\Users\Benjamin\Desktop\Projects\Python\TDDTNews\test.html", "r", encoding="utf-8").read()
        browser.setHtml(html)
        layout_preview.addWidget(browser)
        
class TDDTSidebarMenu(QWidget):
    
    def __init__(self):
        super().__init__()
        self.configure()
        
    def configure(self):
        layout_sidebar = QVBoxLayout()
        self.setLayout(layout_sidebar)
        
        # update calendar
        updatecalendar = QPushButton("Update Calendar")
        layout_sidebar.addWidget(updatecalendar)
        
        # add new event
        createevent = QPushButton("Add New Event")
        layout_sidebar.addWidget(createevent)
        createevent.clicked.connect(self.create_event_handler)
        
        # host image
        hostimage = QPushButton("Host New Image")
        layout_sidebar.addWidget(hostimage)
        
        # previews document -> updates preview
        preview = QPushButton("Preview HTML")
        layout_sidebar.addWidget(preview)
        
        # publishes document -> publish
        publish = QPushButton("Publish NewsLetter")
        layout_sidebar.addWidget(publish)
    
    def update_calendar_handler(self): # no popup dialog
        pass
    
    def create_event_handler(self): # unique popup dialog
        dialog = CreateEventDialog()
        if dialog.exec():
            print(dialog.response)

    def host_image_handler(self): # file popup
        pass
    
    def preview_handler(self): # no popup dialog
        pass
    
    def publish_handler(self): # are you sure popup dialog
        pass
    