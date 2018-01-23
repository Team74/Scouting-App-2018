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

        # displays cubes in switch
        switchDisp = quarterLabel("Cubes put in switch:\n\n" + str(self.switcher.robot.switch), seaFoamGreen)
        displist.append(switchDisp)
        # displays team number
        teamDisp = quarterLabel("Team: " + str(self.switcher.robot.teamNumber), black)
        displist.append(teamDisp)
        # displays event name
        eventDisp = quarterLabel("Event: " + self.switcher.robot.eventName, black)
        displist.append(eventDisp)
        # "climbed" button for climb options
        climb1Color = darkMagenta if self.switcher.robot.climb == "climbed" else lightMagenta # darkening the currently selected climb option
        climbButton1 = eighthButton("Robot\nclimbed\nsuccessfully", climb1Color)
        climbButton1.bind(on_release=lambda x: self.changeClimb("climbed"))
        displist.append(climbButton1)
        # "tried but failed" button for climb options
        climb2Color = darkMagenta if self.switcher.robot.climb == "tried but failed" else lightMagenta # darkening the currently selected climb option
        climbButton2 = eighthButton("Robot\nattempted to\nclimb but\nfailed", climb2Color)
        climbButton2.bind(on_release=lambda x: self.changeClimb("tried but failed"))
        displist.append(climbButton2)

        # decrement switchDisp
        switchDec = eighthButton("-", seaFoamGreen)
        switchDec.bind(on_release=lambda x: self.changeSwitch(-1))
        displist.append(switchDec)
        # increment switchDisp
        switchInc = eighthButton("+", seaFoamGreen)
        switchInc.bind(on_release=lambda x: self.changeSwitch(1))
        displist.append(switchInc)
        # menu button
        menuButton = quarterButton("Menu")
        menuButton.bind(on_release=self.switchMenu)
        displist.append(menuButton)
        # displays scouter name
        scouterDisp = quarterLabel("Scouter: " + self.switcher.robot.scouter, black)
        displist.append(scouterDisp)
        # "levitated" button for climb options
        climb3Color = darkMagenta if self.switcher.robot.climb == "levitated" else lightMagenta # darkening the currently selected climb option
        climbButton3 = eighthButton("Robot\nlevitated", climb3Color)
        climbButton3.bind(on_release=lambda x: self.changeClimb("levitated"))
        displist.append(climbButton3)
        # "did not climb" button for climb options
        climb4Color = darkMagenta if self.switcher.robot.climb == "did not climb" else lightMagenta # darkening the currently selected climb option
        climbButton4 = eighthButton("Robot did\nnot climb", climb4Color)
        climbButton4.bind(on_release=lambda x: self.changeClimb("did not climb"))
        displist.append(climbButton4)

        # scale display
        scaleLayout = StackLayout(size_hint=(.25, .5)) # smaller layout to get around larger widgets in the same line (notesTextInput)
        displist.append(scaleLayout)
        scaleDisp = fullLabel("Cubes put in scale:\n\n" + str(self.switcher.robot.scale), fairBlue)
        scaleLayout.add_widget(scaleDisp)
        # input for notes
        self.notesTextInput = TextInput(text=self.switcher.robot.notes, size_hint=(.5, .5))
        displist.append(self.notesTextInput)
        # displays cubes in exchange
        exchangeLayout = StackLayout(size_hint=(.25, .5))
        displist.append(exchangeLayout)
        exchangeDisp = fullLabel("Cubes put in exchange:\n\n" + str(self.switcher.robot.exchange), lightOrange)
        exchangeLayout.add_widget(exchangeDisp)

        # decrement scaleDisp
        scaleDec = halfButton("-", fairBlue)
        scaleDec.bind(on_release=lambda x: self.changeScale(-1))
        scaleLayout.add_widget(scaleDec)
        # increment scaleDisp
        scaleInc = halfButton("+", fairBlue)
        scaleInc.bind(on_release=lambda x: self.changeScale(1))
        scaleLayout.add_widget(scaleInc)
        # decrement exchangeDisp
        exchangeDec = halfButton("-", lightOrange)
        exchangeDec.bind(on_release=lambda x: self.changeExchange(-1))
        exchangeLayout.add_widget(exchangeDec)
        # increment exchangeDisp
        exchangeInc = halfButton("+", lightOrange)
        exchangeInc.bind(on_release=lambda x: self.changeExchange(1))
        exchangeLayout.add_widget(exchangeInc)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

    def switchMenu(self, _):
        self.switcher.robot.notes = self.notesTextInput.text
        print("saving notes: %s" % self.notesTextInput.text)
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
