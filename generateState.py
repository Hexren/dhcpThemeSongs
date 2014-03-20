#!/usr/bin/env python

from sys import argv
import os
import MySQLdb
import syslog

#add hardware address from last commit
def updateState( hw, cur):
    try:
        cur.execute("SELECT action, ip, tm FROM events WHERE hw = %(hw)s ORDER BY tm desc limit 1", { "hw":hw })
        eventRow = cur.fetchone()  
        ip = eventRow[1] 
        tm = eventRow[2]
        if eventRow[0] == 'commit':
            state = 'online'
        elif eventRow[0] == 'remove':
            state = 'tentatively offline'
        cur.execute("DELETE FROM state WHERE hw = %(hw)s", { "hw":hw })
        cur.execute("INSERT INTO state (hw, state, lastIp, lastSeen) VALUES (%(hw)s, %(state)s, %(ip)s, %(tm)s)", { "hw":hw, "state" : state, "ip" : ip, "tm": tm })
        #cur.execute("DELETE FROM events WHERE hw = %(hw)s", { "hw":hw })
    
    except MySQLdb.Error, e:
        try:
			syslog.syslog(syslog.LOG_ERR, "MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        except IndexError:
            syslog.syslog(syslog.LOG_ERR, "MySQL Error: %s" % str(e))

def ping(ip):
    response = os.system("ping -c 1 " + ip)
    if response == 0:
        syslog.syslog(ip + ' is up')
        return True;
    else:
        syslog.syslog(ip + ' is down')
        return False;


def testSetOffline(ip):
    if not ping(ip):
            cur.execute("UPDATE state SET state = 'offline' WHERE lastIp = %(ip)s", {"ip" : ip}) 

if __name__ == '__main__':
    syslog.syslog('Processing started')
    db = MySQLdb.connect(host="192.168.1.83", user="dhcp", passwd="sdsiuh347sdf435", db="dhcp_log")
    cur = db.cursor()
    cur.execute("SELECT DISTINCT(hw) FROM events")
    for row in cur.fetchall():
        syslog.syslog('Working on:' + row[0])
        hw = row[0]
        updateState(hw, cur)

    cur.execute("SELECT lastIp FROM state WHERE state = 'tentatively offline' AND lastSeen < (NOW() - INTERVAL 5 HOUR)")
    for row in cur.fetchall():
        ip = row[0]
        testSetOffline(ip)
        

    
