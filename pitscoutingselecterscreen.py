from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
import sqlite3

class PitScoutingSelecterLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(TeleopLayout, self).__init__()
        self.display()

    def display(self):
        displist = []

        database = sqlite3.connect("scoutingdatabase.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM pitscoutingdata")
        for teamData in cursor.fetchall():
            teamNumber = teamData[0]
            button = sevenEighthButton(teamNumber)
            button.bind(on_release=lambda x: self.pitScouterMainSwitch(teamNumber))
            displist.append()

    def pitScouterMainSwitch(self, robot):
        self.switcher.robot = PitRobot(robot)
        self.switcher.switch("pit scouting main")
