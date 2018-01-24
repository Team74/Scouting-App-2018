from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from widgetpresets import *
from robotclass import *
import sqlite3

class DataViewLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(DataViewLayout, self).__init__()

    def display(self):
        scrolllist = []
        displist = []

        searchBar = TextInput(size_hint=(.875,.1))
        displist.append(searchBar)

        back = ColorButton("Back", (.125, .1), darkblue)
        back.bind(on_release=lambda x: self.switcher.switch("login"))
        displist.append(back)

        eventList = ScrollView(size_hint=(1, None), size = (Window.width, Window.height-searchBar.height)) # make widgets and layouts for this
        displist.append(eventList) # corresponding with the variables
        eventListLayout = StackLayout(size_hint_y=None)
        eventListLayout.bind(minimum_height=eventListLayout.setter('height'))
        eventList.add_widget(eventListLayout)

        database = sqlite3.connect("scoutingdatabase.db") # data calling from db
        cursor = database.cursor()
        cursor.execute("SELECT * FROM matchdata")
        for teamData in cursor.fetchall():
            print(teamData[0])
            roundNumber = teamData[1]
            teamNumber = teamData[0]
            eventName = teamData[2]
            button = ColorButton("Round: %s, Team: %s, %s" % (roundNumber, teamNumber, eventName), (1, None), fairBlue)
            scrolllist.append(button)
            button.bind(on_release=self.dataViewSwitch)
        database.close()

        for widget in scrolllist:
            eventListLayout.add_widget(widget)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def dataViewSwitch(self, numberButton):
        roundNumber, teamNumber, eventName = numberButton.text.split(", ")
        roundNumber = "".join([x for x in roundNumber if x in "1234567890"])
        teamNumber = "".join([x for x in teamNumber if x in "1234567890"])

        self.switcher.robot = Robot(int(teamNumber), int(roundNumber), eventName, "ree")
        self.switcher.switch('dataview screen')
