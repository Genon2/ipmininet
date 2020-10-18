#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE

HOSTS_PER_ROUTER = 2

class MyTopology(IPTopo):
   
    def build(self, *args, **kwargs):
        
        # Adding hosts
        europe_h1 = self.addHost("eu_h1")
        asia_h1 = self.addHost("asia_h1")

        # Building New York routers
        nwk_1, nwk_5  = self.addRouter("nwk_1", "nwk_5")
        # Building Bhs routers
        bhs_g1, bhs_g2 = self.addRouters("bhs_g1", "bhs_g2")
        # Building Chicago routers
        chi_1, chi_5 = self.addRouters("chi_1", "chi_5")
        # Building Ashburn routers
        ash_1, ash_5 = self.addRouters("ash_1","ash5")
        # Building europe's routers abstractly
        europe = self.addRouter("europe")
        # Building asia's routers abstractly
        asia = self.addRouter("asia")

        # Adding Links between all routers
        self.addLink(nwk_1,  nwk_5,  igp_metric=1)
        self.addLink(bhs_g1, bhs_g2, igp_metric=1)
        self.addLink(ash_1,  ash_5,  igp_metric=1)
        self.addLink(chi_1,  chi_5,  igp_metric=1)

        self.addLink(nwk_1,  bhs_g1, igp_metric=1)
        self.addLink(nwk_1,  ash_1,  igp_metric=1)
        self.addLink(nwk_5,  bhs_g2, igp_metric=1)
        self.addLink(nwk_5,  ash_5,  igp_metric=1)

        self.addLink(chi_1,  bhs_g1, igp_metric=3)
        self.addLink(chi_1,  ash_1,  igp_metric=3)
        self.addLink(chi_5,  bhs_g2, igp_metric=3)
        self.addLink(chi_5,  ash_5,  igp_metric=3)

        # Connecting US TO EU
        self.addLink(nwk_1,  europe, igp_metric=30)
        self.addLink(nwk_5,  europe, igp_metric=30)

        # Connection EU to AS
        self.addLink(europe, asia,   igp_metric=40)

        # Connecting US to AS
        self.addLink(asia,   ash_1,  igp_metric=50)
        self.addLink(asia,   ash_5,  igp_metric=50)
        
      

        # adding OSPF6 as IGP
        nwk_1.addDaemon(OSPF6)
        nwk_5.addDaemon(OSPF6)
        bhs_g1.addDaemon(OSPF6)
        bhs_g2.addDaemon(OSPF6)
        chi_1.addDaemon(OSPF6)
        chi_5.addDaemon(OSPF6)
        ash_1.addDaemon(OSPF6)
        ash_5.addDaemon(OSPF6)
        europe.addDaemon(OSPF6)
        asia.addDaemon(OSPF6)

        nwk_1.addDaemon(BGP)
        nwk_5.addDaemon(BGP)
        bhs_g1.addDaemon(BGP)
        bhs_g2.addDaemon(BGP)
        chi_1.addDaemon(BGP)
        chi_5.addDaemon(BGP)
        ash_1.addDaemon(BGP)
        ash_5.addDaemon(BGP)
        europe.addDaemon(BGP)
        asia.addDaemon(BGP)
        
        self.addAS(16276, (nwk_1,nwk_5,bhs_g1,bhs_g2,chi_1,chi_5,ash_1,ash_5,europe,asia))
        
        set_rr(self, rr=nwk_1, peers=[nwk_5,bhs_g1,bhs_g2,chi_1,chi_5,ash_1,ash_5,europe,asia])
        set_rr(self, rr=chi_1, peers=[nwk_1,nwk_5,bhs_g1,bhs_g2,chi_5,ash_1,ash_5,europe,asia])


        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=MyTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()