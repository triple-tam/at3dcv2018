import sys

from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QVBoxLayout, \
                            QMainWindow, QApplication, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont, QImage, QPainter, QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QCoreApplication, Qt, QObject, QFile, QTextStream, QSize

from open3d import *


class AugmentationUI:

    def start(self, b):
        
        central_widget = QWidget()
        layout = QGridLayout(central_widget)
        layout.setSpacing(10)

        # self.setCentralWidget(central_widget)

        self._thread = None
        if self._thread == None:
            self._thread = QThread(()



        # dummy button
        dummy_button = QPushButton('dummy')
        dummy_button.clicked.connect()
        dummy_button.setFixedWidth(100)
        dummy_button.setFixedHeight(100)

        layout.setContentsMargins(100, 100, 100, 100)
        image_viewer.setFixedWidth(700)
        image_viewer.setFixedHeight(260)

        hbox_dummy = QHBoxLayout()
        hbox_dummy.addWidget(dummy_button)
        layout.addLayout(hbox_dummy, 0, 1, 1, 1, Qt.AlignLeft)

        hbox_start_buttons = QHBoxLayout()
        hbox_start_buttons.addWidget(start_button)
        hbox_start_buttons.addWidget(stop_button)
        layout.addLayout(hbox_start_buttons, 0, 0, 1, 1, Qt.AlignBottom| Qt.AlignCenter)
        # layout.addLayout(hbox_start_buttons, 1, 0, 1, 1, Qt.AlignTop| Qt.AlignCenter)

        # layout.setVerticalSpacing(30)
        layout.setVerticalSpacing(100)

        # 3d reconstruction
        reconstruct_btn = QPushButton('Reconstruct', self)
        reconstruct_btn.clicked.connect()
        # reconstruct_btn.resize(reconstruct_btn.sizeHint())
        reconstruct_btn.setFixedWidth(100)
        reconstruct_btn.setFixedHeight(90)
        # layout.addWidget(reconstruct_btn, 4, 0)

        # Augmentation
        augment_btn = QPushButton('Augment', self)
        augment_btn.clicked.connect()
        augment_btn.resize(reconstruct_btn.sizeHint())
        augment_btn.setFixedWidth(100)
        augment_btn.setFixedHeight(90)
        # layout.addWidget(augment_btn, 4, 2)

        # Compare
        compare_btn = QPushButton('Compare', self)
        compare_btn.clicked.connect()
        compare_btn.resize(reconstruct_btn.sizeHint())
        compare_btn.setFixedWidth(100)
        compare_btn.setFixedHeight(90)

        # Show
        show_btn = QPushButton('Show', self)
        show_btn.clicked.connect()
        show_btn.resize(reconstruct_btn.sizeHint())
        show_btn.setFixedWidth(100)
        show_btn.setFixedHeight(90)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(reconstruct_btn)
        hbox_buttons.addWidget(compare_btn)
        hbox_buttons.addWidget(show_btn)

        # hbox_buttons.addStretch()
        hbox_buttons.addWidget(augment_btn)
        layout.addLayout(hbox_buttons, 3, 0, 1, 2)


        self.setLayout(layout)
        # set geometry
        self.setGeometry(0, 0, 1000, 650)
        self.setWindowTitle('App')
        self.show()
