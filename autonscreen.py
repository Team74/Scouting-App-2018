from kivy.uix.stacklayout import StackLayout
from loginscreen import *

from widgetpresets import ColorLabel, ColorButton, darkened
from robotclass import *
import sqlite3

class AutonLayout(StackLayout):
    def __init__(self, ScreenSwitcher):
        self.switcher = ScreenSwitcher
        super(AutonLayout, self).__init__()


    def display(self):
        displist = []
        def appendLabel(text, sizeHint, color, widget=None, **kwargs):
            label = ColorLabel(text, sizeHint, color, **kwargs)
            if not widget: displist.append(label)
            else: widget.add_widget(label)
            return label
        def appendButton(text, sizeHint, color, bind, widget=None, **kwargs):
            button = ColorButton(text, sizeHint, color, **kwargs)
            button.bind(on_release=bind)
            if not widget: displist.append(button)
            else: widget.add_widget(button)
            return button

        purple = [114/255, 0, 1]
        green = [14/255, 201/255, 170/255]
        magenta = [231/255, 58/255, 177/255]
        lightBlue = [28/255, 129/255, 201/255]
        orange = [255/255, 150/255, 75/255]
        red = [1, 0, 0]
        brown = [81/255, 30/255, 55/255]

        metaInfo = StackLayout(size_hint=(.5, .5))
        displist.append(metaInfo)
        startLayout = StackLayout(size_hint=(.5, .5))
        displist.append(startLayout)

        #try:
            #self.switcher.robot.getStanding()
        #except:
            #print("carl forgot to fix this")

        #row 3

        # scale & exchange display
        switchLayout = StackLayout(size_hint=(.25, .5))
        displist.append(switchLayout)
        # displays cubes in switch in auton
        switchAuton = appendLabel("Cubes put in switch in auton:\n\n" + str(self.switcher.robot.autonSwitch), (1, .5), darkened(purple), switchLayout)
        # decrement AutonSwitchDisp
        appendButton("-", (.5, .5), darkened(purple), lambda x : self.changeSwitch(-1, switchAuton), switchLayout)
        # increment AutonSwitchDisp
        appendButton('+', (.5, .5), darkened(purple), lambda x : self.changeSwitch(1, switchAuton), switchLayout)
        # multi row 1
        multiLayout = StackLayout(size_hint=(.25, .5))
        displist.append(multiLayout)
        # displays team number
        appendLabel("Team: " + str(self.switcher.robot.teamNumber), (.5, .5), darkened(green), metaInfo)
        infoLayout = StackLayout(size_hint=(.5, .5))
        metaInfo.add_widget(infoLayout)
        # menu button
        appendButton(self.switcher.screens['login'].menuText, (.5, .5), lightBlue, lambda x: self.changeScreen(), metaInfo)
        #
        crossLayout = StackLayout(size_hint = (.5, .5))
        metaInfo.add_widget(crossLayout)
        exchangeLayout = StackLayout(size_hint=(.25, .5))
        displist.append(exchangeLayout)
        # scale disp for auton
        sclLbl = appendLabel("Cubes put in scale in auton:\n\n" + str(self.switcher.robot.autonScale), (1, .5), lightBlue, multiLayout)
        # exchange disp for auton
        exchLbl = appendLabel("Cubes put in exchange in auton:\n\n" + str(self.switcher.robot.autonExchange), (1, .5), orange, exchangeLayout)
        # multi row 2
        # decrement for auton scale
        appendButton("-", (.5, .5), lightBlue, lambda x: self.changeScale(-1, sclLbl), multiLayout)
        # increment for auton scale
        appendButton("+", (.5, .5), lightBlue, lambda x: self.changeScale(1, sclLbl), multiLayout)
        # decrement for auton exchange
        appendButton("-", (.5, .5), orange, lambda x: self.changeExchange(-1, exchLbl), exchangeLayout)
        # increment for auton exchange
        appendButton("+", (.5, .5), orange, lambda x: self.changeExchange(1, exchLbl), exchangeLayout)
        #end of multiLayout

        switchSide = StackLayout(size_hint=(.25, .5))
        displist.append(switchSide)
        # "Left" for attemptedSwitchSide
        side1Color = darkened(magenta) if self.switcher.robot.attemptedSwitchSide == "left" else magenta
        appendButton("Robot attempted the left side of the switch", (.5, .5), side1Color, lambda x: self.changeSide("left"), switchSide)
        # "Right" for attemptedSwitchSide
        side2Color = darkened(magenta) if self.switcher.robot.attemptedSwitchSide == "right" else magenta
        appendButton("Robot attempted the right side of the switch", (.5, .5), side2Color, lambda x: self.changeSide("right"), switchSide)
        # "None" for attemptedSwitchSide
        side3Color = darkened(magenta) if self.switcher.robot.attemptedSwitchSide == "none" else magenta
        appendButton("Robot didn't attempt the switch", (1, .5), side3Color, lambda x: self.changeSide("none"), switchSide)

        # --- infoLayout --- #
        # displays event name
        appendLabel("Event: " + self.switcher.robot.eventName, (1, .25), darkened(green), infoLayout)
        # display round number
        appendLabel("Round: " + str(self.switcher.robot.roundNumber), (1, .25), darkened(green), infoLayout)
        # displays scouter name
        print(self.switcher.robot.scouter)
        appendLabel("Scouter: " + self.switcher.robot.scouter, (1, .25), darkened(green), infoLayout)
        #
        appendLabel("Rounds scouted: " + str(self.switcher.screens["login"].scoutNumber), (1, .25), darkened(green), infoLayout)

        # --- crossLayout --- #
        cross1Color = darkened(brown) if self.switcher.robot.cross == "yes" else brown
        appendButton("Robot crossed the line", (1, .5), cross1Color, lambda x: self.changeCross("yes"), crossLayout)
        #
        cross2Color = darkened(brown) if self.switcher.robot.cross == "no" else brown
        appendButton("Robot didn't crossed the line", (1, .5), cross2Color, lambda x: self.changeCross("no"), crossLayout)

        # starting position display
        # left for starting position
        startColor1 = darkened(red, (110/255)) if self.switcher.robot.startingPosition == "left" else red
        appendButton("Started in the Left position", (1/3, 1), startColor1, lambda x: self.changeStart("left"), startLayout)
        # middle for starting position
        startColor2 = darkened(red, (110/255)) if self.switcher.robot.startingPosition == "middle" else red
        appendButton("Started in the Middle position", (1/3, 1), startColor2, lambda x: self.changeStart("middle"), startLayout)
        # right for starting position
        startColor3 = darkened(red, (110/255)) if self.switcher.robot.startingPosition == "right" else red
        appendButton("Started in the Right position", (1/3, 1), startColor3, lambda x: self.changeStart("right"), startLayout)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

    def changeSwitch(self, change, label):
        self.switcher.robot.autonSwitch += change
        if self.switcher.robot.autonSwitch < 0:
            self.switcher.robot.autonSwitch = 0
        label.text = "Cubes put in switch in auton:\n\n" + str(self.switcher.robot.autonSwitch)
    def changeScreen(self):
        if self.switcher.screens["login"].changer == 1:
            self.switcher.screens["login"].changer = 0
            self.switcher.screens["login"].menuText = "Menu"
            self.switcher.switch("teleop")
        else:
            self.switcher.switch("menu")
        self.display()
    def changeSide(self, change):
        self.switcher.robot.attemptedSwitchSide = change
        self.display()
    def changeScale(self, change, label):
        self.switcher.robot.autonScale += change
        if self.switcher.robot.autonScale < 0:
            self.switcher.robot.autonScale = 0
        label.text = "Cubes put in scale in auton:\n\n" + str(self.switcher.robot.autonScale)
    def changeExchange(self, change, label):
        self.switcher.robot.autonExchange += change
        if self.switcher.robot.autonExchange < 0:
            self.switcher.robot.autonExchange = 0
        label.text = "Cubes put in exchange in auton:\n\n" + str(self.switcher.robot.autonExchange)
    def changeStart(self, change):
        self.switcher.robot.startingPosition = change
        self.display()
    def changeCross(self, change):
        self.switcher.robot.cross = change
        self.display()
