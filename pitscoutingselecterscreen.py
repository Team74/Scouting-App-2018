from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window

from widgetpresets import *
from robotclass import *
import sqlite3

class PitScoutingSelecterLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PitScoutingSelecterLayout, self).__init__()
        self.display()

    def display(self):
        scrolllist = []
        displist = []

        searchBar = TextInput(size_hint=(1,.1))
        displist.append(searchBar)

        teamList = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-searchBar.height))
        displist.append(teamList)
        teamListLayout = StackLayout(size_hint_y=None)
        teamListLayout.bind(minimum_height=teamListLayout.setter('height'))
        teamList.add_widget(teamListLayout)

        database = sqlite3.connect("scoutingdatabase.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM pitscoutingdata")
        for teamData in cursor.fetchall():
            teamNumber = str(teamData[0])
            button = ColorButton(teamNumber, (.875, None), fairBlue, height=40)
            button.bind(on_release=lambda x: self.pitScouterMainSwitch(teamNumber))
            scrolllist.append(button)
            hasBeenScouted = "scouted" if teamData[1] else "NOT SCOUTED"
            labelBackground = [0, 1, 0] if teamData[1] else [1, 0, 0]
            label = ColorLabel(hasBeenScouted, (.125,None), labelBackground, height=40)
            scrolllist.append(label)

        for widget in scrolllist:
            teamListLayout.add_widget(widget)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def pitScouterMainSwitch(self, robot):
        self.switcher.robot = PitRobot(robot)
        self.switcher.switch("pitscouting main")
