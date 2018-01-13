from kivy.uix.stacklayout import StackLayout

from widgetpresets import *

class MenuLayout(StackLayout):
    def __init__(self, menu):
        super(MenuLayout, self).__init__()
        self.display()

    def display(self):
        displist = []

        autonButton = halfButton("Auton")
        displist.append(autonButton)

        teleopButton = halfButton("Teleop")
        displist.append(teleopButton)


        teamButton = halfButton("Change team")
        displist.append(teamButton)

        databaseLayout = StackLayout(size_hint=(.5, .5))
        displist.append(databaseLayout)

        saveButton = halfSubButton("Save")
        databaseLayout.add_widget(saveButton)

        exportButton = halfSubButton("Export")
        databaseLayout.add_widget(exportButton)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
