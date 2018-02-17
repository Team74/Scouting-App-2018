import sqlite3
import mysql.connector

class Robot(object):
    def __init__(self, teamNumber, roundNumber, eventName, scouter, switch=0, scale=0, exchange=0, climb="did not climb", notes="", startingPosition=0, attemptedSwitchSide="left", autonSwitch=0, autonScale=0, autonExchange=0):
        self.teamNumber = teamNumber
        self.roundNumber = roundNumber
        self.eventName = eventName
        self.scouter = scouter
        # game pieces, teleop #
        self.switch = switch # integer, how many cubes scored in switch
        self.scale = scale # integer, how many cubes scored in scale
        self.exchange = exchange #integer, how many cubes scored in exchange
        self.climb = climb # string - "climbed", "didn't climb", "assisted", "assisted +1", "assisted +2"
        self.notes = notes # string, notable things on robot
        # auton #
        self.startingPosition = "left" #string - "left", "middle", "right"
        self.attemptedSwitchSide = "left" #string - "left", "right"
        self.autonSwitch = 0 # integer, how many cubes scored in switch
        self.autonScale = 0 # integer, how many cubes scored in scale
        self.autonExchange = 0 # integer, how many cubes scored in scale

        self.reloadRobot(self.teamNumber, self.roundNumber)

    def dumpData(self): #function for putting all values into a list ordered like the sqlite database
        return (self.teamNumber, self.roundNumber, self.eventName, self.scouter, self.switch, self.scale, self.exchange, self.climb, self.notes, self.startingPosition, self.attemptedSwitchSide, self.autonSwitch, self.autonScale, self.autonExchange) # this order matches that of the database

    def localSave(self, _): # _ is there for throwaway on_release argument passed by the button
        print("auton - saving %s" % self.teamNumber)
        database = sqlite3.connect("scoutingdatabase.db") # opens database
        cursor = database.cursor() # acts as a placeholder, allows for fetchone()
        cursor.execute("SELECT * FROM matchdata WHERE teamNumber=? AND roundNumber=? AND eventName=?", self.dumpData()[:3]) # checking if the current robot matches one in the database
        if cursor.fetchone(): # if there was a match in the database:
            print("found match, updating with %s" % str(self.dumpData()[3:]))
            database.execute("""
                UPDATE matchdata SET
                scouter=?, switch=?, scale=?, exchange=?, climb=?, notes=?,
                startingPosition=?, attemptedSwitchSide=?, autonSwitch=?, autonScale=?, autonExchange=?
                WHERE teamNumber=? AND roundNumber=? AND eventName=?""", self.dumpData()[3:] + self.dumpData()[:3]) #list splicing - gives all nonmeta (actual game data) values, then gives meta (team number, round, event, scouter) values
        else: #if there was not a match in the database:
            print("no match")
            database.execute("INSERT INTO matchdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", self.dumpData())
        database.commit()
        database.close()

    def reloadRobot(self, targetBot, targetRound):
        database = sqlite3.connect("scoutingdatabase.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM matchdata WHERE teamNumber=? AND roundNumber=?", (targetBot, targetRound))
        robotData = cursor.fetchone()
        database.close() # no commit needed, no changes were made to the database
        if not robotData: return # if target robot data doesnt exist it will error if we dont stop the function
        print(robotData[0])
        print(robotData[1])

        self.teamNumber = robotData[0]
        self.roundNumber = robotData[1]
        self.eventName = robotData[2]
        # skipping scouter

        self.switch = robotData[4]
        self.scale = robotData[5]
        self.exchange = robotData[6]
        self.climb = robotData[7]
        self.notes = robotData[8]

        self.startingPosition = robotData[9]
        self.attemptedSwitchSide = robotData[10]
        self.autonSwitch = robotData[11]
        self.autonScale = robotData[12]
        self.autonExchange = robotData[13]


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

        self.reloadRobot(self.teamNumber)

    def dumpData(self):
        return [self.teamNumber, self.drivetrain, self.groundPickup, self.switchCapability, self.scaleCapability, self.exchangeCapability, self.climbCapability, self.image, self.notes]

    def localSave(self):
        database = sqlite3.connect("scoutingdatabase.db")
        print("pit scouting - saving %s with %s" % (self.teamNumber, self.dumpData()[1:]))
        database.execute("UPDATE pitscoutingdata SET drivetrain=?, groundPickup=?, switchCapability=?, scaleCapability=?, exchangeCapability=?, climbCapability=?, image=?, notes=? WHERE teamNumber=?", self.dumpData()[1:] + [self.teamNumber])
        database.commit()
        database.close()

    def addRobot(self):
        database = sqlite3.connect("scoutingdatabase.db") # opens database
        cursor = database.cursor() # acts as a placeholder, allows for fetchone()
        cursor.execute("SELECT * FROM pitscoutingdata WHERE teamNumber=?", (self.teamNumber,))
        if not cursor.fetchone():
            database.execute("INSERT INTO pitscoutingdata VALUES (?,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)", (self.teamNumber,))
        database.commit()
        database.close()

    def reloadRobot(self, targetBot):
        database = sqlite3.connect("scoutingdatabase.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM pitscoutingdata WHERE teamNumber=?", (targetBot,))
        robotData = cursor.fetchone()
        database.close() # no commit needed, no changes were made to the database
        if not robotData: return

        self.teamNumber = robotData[0]
        self.drivetrain = robotData[1]
        self.groundPickup = robotData[2]
        self.switchCapability = robotData[3]
        self.scaleCapability = robotData[4]
        self.exchangeCapability = robotData[5]
        self.climbCapability = robotData[6]
        self.image = robotData[7]
        self.notes = robotData[8]

def ipSave(ip):
    database = sqlite3.connect("scoutingdatabase.db")
    database.execute("UPDATE IPAddress SET ip = ?", (ip,))
    database.commit()
    database.close()
def getIp():
    database = sqlite3.connect("scoutingdatabase.db")
    cursor = database.cursor()
    cursor.execute("SELECT ip FROM IPAddress")
    return cursor.fetchone()[0]
def export(ip):
    for char in ip: # testing if the ip is an actual ip and not a word
        if not char in "1234567890.":
            self.ipInputTextHint = "wait a minute\n\nthat's not an ip???///???!?"
            self.display()
            return
    if not ip: # testing if the ip actually exists
        self.ipInputTextHint = "enter IP here"
        self.display()
        return
    try: #TIMEOUT IS IN SECONDS, NOT MILLISECONDS
        mysqldb = mysql.connector.connect(connection_timeout=1, user="jaga663", passwd="chaos", host=ip, database="Scouting2018")
    except mysql.connector.errors.InterfaceError: # thrown when timeout hits or if the ip is incorrect
        self.ipInputTextHint = "incorrect IP"
        self.display()
        return
    ipSave(ip) # from robotclass
    mysqlc = mysqldb.cursor() # mysql cursor
    sqlitedb = sqlite3.connect("scoutingdatabase.db") # sqlite database
    sqlitec = sqlitedb.cursor() # sqlite cursor
    sqlitec.execute("SELECT * FROM matchdata") # first upload all match data
    for row in sqlitec.fetchall(): # see robotclass Robot.dumpData() for order of row
        mysqlc.execute("SELECT * FROM matchdata WHERE teamNumber=%s AND roundNumber=%s AND eventName=%s", row[:3])
        if mysqlc.fetchone(): # if a row similar to the one in the mysql database exists
            print(len(row[3:] + row[:3]))
            mysqlc.execute("""
                UPDATE matchdata SET
                scouter=%s, switch=%s, scale=%s, exchange=%s, climb=%s, notes=%s,
                startingPosition=%s, attemptedSwitchSide=%s, autonSwitch=%s, autonScale=%s, autonExchange=%s
                WHERE teamNumber=%s AND roundNumber=%s AND eventName=%s
            """, row[3:] + row[:3]) # overwrite instead of make a new one
        else: # if there was no row found
            mysqlc.execute("INSERT INTO matchdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", row) # make a new row
    sqlitec.execute("SELECT * FROM pitscoutingdata")
    for pitscoutdata in sqlitec.fetchall(): # see robotclass PitRobot.dumpData() for order of row
        row = list(pitscoutdata)
        print("uploading psdata for team %s" % row[0])
        try:
            print("picture at %s" % row[7])
            row[7] = open(row[7], "rb").read()
            print(len(row[7]))
        except FileNotFoundError:
            print("unable to find file %s" % row[7])
            row[7] = "unable to find"
        except TypeError:
            print("no picture to upload")
            row[7] = "unable to find"

        mysqlc.execute("SELECT * FROM pitscoutingdata WHERE teamNumber=%s", (row[0],))
        if mysqlc.fetchone(): # if a row similar to the one in the mysql database exists
            mysqlc.execute("""
                UPDATE pitscoutingdata SET
                drivetrain=%s, groundPickup=%s, scaleCapability=%s, switchCapability=%s, exchangeCapability=%s, image=%s, notes=%s
                WHERE teamNumber=%s
            """, row[2:] + [row[0]]) # replace instead of insert
        else: # if there was no match
            mysqlc.execute("INSERT INTO pitscoutingdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", row) # insert instead of replace
    mysqldb.commit()
    mysqldb.close()
    sqlitedb.close()
