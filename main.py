from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from menuscreen import MenuLayout
from loginscreen import LoginLayout
from teleopscreen import TeleopLayout
from robotclass import *

class ScreenSwitcher(BoxLayout):
    def __init__(self):
        super(ScreenSwitcher, self).__init__()
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
