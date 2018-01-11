import sqlite3

class Robot(object):
    def __init__(self, teamNumber):
        self.teamNumber = teamNumber
        # game pieces, teleop
        self.switch = 0
        self.scale = 0
        self.exchange = 0
        self.climb = "did not climb" # will be string - "did not climb", "tried but failed", "levitated", "climbed"
        self.notes = ""
        # auton
        self.startingPosition = 0 #TODO: which position is which?
        self.attemptedSwitchSide = "left" #or right
        self.autonSwitch = 0 # boolean, whether or not they scored in the switch
        self.autonScale = 0 # boolean, whether or not they scored in the scale
        self.autonExchange = 0 # boolean, whether or not they scored in the scale

class PitRobot(object):
    def __init__(self, teamNumber):
        self.teamNumber = teamNumber

        self.drivetrainType = "" # string, "tank variants", "mecanum", "swerve", "holonomic"
        self.canPickCubeOffGround = 0 # boolean, self explanatory
        self.canSwitch = 0 # boolean, whether or not they can drop a cube onto the switch
        self.canScale = 0 # boolean, whether or not they can drop a cube onto the scale
        self.canExchange = 0 # boolean, whether or not they can put a cube into the exchange
        self.image = None #TODO: PIL??
        self.notes = ""
