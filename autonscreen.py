from kivy.uix.stacklayout import StackLayout
from loginscreen import *

from widgetpresets import *
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
        def appendButton(text, sizeHint, color, bind, widget=None, **kwargs):
            button = ColorButton(text, sizeHint, color, **kwargs)
            button.bind(on_release=bind)
            if not widget: displist.append(button)
            else: widget.add_widget(button)

        # row 1

        # displays cubes in switch in auton
        appendLabel("Cubes put in switch:\n\n" + str(self.switcher.robot.autonSwitch), quarterQuarter, lightOrange)
        # displays team number
        appendLabel("Team: " + str(self.switcher.robot.teamNumber), quarterQuarter, black)
        # displays event name
        appendLabel("Event: " + self.switcher.robot.eventName, quarterQuarter, black)
        # "Left" for attemptedSwitchSide
        side1Color = darkMagenta if self.switcher.robot.attemptedSwitchSide == "left" else lightMagenta
        appendButton("Robot\nattempted\nthe Left\nside", eighthQuarter, side1Color, lambda x: self.changeSide("left"))
        # "Right" for attemptedSwitchSide
        side2Color = darkMagenta if self.switcher.robot.attemptedSwitchSide == "right" else lightMagenta
        appendButton("Robot\nattempted\nthe Right\nside", eighthQuarter, side2Color, lambda x: self.changeSide("right"))

        # row 2

        # decrement AutonSwitchDisp
        appendButton("-", eighthQuarter, lightOrange, lambda x : self.changeSwitch(-1))
        # increment AutonSwitchDisp
        appendButton('+', eighthQuarter, lightOrange, lambda x : self.changeSwitch(1))
        # menu button
        appendButton("Menu", quarterQuarter, grey, lambda x: self.switcher.switch("menu"))
        #
        scoutLayout = StackLayout(size_hint = quarterQuarter)
        displist.append(scoutLayout)
        # "None" for attemptedSwitchSide
        side3Color = darkMagenta if self.switcher.robot.attemptedSwitchSide == "none" else lightMagenta
        appendButton("Robot\ndidn't\nattempt\nthe switch", quarterQuarter, side3Color, lambda x: self.changeSide("none"))

        # --- scoutLayout --- #
        # displays scouter name
        appendLabel("Scouter: " + self.switcher.robot.scouter, (1, .5), black, scoutLayout)
        #
        appendLabel("Rounds scouted: " + str(self.switcher.screens["login"].scoutNumber), (1, .5), black, scoutLayout)

        #row 3

        # scale & exchange display
        # multi row 1
        multiLayout = StackLayout(size_hint=halfHalf)
        displist.append(multiLayout)
        # scale disp for auton
        appendLabel("Cubes put in scale\nin auton:\n" + str(self.switcher.robot.autonScale), halfHalf, fairBlue, multiLayout)
        # exchange disp for auton
        appendLabel("Cubes put in\nExchange\nin auton:\n" + str(self.switcher.robot.autonExchange), halfHalf, grey, multiLayout)
        # multi row 2
        # decrement for auton scale
        appendButton("-", quarterHalf, fairBlue, lambda x: self.changeScale(-1), multiLayout)
        # increment for auton scale
        appendButton("+", quarterHalf, fairBlue, lambda x: self.changeScale(1), multiLayout)
        # decrement for auton exchange
        appendButton("-", quarterHalf, grey, lambda x: self.changeExchange(-1), multiLayout)
        # increment for auton exchange
        appendButton("+", quarterHalf, grey, lambda x: self.changeExchange(1), multiLayout)
        #end of multiLayout

        # starting position display
        startLayout = StackLayout(size_hint=halfHalf)
        displist.append(startLayout)
        # left for starting position
        startColor1 = darkRed if self.switcher.robot.startingPosition == "left" else red
        appendButton("Started in the\nLeft position", thirdWhole, startColor1, lambda x: self.changeStart("left"), startLayout)
        # middle for starting position
        startColor2 = darkRed if self.switcher.robot.startingPosition == "middle" else red
        appendButton("Started in the\nMiddle position", thirdWhole, startColor2, lambda x: self.changeStart("middle"), startLayout)
        # right for starting position
        startColor3 = darkRed if self.switcher.robot.startingPosition == "right" else red
        appendButton("Started in the\nRight position", thirdWhole, startColor3, lambda x: self.changeStart("right"), startLayout)

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
