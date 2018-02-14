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
        self.query = ""

    def display(self):
        scrolllist = []
        displist = []

        searchBar = TextInput(size_hint=(.75,.1), multiline=False)
        searchBar.bind(on_text_validate=lambda x: self.processQuery(searchBar.text))
        displist.append(searchBar)

        back = ColorButton("Go", (.125, .1), darkblue)
        back.bind(on_release=lambda x: self.processQuery(searchBar.text))
        displist.append(back)

        back = ColorButton("Back", (.125, .1), darkblue)
        back.bind(on_release=lambda x: self.switcher.switch("login"))
        displist.append(back)

        teamList = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-searchBar.height))
        displist.append(teamList)
        teamListLayout = StackLayout(size_hint_y=None)
        teamListLayout.bind(minimum_height=teamListLayout.setter('height'))
        teamList.add_widget(teamListLayout)

        database = sqlite3.connect("scoutingdatabase.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM pitscoutingdata " + self.query)
        for teamData in cursor.fetchall():
            teamNumber = teamData[0]
            button = ColorButton(str(teamNumber), (.875,None), fairBlue, height=40)
            button.bind(on_release=self.pitScouterMainSwitch)
            scrolllist.append(button)
            hasBeenScouted = "scouted" if teamData[1] else "NOT SCOUTED"
            labelBackground = green if teamData[1] else red
            label = ColorLabel(hasBeenScouted, (.125,None), labelBackground, height=40)
            scrolllist.append(label)
        database.close()

        addTeam = ColorButton("add team", (.5, None), darkblue, height=40)
        addTeam.bind(on_release=lambda x: self.addPitRobot(addText.text))
        scrolllist.append(addTeam)
        addText = TextInput(text=str(""), multiline=False, size_hint=(.5, None), height=40)
        addText.bind(on_validate_text=lambda x: self.addPitRobot(addText.text))
        scrolllist.append(addText)

        for widget in scrolllist:
            teamListLayout.add_widget(widget)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def processQuery(self, search):
        self.query = ""
        print("searching with %s" % search)
        if not search:
            self.display()
            return
        search = search.split(" ")
        print("params are %s" % [x for x in search])
        if "scouted" in search and not "not" in search:
            self.query = "WHERE NOT drivetrain=NULL"
        if "not" in search and "scouted" in search:
            self.query = "WHERE drivetrain=NULL"
        if "team" in search:
            if len(search) >= 2:
                self.query = "WHERE teamNumber=%s" % search[1]
        if search[0][0] in "1234567890":
            self.query = "WHERE teamNumber=%s" % search[0]
        self.display()

    def pitScouterMainSwitch(self, numberButton):
        self.switcher.robot = PitRobot(numberButton.text)
        self.switcher.switch("pitscouting main")

    def addPitRobot(self, teamNumber):
        number = "1234567890"
        if not teamNumber: return
        for i in teamNumber:
            if not i in number:
                return
        PitRobot(str(teamNumber)).addRobot()
        self.display()
