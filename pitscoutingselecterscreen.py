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

    def display(self):
        scrolllist = []
        displist = []

        searchBar = TextInput(size_hint=(.875,.1))
        displist.append(searchBar)

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
        cursor.execute("SELECT * FROM pitscoutingdata")
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
        addText = TextInput(text=str(""), multiline=False, size_hint=(.5, None))
        scrolllist.append(addText)

        for widget in scrolllist:
            teamListLayout.add_widget(widget)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def pitScouterMainSwitch(self, numberButton):
        self.switcher.robot = PitRobot(numberButton.text)
        self.switcher.switch("pitscouting main")

    def addPitRobot(self, teamNumber):
<<<<<<< HEAD
        PitRobot(str(teamNumber)).addRobot()
=======
        number = "1234567890"
        for i in teamNumber:
            if not i in number:
                return
        PitRobot(str(teamNumber)).pitLocalSave()
>>>>>>> 9eb81f8ace649fe45d673c0ffec70a2abd275813
        self.display()
