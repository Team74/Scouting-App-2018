from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from widgetpresets import *

class PitScoutingLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PitScoutingLayout, self).__init__()

    def display(self):
        displist = []

        # switch capability
        print("ree")
        colorSwitchCan = darkSeaFoamGreen if self.switcher.robot.switchCapability else seaFoamGreen
        switchCanButton = quarterButton("CAN put cube on switch", colorSwitchCan)
        switchCanButton.bind(on_release=lambda x: self.changeSwitch(1))
        displist.append(switchCanButton)

        # menu button
        menuButton = quarterButton("Menu")
        displist.append(menuButton)

        # team display
        teamDisp = quarterLabel("Team: " + str(self.switcher.robot.teamNumber), black)
        displist.append(teamDisp)

        # climb capability
        climbCanButton = quarterButton("CAN climb", darkMagenta)
        displist.append(climbCanButton)


        # switch capability
        colorSwitchCant = darkSeaFoamGreen if not self.switcher.robot.switchCapability else seaFoamGreen
        switchCantButton = quarterButton("CANT put cube on switch", colorSwitchCant)
        displist.append(switchCantButton)

        # drivetrain layout
        drivetrainLayout = StackLayout(size_hint=(.5,.25))
        displist.append(drivetrainLayout)

        # tank drive
        tankDriveButton = halfButton("Tank drive / tank variants", fairBlue)
        drivetrainLayout.add_widget(tankDriveButton)

        # swerve drive
        swerveDriveButton = halfButton("Swerve drive", fairBlue)
        drivetrainLayout.add_widget(swerveDriveButton)

        # mecanum drive
        mecanumDriveButton = halfButton("Mecanum drive", fairBlue)
        drivetrainLayout.add_widget(mecanumDriveButton)

        # holographic drive
        holoDriveButton = halfButton("Holographic drive", fairBlue)
        drivetrainLayout.add_widget(holoDriveButton)

        # climb capability
        climbCantButton = quarterButton("CAN'T climb", darkMagenta)
        displist.append(climbCantButton)


        # scale capability
        scaleCanButton = quarterButton("CAN put cube on scale", tameRed)
        displist.append(scaleCanButton)

        # ground capability
        groundCanButton = quarterButton("CAN pick up cubes off ground", tameGreen)
        displist.append(groundCanButton)

        # photo button
        photoButton = quarterButton("Photo", lightMagenta)
        displist.append(photoButton)

        # exchange capability
        exchangeCanButton = quarterButton("CAN put cube in exchange", lightOrange)
        displist.append(exchangeCanButton)


        # scale capability
        scaleCantButton = quarterButton("CAN'T put cube in scale", tameRed)
        displist.append(scaleCantButton)

        # ground capability
        groundCantButton = quarterButton("CAN'T pick up cubes off ground", tameGreen)
        displist.append(groundCantButton)

        # notes
        notesInput = TextInput(size_hint=(.25, .25))
        displist.append(notesInput)

        # exchange capability
        exchangeCantButton = quarterButton("CAN'T put cube in exchange", lightOrange)
        displist.append(exchangeCantButton)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def changeDrivetrain(self, change):
        self.switcher.robot.drivetrain = change
        self.display()

    def changeGround(self, change):
        self.switcher.robot.groundPickup = change

    def changeSwitch(self, change):
        self.switcher.robot.switchCapability = change

    def changeScale(self, change):
        self.switcher.robot.scaleCapability = change

    def changeExchange(self, change):
        self.switcher.robot.exchangeCapability = change
        self.display()

    def changeClimb(self, change):
        self.switcher.robot.climbCapability = change
        self.display()

    def changeImage(self):
        # TODO: implement image
        self.display()
