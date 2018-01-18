from kivy.uix.stacklayout import StackLayout

from widgetpresets import *

class MenuLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(MenuLayout, self).__init__()

    def display(self):
        displist = []
        # auton switch
        autonButton = halfButton("Auton")
        autonButton.bind(on_release=lambda x: self.switcher.switch("auton"))
        displist.append(autonButton)
        # teleop switch
        teleopButton = halfButton("Teleop")
        teleopButton.bind(on_release=lambda x: self.switcher.switch("teleop"))
        displist.append(teleopButton)

        # login switch
        teamButton = halfButton("Change team (data will be lost if not saved)")
        teamButton.bind(on_release=lambda x: self.switcher.switch("login"))
        displist.append(teamButton)
        # layout for save and export buttons
        databaseLayout = StackLayout(size_hint=(.5, .5))
        displist.append(databaseLayout)
        # save button
        saveButton = fullButton("Save")
        saveButton.bind(on_release=self.switcher.robot.localSave)
        databaseLayout.add_widget(saveButton)
        # export button
        exportButton = fullButton("Export")
        databaseLayout.add_widget(exportButton)

        # actually displaying everything
        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
