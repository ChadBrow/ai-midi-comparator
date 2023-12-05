from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import time
import pygame
import pygame_gui
import sys
import os
import threading

TICK = pygame.USEREVENT + 1

class UI:
    def __init__(self, sys, exitFunc=None):
        #this is our UI class
        #we will be given extra func to call when user exits
        self.exitFunc = exitFunc
        self.x = 1

        #start app and main window
        self.app = QApplication(sys.argv)
        self.win = QWidget()
        self.win.setGeometry(200,200,300,300)#doesn't matter cause we maximize window
        self.win.setWindowTitle("App")

        self.layout = QGridLayout()#our grid layout. Let's add some stuff to it

        self.rightHandContainer = QWidget()
        self.rightHandColumn = QGridLayout() #this is the toolbar on the right
        self.statusLabel = QLabel()
        # self.statusLabel.setText("Select a file to start")
        self.scoreLabel = QLabel()
        # self.scoreLabel.setText("Enter a file to start")
        self.mainButton = QPushButton()
        self.mainButton.setText("Start")
        self.mainButton.setEnabled(True)
        self.mainButton.clicked.connect(self.start)
        self.quitButton = QPushButton()
        self.quitButton.setText("Quit")
        self.quitButton.clicked.connect(self.exit)
        self.rightHandColumn.addWidget(self.statusLabel, 0, 0)
        self.rightHandColumn.addWidget(self.scoreLabel, 1, 0)
        self.rightHandColumn.addWidget(self.mainButton, 2, 0)
        self.rightHandColumn.addWidget(self.quitButton, 3, 0)
        self.rightHandContainer.setLayout(self.rightHandColumn)

        self.leftHandContainer = QWidget()
        self.leftHandColumn = QStackedLayout() #this is the main screen on the left where sheet music will appear
        self.fileSelectContainer = QWidget() #every item in stacked layout must be a widget
        self.fileSelectPage = QGridLayout()
        self.fileSelect = QPushButton()
        self.fileSelect.setText("Select a Midi File before Starting")
        self.channelSelect = QComboBox()
        self.channelSelect.addItems(['0', '1', '2', '3'])
        self.channelSelect.setAccessibleName("Select a Midi Input Channel before Starting")
        self.channelSelectTitle = QLabel()
        self.channelSelectTitle.setText("Midi Channel")
        self.fileSelectPage.addWidget(self.fileSelect, 0, 0)
        self.fileSelectPage.addWidget(self.channelSelectTitle, 1, 0)
        self.fileSelectPage.addWidget(self.channelSelect, 2, 0)
        self.fileSelectContainer.setLayout(self.fileSelectPage)
        self.leftHandColumn.addWidget(self.fileSelectContainer)
        # leftHandColumn.setCurrentIndex(0)
        self.leftHandContainer.setLayout(self.leftHandColumn)

        self.layout.addWidget(self.leftHandContainer, 0, 0, 1, 3)
        self.layout.addWidget(self.rightHandContainer, 0, 3)

        self.win.setLayout(self.layout)

        #Set our periodic task and our threadpool
        self.threadpool = QtCore.QThreadPool()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick)
        # self.timer.start()

        self.win.show()
        self.win.showMaximized()#want window to be max size
        sys.exit(self.app.exec_())

    
    def exit(self):
        if self.exitFunc:
            self.exitFunc()
        self.app.quit()
    
    def start(self):
        # self.win.dataParseThread = DataParseThread(self.doStuff)
        self.timer.start()
    
    def tick(self):
        worker = Worker(self.doStuff)
        self.threadpool.start(worker)
    
    def doStuff(self):
        self.x = self.x + 1
        time.sleep(1)
        self.statusLabel.setText(f'{self.x}')
        time.sleep(1)
        self.x += 1
        self.scoreLabel.setText(f'{self.x}')

class DataParseThread(QtCore.QThread):
    def __init__(self, *args, **kwargs):
        print(args)
        QtCore.QThread.__init__(self, *args[1:], **kwargs)
        self.dataCollectionTimer = QtCore.QTimer()
        self.dataCollectionTimer.moveToThread(self)
        self.dataCollectionTimer.timeout.connect(args[0])

    def run(self):
        self.dataCollectionTimer.start(4000)
        loop = QtCore.QEventLoop()
        loop.exec_()

class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
    
    @QtCore.pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

class PygameUI():
    def __init__(self, img):
        pygame.init()

        #create our window. We start it full screen
        pygame.display.set_caption('Quick Start')
        self.screen = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        self.manager = pygame_gui.UIManager((self.width, self.height))

        #create background
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(pygame.Color('#000000'))

        #text font
        self.font = pygame.font.Font(None, 32)

        #colors
        self.backgroundColor = (80, 80, 80)

        #labels
        self.beat = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0.8 * self.width, 0.1 * self.height, 200, 50),
                                                   text="Beat", manager=self.manager)
        
        #sheet music
        self.musicPage = pygame_gui.elements.UIImage(relative_rect=pygame.Rect(0.1 * self.width, 0.1 * self.height, 0.4 * self.width, 0.8 * self.height),
                                                   image_surface=pygame.image.load(os.path.abspath(img)), 
                                                   manager=self.manager)
        
        #exit button
        self.exitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0.8 * self.width, 0.5 * self.height, 200, 50),
                                                   text="Exit", manager=self.manager)

        # background = pygame.Surface((800, 600))
        # background.fill(pygame.Color('#000000'))

        #start threads
        # self.guiLoop()
    
    def quit(self):
        pygame.quit()
    
    def guiLoop(self):
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #check for exit
                    self.quit()
                if event.type == TICK:
                    pass
                self.manager.process_events(event)
            
            # #update all our elements
            # self.screen.blit(self.background, (0, 0))
            # self.manager.update(10)
            # #draw screen
            # self.manager.draw_ui(self.screen)
            # pygame.display.flip()
            
    def tick(self, delta):
        #update all our elements
        self.screen.blit(self.background, (0, 0))
        self.manager.update(10)
        #draw screen
        self.manager.draw_ui(self.screen)
        pygame.display.flip()
        


