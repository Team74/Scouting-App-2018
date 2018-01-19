from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from widgetpresets import *

class PitScoutingLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PitScoutingLayout, self).__init__()

    def display(self):
        displist = []
        robot = self.switcher.robot

        # switch capability
        colorSwitchCan = darkSeaFoamGreen if robot.switchCapability else seaFoamGreen
        switchCanButton = quarterButton("CAN put cube on switch", colorSwitchCan)
        switchCanButton.bind(on_release=lambda x: self.changeSwitch(1))
        displist.append(switchCanButton)

        # menu button
        menuButton = quarterButton("Menu")
<<<<<<< HEAD
        menuButton.bind(on_release=lambda x: self.switcher.switch("pitscouting menu"))
=======
        menuButton.bind(on_release=lambda x: self.switcher.switch("pitscouting selecter"))
>>>>>>> 9eb81f8ace649fe45d673c0ffec70a2abd275813
        displist.append(menuButton)

        # team display
        teamDisp = quarterLabel("Team: " + str(robot.teamNumber), black)
        displist.append(teamDisp)

        # climb capability
        colorClimbCan = darkMagenta if robot.climbCapability else lightMagenta
        climbCanButton = quarterButton("CAN climb", colorClimbCan)
        climbCanButton.bind(on_release=lambda x: self.changeClimb(1))
        displist.append(climbCanButton)


        # switch capability
        colorSwitchCant = darkSeaFoamGreen if not robot.switchCapability else seaFoamGreen
        switchCantButton = quarterButton("CAN'T put cube on switch", colorSwitchCant)
        switchCantButton.bind(on_release=lambda x: self.changeSwitch(0))
        displist.append(switchCantButton)

        # drivetrain layout
        drivetrainLayout = StackLayout(size_hint=(.5,.25))
        displist.append(drivetrainLayout)

        # tank drive
        colorTankDrive = darkFairBlue if robot.drivetrain == "tank" else fairBlue
        tankDriveButton = halfButton("Tank drive / tank variants", colorTankDrive)
        tankDriveButton.bind(on_release=lambda x: self.changeDrivetrain("tank"))
        drivetrainLayout.add_widget(tankDriveButton)

        # swerve drive
        colorSwerveDrive = darkFairBlue if robot.drivetrain == "swerve" else fairBlue
        swerveDriveButton = halfButton("Swerve drive", colorSwerveDrive)
        swerveDriveButton.bind(on_release=lambda x: self.changeDrivetrain("swerve"))
        drivetrainLayout.add_widget(swerveDriveButton)

        # mecanum drive
        colorMecanumDrive = darkFairBlue if robot.drivetrain == "mecanum" else fairBlue
        mecanumDriveButton = halfButton("Mecanum drive", colorMecanumDrive)
        mecanumDriveButton.bind(on_release=lambda x: self.changeDrivetrain("mecanum"))
        drivetrainLayout.add_widget(mecanumDriveButton)

        # holographic drive
        colorHoloDrive = darkFairBlue if robot.drivetrain == "holographic" else fairBlue
        holoDriveButton = halfButton("Holographic drive", colorHoloDrive)
        holoDriveButton.bind(on_release=lambda x: self.changeDrivetrain("holographic"))
        drivetrainLayout.add_widget(holoDriveButton)

        # climb capability
        colorClimbCant = darkMagenta if not robot.climbCapability else lightMagenta
        climbCantButton = quarterButton("CAN'T climb", colorClimbCant)
        climbCantButton.bind(on_release=lambda x: self.changeClimb(0))
        displist.append(climbCantButton)


        # scale capability
        colorScaleCan = darkTameRed if robot.scaleCapability else tameRed
        scaleCanButton = quarterButton("CAN put cube on scale", colorScaleCan)
        scaleCanButton.bind(on_release=lambda x: self.changeScale(1))
        displist.append(scaleCanButton)

        # ground capability
        colorGroundCan = darkTameGreen if robot.groundPickup else tameGreen
        groundCanButton = quarterButton("CAN pick up cubes off ground", colorGroundCan)
        groundCanButton.bind(on_release=lambda x: self.changeGround(1))
        displist.append(groundCanButton)

        # photo button
        photoButton = quarterButton("Photo", lightMagenta)
        displist.append(photoButton)

        # exchange capability
        colorExchangeCan = darkOrange if robot.exchangeCapability else lightOrange
        exchangeCanButton = quarterButton("CAN put cube in exchange", colorExchangeCan)
        exchangeCanButton.bind(on_release=lambda x: self.changeExchange(1))
        displist.append(exchangeCanButton)


        # scale capability
        colorScaleCant = darkTameRed if not robot.scaleCapability else tameRed
        scaleCantButton = quarterButton("CAN'T put cube in scale", colorScaleCant)
        scaleCantButton.bind(on_release=lambda x: self.changeScale(0))
        displist.append(scaleCantButton)

        # ground capability
        colorGroundCant = darkTameGreen if not robot.groundPickup else tameGreen
        groundCantButton = quarterButton("CAN'T pick up cubes off ground", colorGroundCant)
        groundCantButton.bind(on_release=lambda x: self.changeGround(0))
        displist.append(groundCantButton)

        # notes
        notesInput = TextInput(size_hint=(.25, .25))
        displist.append(notesInput)

        # exchange capability
        colorExchangeCant = darkOrange if not robot.exchangeCapability else lightOrange
        exchangeCantButton = quarterButton("CAN'T put cube in exchange", colorExchangeCant)
        exchangeCantButton.bind(on_release=lambda x: self.changeExchange(0))
        displist.append(exchangeCantButton)

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def changeDrivetrain(self, change):
        self.switcher.robot.drivetrain = change
        self.display()

    def changeGround(self, change):
        self.switcher.robot.groundPickup = change
        self.display()

    def changeSwitch(self, change):
        self.switcher.robot.switchCapability = change
        self.display()

    def changeScale(self, change):
        self.switcher.robot.scaleCapability = change
        self.display()

    def changeExchange(self, change):
        self.switcher.robot.exchangeCapability = change
        self.display()

    def changeClimb(self, change):
        self.switcher.robot.climbCapability = change
        self.display()

    def changeImage(self):
        # TODO: implement image
        self.display()
