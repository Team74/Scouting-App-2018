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
        self.query = ""

    def display(self):
        scrolllist = []
        def appendScroll(text, color, font_size="15sp"):
            scrolllist.append(ColorLabel(text, (1/12, None), color, height=40, font_size=font_size))
        displist = []

        searchBar = TextInput(size_hint=(.75,.1))
        displist.append(searchBar)

        go = ColorButton("Go", (.125, .1), darkblue)
        go.bind(on_release=lambda x: self.processQuery(searchBar.text))
        displist.append(go)

        back = ColorButton("Back", (.125, .1), darkblue)
        back.bind(on_release=lambda x: self.switcher.switch("login"))
        displist.append(back)

        dataTable = ScrollView(size_hint=(1, None), size = (Window.width, Window.height-searchBar.height)) # make widgets and layouts for this
        displist.append(dataTable) # corresponding with the variables
        dataTableLayout = StackLayout(size_hint_y=None)
        dataTableLayout.bind(minimum_height=dataTableLayout.setter('height'))
        dataTable.add_widget(dataTableLayout)

        # meta
        appendScroll("team", tameGreen) # 0
        appendScroll("round", tameGreen) # 1
        appendScroll("event", tameGreen) # 2

        # nonmeta teleop
        appendScroll("switch", fairBlue) # 4
        appendScroll("scale", fairBlue) # 5
        appendScroll("exchange", fairBlue, "13sp") # 6
        appendScroll("climb", fairBlue) # 7

        # nonmeta auton
        appendScroll("start\npos", tameRed) # 9
        appendScroll("switch\nside", tameRed) # 10
        appendScroll("auton\nswitch", tameRed) # 11
        appendScroll("auton\nscale", tameRed) # 12
        appendScroll("auton\nexchange", tameRed, "13sp") # 13

        database = sqlite3.connect("scoutingdatabase.db") # data calling from db
        cursor = database.cursor()
        cursor.execute("SELECT teamNumber, roundNumber, eventName, switch, scale, exchange, climb, startingPosition, attemptedSwitchSide, autonSwitch, autonScale, autonExchange FROM matchdata " + self.query) # TODO: ORDER BY, add capability to order by based on the text input on the top
        for teamData in cursor.fetchall():
            for data in teamData:
                appendScroll(data, grey)

        database.close()

        for widget in scrolllist:
            dataTableLayout.add_widget(widget)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def processQuery(self, search):
        if "team" in search:
            self.query = "ORDER BY team"

        self.display()
