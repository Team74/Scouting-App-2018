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
        self.index = 0

        self.display()

    def display(self):
        scrolllist = []
        displist = []
        def appendLabel(text, color, font_size="15sp", parent=displist):
            parent.append(ColorLabel(text, (1/12, None), color, height=40, font_size=font_size))
        def appendButton(text, color, bind, font_size="15sp", parent=displist):
            button = ColorButton(text, (1/12, None), [x + (30/255) for x in color], height=40, font_size=font_size)
            button.bind(on_release=bind)
            parent.append(button)

        searchBar = TextInput(size_hint=(.75,.1), multiline=False)
        searchBar.bind(on_text_validate=lambda x: self.processQuery(searchBar.text))
        displist.append(searchBar)

        go = ColorButton("Go", (.125, .1), darkblue)
        go.bind(on_release=lambda x: self.processQuery(searchBar.text))
        displist.append(go)

        back = ColorButton("Back", (.125, .1), darkblue)
        back.bind(on_release=lambda x: self.switcher.displayMain("_"))
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

        for robot in self.queuedRobots:
            teamData = [
                robot.teamNumber, robot.roundNumber, robot.eventName,
                robot.switch, robot.scale, robot.exchange, robot.climb,
                robot.startingPosition, robot.attemptedSwitchSide, robot.autonSwitch, robot.autonScale, robot.autonExchange
            ]
            for data in teamData:
                appendLabel(data, grey, parent=scrolllist)

        for widget in scrolllist:
            dataTableLayout.add_widget(widget)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def displayPage(self):
        lo = self.index * 7
        hi = (self.index + 1) * 7
        queue = self.queuedRobots[self.index*7:(self.index+1)*7]

    def processQuery(self, search):
        search = search.split(" ")
        command = search[0]
        args = search[1:]
        targets = [num for num in args if num[0] in "1234567890"]
        modifiers = [mod for mod in args if not mod in targets]

        editedTargets = []
        for target in targets:
            editedTargets.append(int(target))
        targets = editedTargets
        editedMods = []
        for mod in modifiers:
            if mod in ["=", "equals", "=="]:
                mod = "equal"
            elif mod in ["<", "lesser", "under"]:
                mod = "less"
            elif mod in [">", "greater", "over"]:
                mod = "more"
            elif mod == "<=":
                editedMods.append("equal")
                mod = "less"
            elif mod == ">=":
                editedMods.append("equal")
                mod = "more"

            editedMods.append(mod)
        modifiers = editedMods
        print(command)
        print(targets)
        print(modifiers)
        numbers = "1234567890"

        # here there be dragons, reckless behavior is ill-advised
        ###########################################################################################################################################
        # WARNING - JANKY SHIT INBOUND                                                                                                            #
        selRange = lambda botParam, lo, hi: [bot for bot in self.robots if bot.__dict__[botParam] > lo and bot.__dict__[botParam] < hi]
        # WARNING - JANKY SHIT INBOUND                                                                                                            #
        ###########################################################################################################################################
        # whydoesthisworkwhydoesthisworkwhydoesthisworkwhydoesthisworkwhydoesthisworkwhydoesthiswork

        key = lambda bot: bot.teamNumber
        if "team" == command:
            key = lambda bot: bot.teamNumber
            selecter = "teamNumber"
        if "round" == command:
            key = lambda bot: bot.roundNumber
            selecter = "roundNumber"
        if "switch" == command:
            key = lambda bot: bot.switch
            selecter = "switch"
        if "scale" in command:
            key = lambda bot: bot.scale
            selecter = "scale"

        lo = 0 # no value will subsede 0
        hi = 10000 # a value guaranteed higher than any values that will realistically be recorded
        if len(targets) == 2:
            lo = targets[0]
            hi = targets[1]
        if len(targets) == 1 and "more" in modifiers:
            print("I FOUND MORE")
            lo = targets[0]
        if len(targets) == 1 and "less" in modifiers:
            print("I FOUND LESS")
            hi = targets[0]

        selectedRobots = []
        if targets and ("equal" in modifiers or not modifiers):
            selectedRobots += selRange(selecter, targets[0]-1, targets[0]+1)
        if targets and ("less" in modifiers or "more" in modifiers):
            selectedRobots += selRange(selecter, lo, hi)
        if not selectedRobots:
            selectedRobots = self.robots

        self.queuedRobots = sorted(selectedRobots, key=key)

        self.display()
