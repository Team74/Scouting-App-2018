from kivy.uix.stacklayout import StackLayout

from widgetpresets import *

class PitMenuLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PitMenuLayout, self).__init__()

    def display(self):
        displist = []

        saveButton = fullButton("Save", darkPurple)
        saveButton.bind(on_release=lambda x: self.switcher.robot.localSave())
        displist.append(saveButton)

        pitScoutingSelecterButton = halfButton("Pit scouting team selection\n(all unsaved data will be lost)", darkPurple)
        pitScoutingSelecterButton.bind(on_release=lambda x: self.switcher.switch("pitscouting selecter"))
        displist.append(pitScoutingSelecterButton)

        backButton = halfButton("Back", darkPurple)
        backButton.bind(on_release=lambda x: self.switcher.switch("pitscouting main"))
        displist.append(backButton)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)
