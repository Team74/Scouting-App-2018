from kivy.app import App

from widgetpresets import *
from robotclass import *
from teleopscreen import *

class MyApp(App):
    def build(self):
        return TeleopLayout(Robot(1, "none", "some gay"))

if __name__ == "__main__":
    MyApp().run()
