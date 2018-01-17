from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from widgetpresets import *

class PitScoutingLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PitScoutingLayout, self).__init__()
        self.display()

    def display(self):
        displist = []

        # switch capability
        switchCanButton = quarterButton("CAN put cube on switch")
        displist.append(switchCanButton)

        # menu button
        menuButton = quarterButton("Menu")
        displist.append(menuButton)

        # team display
        teamDisp = quarterLabel("Team: " + str(self.switcher.robot.teamNumber))
        displist.append(teamDisp)

        # climb capability
        climbCanButton = quarterButton("CAN climb")
        displist.append(climbCanButton)


        # switch capability
        switchCantButton = quarterButton("CANT put cube on switch")
        displist.append(switchCantButton)

        # drivetrain layout
        drivetrainLayout = StackLayout(size_hint=(.5,.25))
        displist.append(drivetrainLayout)

        # tank drive
        tankDriveButton = halfButton("Tank drive / tank variants")
        drivetrainLayout.add_widget(tankDriveButton)

        # swerve drive
        swerveDriveButton = halfButton("Swerve drive")
        drivetrainLayout.add_widget(swerveDriveButton)

        # mecanum drive
        mecanumDriveButton = halfButton("Mecanum drive")
        drivetrainLayout.add_widget(mecanumDriveButton)

        # holographic drive
        holoDriveButton = halfButton("Holographic drive")
        drivetrainLayout.add_widget(holoDriveButton)

        # climb capability
        climbCantButton = quarterButton("CAN'T climb")
        displist.append(climbCantButton)


        # scale capability
        scaleCanButton = quarterButton("CAN put cube on scale")
        displist.append(scaleCanButton)

        # ground capability
        groundCanButton = quarterButton("CAN pick up cubes off ground")
        displist.append(groundCanButton)

        # photo button
        photoButton = quarterButton("Photo")
        displist.append(photoButton)

        # exchange capability
        exchangeCanButton = quarterButton("CAN put cube in exchange")
        displist.append(exchangeCanButton)


        # scale capability
        scaleCantButton = quarterButton("CAN'T put cube in scale")
        displist.append(scaleCantButton)

        # ground capability
        groundCantButton = quarterButton("CAN'T pick up cubes off ground")
        displist.append(groundCantButton)

        # notes
        notesInput = TextInput(size_hint=(.25, .25))
        displist.append(notesInput)

        # exchange capability
        exchangeCantButton = quarterButton("CAN'T put cube in exchange")
        displist.append(exchangeCantButton)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)
