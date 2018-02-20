from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from widgetpresets import ColorButton, ColorLabel

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

        seaFoamGreen = [14/255, 201/255, 170/255]
        darkSeaFoamGreen = [0/255, 141/255, 110/255]
        purple = [114/255, 0, 1]
        black = [0, 0, 0]
        lightMagenta = [231/255, 58/255, 177/255]
        darkMagenta = [171/255, 0/255, 117/255]
        darkFairBlue = [0/255, 69/255, 141/255]
        darkblue = [0, 0, 1]
        tameGreen = [0, 200/255, 0]
        darkTameGreen = [0, 140/255, 0]
        lightOrange = [255/255, 150/255, 75/255]
        darkOrange = [195/255, 90/255, 15/255]
        fairBlue = [28/255, 129/255, 201/255]
        darkFairBlue = [0/255, 69/255, 141/255]
        tameRed = [200/255, 0, 0]
        darkTameRed = [140/255, 0, 0]

        robot = self.switcher.robot

        # switch capability
        colorSwitchCan = darkSeaFoamGreen if robot.switchCapability else seaFoamGreen
        appendButton("CAN put cube on switch", (.25, .25), colorSwitchCan, lambda x: self.changeSwitch(1))

        # menu button
        appendButton("Menu", (.25, .25), purple, self.switchMenu)

        # team display
        appendLabel("Team: " + str(robot.teamNumber), (.25, .25), black)

        # climb capability
        colorClimbCan = darkMagenta if robot.climbCapability else lightMagenta
        appendButton("CAN climb", (.25, .25), colorClimbCan, lambda x: self.changeClimb(1))


        # switch capability
        colorSwitchCant = darkSeaFoamGreen if not robot.switchCapability else seaFoamGreen
        appendButton("CAN'T put cube on switch", (.25, .25), colorSwitchCant, lambda x: self.changeSwitch(0))

        # drivetrain layout
        drivetrainLayout = StackLayout(size_hint=(.5, .25))
        displist.append(drivetrainLayout)

        # tank drive
        colorTankDrive = darkFairBlue if robot.drivetrain == "tank" else fairBlue
        appendButton("Tank drive / tank variants", (.5, .5  ), colorTankDrive, lambda x: self.changeDrivetrain("tank"), drivetrainLayout)

        # swerve drive
        colorSwerveDrive = darkFairBlue if robot.drivetrain == "swerve" else fairBlue
        appendButton("Swerve drive", (.5, .5), colorSwerveDrive, lambda x: self.changeDrivetrain("swerve"), drivetrainLayout)

        # mecanum drive
        colorMecanumDrive = darkFairBlue if robot.drivetrain == "mecanum" else fairBlue
        appendButton("Mecanum drive", (.5, .5), colorMecanumDrive, lambda x: self.changeDrivetrain("mecanum"), drivetrainLayout)

        # holographic drive
        colorHoloDrive = darkFairBlue if robot.drivetrain == "holonomic" else fairBlue
        appendButton("Holonomic drive", (.5, .5), colorHoloDrive, lambda x: self.changeDrivetrain("holonomic"), drivetrainLayout)

        # climb capability
        colorClimbCant = darkMagenta if not robot.climbCapability else lightMagenta
        appendButton("CAN'T climb", (.25, .25), colorClimbCant, lambda x: self.changeClimb(0))


        # scale capability
        colorScaleCan = darkTameRed if robot.scaleCapability else tameRed
        appendButton("CAN put cube on scale", (.25, .25), colorScaleCan, lambda x: self.changeScale(1))

        # ground capability
        colorGroundCan = darkTameGreen if robot.groundPickup else tameGreen
        appendButton("CAN pick up cubes off ground", (.25, .25), colorGroundCan, lambda x: self.changeGround(1))

        # photo button
        appendButton("Photo", (.25, .25), lightMagenta, lambda x: self.switcher.switch("photo"))

        # exchange capability
        colorExchangeCan = darkOrange if robot.exchangeCapability else lightOrange
        appendButton("CAN put cube in exchange", (.25, .25), colorExchangeCan, lambda x: self.changeExchange(1))


        # scale capability
        colorScaleCant = darkTameRed if not robot.scaleCapability else tameRed
        appendButton("CAN'T put cube in scale", (.25, .25), colorScaleCant, lambda x: self.changeScale(0))

        # ground capability
        colorGroundCant = darkTameGreen if not robot.groundPickup else tameGreen
        appendButton("CAN'T pick up cubes off ground", (.25, .25), colorGroundCant, lambda x: self.changeGround(0))

        # notes
        self.notesInput = TextInput(size_hint=(.25, .25))
        displist.append(self.notesInput)

        # exchange capability
        colorExchangeCant = darkOrange if not robot.exchangeCapability else lightOrange
        appendButton("CAN'T put cube in exchange", (.25, .25), colorExchangeCant, lambda x: self.changeExchange(0))

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
