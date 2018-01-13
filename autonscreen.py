from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

seaFoamGreen = [(14/255),(201/255),(170/255)]
darkMagenta = [(201/255),(28/255),(147/255)]
fairBlue = [(28/255),(129/255),(201/255)]
brintGreen = [(28/255),(201/255),(40/255)]
lightOrange = [(201/255),(170/255),(28/255)]
black = [0, 0, 0, 1]

class autonLayout(StackLayout):
    def __init__(self, robot):
        self.robot = robot
        super(autonLayout, self).__init__()
        self.display()

    def display(self):
        displist = []

        #row 1
        AutonSwitchDisp = normalLabel("Cubes put in switch:\n\n" + str(self.robot.autonSwitch), lightOrange)
        displist.append(AutonSwitchDisp)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

        def AchangeSwitch(self, change):
            self.robot.autonSwitch += change
            if self.robot.autonSwitch < 0:
                self.robot.autonSwitch = 0
