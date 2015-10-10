#!/usr/bin/env python
import MySQLdb
import numpy
import matplotlib.pyplot as plt

mysqlHost = "localhost"
mysqlDatabase = ""
mysqlTable = ""
mysqlUser = ""
mysqlPass = ""
fileExport = "foo.png"

def exportMatGraph():
    conn = MySQLdb.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPass, db=mysqlDatabase)
    curs = conn.cursor()
    sql = "select surge, type, DATE_FORMAT(date, '%Y-%m-%d') from " + mysqlTable + " order by date desc limit 24;"
    numrows = curs.execute(sql)
    A = numpy.fromiter(curs.fetchall(), count=numrows, dtype=('float128, a25, datetime64[D]'))

    surgeNum = tuple(A['f0'])
    date = tuple(A['f2'])

    fig, ax = plt.subplots()

    index = numpy.arange(numrows)

    bar_width = 0.3
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    plt.figure(figsize=(17,11))

    rects1 = plt.bar(index, surgeNum, bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config)

    plt.xlabel('Hours ago')
    plt.ylabel('Surge Rate')
    plt.title('UberX rates in San Franciso')
#    plt.xticks(index + bar_width, (date))
    plt.xticks(index + bar_width, (index))

    plt.tight_layout()
    plt.savefig(fileExport)
    print "Graph saved to:", fileExport


if __name__ == "__main__":
    exportMatGraph()
