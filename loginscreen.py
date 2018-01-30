from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *
import sqlite3

class LoginLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(LoginLayout, self).__init__()


    def display(self):
        database = sqlite3.connect("scoutingdatabase.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM crash WHERE Exited=0")
        result = cursor.fetchone()
        if result:
            if not result[2] == "placeholder":
                self.switcher.robot = Robot(int(result[0]), int(result[1]), self.switcher.eventName, result[2])
                database.execute("UPDATE crash SET Exited=1")
                database.commit()
                database.close()
                self.switcher.switch("teleop")
            else:
                database.commit()
                database.close()
        else:
            database.commit()
            database.close()
        displist = []

        # scouter display
        scouterDisp = bigLabel("scouter", seaFoamGreen)
        displist.append(scouterDisp)
        # scouter input
        scouterInput = TextInput(text=str(""), multiline=False, size_hint=(.5, .25))
        displist.append(scouterInput)

        #row 2
        teamDisp = bigLabel("team", seaFoamGreen)
        displist.append(teamDisp)

        teamInput = TextInput(text=str(""), multiline=False, size_hint=(.5, .25))
        displist.append(teamInput)

        #row 3
        roundDisp = bigLabel("round", seaFoamGreen)
        displist.append(roundDisp)

        roundInput = TextInput(text=str(""), multiline=False, size_hint=(.5, .25))
        displist.append(roundInput)

        #row 4
        pitScout = quarterButton("Pit Scouting", fairBlue)
        pitScout.bind(on_release=lambda x: self.switcher.switch("pitscouting selecter"))
        displist.append(pitScout)

        dataview = quarterButton('dataview', fairBlue)
        dataview.bind(on_release=lambda x: self.switcher.switch("dataview"))
        displist.append(dataview)

        goButton = bigButton("Go", fairBlue)
        def teleopSwitch(_):
            number = "1234567890"
            #checking to see if team number and round number are input correctly so we dont have data type mismatch in sql database
            if not teamInput.text or not roundInput.text or not scouterInput.text: return
            for i in teamInput.text:
                if not i in number:
                    teamInput.text_hint = "invalid team number"
                    return
            for i in roundInput.text:
                if not i in number:
                    roundInput.text_hint = "invalid round number"
                    return
            self.switcher.robot = Robot(int(teamInput.text), int(roundInput.text), self.switcher.eventName, scouterInput.text)
            self.switcher.switch("auton")
        goButton.bind(on_release=teleopSwitch)
        displist.append(goButton)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
