import sqlite3

class Robot(object):
    def __init__(self, teamNumber, switch=0, scale=0, exchange=0, climb="did not climb", notes="", startingPosition=0, attemptedSwitchSide="left", autonSwitch=0, autonScale=0, autonExchange=0):
        self.teamNumber = teamNumber
        # game pieces, teleop #
        self.switch = switch # integer, how many cubes scored in switch
        self.scale = scale # integer, how many cubes scored in scale
        self.exchange = exchange #integer, how many cubes stored in exchange
        self.climb = climb # string - "did not climb", "tried but failed", "levitated", "climbed"
        self.notes = notes # string, notable things on robot
        # auton #
        self.startingPosition = 0 #TODO: which position is which?
        self.attemptedSwitchSide = "left" #or right
        self.autonSwitch = 0 # boolean, whether or not they scored in the switch
        self.autonScale = 0 # boolean, whether or not they scored in the scale
        self.autonExchange = 0 # boolean, whether or not they scored in the scale

class PitRobot(object):
    def __init__(self, teamNumber, drivetrainType="tank variants", cubeOffGround=0, canSwitch=0, canScale=0, canExchange=0, image=None, notes=""):
        self.teamNumber = teamNumber

        self.drivetrainType = "tank variants" # string, "tank variants", "mecanum", "swerve", "holonomic"
        self.cubeOffGround = 0 # boolean, whether or not they can pick up cubes off the ground
        self.canSwitch = 0 # boolean, whether or not they can drop a cube onto the switch
        self.canScale = 0 # boolean, whether or not they can drop a cube onto the scale
        self.canExchange = 0 # boolean, whether or not they can put a cube into the exchange
        self.image = None #TODO: PIL??
        self.notes = ""
