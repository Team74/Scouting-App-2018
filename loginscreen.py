from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

seaFoamGreen = [(14/255),(201/255),(170/255)]
darkMagenta = [(201/255),(28/255),(147/255)]
fairBlue = [(28/255),(129/255),(201/255)]
brintGreen = [(28/255),(201/255),(40/255)]
lightOrange = [(201/255),(170/255),(28/255)]
black = [0, 0, 0, 1]

class LoginLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(LoginLayout, self).__init__()

    def display(self):
        displist = []

        # scouter display
        scouterDisp = bigLabel("scouter", seaFoamGreen)
        displist.append(scouterDisp)
        # scouter input
        scouterInput = TextInput(text=str(""), multiline=False, size_hint=(.5, .25))
        displist.append(scouterInput)

        #row 2
        teamDisp = bigLabel("team", seaFoamGreen)
        displist.append(teamDisp)

        teamInput = TextInput(text=str(""), multiline=False, size_hint=(.5, .25))
        displist.append(teamInput)

        #row 3
        roundDisp = bigLabel("round", seaFoamGreen)
        displist.append(roundDisp)

        roundInput = TextInput(text=str(""), multiline=False, size_hint=(.5, .25))
        displist.append(roundInput)

        #row 4
        pitScout = bigButton("Pit Scouting", fairBlue)
        pitScout.bind(on_release=lambda x: self.switcher.switch("pitscouting selecter"))
        displist.append(pitScout)

        goButton = bigButton("Go", fairBlue)
        def teleopSwitch(_):
            if not int(teamInput.text):
                self.switcher.robot = Robot(int(teamInput.text), int(roundInput.text), self.switcher.eventName, scouterInput.text)
                self.switcher.switch("teleop")
        goButton.bind(on_release=teleopSwitch)
        displist.append(goButton)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
