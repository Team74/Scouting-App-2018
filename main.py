from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from menuscreen import MenuLayout
from loginscreen import LoginLayout
from autonscreen import AutonLayout
from teleopscreen import TeleopLayout
from pitmenuscreen import PitMenuLayout
from dataviewscreen import DataViewLayout
from pitscoutingscreen import PitScoutingLayout
from pitscoutingselecterscreen import PitScoutingSelecterLayout

from robotclass import *

class ScreenSwitcher(BoxLayout):
    def __init__(self):
        super(ScreenSwitcher, self).__init__()
        self.eventName = "Test"
        self.robot = Robot(1, 1, self.eventName, "placeholder")
        self.screens = {"login": LoginLayout(self), "menu": MenuLayout(self), "teleop": TeleopLayout(self), "pitscouting selecter": PitScoutingSelecterLayout(self), "auton": AutonLayout(self), "pitscouting main": PitScoutingLayout(self), "pitscouting menu": PitMenuLayout(self), "dataview": DataViewLayout(self)}
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
        return ScreenSwitcher()

if __name__ == "__main__":
    MyApp().run()
