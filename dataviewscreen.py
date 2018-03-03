from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window

from widgetpresets import *
from robotclass import *
import sqlite3
#import numpy as np
import os

class DataViewLayout(StackLayout):
    def __init__(self, parentScreen, ip):
        self.switcher = parentScreen
        super(DataViewLayout, self).__init__()
        self.query = ""
        self.robots = []
        database = sqlite3.connect("scoutingdatabase.db")
        cursor = database.cursor()
        print('____________________________________________________')
        print(cursor)
        print('____________________________________________________')
        cursor.execute("SELECT * FROM matchdata")
        for td in cursor.fetchall():
            print('_______________________________________________________________________________________________________________________________________________________________')
            print(td)
            print('_______________________________________________________________________________________________________________________________________________________________')
            self.robots.append(Robot(td[0], td[1], td[2], td[3], td[4], td[5], td[6], td[7], td[8], td[9], td[10], td[11], td[12], td[13]))
        database.close()
        self.queuedRobots = self.robots
        self.queue = []
        self.index = -1
        self.changePage(1)
        self.fromDataView = 0

    def appendButton(self, text, size_hint, bind):
        button = Button(text=text, size_hint=size_hint)
        button.bind(on_release=bind)
        self.displist.append(button)
    def appendPicture(self, source, size_hint):
        photo = Image(source=source, size_hint=size_hint, allow_stretch=True, keep_ratio=False)
        self.displist.append(photo)
    def addAll(self):
        self.clear_widgets()
        for widget in self.displist:
            self.add_widget(widget)

    def display(self):
        displist = []
        def appendLabel(text, sizeHint, color, widget=None, **kwargs):
            label = ColorLabel(text, sizeHint, color, **kwargs)
            if not widget: displist.append(label)
            else: widget.add_widget(label)
        def appendButton(text, sizeHint, color, bind, widget=None, **kwargs):
            button = ColorButton(text, sizeHint, color, **kwargs)
            button.bind(on_release=bind)
            if not widget: displist.append(button)
            else: widget.add_widget(button)

        # size hints
        searchSize = (5/8, 1/9)
        inputSize = (1/8, 1/9)
        labelSize = (1/12, 1/9)
        buttonSize = (1/2, 1/9)

        # index display
        appendLabel("Index:\n%s" % (self.index+1), inputSize, seaFoamGreen)

        # search bar
        searchBar = TextInput(size_hint=searchSize, multiline=False)
        searchBar.bind(on_text_validate=lambda _: self.processQuery(searchBar.text))
        displist.append(searchBar)

        # go button, back button
        appendButton("Go", inputSize, darkblue, lambda _: self.processQuery(searchBar.text))
        appendButton("Back", inputSize, darkblue, lambda x: self.changeScreens())

        # meta
        appendButton("team", labelSize, tameGreen, lambda _: self.processQuery("team")) # 0
        appendButton("round", labelSize, tameGreen, lambda _: self.processQuery("round")) # 1
        appendLabel("event", labelSize, tameGreen) # 2

        # nonmeta teleop
        appendButton("switch", labelSize, fairBlue, lambda _: self.processQuery("switch")) # 4
        appendButton("scale", labelSize, fairBlue, lambda _: self.processQuery("scale")) # 5
        appendButton("exchange", labelSize, fairBlue, lambda _: self.processQuery("exchange"), text_size="13sp") # 6
        appendLabel("climb", labelSize, fairBlue) # 7

        # nonmeta auton
        appendLabel("start\npos", labelSize, tameRed) # 9
        appendLabel("switch\nside", labelSize, tameRed) # 10
        appendButton("auton\nswitch", labelSize, tameRed, lambda _: self.processQuery("auton switch")) # 11
        appendButton("auton\nscale", labelSize, tameRed, lambda _: self.processQuery("auton scale")) # 12
        appendButton("auton\nexchange", labelSize, tameRed, lambda _: self.processQuery("auton exchange"), text_size="13sp") # 13

        for robot in self.queue:
            teamData = [
                robot.teamNumber, robot.roundNumber, robot.eventName,
                robot.switch, robot.scale, robot.exchange, robot.climb,
                robot.startingPosition, robot.attemptedSwitchSide, robot.autonSwitch, robot.autonScale, robot.autonExchange
            ]
            for data in teamData:
                appendLabel(data, labelSize, grey)

        appendButton("Prev page", buttonSize, fairBlue, lambda _: self.changePage(-1))
        appendButton("Next page", buttonSize, fairBlue, lambda _: self.changePage(1))

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def changeScreens(self):
        self.fromDataView = 1
        self.switcher.switch("login")

    def changePage(self, change):
        print(self.index + change)
        lo = (self.index + change) * 6
        hi = lo + 6
        newQueue = []
        for i in range(lo, hi):
            if i < 0: break
            try: newQueue.append(self.queuedRobots[i])
            except IndexError: break
        if newQueue: # making sure there is data in the page we're trying to switch to
            self.queue = newQueue
            self.index += change
        self.display()

    def processQuery(self, search):
        search = search.split(" ")
        command = search[0]
        args = search[1:]
        targets = [num for num in args if num[0] in "1234567890"]
        modifiers = [mod for mod in args if not mod in targets]

        editedTargets = [] # using to cheat scope
        for target in targets:
            editedTargets.append(int(target))
        targets = editedTargets

        editedMods = [] # using to cheat scope
        # simplifying modifiers
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

        # debugging
        print(command)
        print(targets)
        print(modifiers)

        # modular function to easily grab a range of robots with a certain parameter
        # here there be dragons, reckless behavior is ill-advised
        ################################################################################################################################
        # WARNING - JANKY SHIT INBOUND                                                                                                 #
        selRange = lambda botParam, lo, hi: [bot for bot in self.robots if bot.__dict__[botParam] > lo and bot.__dict__[botParam] < hi]# only for numerical
        selEqual = lambda botParam, search: [bot for bot in self.robots if bot.__dict__[botParam] == search]                           # for numerical and not
        # WARNING - JANKY SHIT INBOUND                                                                                                 #
        ################################################################################################################################

        # checking query
        nonNum = False # if the selecter is a numerical value
        key = lambda bot: bot.teamNumber
        # meta
        if   "team" == command:
            key = lambda bot: bot.teamNumber
            selecter = "teamNumber"
        elif "round" == command:
            key = lambda bot: bot.roundNumber
            selecter = "roundNumber"
        elif "event" == command:
            key = lambda bot: bot.event
            selecter = "event"
            nonNum = True
        # non-meta teleop
        elif "switch" == command:
            key = lambda bot: bot.switch
            selecter = "switch"
        elif "scale" == command:
            key = lambda bot: bot.scale
            selecter = "scale"
        elif "exchange" == command:
            key = lambda bot: bot.exchange
            selecter = "exchange"
        elif "climb" == command:
            key = lambda bot: bot.climb
            selecter = "climb"
            nonNum = True
        # non-meta auton
        elif "start" == command and modifiers[0] in ["side", "pos", "position"]:
            key = lambda bot: bot.startingPosition
            selecter = "startingPosition"
            nonNum = True
            modifiers.pop(0) # since modifiers[0] is part of the command, it can't be used as the search value
        elif "switch" == command and modifiers[0] in ["side", "pos", "position"]:
            key = lambda bot: bot.attemptedSwitchSide
            selecter = "attemptedSwitchSide"
            nonNum = True
            modifiers.pop(0) # ^^
        elif "auton" == command and modifiers[0] == "switch":
            key = lambda bot: bot.autonSwitch
            selecter = "autonSwitch"
            modifiers.pop(0)
        elif "auton" == command and modifiers[0] == "scale":
            key = lambda bot: bot.autonScale
            selecter = "autonScale"
            modifiers.pop(0)
        elif "auton" == command and modifiers[0] == "exchange":
            key = lambda bot: bot.autonExchange
            selecter = "autonExchange"
            modifiers.pop(0)

        print(targets)
        print(modifiers)

        lo = 0 # no value will subsede 0
        hi = 8000 # a value guaranteed higher than any values that will realistically be recorded, team numbers are all under 8000 this year

        # for numerical values, set a high and a low value
        if len(targets) == 2:
            lo = targets[0]
            hi = targets[1]
        if len(targets) == 1 and "more" in modifiers:
            print("I FOUND MORE")
            lo = targets[0]
            print(lo)
        if len(targets) == 1 and "less" in modifiers:
            print("I FOUND LESS")
            hi = targets[0]

        # for non-numerical values, use the modifiers list to get the search
        # non-numerical values will only use equivalency
        selectedRobots = []
        if nonNum:
            search = " ".join(modifiers)
            selectedRobots += selEqual(selecter, search)

        if targets and ("equal" in modifiers or not modifiers):
            selectedRobots += selEqual(selecter, targets[0])
        if targets and ("less" in modifiers or "more" in modifiers):
            selectedRobots += selRange(selecter, lo, hi)
        if not selectedRobots and not targets and not modifiers: # if there was no query (except for command)
            print("no command")
            selectedRobots = self.robots

        print(selectedRobots)

        self.queuedRobots = []
        self.queuedRobots = sorted(selectedRobots, key=key)

        self.changePage(0) # updates the queue to only include self.queuedRobots

    def switchBack(self, _):
        self.switcher.displayMain("_")
        self.clear_widgets()

    def graphSwitch(self, _):
        teamValues = {}
        for robot in self.queuedRobots:
            if robot.teamNumber in teamValues:
                teamValues[robot.teamNumber].append(robot.switch)

        currentDir = os.path.dirname(os.path.realpath(__file__))
        database = sqlite3.connect("%s/r/graphdata.db" % currentDir)
        database.execute("DELETE FROM switch")
        for team in teamValues:
            teamNumber = team
            mean = 0#np.mean(teamValues[team])
            standev = 0#np.std(teamValues[team])
            database.execute("INSERT INTO switch VALUES (?, ?, ?)", (team, mean, standev))
        database.commit()
        database.close()

        os.system("Rscript %s/r/switch.r" % currentDir) # will create a png in /r/graphs/switch.png

        self.displist = []
        self.appendButton("Back", (1, .05), lambda _: self.processQuery("")) # clears the queued robots and goes back to display
        self.appendPicture("%s/r/graphs/switch.png" % currentDir, (1, .95))
        self.addAll()
