#!/usr/bin/env python

from sys import argv
import os
import MySQLdb
import syslog

#beware of isc dhcp number conversion 'd0:22:be:20:05:e6' becomes 'd0:22:be:20:5:e6', without leading zeroes
themes = {
    'bc:f5:ac:f6:2d:46': 'http://eric.hernandez3.free.fr/VOX/VOX/bruitage%203/TV%20&%20Movie%20Themes%20-%20Star%20Wars%20-%20Imperial%20March.mp3',
    'd0:22:be:20:5:e6': 'http://www.synthesisradio.com/dailyguru/TTWT.mp3',
    '8c:3a:e3:92:5f:bf' : 'http://strom.on.masendav.org/stuff/Carl%20Orff%20-%20Carmina%20Burana%20-%20O%20Fortuna%20%28Edited%20by%20Strom%29.mp3'
}

#should be discovered by name
wohnzimmer = '192.168.1.129';
atrium = '192.168.1.132'
sonosPlayer = atrium

#add hardware address from last commit
def addHw(data, cur):
    try:
        cur.execute("SELECT hw FROM events WHERE action = 'commit' AND ip = %(ip)s ORDER BY tm DESC LIMIT 1", data)
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

#gets last action before the one just inserted
def getLastAction(data, cur):
    try:
        cur.execute("select action from events where hw = %(hw)s order by tm desc limit 1,1", data)
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
        if sonos.get_current_transport_info() == 'PLAYING':
            return '';
        sonos.unjoin();
        sonos.play_uri(themes[data['hw']])
        sonos.volume = 20;
        if sonos.get_current_transport_info() == 'PLAYING':
            return '';    
        sonos.play()
        syslog.syslog('Playing theme for: ' + data['hw'])
        


if __name__ == '__main__':
        syslog.syslog('Processing started')
        newpid = os.fork()
        if newpid == 0:
                db = MySQLdb.connect(host="192.168.1.83", user="dhcp", passwd="sdsiuh347sdf435", db="dhcp_log")

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

	
