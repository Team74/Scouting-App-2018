from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

seaFoamGreen = [(14/255),(201/255),(170/255)]
darkMagenta = [(201/255),(28/255),(147/255)]
lightMagenta = [(231/255),(58/255),(177/255)]
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

        # displays cubes in switch in auton
        AutonSwitchDisp = normalLabel("Cubes put in switch:\n\n" + str(self.robot.autonSwitch), lightOrange)
        displist.append(AutonSwitchDisp)
        # displays team number
        teamDisp = normalLabel("Team: " + str(self.robot.teamNumber), black)
        displist.append(teamDisp)
        # displays event name
        eventDisp = normalLabel("Event: " + self.robot.eventName, black)
        displist.append(eventDisp)
        # "Left" for attemptedSwitchSide
        side1Color = darkMagenta if self.robot.attemptedSwitchSide == "Left" else lightMagenta
        sideButton1 = smallButton("Robot\nattempted\nthe Left\nside", side1Color)
        sideButton1.bind(on_release=lambda x: self.changeSide("Left"))
        displist.append(sideButton1)
        # "Right" for attemptedSwitchSide
        side2Color = darkMagenta if self.robot.attemptedSwitchSide == "Right" else lightMagenta
        sideButton2 = smallButton("Robot\nattempted\nthe Right\nside", side2Color)
        sideButton2.bind(on_release=lambda x: self.changeSide("Right"))
        displist.append(sideButton2)

        #row 2

        # decrement AutonSwitchDisp
        AutonSwitchDec = smallButton("-", lightOrange)
        AutonSwitchDec.bind(on_release=lambda x : self.AutonChangeSwitch(-1))
        displist.append(AutonSwitchDec)
        # increment AutonSwitchDisp
        AutonSwitchInc = smallButton('+', lightOrange)
        AutonSwitchInc.bind(on_release=lambda x : self.AutonChangeSwitch(1))
        displist.append(AutonSwitchInc)
        # menu button
        menuButton = normalButton("Menu") # TODO: create menu, hook up to teleop
        displist.append(menuButton)
        # displays scouter name
        scouterDisp = normalLabel("Scouter: " + self.robot.scouter, black)
        displist.append(scouterDisp)
        # "None" for attemptedSwitchSide
        side3Color = darkMagenta if self.robot.attemptedSwitchSide == "None" else lightMagenta
        sideButton3 = normalButton("Robot\ndidn't\nattempt\nthe switch", side3Color)
        sideButton3.bind(on_release=lambda x: self.changeSide("None"))
        displist.append(sideButton3)

        #row 3

        # scale & ecchange display
        multiLayout = StackLayout(size_hint=(.5, .5))
        displist.append(multiLayout)
        AutonScaleDisp = normalSubLable("Cubes put in scale:\nin auton\n" + str(self.robot.autonScale), fairBlue)
        multiLayout.add_widget(AutonScaleDisp)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

        def AutonChangeSwitch(self, change):
            self.robot.autonSwitch += change
            if self.robot.autonSwitch < 0:
                self.robot.autonSwitch = 0
        def changeSide(self, change):
            self.robot.attemptedSwitchSide = change
            self.display()
