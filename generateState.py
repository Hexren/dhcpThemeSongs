#!/usr/bin/env python

from sys import argv
import os
import MySQLdb
import syslog


if __name__ == '__main__':
    syslog.syslog('Processing started')
    db = MySQLdb.connect(host="192.168.1.83", user="dhcp", passwd="sdsiuh347sdf435", db="dhcp_log")
    cur = db.cursor()
    cur.execute("SELECT DISTINCT(hw) FROM events")
    for row in cur.fetchall() :
        hw = row[0]
        foo = { "hw":hw }
        cur.execute("SELECT * FROM events WHERE hw = %(hw)s ORDER BY tm", { "hw":hw })
        
        for eventRow in cur.fetchall():   
            print eventRow
