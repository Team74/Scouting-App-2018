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
lightOrange = [(201/255),(170/255),(28/255)]
black = [0, 0, 0, 1]

class TeleopLayout(StackLayout):
    def __init__(self, robot):
        self.robot = robot
        super(TeleopLayout, self).__init__()
        self.display()

    def display(self):
        displist = []

        # displays cubes in switch
        switchDisp = normalLabel("Cubes put in switch:\n\n" + str(self.robot.switch), seaFoamGreen)
        displist.append(switchDisp)
        # displays team number
        teamDisp = normalLabel("Team: " + str(self.robot.teamNumber), black)
        displist.append(teamDisp)
        # displays event name
        eventDisp = normalLabel("Event: " + self.robot.eventName, black)
        displist.append(eventDisp)
        # "climbed" button for climb options
        climb1Color = darkMagenta if self.robot.climb == "climbed" else lightMagenta # darkening the currently selected climb option
        climbButton1 = smallButton("Robot\nclimbed\nsuccessfully", climb1Color)
        climbButton1.bind(on_release=lambda x: self.changeClimb("climbed"))
        displist.append(climbButton1)
        # "tried but failed" button for climb options
        climb2Color = darkMagenta if self.robot.climb == "tried but failed" else lightMagenta # darkening the currently selected climb option
        climbButton2 = smallButton("Robot \nattempted to\nclimb but\nfailed", climb2Color)
        climbButton2.bind(on_release=lambda x: self.changeClimb("tried but failed"))
        displist.append(climbButton2)

        # decrement switchDisp
        switchDec = smallButton("-", seaFoamGreen)
        switchDec.bind(on_release=lambda x: self.changeSwitch(-1))
        displist.append(switchDec)
        # increment switchDisp
        switchInc = smallButton("+", seaFoamGreen)
        switchInc.bind(on_release=lambda x: self.changeSwitch(1))
        displist.append(switchInc)
        # menu button
        menuButton = normalButton("Menu") # TODO: create menu, hook up to teleop
        displist.append(menuButton)
        # displays scouter name
        scouterDisp = normalLabel("Scouter: " + self.robot.scouter, black)
        displist.append(scouterDisp)
        # "levitated" button for climb options
        climb3Color = darkMagenta if self.robot.climb == "levitated" else lightMagenta # darkening the currently selected climb option
        climbButton3 = smallButton("Robot\nlevitated", climb3Color)
        climbButton3.bind(on_release=lambda x: self.changeClimb("levitated"))
        displist.append(climbButton3)
        # "did not climb" button for climb options
        climb4Color = darkMagenta if self.robot.climb == "did not climb" else lightMagenta # darkening the currently selected climb option
        climbButton4 = smallButton("Robot did\nnot climb", climb4Color)
        climbButton4.bind(on_release=lambda x: self.changeClimb("did not climb"))
        displist.append(climbButton4)

        # scale display
        scaleLayout = StackLayout(size_hint=(.25, .5)) # smaller layout to get around larger widgets in the same line (notesTextInput)
        displist.append(scaleLayout)
        scaleDisp = largeSubLabel("Cubes put in scale:\n\n" + str(self.robot.scale), fairBlue)
        scaleLayout.add_widget(scaleDisp)
        # input for notes
        notesTextInput = TextInput(size_hint=(.5, .5))
        displist.append(notesTextInput)
        # displays cubes in exchange
        exchangeLayout = StackLayout(size_hint=(.25, .5))
        displist.append(exchangeLayout)
        exchangeDisp = largeSubLabel("Cubes put in exchange:\n\n" + str(self.robot.exchange), lightOrange)
        exchangeLayout.add_widget(exchangeDisp)

        # decrement scaleDisp
        scaleDec = smallSubButton("-", fairBlue)
        scaleDec.bind(on_release=lambda x: self.changeScale(-1))
        scaleLayout.add_widget(scaleDec)
        # increment scaleDisp
        scaleInc = smallSubButton("+", fairBlue)
        scaleInc.bind(on_release=lambda x: self.changeScale(1))
        scaleLayout.add_widget(scaleInc)
        # decrement exchangeDisp
        exchangeDec = smallSubButton("-", lightOrange)
        exchangeDec.bind(on_release=lambda x: self.changeExchange(-1))
        exchangeLayout.add_widget(exchangeDec)
        # increment exchangeDisp
        exchangeInc = smallSubButton("+", lightOrange)
        exchangeInc.bind(on_release=lambda x: self.changeExchange(1))
        exchangeLayout.add_widget(exchangeInc)

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
