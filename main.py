from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from robotclass import *
from menuscreen import MenuLayout
from loginscreen import LoginLayout
from autonscreen import AutonLayout
from teleopscreen import TeleopLayout
from pitmenuscreen import PitMenuLayout
from dataviewscreen import DataViewLayout
from pitscoutingscreen import PitScoutingLayout
from pitscoutingselecterscreen import PitScoutingSelecterLayout
from photoscreen import PhotoLayout
from robotclass import *
import sqlite3

class ScreenSwitcher(BoxLayout):
    def __init__(self):
        super(ScreenSwitcher, self).__init__()
        self.eventName = "Test"
        self.robot = Robot(1, 1, self.eventName, "placeholder")
        self.screens = {"login": LoginLayout(self), "menu": MenuLayout(self), "teleop": TeleopLayout(self), "pitscouting selecter": PitScoutingSelecterLayout(self), "auton": AutonLayout(self), "pitscouting main": PitScoutingLayout(self), "pitscouting menu": PitMenuLayout(self), "dataview": DataViewLayout(self), "photo": PhotoLayout(self)}
        self.currentScreen = self.screens["login"]
        self.display()

    def display(self):
        self.clear_widgets()
        self.add_widget(self.currentScreen)
        self.currentScreen.display()

    def switch(self, target, robot=None):
        self.currentScreen = self.screens[target]
        self.display()

class MyApp(App):
    def build(self):
        self.screenSwitcher = ScreenSwitcher()
        win = Window
        win.bind(on_keyboard=self.key_handler)
        return self.screenSwitcher
    def key_handler(self, _a, escape, _b, _c, _d):
        if escape in [27, 1001]:
            return """
            Nihilists with good imaginations

            I am satisfied hiding in our friend's apartment
            Only leaving once a day to buy some groceries
            Daylight, I'm so absent minded
            Nighttime, meeting new anxieties
            So am I erasing myself?
            Hope I'm not erasing myself

            I guess it would be nice to give my heart to a God
            But which one, which one do I choose?
            All the churches filled with losers, psycho or confused
            I just want to hold the divine in mine
            And forget, all of the beauty's wasted

            Let's fall back to earth and do something pleasant, say it
            We fell back to earth like gravity's bitches, bitches
            Physics makes us all its bitches

            I guess it would be nice to help in your escape
            From patterns your parents designed
            All the party people dancing for the indie star
            But he's the worst faker by far in the set
            I forget, all of the beauty's wasted

            I guess it would be nice
            Show me that things can be nice
            I guess it would be nice
            Show me that things can be nice
            """
        return False

if __name__ == "__main__":
    myapp = MyApp()
    try:
        myapp.run()
    except Exception as error:
        robot = myapp.screenSwitcher.robot
        if isinstance(robot, PitRobot): raise error
        robot.localSave("ree")
        database = sqlite3.connect("scoutingdatabase.db")
        database.execute("UPDATE crash SET Team=?, Round=?, Scouter=?, Exited=?", (robot.teamNumber, robot.roundNumber, robot.scouter, 0))
        database.commit()
        database.close()
        raise error
