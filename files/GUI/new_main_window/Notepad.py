from PyQt5 import QtWidgets


class Notepad(QtWidgets.QWidget):

    # gets a location of file to open and its name (and the window icon
    def __init__(self, name, loc, icon):
        super(Notepad, self).__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.save_btn = QtWidgets.QPushButton('Save')
        self.save_btn.clicked.connect(self.save_file)
        self.name, self.location = name, loc
        self.text_edit = QtWidgets.QTextEdit()
        self.setWindowIcon(icon)
        self.setWindowTitle(name)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.save_btn)
        self.setLayout(self.layout)
        self.save_action = QtWidgets.QAction('Save', self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)
        self.addAction(self.save_action)
        self.resize(600, 600)
        with open(loc, 'r') as file:
            text = file.read()
            self.text_edit.setText(text)
        self.show()

    def save_file(self):
        with open(self.location, 'w') as file:
            text = self.text_edit.toPlainText()
            file.write(text)


