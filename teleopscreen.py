from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

#color presets
seaFoamGreen = [(14/255),(201/255),(170/255)]
darkMagenta = [(171/255),(0/255),(117/255)]
lightMagenta = [(231/255),(58/255),(177/255)]
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

        switchDisp = normalLabel("Cubes scored in switch:\n" + str(self.robot.switch), seaFoamGreen); displist.append(switchDisp) # displays switch score
        teamDisp = normalLabel("Team: " + str(self.robot.teamNumber), black); displist.append(teamDisp) # displays team number
        eventDisp = normalLabel("Event: " + self.robot.eventName, black); displist.append(eventDisp) # displays event name
        climb1Color = darkMagenta if self.robot.climb == "climbed" else lightMagenta # darkening the currently selected climb option
        climbButton1 = smallButton("Robot\nclimbed\nsuccessfully", climb1Color); climbButton1.bind(on_release=lambda x: self.changeClimb("climbed")); displist.append(climbButton1)
        climb2Color = darkMagenta if self.robot.climb == "tried but failed" else lightMagenta # darkening the currently selected climb option
        climbButton2 = smallButton("Robot \nattempted to\nclimb but\nfailed", climb2Color); climbButton2.bind(on_release=lambda x: self.changeClimb("tried but failed")); displist.append(climbButton2)

        switchDec = smallButton("-", seaFoamGreen); switchDec.bind(on_release=lambda x: self.changeSwitch(-1)); displist.append(switchDec) # decrement switchDisp
        switchInc = smallButton("+", seaFoamGreen); switchInc.bind(on_release=lambda x: self.changeSwitch(1)); displist.append(switchInc) # increment switchDisp
        menuButton = normalButton("Menu"); displist.append(menuButton) # TODO: create menu, hook up to teleop
        scouterDisp = normalLabel("Scouter: " + self.robot.scouter, black); displist.append(scouterDisp) # displays scouter name
        climb3Color = darkMagenta if self.robot.climb == "levitated" else lightMagenta # darkening the currently selected climb option
        climbButton3 = smallButton("Robot\nlevitated", climb3Color); climbButton3.bind(on_release=lambda x: self.changeClimb("levitated")); displist.append(climbButton3)
        climb4Color = darkMagenta if self.robot.climb == "did not climb" else lightMagenta # darkening the currently selected climb option
        climbButton4 = smallButton("Robot did\nnot climb", climb4Color); climbButton4.bind(on_release=lambda x: self.changeClimb("did not climb")); displist.append(climbButton4)

        scaleDisp = normalLabel(self.robot.scale, fairBlue); displist.append(scaleDisp)

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
        self.display()
