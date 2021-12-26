import sys, os
from PyQt6.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QWidget

from tddtgui.widgets import TDDTPreviewWindow,TDDTSidebarMenu, ActionTypes
from tddtgui.popups import CreateEventDialog, TDDTErrorBox, TDDTSuccessBox
from imagehoster.imageHoster import ImageHoster

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
        self.setWindowTitle("TDDT News Creator Tool")
        
        layout_frame = QHBoxLayout(self)
        self.setLayout(layout_frame)
        
        # sidebar
        self.sidebar_widget = TDDTSidebarMenu()
        layout_frame.addWidget(self.sidebar_widget)
        [signal.connect(self.event_handler) for signal in [
            self.sidebar_widget.update_calendar_signal,
            self.sidebar_widget.add_event_signal,
            self.sidebar_widget.host_image_signal,
            self.sidebar_widget.publish_signal
        ]]
        
        # preview
        self.preview_widget = TDDTPreviewWindow()
        layout_frame.addWidget(self.preview_widget)
    
    def event_handler(self, type : ActionTypes):
        if type == ActionTypes.UPDATECALENDAR:
            self.preview_widget.update()
        elif type == ActionTypes.CREATEEVENT:
            try:
                dialog = CreateEventDialog()
                if dialog.exec():
                    if self.preview_widget.add_new_event(dialog.response):
                        TDDTSuccessBox("Successfully created new event!").show()
                    else:
                        raise Exception
                else:
                    raise Exception
            except:
                TDDTErrorBox("Something went wrong. Try Again!").show()
        elif type == ActionTypes.HOSTIMAGE:
            try:
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
                dialog.setMimeTypeFilters(["image/jpeg","image/png"])
                if dialog.exec():
                    filenames = dialog.selectedFiles()
                    if filenames:
                        hoster = ImageHoster()
                        for file in filenames:
                            name = os.path.split(file)[-1].split(".")[0]
                            if not hoster.upload_image(name, file):
                                raise Exception
                        TDDTSuccessBox("Successfully hosted image(s)!").show()    
                else:
                    raise Exception
            except:
                TDDTErrorBox("Couldn't host images. Try Again!").show()
        elif type == ActionTypes.PUBLISH:
            pass #TODO: publish main code
        