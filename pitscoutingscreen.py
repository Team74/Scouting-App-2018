from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from widgetpresets import ColorButton, ColorLabel, darkened

class PitScoutingLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PitScoutingLayout, self).__init__()
        self.notesInput = TextInput(text="ree")

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

        robot = self.switcher.robot # i got tired of having to type the full self.switcher.robot out

        purple = [114/255, 0, 1]
        green = [14/255, 201/255, 170/255]
        darkGreen = [0, 200/255, 0]
        magenta = [231/255, 58/255, 177/255]
        lightBlue = [28/255, 129/255, 201/255]
        orange = [255/255, 150/255, 75/255]
        black = [0, 0, 0]
        red = [200/255, 0, 0]

        # row 1

        # team display
        appendLabel("Team: " + str(robot.teamNumber), (.25, .25), black)

        # photo button
        appendButton("Photo", (.25, .25), purple, lambda x: self.switcher.switch("photo"))

        # notes
        self.notesInput = TextInput(text=robot.notes, size_hint=(.25, .25))
        displist.append(self.notesInput)

        # climb capability
        colorClimbCan = darkened(magenta) if robot.climbCapability else magenta
        appendButton("CAN climb", (.25, .25), colorClimbCan, lambda x: self.changeClimb(1))

        # row 2

        # menu button
        appendButton("Menu", (.25, .25), purple, self.switchMenu)

        # drivetrain layout
        drivetrainLayout = StackLayout(size_hint=(.5, .25))
        displist.append(drivetrainLayout)

        # tank drive
        colorTankDrive = darkened(lightBlue) if robot.drivetrain == "tank" else lightBlue
        appendButton("Tank drive / tank variants", (.5, .5), colorTankDrive, lambda x: self.changeDrivetrain("tank"), drivetrainLayout)

        # swerve drive
        colorSwerveDrive = darkened(lightBlue) if robot.drivetrain == "swerve" else lightBlue
        appendButton("Swerve drive", (.5, .5), colorSwerveDrive, lambda x: self.changeDrivetrain("swerve"), drivetrainLayout)

        # mecanum drive
        colorMecanumDrive = darkened(lightBlue) if robot.drivetrain == "mecanum" else lightBlue
        appendButton("Mecanum drive", (.5, .5), colorMecanumDrive, lambda x: self.changeDrivetrain("mecanum"), drivetrainLayout)

        # holographic drive
        colorHoloDrive = darkened(lightBlue) if robot.drivetrain == "holonomic" else lightBlue
        appendButton("Holonomic drive", (.5, .5), colorHoloDrive, lambda x: self.changeDrivetrain("holonomic"), drivetrainLayout)

        # climb capability
        colorClimbCant = darkened(magenta) if not robot.climbCapability else magenta
        appendButton("CAN'T climb", (.25, .25), colorClimbCant, lambda x: self.changeClimb(0))

        # row 3

        # ground capability
        colorGroundCan = darkened(darkGreen) if robot.groundPickup else darkGreen
        appendButton("CAN pick up cubes off ground", (.25, .25), colorGroundCan, lambda x: self.changeGround(1))

        # switch capability
        colorSwitchCan = darkened(green) if robot.switchCapability else green
        appendButton("CAN put cube on switch", (.25, .25), colorSwitchCan, lambda x: self.changeSwitch(1))

        # scale capability
        colorScaleCan = darkened(red) if robot.scaleCapability else red
        appendButton("CAN put cube on scale", (.25, .25), colorScaleCan, lambda x: self.changeScale(1))

        # exchange capability
        colorExchangeCan = darkened(orange) if robot.exchangeCapability else orange
        appendButton("CAN put cube in exchange", (.25, .25), colorExchangeCan, lambda x: self.changeExchange(1))

        # row 4

        # ground capability
        colorGroundCant = darkened(darkGreen) if not robot.groundPickup else darkGreen
        appendButton("CAN'T pick up cubes off ground", (.25, .25), colorGroundCant, lambda x: self.changeGround(0))

        # switch capability
        colorSwitchCant = darkened(green) if not robot.switchCapability else green
        appendButton("CAN'T put cube on switch", (.25, .25), colorSwitchCant, lambda x: self.changeSwitch(0))

        # scale capability
        colorScaleCant = darkened(red) if not robot.scaleCapability else red
        appendButton("CAN'T put cube in scale", (.25, .25), colorScaleCant, lambda x: self.changeScale(0))

        # exchange capability
        colorExchangeCant = darkened(orange) if not robot.exchangeCapability else orange
        appendButton("CAN'T put cube in exchange", (.25, .25), colorExchangeCant, lambda x: self.changeExchange(0))

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def switchMenu(self, _):
        self.switcher.robot.notes = self.notesInput.text
        self.switcher.switch("pitscouting menu")

    def changeDrivetrain(self, change):
        self.switcher.robot.drivetrain = change
        self.switcher.robot.notes = self.notesInput.text
        self.display()

    def changeGround(self, change):
        self.switcher.robot.groundPickup = change
        self.switcher.robot.notes = self.notesInput.text
        self.display()

    def changeSwitch(self, change):
        self.switcher.robot.switchCapability = change
        self.switcher.robot.notes = self.notesInput.text
        self.display()

    def changeScale(self, change):
        self.switcher.robot.scaleCapability = change
        self.switcher.robot.notes = self.notesInput.text
        self.display()

    def changeExchange(self, change):
        self.switcher.robot.exchangeCapability = change
        self.switcher.robot.notes = self.notesInput.text
        self.display()

    def changeClimb(self, change):
        self.switcher.robot.climbCapability = change
        self.switcher.robot.notes = self.notesInput.text
        self.display()

    def changeImage(self):
        # TODO: implement image
        self.display()
