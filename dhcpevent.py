#!/usr/bin/env python
#from soco import SoCo
from sys import argv
import os
import MySQLdb

if __name__ == '__main__':
        newpid = os.fork()
        
        if newpid == 0:
                db = MySQLdb.connect(host="192.168.1.83", # your host, usually localhost
                                             user="dhcp", # your username
                                              passwd="sdsiuh347sdf435", # your password
                                              db="dhcp_log") # name of the data base

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
                        data['hw'] = '' 
                cur.execute("INSERT INTO events (action, ip, hw) VALUES (%(action)s, %(ip)s, %(hw)s)", data)  
