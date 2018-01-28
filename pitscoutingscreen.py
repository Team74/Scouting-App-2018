from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from widgetpresets import *

class PitScoutingLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PitScoutingLayout, self).__init__()

    def display(self):
        displist = []
        def appendLabel(text, sizeHint, color, widget=None, **kwargs):
            label = ColorLabel(text, sizeHint, color, **kwargs)
            if not widget: displist.append(label)
            else: widget.add_widget(label)
        def appendButton(text, sizeHint, color, bind, widget=None, **kwargs):
            button = ColorButton(text, sizeHint, color, **kwargs)
            button.bind(on_release=bind)
            if not widget: displist.append(button)
            else: widget.add_widget(button)

        robot = self.switcher.robot

        # switch capability
        colorSwitchCan = darkSeaFoamGreen if robot.switchCapability else seaFoamGreen
        appendButton("CAN put cube on switch", quarterQuarter, colorSwitchCan, lambda x: self.changeSwitch(1))

        # menu button
        appendButton("Menu", quarterQuarter, grey, self.switchMenu)

        # team display
        appendLabel("Team: " + str(robot.teamNumber), quarterQuarter, black)

        # climb capability
        colorClimbCan = darkMagenta if robot.climbCapability else lightMagenta
        appendButton("CAN climb", quarterQuarter, colorClimbCan, lambda x: self.changeClimb(1))


        # switch capability
        colorSwitchCant = darkSeaFoamGreen if not robot.switchCapability else seaFoamGreen
        appendButton("CAN'T put cube on switch", quarterQuarter, colorSwitchCant, lambda x: self.changeSwitch(0))

        # drivetrain layout
        drivetrainLayout = StackLayout(size_hint=(.5,.25))
        displist.append(drivetrainLayout)

        # tank drive
        colorTankDrive = darkFairBlue if robot.drivetrain == "tank" else fairBlue
        appendButton("Tank drive / tank variants", halfHalf, colorTankDrive, lambda x: self.changeDrivetrain("tank"), drivetrainLayout)

        # swerve drive
        colorSwerveDrive = darkFairBlue if robot.drivetrain == "swerve" else fairBlue
        appendButton("Swerve drive", halfHalf, colorSwerveDrive, lambda x: self.changeDrivetrain("swerve"), drivetrainLayout)

        # mecanum drive
        colorMecanumDrive = darkFairBlue if robot.drivetrain == "mecanum" else fairBlue
        appendButton("Mecanum drive", halfHalf, colorMecanumDrive, lambda x: self.changeDrivetrain("mecanum"), drivetrainLayout)

        # holographic drive
        colorHoloDrive = darkFairBlue if robot.drivetrain == "holonomic" else fairBlue
        appendButton("Holonomic drive", halfHalf, colorHoloDrive, lambda x: self.changeDrivetrain("holonomic"), drivetrainLayout)

        # climb capability
        colorClimbCant = darkMagenta if not robot.climbCapability else lightMagenta
        appendButton("CAN'T climb", quarterQuarter, colorClimbCant, lambda x: self.changeClimb(0))


        # scale capability
        colorScaleCan = darkTameRed if robot.scaleCapability else tameRed
        appendButton("CAN put cube on scale", quarterQuarter, colorScaleCan, lambda x: self.changeScale(1))

        # ground capability
        colorGroundCan = darkTameGreen if robot.groundPickup else tameGreen
        appendButton("CAN pick up cubes off ground", quarterQuarter, colorGroundCan, lambda x: self.changeGround(1))

        # photo button
        appendLabel("Photo", quarterQuarter, lightMagenta)

        # exchange capability
        colorExchangeCan = darkOrange if robot.exchangeCapability else lightOrange
        appendButton("CAN put cube in exchange", quarterQuarter, colorExchangeCan, lambda x: self.changeExchange(1))


        # scale capability
        colorScaleCant = darkTameRed if not robot.scaleCapability else tameRed
        appendButton("CAN'T put cube in scale", quarterQuarter, colorScaleCant, lambda x: self.changeScale(0))

        # ground capability
        colorGroundCant = darkTameGreen if not robot.groundPickup else tameGreen
        appendButton("CAN'T pick up cubes off ground", quarterQuarter, colorGroundCant, lambda x: self.changeGround(0))

        # notes
        self.notesInput = TextInput(size_hint=quarterQuarter)
        displist.append(self.notesInput)

        # exchange capability
        colorExchangeCant = darkOrange if not robot.exchangeCapability else lightOrange
        appendButton("CAN'T put cube in exchange", quarterQuarter, colorExchangeCant, lambda x: self.changeExchange(0))

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def switchMenu(self, _):
        self.switcher.robot.notes = self.notesInput.text
        self.switcher.switch("pitscouting menu")

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
