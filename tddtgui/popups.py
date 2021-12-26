from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout

class CreateEventDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.configure()
        self.response = None
        
    def configure(self):
        self.resize(400,300)
        self.setWindowTitle("Create New Event")
        layout_createevent = QVBoxLayout()
        
        title_label = QLabel("Title:")
        self.title = QLineEdit()
        
        content_label = QLabel("Content:")
        self.content = QTextEdit()
        
        submit = QPushButton("Submit")
        submit.clicked.connect(self.submit_handler)
        submit.setDefault(True)
        
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.cancel_handler)
        cancel.setDefault(True)
        
        [layout_createevent.addWidget(i) for i in [title_label,self.title, content_label, self.content, submit, cancel]]
        self.setLayout(layout_createevent)
    
    def submit_handler(self):
        title = self.title.text()
        content = self.content.document().toPlainText().lstrip().rstrip()
        print(content)
        if not title:
            TDDTErrorBox("Title is empty").show()
        elif not content:
            TDDTErrorBox("Content is empty").show()
        else:
            self.response = {
                "title" : title,
                "content" : content
            }
            self.accept()
    
    def cancel_handler(self):
        self.reject()
            
class TDDTErrorBox(QMessageBox):
    
    def __init__(self, msg):
        super().__init__()
        self.setText("Error:")
        self.setInformativeText(msg)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setDefaultButton(QMessageBox.StandardButton.Ok)
    
    def show(self):
        return self.exec()