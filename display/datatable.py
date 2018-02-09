from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window

from widgetpresets import *
from robotclass import *
import sqlite3

class DataViewLayout(StackLayout):
    def __init__(self, screenSwitcher, ip):
        self.switcher = screenSwitcher
        super(DataViewLayout, self).__init__()
        self.query = ""
        self.robots = []
        database = mysql.connector.connect(connection_timeout=1, user="jaga663", passwd="chaos", host=ip, database="Scouting2018")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM matchdata")
        for td in cursor.fetchall():
            self.robots.append(Robot(td[0], td[1], td[2], td[3], td[4], td[5], td[6], td[7], td[8], td[9], td[10], td[11], td[12], td[13]))
        database.close()
        self.queuedRobots = self.robots

        self.display()

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
        back.bind(on_release=lambda x: self.switcher.displayMain())
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

        for teamData in self.queuedRobots:
            for data in teamData:
                appendLabel(data, grey)

        for widget in scrolllist:
            dataTableLayout.add_widget(widget)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def processQuery(self, search):
        search = search.split(" ")
        command = search[0]
        args = search[1:]
        numbers = "1234567890"

        selectedRobots = self.robots

        # here there be dragons, reckless behavior is ill-advised
        #############################################################################################
        # WARNING - JANKY SHIT INBOUND                                                              #
        selecter = lambda botParam: [bot for bot in self.robots if bot.__dict__[botParam] == args[0]]
        # WARNING - JANKY SHIT INBOUND                                                              #
        #############################################################################################
        # whydoesthisworkwhydoesthisworkwhydoesthisworkwhydoesthisworkwhydoesthisworkwhydoesthiswork

        key = lambda bot: pass
        if "team" in command:
            key = lambda bot: bot.teamNumber
            if args[0] in numbers:
                selectedRobots = selecter("teamNumber")
        if "round" in command:
            key = lambda bot: bot.roundNumber
            if args[0] in numbers:
                selectedRobots = selecter("roundNumber")
        if "switch" in command:
            key = lambda bot: bot.switch
            if args[0] in numbers:
                selectedRobots = selecter("switch")
        if "scale" in command:
            key =

        self.queuedRobots = sorted(self.selectedRobots, key=key)


        self.display()
