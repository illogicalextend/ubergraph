#!/usr/bin/env python

import requests
import geopy
from datetime import datetime
import time
import MySQLdb

mysqlHost = "localhost"
mysqlDatabase = ""
mysqlTable = ""
mysqlUser = ""
mysqlPass = ""
# uber api token
uberToken = "" 

def main():
    userarea = getgeo()
    print userarea

    url = 'https://api.uber.com/v1/estimates/price'

    parameters = {
        "server_token": uberToken,
        "start_latitude": userarea.latitude,
        "start_longitude": userarea.longitude,
        "end_latitude": userarea.latitude,
        "end_longitude": userarea.longitude,
    }

    response = requests.get(url, params=parameters)
    data = response.json()
    prices = data['prices']

    for service in range(0, len(prices)):
        displayName = prices[service]['display_name']
        surgeMultiplier = prices[service]['surge_multiplier']
        #writeMysql(displayName, surgeMultiplier)

        # write uberx to uberx table
        if displayName == "uberX":
            writeUberxMysql(displayName, surgeMultiplier)

#    savedata(userarea.latitude, userarea.longitude)

def getgeo():
    while True:
        try:
            geolocator = geopy.Nominatim()
            #location = geolocator.geocode(raw_input("Enter a location: \n"))
            # hard code location for testing
            location = geolocator.geocode("market street san francisco")
            break
        except:
            print "Connection to geolocator timed out. Trying again.."
            time.sleep(3)
    return location

def savedata(lat, longi):
    f = open('data.txt', 'a')
    f.write(datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + str(lat) + str(longi) +  "\n")

def writeUberxMysql(fareType, surge):
    db = MySQLdb.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPass, db=mysqlDatabase)
    cur = db.cursor()
    print "Current surge rate for " + str(fareType) + " is " + str(surge)
    sql = "insert into " + mysqlTable + " (type, date, surge) values('%s', now(), '%s')" % (fareType, surge)
    cur.execute(sql)
    db.commit()
    for row in cur.fetchall():
        print row[0]



if __name__ == "__main__":
    main()
