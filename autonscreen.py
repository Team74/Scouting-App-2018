from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

seaFoamGreen = [(14/255),(201/255),(170/255)]
darkMagenta = [(171/255),(0/255),(117/255)]
lightMagenta = [(231/255),(58/255),(177/255)]
fairBlue = [(28/255),(129/255),(201/255)]
brintGreen = [(28/255),(201/255),(40/255)]
lightOrange = [(201/255),(170/255),(28/255)]
black = [0, 0, 0, 1]
grey = [.5,.5,.5]
red = [1, 0, 0]
darkRed = [(115/255), 0, 0]

class AutonLayout(StackLayout):
    def __init__(self, ScreenSwitcher):
        self.switcher = ScreenSwitcher
        super(AutonLayout, self).__init__()
        self.display()

    def display(self):
        displist = []

        # row 1

        # displays cubes in switch in auton
        AutonSwitchDisp = quarterLabel("Cubes put in switch:\n\n" + str(self.switcher.robot.autonSwitch), lightOrange)
        displist.append(AutonSwitchDisp)
        # displays team number
        teamDisp = quarterLabel("Team: " + str(self.switcher.robot.teamNumber), black)
        displist.append(teamDisp)
        # displays event name
        eventDisp = quarterLabel("Event: " + self.switcher.robot.eventName, black)
        displist.append(eventDisp)
        # "Left" for attemptedSwitchSide
        side1Color = darkMagenta if self.switcher.robot.attemptedSwitchSide == "left" else lightMagenta
        sideButton1 = eighthButton("Robot\nattempted\nthe Left\nside", side1Color)
        sideButton1.bind(on_release=lambda x: self.changeSide("left"))
        displist.append(sideButton1)
        # "Right" for attemptedSwitchSide
        side2Color = darkMagenta if self.switcher.robot.attemptedSwitchSide == "right" else lightMagenta
        sideButton2 = eighthButton("Robot\nattempted\nthe Right\nside", side2Color)
        sideButton2.bind(on_release=lambda x: self.changeSide("right"))
        displist.append(sideButton2)

        # row 2

        # decrement AutonSwitchDisp
        AutonSwitchDec = eighthButton("-", lightOrange)
        AutonSwitchDec.bind(on_release=lambda x : self.changeSwitch(-1))
        displist.append(AutonSwitchDec)
        # increment AutonSwitchDisp
        AutonSwitchInc = eighthButton('+', lightOrange)
        AutonSwitchInc.bind(on_release=lambda x : self.changeSwitch(1))
        displist.append(AutonSwitchInc)
        # menu button
        menuButton = quarterButton("Menu")
        menuButton.bind(on_release=lambda x: self.switcher.switch("menu"))
        displist.append(menuButton)
        # displays scouter name
        scouterDisp = quarterLabel("Scouter: " + self.switcher.robot.scouter, black)
        displist.append(scouterDisp)
        # "None" for attemptedSwitchSide
        side3Color = darkMagenta if self.switcher.robot.attemptedSwitchSide == "none" else lightMagenta
        sideButton3 = quarterButton("Robot\ndidn't\nattempt\nthe switch", side3Color)
        sideButton3.bind(on_release=lambda x: self.changeSide("none"))
        displist.append(sideButton3)

        #row 3

        # scale & ecchange display
        # multi row 1
        multiLayout = StackLayout(size_hint=(.5, .5))
        displist.append(multiLayout)
        # scale disp for auton
        AutonScaleDisp = halfLabel("Cubes put in scale\nin auton:\n" + str(self.switcher.robot.autonScale), fairBlue)
        multiLayout.add_widget(AutonScaleDisp)
        # exchange disp for auton
        autonExchangeDisp = halfLabel("Cubes put in\nExchange\nin auton:\n" + str(self.switcher.robot.autonExchange), grey)
        multiLayout.add_widget(autonExchangeDisp)
        # multi row 2
        # decrement for auton scale
        AutonScaleDec = quaterHalfButton("-", fairBlue)
        AutonScaleDec.bind(on_release=lambda x: self.changeScale(-1))
        multiLayout.add_widget(AutonScaleDec)
        # increment for auton scale
        AutonScaleInc = quaterHalfButton("+", fairBlue)
        AutonScaleInc.bind(on_release=lambda x: self.changeScale(1))
        multiLayout.add_widget(AutonScaleInc)
        # decrement for auton exchange
        autonExchangeDec = quaterHalfButton("-", grey)
        autonExchangeDec.bind(on_release=lambda x: self.changeExchange(-1))
        multiLayout.add_widget(autonExchangeDec)
        # increment for auton exchange
        autonExchangeInc = quaterHalfButton("+", grey)
        autonExchangeInc.bind(on_release=lambda x: self.changeExchange(1))
        multiLayout.add_widget(autonExchangeInc)
        #end of multiLayout
        # starting position display
        startLayout = StackLayout(size_hint=(.5, .5))
        displist.append(startLayout)
        # left for starting position
        startColor1 = darkRed if self.switcher.robot.startingPosition == "left" else red
        startButton1 = tripleButton("Started in the\nLeft position", startColor1)
        startButton1.bind(on_release=lambda x: self.changeStart("left"))
        startLayout.add_widget(startButton1)
        # middle for starting position
        startColor2 = darkRed if self.switcher.robot.startingPosition == "middle" else red
        startButton2 = tripleButton("Started in the\nMiddle position", startColor2)
        startButton2.bind(on_release=lambda x: self.changeStart("middle"))
        startLayout.add_widget(startButton2)
        # right for starting position
        startColor3 = darkRed if self.switcher.robot.startingPosition == "right" else red
        startButton3 = tripleButton("Started in the\nRight position", startColor3)
        startButton3.bind(on_release=lambda x: self.changeStart("right"))
        startLayout.add_widget(startButton3)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

    def changeSwitch(self, change):
        self.switcher.robot.autonSwitch += change
        if self.switcher.robot.autonSwitch < 0:
            self.switcher.robot.autonSwitch = 0
        self.display()
    def changeSide(self, change):
        self.switcher.robot.attemptedSwitchSide = change
        self.display()
    def changeScale(self, change):
        self.switcher.robot.autonScale += change
        if self.switcher.robot.autonScale < 0:
            self.switcher.robot.autonScale = 0
        self.display()
    def changeExchange(self, change):
        self.switcher.robot.autonExchange += change
        if self.switcher.robot.autonExchange < 0:
            self.switcher.robot.autonExchange = 0
        self.display()
    def changeStart(self, change):
        self.switcher.robot.startingPosition = change
        self.display()
