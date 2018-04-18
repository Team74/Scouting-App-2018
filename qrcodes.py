import pyqrcode
import qrcode
from qrcode.image import svg
import sqlite3

db = sqlite3.connect("scoutingdatabase.db")
c = db.cursor()

#URL is http://a.hostx7.com/?a=RRRTTTTDPALHvv^^EE&b=
#where
# RRR is round number
# TTTT is team number
# D is whether they drove forward or not
# P is what position they started in
# A is which switch side they attempted
# L is the number of cubes put in the switch in auton
# H is the number of cubes put in the scale in auton
# vv is the number of cubes put in the switch in teleop
# ^^ is the number of cubes put in the scale in teleop
# EE is the number of cubes put in the exchange in teleop

def generateQR(roundNumber, rounds):
    print("roundNumber %s, rounds %s" % (roundNumber, rounds))
    lastFive = c.execute("SELECT * FROM matchdata WHERE roundNumber>? AND roundNumber<=?", (roundNumber-rounds, roundNumber))
    urlData = []
    for robot in lastFive:
        roundNum = "%03d" % int(robot[1]) if int(robot[1]) <= 999 else 999
        teamNum = "%04d" % int(robot[0]) if int(robot[0]) <= 9999 else 9999
        forward = str(0) #str(robot[15])
        startPos = robot[9][0] # first letter of string
        switchSide = robot[10][0] # ^
        switchA = str(robot[11]) if int(robot[11])<= 9 else "9"
        scaleA = str(robot[12]) if int(robot[12])<=9 else "9"
        switch = "%02d" % int(robot[4]) if int(robot[4])<=99 else 99
        scale = "%02d" % int(robot[5]) if int(robot[5])<=99 else 99
        exchange = str(robot[6]) if int(robot[6])<=9 else "9"
        urlData.append(roundNum+teamNum+forward+startPos+switchSide+switchA+scaleA+switch+scale)
    fullURL = "http://a.hostx7.com/?a[]=" + "&a[]=".join(urlData)

    qr = pyqrcode.create(fullURL)
    #qr.png("url.png", scale=5)
    qr.svg("url.svg", scale=1, background="white")
    options = {
      "input": "url.svg",
      "output": "url.svg",
      "width": "100",
      "height": "100"
    }
    svgresize.process_stream(options)
    return qr.text()

def generateRealQR(roundNumber, rounds):
    print("roundNumber %s, rounds %s" % (roundNumber, rounds))
    lastFive = c.execute("SELECT * FROM matchdata WHERE roundNumber>? AND roundNumber<=?", (roundNumber-rounds, roundNumber))
    urlData = []
    for robot in lastFive:
        roundNum = "%03d" % int(robot[1]) if int(robot[1]) <= 999 else 999
        teamNum = "%04d" % int(robot[0]) if int(robot[0]) <= 9999 else 9999
        forward = str(0) #str(robot[15])
        startPos = robot[9][0] # first letter of string
        switchSide = robot[10][0] # ^
        switchA = str(robot[11]) if int(robot[11])<= 9 else "9"
        scaleA = str(robot[12]) if int(robot[12])<=9 else "9"
        switch = "%02d" % int(robot[4]) if int(robot[4])<=99 else 99
        scale = "%02d" % int(robot[5]) if int(robot[5])<=99 else 99
        exchange = str(robot[6]) if int(robot[6])<=9 else "9"
        urlData.append(roundNum+teamNum+forward+startPos+switchSide+switchA+scaleA+switch+scale)
    fullURL = "http://a.hostx7.com/?a[]=" + "&a[]=".join(urlData)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(fullURL)
    img = qrcode.make(fullURL, image_factory=svg.SvgPathFillImage)

    img.save("url.svg")

if __name__ == "__main__":
    generateQR(63, 20)
