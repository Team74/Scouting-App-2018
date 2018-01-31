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

        # displays cubes in switch
        appendLabel("Cubes put in switch:\n\n" + str(self.switcher.robot.switch), quarterQuarter, seaFoamGreen)
        # displays team number
        appendLabel("Team: " + str(self.switcher.robot.teamNumber), quarterQuarter, black)
        # displays event name
        appendLabel("Event: " + self.switcher.robot.eventName, quarterQuarter, black)
        # "climbed" button for climb options
        climb1Color = darkMagenta if self.switcher.robot.climb == "climbed" else lightMagenta # darkening the currently selected climb option
        appendButton("Robot\nclimbed\nsuccessfully", eighthQuarter, climb1Color, lambda x: self.changeClimb("climbed"))
        # "tried but failed" button for climb options
        climb2Color = darkMagenta if self.switcher.robot.climb == "tried but failed" else lightMagenta # darkening the currently selected climb option
        appendButton("Robot\nattempted to\nclimb but\nfailed", eighthQuarter, climb2Color, lambda x: self.changeClimb("tried but failed"))

        # decrement switchDisp
        appendButton("-", eighthQuarter, seaFoamGreen, lambda x: self.changeSwitch(-1))
            #stop time // dont save
        # increment switchDisp
        appendButton("+", eighthQuarter, seaFoamGreen, lambda x: self.changeSwitch(1))
            #start time
        # menu button
        appendButton("Menu", quarterQuarter, grey, self.switchMenu)
        # displays scouter name
        appendLabel("Scouter: " + self.switcher.robot.scouter, quarterQuarter, black)
        # "levitated" button for climb options
        climb3Color = darkMagenta if self.switcher.robot.climb == "levitated" else lightMagenta # darkening the currently selected climb option
        appendButton("Robot\nlevitated", eighthQuarter, climb3Color, lambda x: self.changeClimb("levitated"))
        # "did not climb" button for climb options
        climb4Color = darkMagenta if self.switcher.robot.climb == "did not climb" else lightMagenta # darkening the currently selected climb option
        appendButton("Robot did\nnot climb", eighthQuarter, climb4Color, lambda x: self.changeClimb("did not climb"))

        # scale layout
        scaleLayout = StackLayout(size_hint=quarterHalf) # smaller layout to get around larger widgets in the same line (notesTextInput)
        displist.append(scaleLayout)
        # displays cubes in scale
        appendLabel("Cubes put in scale:\n\n" + str(self.switcher.robot.scale), wholeHalf, fairBlue, scaleLayout)
        # input for notes
        self.notesTextInput = TextInput(text=self.switcher.robot.notes, size_hint=halfHalf)
        displist.append(self.notesTextInput)
        # exchange layout
        exchangeLayout = StackLayout(size_hint=(.25, .5))
        displist.append(exchangeLayout)
        # displays cubes in exchange
        appendLabel("Cubes put in exchange:\n\n" + str(self.switcher.robot.exchange), wholeHalf, lightOrange, exchangeLayout)

        # decrement scaleDisp
        appendButton("-", halfHalf, fairBlue, lambda x: self.changeScale(-1), scaleLayout)
        # increment scaleDisp
        appendButton("+", halfHalf, fairBlue, lambda x: self.changeScale(1), scaleLayout)
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
