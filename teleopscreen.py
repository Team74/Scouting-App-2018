from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

#color presets
seaFoamGreen = [(14/255),(201/255),(170/255)]
darkMagenta = [(201/255),(28/255),(147/255)]
fairBlue = [(28/255),(129/255),(201/255)]
brintGreen = [(28/255),(201/255),(40/255)]
lightOrange = [(201/255),(170/255),(28/255)]
black = [0, 0, 0, 1]



class TeleopLayout(StackLayout):
    def __init__(self, robot):
        self.robot = robot
        super(TeleopLayout, self).__init__()
        self.display()

    def display(self):
        displist = []

        switchDisp = normalLabel(self.robot.switch, seaFoamGreen); displist.append(switchDisp) # displays switch score
        teamDisp = normalLabel("Team: " + str(self.robot.teamNumber), black); displist.append(teamDisp) # displays team number
        eventDisp = normalLabel("Event: " + self.robot.eventName, black); displist.append(eventDisp) # displays event name
        climbButton1 = smallButton("Robot\nclimbed\nsuccessfully", darkMagenta); climbButton1.bind(on_press=lambda x: self.changeClimb("climbed")); displist.append(climbButton1)
        climbButton2 = smallButton("Robot \nattempted to\nclimb but\nfailed", darkMagenta); climbButton2.bind(on_press=lambda x: self.changeClimb("tried but failed")); displist.append(climbButton2)

        switchDec = smallButton("-", seaFoamGreen); switchDec.bind(on_press=lambda x: self.changeSwitch(-1)); displist.append(switchDec) # decrement switchDisp
        switchInc = smallButton("+", seaFoamGreen); switchInc.bind(on_press=lambda x: self.changeSwitch(1)); displist.append(switchInc) # increment switchDisp
        menuButton = normalButton("Menu"); displist.append(menuButton) # TODO: create menu, hook up to teleop
        scouterDisp = normalLabel("Scouter: " + self.robot.scouter, black); displist.append(scouterDisp) # displays scouter name
        climbButton3 = smallButton("Robot\nlevitated", darkMagenta); climbButton3.bind(on_press=lambda x: self.changeClimb("levitated")); displist.append(climbButton3)
        climbButton4 = smallButton("Robot did\nnot climb", darkMagenta); climbButton4.bind(on_press=lambda x: self.changeClimb("did not climb")); displist.append(climbButton4)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)



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
        self.robot.climb = change
