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
        def appendLabel(text, color, font_size="15sp"):
            scrolllist.append(ColorLabel(text, (1/12, None), color, height=40, font_size=font_size))
        def appendButton(text, color, bind, font_size="15sp"):
            button = ColorButton(text, (1/12, None), [x + (30/255) for x in color], height=40, font_size=font_size)
            button.bind(on_release=bind)
            scrolllist.append(button)
        displist = []

        searchBar = TextInput(size_hint=(.75,.1), multiline=False)
        searchBar.bind(on_text_validate=lambda x: self.processQuery(searchBar.text))
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
        appendButton("team", tameGreen, lambda x: self.processQuery("team")) # 0
        appendButton("round", tameGreen, lambda x: self.processQuery("round")) # 1
        appendLabel("event", tameGreen) # 2

        # nonmeta teleop
        appendButton("switch", fairBlue, lambda x: self.processQuery("switch")) # 4
        appendButton("scale", fairBlue, lambda x: self.processQuery("scale")) # 5
        appendButton("exchange", fairBlue, lambda x: self.processQuery("exchange"), "13sp") # 6
        appendLabel("climb", fairBlue) # 7

        # nonmeta auton
        appendLabel("start\npos", tameRed) # 9
        appendLabel("switch\nside", tameRed) # 10
        appendButton("auton\nswitch", tameRed, lambda x: self.processQuery("auton switch")) # 11
        appendButton("auton\nscale", tameRed, lambda x: self.processQuery("auton scale")) # 12
        appendButton("auton\nexchange", tameRed, lambda x: self.processQuery("auton exchange"), "13sp") # 13

        database = sqlite3.connect("scoutingdatabase.db") # data calling from db
        cursor = database.cursor()
        cursor.execute("SELECT teamNumber, roundNumber, eventName, switch, scale, exchange, climb, startingPosition, attemptedSwitchSide, autonSwitch, autonScale, autonExchange FROM matchdata " + self.query)
        for teamData in cursor.fetchall():
            for data in teamData:
                appendLabel(data, grey)

        database.close()

        for widget in scrolllist:
            dataTableLayout.add_widget(widget)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def processQuery(self, search):
        search = search.split(" ")
        self.query = ""
        if "team" in search:
            self.query = "ORDER BY teamNumber"
            for i in search:
                if i[0] in "1234567890":
                    self.query = "WHERE teamNumber=%s" % i
        if "round" in search:
            self.query = "ORDER BY roundNumber"
            for i in search:
                if i[0] in "1234567890":
                    self.query = "WHERE roundNumber=%s" % i
        if "event" in search:
            if len(search) >= 2:
                self.query = "WHERE eventName=%s" % search[1]
        if "switch" in search and not "auton" in search:
            self.query = "ORDER BY switch DESC"
            for i in search:
                if i[0] in "123457890":
                    self.query = "WHERE switch=%s" % i
        if "scale" in search and not "auton" in search:
            self.query = "ORDER BY scale DESC"
            for i in search:
                if i[0] in "1234567890":
                    self.query = "WHERE scale=%s" % i
        if "exchange" in search and not "auton" in search:
            self.query = "ORDER BY exchange DESC"
            for i in search:
                if i[0] in "1234567890":
                    self.query = "WHERE exchange=%s" % i
        if "climb" in search or "climbed" in search:
            if len(search) >= 2:
                self.query = "WHERE climb='%s'" % " ".join(search[1:])
        if "start" in search and "pos" in search:
            if len(search) >= 3:
                self.query = "WHERE startingPosition='%s'" % search[2]
        if "switch" in search and "side" in search:
            if len(search) >= 3:
                self.query = "WHERE attemptedSwitchSide='%s'" % search[2]
        if "auton" in search and "switch" in search:
            self.query = "ORDER BY autonSwitch DESC"
            for i in search:
                if i[0] in "1234567890":
                    self.query = "WHERE autonSwitch=%s" % i
        if "auton" in search and "scale" in search:
            self.query = "ORDER BY autonScale DESC"
            for i in search:
                if i[0] in "1234567890":
                    self.query = "WHERE autonScale=%s" % i
        if "auton" in search and "exchange" in search:
            self.query = "ORDER BY autonExchange DESC"
            for i in search:
                if i[0] in "1234567890":
                    self.query = "WHERE autonExchange='%s'" % i


        self.display()
