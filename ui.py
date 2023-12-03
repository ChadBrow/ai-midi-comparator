from PyQt5.QtWidgets import *

class UI:
    def __init__(self, sys, exitFunc=None):
        self.exitFunc = exitFunc

        self.app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.win.setGeometry(200,200,300,300) 
        self.win.setWindowTitle("My first window!") 
        
        label = QLabel(win)
        label.setText("my first label")
        label.move(50, 50)  

        self.win.show()
        self.win.showMaximized()
        sys.exit(self.exit())
    
    def exit(self):
        if self.exitFunc:
            self.exitFunc()
        self.app.exec_()