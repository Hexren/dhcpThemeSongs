#!/usr/bin/env python

from sys import argv
#import os
import syslog
from soco import SoCo

#beware of isc dhcp number conversion 'd0:22:be:20:05:e6' becomes 'd0:22:be:20:5:e6', without leading zeroes
themes = {
    'ttwt': 'http://www.synthesisradio.com/dailyguru/TTWT.mp3',
    'closer': 'x-file-cifs://giselnas/music/FLAC/Kings%20Of%20Leon/Only%20By%20The%20Night/Kings%20Of%20Leon%20-%2001%20-%20Closer.flac'
}

#should be discovered by name
wohnzimmer = '192.168.1.129';
atrium = '192.168.1.135'
wc = '192.168.1.162'
sonosPlayer = wc
	
def playTheme(themes, sonosPlayer):
    sonos = SoCo(sonosPlayer)
    #syslog.syslog('%s' % str(sonos.get_current_track_info()))
    #return '';
    if playerPlays(sonos):
        syslog.syslog('Already playing')
        return '';
    sonos.unjoin()
    sonos.clear_queue()
    sonos.add_uri_to_queue(themes['closer'])
    sonos.play_mode = 'REPEAT_ALL'
    syslog.syslog('%s' % sonos.play_mode)
    sonos.volume = 5;    
    if playerPlays(sonos):
        return '';    
    sonos.play()
    syslog.syslog('Playing Closer')
   
def playerPlays(sonos):
    return sonos.get_current_transport_info()['current_transport_state'] == 'PLAYING'    


if __name__ == '__main__':
        syslog.syslog('Closer starting script')
        playTheme(themes, sonosPlayer) 

	
