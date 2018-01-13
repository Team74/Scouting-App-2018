from kivy.app import App

from widgetpresets import *
from robotclass import *
from teleopscreen import *
from loginscreen import *
from autonscreen import *

class MyApp(App):
    def build(self):
        #return LoginLayout()
        #return TeleopLayout(Robot(1, "none", "some gay"))#team, event, scouter
        return autonLayout(Robot(1, "none", "some gay"))

if __name__ == "__main__":
    MyApp().run()
