import sys, glob, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets

from collections import defaultdict

from open3d import *
from config import *

from paths import augmentation_util, furnitures_path
sys.path.append(augmentation_util)
from utils import helper
from utils.icp_helper import get_registeration
from utils.vis_helper import *

 
class AugmentationUI(QtWidgets.QWidget):

    def __init__(self, augmentor):

        super().__init__()

        self.augmentor = augmentor
        self.furnitures = get_all_objects()
        self.target_object = ''
        self.source_object = ''

        self.setObjectName('AU')

        self.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QWidget()
        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()
        self.stack3 = QtWidgets.QWidget()

        self.MainWindow()
        self.ChangeObjectWindow()
        self.RemoveObjectWindow()
        self.ShowOneObjectWindow()

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)

        self.ChangeObjectButton.clicked.connect(self.OpenChangeObjectWindow)
        self.RemoveObjectButton.clicked.connect(self.OpenRemoveObjectWindow)
        self.ShowOneObjectButton.clicked.connect(self.OpenShowOneObjectWindow)

        self.ShowRawButton.clicked.connect(self.show_raw_point_cloud)
        self.ShowLabledButton.clicked.connect(self.show_labled_point_cloud)
        self.ShowWithTrajectoryButton.clicked.connect(self.show_with_trajectory)


    def OpenRemoveObjectWindow(self):
        self.QtStack.setCurrentIndex(1)
    def OpenChangeObjectWindow(self):
        self.QtStack.setCurrentIndex(2)
    def OpenShowOneObjectWindow(self):
        self.QtStack.setCurrentIndex(3)
    def OpenMainWindow(self):
        self.QtStack.setCurrentIndex(0)

    
    def show_with_trajectory(self):
        show_pcd([self.augmentor.pointcloud])
    def show_labled_point_cloud(self):
        show_pcd([self.augmentor.labeld_pointcloud])
    def show_raw_point_cloud(self):
        show_pcd([self.augmentor.pointcloud])

    def show_one_object(self, object_name):
        color = objects_hash[object_name]
        t = self.augmentor.get_object_with_hashed_color(color)
        show_pcd([t])

    def remove_one_object(self, object_name):
        color = objects_hash[object_name]
        t = self.augmentor.remove_object_with_index(color)
        show_pcd([t])

    def MainWindow(self):

        self.ShowRawButton = QtWidgets.QPushButton(self.stack0)
        self.ShowRawButton.setText('Show Point Cloud')
        self.ShowRawButton.setGeometry(QtCore.QRect(100, 100, 200, 30))
        
        self.ShowLabledButton = QtWidgets.QPushButton(self.stack0)
        self.ShowLabledButton.setText('Show Labled Point Cloud')
        self.ShowLabledButton.setGeometry(QtCore.QRect(100, 150, 200, 30))

        self.ShowWithTrajectoryButton = QtWidgets.QPushButton(self.stack0)
        self.ShowWithTrajectoryButton.setText('Show With Trajectory')
        self.ShowWithTrajectoryButton.setGeometry(QtCore.QRect(100, 200, 200, 30))
        
        self.RemoveObjectButton = QtWidgets.QPushButton(self.stack0)
        self.RemoveObjectButton.setText('Remove Object')
        self.RemoveObjectButton.setGeometry(QtCore.QRect(100, 250, 200, 30))

        self.ShowOneObjectButton = QtWidgets.QPushButton(self.stack0)
        self.ShowOneObjectButton.setText('Show One Object')
        self.ShowOneObjectButton.setGeometry(QtCore.QRect(100, 300, 200, 30))

        self.ChangeObjectButton = QtWidgets.QPushButton(self.stack0)
        self.ChangeObjectButton.setText('Change Object')
        self.ChangeObjectButton.setGeometry(QtCore.QRect(100, 350, 200, 30))


    def RemoveObjectWindow(self):

        objectChoice = QtGui.QLabel('Which Object You Want to Remove?', self.stack1)

        comboBox = QtGui.QComboBox(self.stack1)
        for item in self.augmentor.objects_dictionary_by_color:
            if(item in hashed_color_names.keys()):
                comboBox.addItem(hashed_color_names[item])

        comboBox.activated[str].connect(self.remove_one_object)

        self.horizontalGroupBox = QGroupBox('', self.stack1)
        layout = QGridLayout()
        
        layout.setColumnStretch(5, 5)
        layout.addWidget(objectChoice,0,0)
        layout.addWidget(comboBox,0,1)

        self.horizontalGroupBox.setLayout(layout)

        self.__add_back_button(self.stack1)

    def ShowOneObjectWindow(self):
        
        objectChoice = QtGui.QLabel('Which Object You Want to See?', self.stack3)

        comboBox = QtGui.QComboBox(self.stack3)
        for item in self.augmentor.objects_dictionary_by_color:
            if(item in hashed_color_names.keys()):
                comboBox.addItem(hashed_color_names[item])

        comboBox.activated[str].connect(self.show_one_object)

        self.horizontalGroupBox = QGroupBox('', self.stack3)
        layout = QGridLayout()
        
        layout.setColumnStretch(5, 5)
        layout.addWidget(objectChoice,0,0)
        layout.addWidget(comboBox,0,1)

        self.horizontalGroupBox.setLayout(layout)

        self.__add_back_button(self.stack3)

    def ChangeObjectWindow(self):

        objectChoice = QtGui.QLabel('Which Object You Want to Change?', self.stack2)

        comboBox = QtGui.QComboBox(self.stack2)
        for item in self.augmentor.objects_dictionary_by_color:
            if(item in hashed_color_names.keys()):
                comboBox.addItem(hashed_color_names[item])
        comboBox.activated[str].connect(self.__select_target_object)

        objectChoiceII = QtGui.QLabel('Which New Object You Want to Choose?', self.stack2)
        comboBoxII = QtGui.QComboBox(self.stack2)
        for key in self.furnitures.keys():
            i = 0
            for item in self.furnitures[key]:
                comboBoxII.addItem(key + ':' + str(i))
                i += 1

        comboBoxII.activated[str].connect(self.__select_source_object)

        ChangeButton = QtWidgets.QPushButton(self.stack2)
        ChangeButton.setText('Change')
        ChangeButton.clicked.connect(self.__change_object)
        
        self.horizontalGroupBox = QGroupBox('', self.stack2)
        layout = QGridLayout()
        
        layout.setColumnStretch(5, 5)
        layout.addWidget(objectChoice,0,0)
        layout.addWidget(comboBox,0,1)
        layout.addWidget(objectChoiceII,2,0)
        layout.addWidget(comboBoxII, 2,2)
        
        layout.addWidget(ChangeButton, 4,4)

        self.horizontalGroupBox.setLayout(layout)

        self.__add_back_button(self.stack2)

    def __select_target_object(self, name):
        self.target_object = name
    def __select_source_object(self, name):
        self.source_object = name

    def __change_object(self):

        temp = self.source_object.split(':')
        source = self.furnitures[temp[0]][int(temp[1])]

        target = self.target_object

        [a, b] = self.augmentor.change_object(target, source)
        show_pcd([a, b])
    
    def __add_back_button(self, stack):
        self.BackButton = QtWidgets.QPushButton(stack)
        self.BackButton.setText('Back')
        self.BackButton.setGeometry(QtCore.QRect(400, 400, 50, 30))
        self.BackButton.clicked.connect(self.OpenMainWindow)

def get_objects(name):
    os.chdir(furnitures_path + name)
    l = []
    for file in glob.glob("*.ply"):
        t = read_point_cloud(furnitures_path + name + file)
        l.append(t)
        if(len(l) > 3):
            break
            
    return l

def get_all_objects():
    t = defaultdict(list)
    t['table'] = get_objects('table/')
    t['chair'] = get_objects('chair/')
    t['bed'] = get_objects('bed/')

    return t
