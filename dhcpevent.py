#!/usr/bin/env python

from sys import argv
import os
import MySQLdb
import syslog

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
			
	



if __name__ == '__main__':
        syslog.syslog('Processing started')
        newpid = os.fork()
        if newpid == 0:
				#from soco import SoCo
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

	
