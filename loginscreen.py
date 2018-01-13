from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

seaFoamGreen = [(14/255),(201/255),(170/255)]
darkMagenta = [(201/255),(28/255),(147/255)]
fairBlue = [(28/255),(129/255),(201/255)]
brintGreen = [(28/255),(201/255),(40/255)]
lightOrange = [(201/255),(170/255),(28/255)]
black = [0, 0, 0, 1]

class LoginLayout(StackLayout):
    def __init__(self, robot):
        self.robot = robot
        super(LoginLayout, self).__init__()
        self.display()

    def display(self):
        displist = []
        test = bigLabel("test", seaFoamGreen); displist.append(test)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
