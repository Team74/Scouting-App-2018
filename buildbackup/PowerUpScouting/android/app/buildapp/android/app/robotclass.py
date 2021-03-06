import sqlite3

class Robot(object):
    def __init__(self, teamNumber, roundNumber, eventName, scouter, switch=0, scale=0, exchange=0, climb="did not climb", notes="", startingPosition=0, attemptedSwitchSide="left", autonSwitch=0, autonScale=0, autonExchange=0):
        self.teamNumber = teamNumber
        self.roundNumber = roundNumber
        self.eventName = eventName
        self.scouter = scouter
        # game pieces, teleop #
        self.switch = switch # integer, how many cubes scored in switch
        self.scale = scale # integer, how many cubes scored in scale
        self.exchange = exchange #integer, how many cubes stored in exchange
        self.climb = climb # string - "did not climb", "tried but failed", "levitated", "climbed"
        self.notes = notes # string, notable things on robot
        # auton #
        self.startingPosition = "left" #string - "left", "middle", "right"
        self.attemptedSwitchSide = "left" #string - "left", "right"
        self.autonSwitch = 0 # integer, how many cubes scored in switch
        self.autonScale = 0 # integer, how many cubes scored in scale
        self.autonExchange = 0 # integer, how many cubes scored in scale

    def dumpData(self):
        return (self.teamNumber, self.roundNumber, self.eventName, self.scouter, self.switch, self.scale, self.exchange, self.climb, self.notes, self.startingPosition, self.attemptedSwitchSide, self.autonSwitch, self.autonScale, self.autonExchange) # this order matches that of the database

    def localSave(self, _): # _ is there for throwaway on_release argument passed by the button
        database = sqlite3.connect("scoutingdatabase.db") # opens database
        cursor = database.cursor() # acts as a placeholder, allows for fetchone()
        cursor.execute("SELECT * FROM matchdata WHERE teamNumber=? AND roundNumber=? AND eventName=?", self.dumpData()[:3]) # checking if the current robot matches one in the database
        if cursor.fetchone(): # if there was a match in the database:
            database.execute("UPDATE matchdata SET switch=?, scale=?, exchange=?, climb=?, notes=?, startingPosition=?, attemptedSwitchSide=?, autonSwitch=?, autonScale=?, autonExchange=? WHERE teamNumber=? AND roundNumber=? AND eventName=? AND scouter=?", self.dumpData()[4:] + self.dumpData()[:4])
        else: #if there was not a match in the database:
            database.execute("INSERT INTO matchdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", self.dumpData())
        database.commit()
        database.close()

class PitRobot(object):
    def __init__(self, teamNumber, drivetrain="tank variants", groundPickup=0, switchCapability=0, scaleCapability=0, exchangeCapability=0, climbCapability=0, image=None, notes=""):
        self.teamNumber = teamNumber
        print(self.teamNumber)
        self.drivetrain = drivetrain # string, "tank variants", "mecanum", "swerve", "holonomic"
        self.groundPickup = groundPickup # boolean, whether or not they can pick up cubes off the ground
        self.switchCapability = switchCapability # boolean, whether or not they can drop a cube onto the switch
        self.scaleCapability = scaleCapability # boolean, whether or not they can drop a cube onto the scale
        self.exchangeCapability = exchangeCapability # boolean, whether or not they can put a cube into the exchange
        self.climbCapability = climbCapability # boolean, whether or not they can climb
        self.image = image #TODO: will be a path name, make use of kivy's built in camera
        self.notes = notes

    def dumpData(self):
        return [self.teamNumber, self.drivetrain, self.groundPickup, self.switchCapability, self.scaleCapability, self.exchangeCapability, self.climbCapability, self.image, self.notes]

    def addRobot(self):
        database = sqlite3.connect("scoutingdatabase.db") # opens database
        cursor = database.cursor() # acts as a placeholder, allows for fetchone()
        cursor.execute("SELECT * FROM pitscoutingdata WHERE teamNumber=?", (self.teamNumber,))
        if not cursor.fetchone():
            database.execute("INSERT INTO pitscoutingdata VALUES (?,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)", (self.teamNumber,))
        database.commit()
        database.close()

    def localSave(self):
        database = sqlite3.connect("scoutingdatabase.db")
        database.execute("UPDATE pitscoutingdata SET drivetrain=?, groundPickup=?, switchCapability=?, scaleCapability=?, exchangeCapability=?, climbCapability=?, image=?, notes=? WHERE teamNumber=?", self.dumpData()[1:] + [self.teamNumber])
        database.commit()
        database.close()
