dhcpThemeSongs
==============

Connecting isc dhcp to sonos for theme songs on entering a flat

dependencies
============
[SoCo/SoCo](https://github.com/SoCo/SoCo) should be installed


add dhcp hooks
===============

    on commit {
      set clip = binary-to-ascii(10, 8, ".", leased-address);
      set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
      execute("/usr/local/sbin/dhcpevent", "commit", clip, clhw);
    }

    on release {
  
                          set clip = binary-to-ascii(10, 8, ".", leased-address);
                          set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
                          execute("/usr/local/sbin/dhcpevent", "remove", clip, clhw);
  
                  }

    on expiry {
                        set clip = binary-to-ascii(10, 8, ".", leased-address);
                        if(exists agent.remote-id) {

                                set clhw = binary-to-ascii(16, 8, ":", substring(option agent.remote-id, 2, 6));
                                execute("/usr/local/sbin/dhcpevent", "remove", clip, clhw);

                        } else {

                                set clhw = "";
                                execute("/usr/local/sbin/dhcpevent", "remove", clip);

                        }

  
    }
