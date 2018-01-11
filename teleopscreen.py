from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

class TeleopLayout(StackLayout):
    def __init__(self, robot):
        self.robot = robot
        super(Screen, self).__init__()
        self.display()

    def display(self):
        displist = []

        switchDisp = normalLabel(self.robot.switch); displist.append(switchDisp) # displays switch score
        teamDisp = normalLabel("Team: " + self.robot.teamNumber); displist.append(teamDisp) # displays team number
        eventDisp = normalLabel("Event: " + self.robot.eventName); displist.append(eventDisp) # displays event name
        climbDisp = normalLabel("Did they climb?\n" + self.robot.climb); displist.append(climbDisp) # displays climb options

        switchDec = smallButton("-"); switchDec.bind(on_press=lambda x: self.changeSwitch(-1)); displist.append(switchDec) # decrement switchDisp
        switchInc = smallButton("+"); switchInc.bind(on_press=lambda x: self.changeSwitch(1)); displist.append(switchInc) # increment switchDisp
        menuButton = normalButton(""); displist.append(menuButton) # TODO: create menu, hook up to teleop
        scouterDisp = normalLabel("Scouter: " + self.robot.scouter); displist.append(scouterDisp) # displays scouter name


    def changeSwitch(self, change):
        self.robot.switch += change
        self.display()
    def changeScale(self, change):
        self.robot.scale += change
        self.display()
    def changeExchange(self, change):
        self.robot.exchange += change
        self.display()
    def changeClimb(self, change):
        climbOptions = ["did not climb", "tried but failed", "levitated", "climbed"]
        position = climbOptions.index(self.robot.climb)
        if position == 3 and change == 1:
            position = 0
        elif position == 0 and change == -1:
            position = 3
        else:
            position += change
        self.robot.climb = climbOptions[position]
