from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

class TeleopLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(TeleopLayout, self).__init__()

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

        # A layout that holds
        screenLayout = StackLayout(size_hint=(.75, .5))
        displist.append(screenLayout)
        # climb Layout
        climbLayout = StackLayout(size_hint=quarterHalf)
        displist.append(climbLayout)
        # scale layout
        scaleLayout = StackLayout(size_hint=quarterHalf) # smaller layout to get around larger widgets in the same line (notesTextInput)
        displist.append(scaleLayout)
        # input for notes
        self.notesTextInput = TextInput(text=self.switcher.robot.notes, size_hint=halfHalf)
        displist.append(self.notesTextInput)
        # exchange layout
        exchangeLayout = StackLayout(size_hint=(.25, .5))
        displist.append(exchangeLayout)

        # --- screenLayout --- #
        # displays cubes in switch
        appendLabel("Cubes put in switch:\n\n" + str(self.switcher.robot.switch), (1/3, .5), seaFoamGreen, screenLayout)
        # displays team number
        appendLabel("Team: " + str(self.switcher.robot.teamNumber), (1/3, .5), black, screenLayout)
        # displays event name
        appendLabel("Event: " + self.switcher.robot.eventName, (1/3, .5), black, screenLayout)
        # decrement switchDisp
        appendButton("-", (1/6, .5), seaFoamGreen, lambda x: self.changeSwitch(-1), screenLayout)
            #stop time // dont save
        # increment switchDisp
        appendButton("+", (1/6, .5), seaFoamGreen, lambda x: self.changeSwitch(1), screenLayout)
            #start time
        # menu button
        appendButton("Menu", (1/3, .5), grey, self.switchMenu, screenLayout)
        # displays scouter name
        appendLabel("Scouter: " + self.switcher.robot.scouter, (1/3, .5), black, screenLayout)

        # --- climbLayout --- #
        # "assisted" button for climb options
        climb1Color = darkMagenta if self.switcher.robot.climb == "assisted" else lightMagenta # darkening the currently selected climb option
        appendButton("Robot\nwas\nassisted", (.5, .40), climb1Color, lambda x: self.changeClimb("assisted"), climbLayout)
        # "climbed" button for climb options
        climb2Color = darkMagenta if self.switcher.robot.climb == "climbed" else lightMagenta # darkening the currently selected climb option
        appendButton("Robot\nClimbed\nSuccessfully", (.5, .40), climb2Color, lambda x: self.changeClimb("climbed"), climbLayout)
        # "climbed +1" button for climb options
        climb3Color = darkMagenta if self.switcher.robot.climb == "assisted +1" else lightMagenta # darkening the currently selected climb option
        appendButton("assisted\n1", (.5, .40), climb3Color, lambda x: self.changeClimb("assisted 1"), climbLayout)
        # "climbed +2" button for climb options
        climb4color = darkMagenta if self.switcher.robot.climb == "assisted +2" else lightMagenta
        appendButton("assisted\n2", (.5, .40), climb4color, lambda x: self.changeClimb("assisted 2"), climbLayout)
        # "did not climb" button for climb options
        climb5Color = darkMagenta if self.switcher.robot.climb == "didn't climbed" else lightMagenta # darkening the currently selected climb option
        appendButton("Robot didn't\n climb", (1, .20), climb5Color, lambda x: self.changeClimb("didn't climb"), climbLayout)

        # --- scaleLayout --- #
        # displays cubes in scale
        appendLabel("Cubes put in scale:\n\n" + str(self.switcher.robot.scale), wholeHalf, fairBlue, scaleLayout)
        # decrement scaleDisp
        appendButton("-", halfHalf, fairBlue, lambda x: self.changeScale(-1), scaleLayout)
        # increment scaleDisp
        appendButton("+", halfHalf, fairBlue, lambda x: self.changeScale(1), scaleLayout)

        # --- exchangeLayout --- #
        # displays cubes in exchange
        appendLabel("Cubes put in exchange:\n\n" + str(self.switcher.robot.exchange), wholeHalf, lightOrange, exchangeLayout)
        # decrement exchangeDisp
        appendButton("-", halfHalf, lightOrange, lambda x: self.changeExchange(-1), exchangeLayout)
        # increment exchangeDisp
        appendButton("+", halfHalf, lightOrange, lambda x: self.changeExchange(1), exchangeLayout)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

    def switchMenu(self, _):
        self.switcher.robot.notes = self.notesTextInput.text
        self.switcher.switch("menu")

    def changeSwitch(self, change):
        self.switcher.robot.switch += change
        if self.switcher.robot.switch < 0:
            self.switcher.robot.switch = 0
        self.display()
    def changeScale(self, change):
        self.switcher.robot.scale += change
        if self.switcher.robot.scale < 0:
            self.switcher.robot.scale = 0
        self.display()
    def changeExchange(self, change):
        self.switcher.robot.exchange += change
        if self.switcher.robot.exchange < 0:
            self.switcher.robot.exchange = 0
        self.display()
    def changeClimb(self, change):
        self.switcher.robot.climb = change
        self.display()
