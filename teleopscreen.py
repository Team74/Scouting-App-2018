from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.clock import Clock
from widgetpresets import ColorLabel, ColorButton, darkened
from robotclass import *
import sqlite3
import time

class TeleopLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(TeleopLayout, self).__init__()
        self.start = 0
        self.didStart = 0

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


        green = [14/255, 201/255, 170/255]
        purple = [114/255, 0, 1]
        magenta = [231/255, 58/255, 177/255]
        lightBlue = [28/255, 129/255, 201/255]
        orange = [255/255, 150/255, 75/255]
        red = [1, 0, 0]

        # jacob wtf is this comment vv
        # A layout that holds downs
        screenLayout = StackLayout(size_hint=(.25, .5))
        displist.append(screenLayout)
        # input for notes
        self.notesTextInput = TextInput(text=self.switcher.robot.notes, size_hint=(.5, .5))
        displist.append(self.notesTextInput)
        # climb Layout
        climbLayout = StackLayout(size_hint=(.25, .5))
        displist.append(climbLayout)
        # switch layout
        switchLayout = StackLayout(size_hint=(.25, .5))
        displist.append(switchLayout)
        # scale layout
        scaleLayout = StackLayout(size_hint=(.25, .5)) # smaller layout to get around larger widgets in the same line (notesTextInput)
        displist.append(scaleLayout)
        # exchange layout
        exchangeLayout = StackLayout(size_hint=(.25, .5))
        displist.append(exchangeLayout)
        # miss Layout
        missLayout = StackLayout(size_hint=(.25, .5))
        displist.append(missLayout)

        # ---switchLayout--- #
        # displays cubes in switch
        swtLbl = appendLabel("Cubes put in switch:\n\n" + str(self.switcher.robot.switch), (1, .5), darkened(purple), switchLayout)
        # decrement switchDisp
        appendButton("-", (.5, .5), darkened(purple), lambda x: self.changeSwitch(-1, swtLbl), switchLayout)
        # increment switchDisp
        appendButton("+", (.5, .5), darkened(purple), lambda x: self.changeSwitch(1, swtLbl), switchLayout)

        # --- screenLayout --- #
        infoLayout = StackLayout(size_hint=(1, .5))
        screenLayout.add_widget(infoLayout)
        # menu button
        appendButton("Menu", (1, .5), lightBlue, self.switchMenu, screenLayout)

        # --- infoLayout --- #
        # display round number
        appendLabel("Round: " + str(self.switcher.robot.roundNumber), (1, (1/3)), darkened(green), infoLayout)
        # displays scouter name
        # displays team number
        appendLabel("Team: " + str(self.switcher.robot.teamNumber), (1, (1/3)), darkened(green), infoLayout)
        # made to crash the app to test our quick save feature
        #appendButton("Team: " + str(self.switcher.robot.teamNumber), (1/3, .5), darkened(green), lambda x: self.crash() , screenLayout)
        #
        appendLabel("Scouter: " + self.switcher.robot.scouter, (1, (1/3)), darkened(green), infoLayout)

        # --- climbLayout --- #
        # "assisted" button for climb options
        climb1Color = darkened(magenta) if self.switcher.robot.climb == "were assisted" else magenta # darkening the currently selected climb option
        appendButton("Robot was assisted by another robot", (.5, .40), climb1Color, lambda x: self.changeClimb("were assisted"), climbLayout)
        # "did not climb" button for climb options
        climb2Color = darkened(magenta) if self.switcher.robot.climb == "didn't climb" else magenta # darkening the currently selected climb option
        appendButton("Robot didn't climb", (.5, .40), climb2Color, lambda x: self.changeClimb("didn't climb"), climbLayout)
        # "climbed" button for climb options
        climb3Color = darkened(magenta) if self.switcher.robot.climb == "climbed" or self.switcher.robot.climb == "climbed and assisted +1" or self.switcher.robot.climb == "climbed and assisted +2" else magenta # darkening the currently selected climb option
        appendButton("Robot climbed successfully", (1, .20), climb3Color, lambda x: self.changeClimb("climbed"), climbLayout)
        # "climbed +1" button for climb options
        climb4Color = darkened(magenta) if self.switcher.robot.climb == "assisted +1" or self.switcher.robot.climb == "climbed and assisted +1" else magenta # darkening the currently selected climb option
        appendButton("Assisted 1 other robot", (.5, .40), climb4Color, lambda x: self.changeClimb("assisted +1"), climbLayout)
        # "climbed +2" button for climb options
        climb5color = darkened(magenta) if self.switcher.robot.climb == "assisted +2" or self.switcher.robot.climb == "climbed and assisted +2" else magenta
        appendButton("Assisted 2 other robots", (.5, .40), climb5color, lambda x: self.changeClimb("assisted +2"), climbLayout)

        # --- scaleLayout --- #
        # displays cubes in scale
        sclLbl = appendLabel("Cubes put in scale:\n\n" + str(self.switcher.robot.scale), (1, .5), lightBlue, scaleLayout)
        # decrement scaleDisp
        appendButton("-", (.5, .5), lightBlue, lambda x: self.changeScale(-1, sclLbl), scaleLayout)
        # increment scaleDisp
        appendButton("+", (.5, .5), lightBlue, lambda x: self.changeScale(1, sclLbl), scaleLayout)

        # --- exchangeLayout --- #
        # displays cubes in exchange
        exchLbl = appendLabel("Cubes put in exchange:\n\n" + str(self.switcher.robot.exchange), (1, .5), orange, exchangeLayout)
        # decrement exchangeDisp
        appendButton("-", (.5, .5), orange, lambda x: self.changeExchange(-1, exchLbl), exchangeLayout)
        # increment exchangeDisp
        appendButton("+", (.5, .5), orange, lambda x: self.changeExchange(1, exchLbl), exchangeLayout)

        # --- missLayout --- #
        # miss cube displays
        misLbl = appendLabel("Cubes the robot has missed:\n\n" + str(self.switcher.robot.miss), (1, .5), red, missLayout)
        # dec miss
        appendButton("-", (.5, .5), red, lambda x: self.changeMiss(-1, misLbl), missLayout)
        #inc miss
        appendButton("+", (.5, .5), red, lambda x: self.changeMiss(1, misLbl), missLayout)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

    def switchMenu(self, _):
        self.switcher.robot.notes = self.notesTextInput.text
        self.switcher.switch("menu")

    def changeSwitch(self, change, label):
        self.switcher.robot.switch += change
        if self.switcher.robot.switch < 0:
            self.switcher.robot.switch = 0
        label.text = "Cubes put in switch:\n\n" + str(self.switcher.robot.switch)
    def changeScale(self, change, label):
        self.switcher.robot.scale += change
        if self.switcher.robot.scale < 0:
            self.switcher.robot.scale = 0
        label.text = "Cubes put in scale:\n\n" + str(self.switcher.robot.scale)
    def changeExchange(self, change, label):
        self.switcher.robot.exchange += change
        if self.switcher.robot.exchange < 0:
            self.switcher.robot.exchange = 0
        label.text = "Cubes put in exchange:\n\n" + str(self.switcher.robot.exchange)
    def changeMiss(self, change, label):
        self.switcher.robot.miss += change
        if self.switcher.robot.miss < 0:
            self.switcher.robot.miss = 0
        label.text = "Cubes the robot has missed:\n\n" + str(self.switcher.robot.miss)
    def changeClimb(self, change):
        self.switcher.robot.notes = self.notesTextInput.text
        if change == "climbed":
            if self.switcher.robot.climb == "assisted +1":
                change = "climbed and assisted +1"
            if self.switcher.robot.climb == "assisted +2":
                change = "climbed and assisted +2"
        if change == "assisted +1":
            if self.switcher.robot.climb == "climbed":
                chage = "climbed and assisted +1"
        if change == "assisted +2":
            if self.switcher.robot.climb == "climbed":
                change = "climbed and assisted +2"
        print(change)
        self.switcher.robot.climb = change
        self.display()
