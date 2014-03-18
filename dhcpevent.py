#!/usr/bin/env python

from sys import argv
import os
import MySQLdb
import syslog


themes = {
    'bc:f5:ac:f6:2d:46': 'http://eric.hernandez3.free.fr/VOX/VOX/bruitage%203/TV%20&%20Movie%20Themes%20-%20Star%20Wars%20-%20Imperial%20March.mp3'
}

#should be discovered by name
sonosPlayer = '192.168.1.129'

#add hardware address from last commit
def addHw(data, cur):
    try:
        cur.execute("SELECT hw FROM events WHERE action = 'commit' AND ip = %(ip)s ORDER BY tm ASC LIMIT 1", data)
        if cur.rowcount > 0:
            row = cur.fetchone()
            return row[0]
        else:
            return ''
    except MySQLdb.Error, e:
        try:
			syslog.syslog(syslog.LOG_ERR, "MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        except IndexError:
            syslog.syslog(syslog.LOG_ERR, "MySQL Error: %s" % str(e))
    exit(233)

#add hardware address from last commit
def getLastAction(data, cur):
    try:
        cur.execute("select action from events where ip = %(ip)s and hw = %(hw)s order by tm desc limit 1,1", data)
        if cur.rowcount > 0:
            row = cur.fetchone()
            return row[0]
        else:
            return ''
    except MySQLdb.Error, e:
        try:
			syslog.syslog(syslog.LOG_ERR, "MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        except IndexError:
            syslog.syslog(syslog.LOG_ERR, "MySQL Error: %s" % str(e))
    exit(233)

			
	
def playTheme(data, cur, themes, sonosPlayer):
    if data['hw'] in themes.keys() and getLastAction(data, cur) == 'remove':
        from soco import SoCo
        sonos = SoCo(sonosPlayer)
        sonos.play_uri(themes[data['hw']])
        sonos.play()




if __name__ == '__main__':
        syslog.syslog('Processing started')
        newpid = os.fork()
        if newpid == 0:
                db = MySQLdb.connect(host="192.168.1.83", user="dhcp", passwd="sdsiuh347sdf435", db="dhcp_log")

                # you must create a Cursor object. It will let
                #  you execute all the queries you need
                cur = db.cursor()
                data = {
                        'action' : argv[1],
                        'ip' : argv[2]
                }
                if len(argv) >= 4:
                        data['hw'] = argv[3] 
                else:
                        data['hw'] = addHw(data, cur) 
                cur.execute("INSERT INTO events (action, ip, hw) VALUES (%(action)s, %(ip)s, %(hw)s)", data) 
                playTheme(data, cur, themes, sonosPlayer) 

	
