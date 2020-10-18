#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE

HOSTS_PER_ROUTER = 2

class MyTopology(IPTopo):
   
    def build(self, *args, **kwargs):
        
        # Building stubs
        chi_1_charter = self.addHost("charter1")
        ash_1_charter = self.addHost("charter2")
        ash_1_amazon = self.addHost("amazon1")
        ash_5_amazon = self.addHost("amazon2")

        # Building New York routers
        nwk_1, nwk_5  = self.addRouters("nwk_1", "nwk_5")
        # Building Bhs routers
        bhs_g1, bhs_g2 = self.addRouters("bhs_g1", "bhs_g2")
        # Building Chicago routers
        chi_1, chi_5 = self.addRouters("chi_1", "chi_5")
        # Building Ashburn routers
        ash_1, ash_5 = self.addRouters("ash_1","ash_5")
        # Building europe's routers abstractly
        europe = self.addRouter("europe")
        # Building asia's routers abstractly
        asia = self.addRouter("asia")

        as16276_routers = [nwk_1,nwk_5,bhs_g1,bhs_g2,chi_1,chi_5,ash_1,ash_5,europe,asia]
        
        self.addAS(16276, (nwk_1,nwk_5,bhs_g1,bhs_g2,chi_1,chi_5,ash_1,ash_5,europe,asia))
        
        # Adding OSPFv3 and BGP to all routers
        for r in as16276_routers:
            r.addDaemon(OSPF6)
            r.addDaemon(BGP)

        # Adding Links  and igp_costs between all routers
        self.addLink(nwk_1,  nwk_5,  igp_cost=1)
        self.addLink(bhs_g1, bhs_g2, igp_cost=1)
        self.addLink(ash_1,  ash_5,  igp_cost=1)
        self.addLink(chi_1,  chi_5,  igp_cost=1)

        self.addLink(nwk_1,  bhs_g1, igp_cost=1)
        self.addLink(nwk_1,  ash_1,  igp_cost=1)
        self.addLink(nwk_5,  bhs_g2, igp_cost=1)
        self.addLink(nwk_5,  ash_5,  igp_cost=1)

        self.addLink(chi_1,  bhs_g1, igp_cost=3)
        self.addLink(chi_1,  ash_1,  igp_cost=3)
        self.addLink(chi_5,  bhs_g2, igp_cost=3)
        self.addLink(chi_5,  ash_5,  igp_cost=3)

        # Connecting US TO EU
        self.addLink(nwk_1,  europe, igp_cost=30)
        self.addLink(nwk_5,  europe, igp_cost=30)

        # Connection EU to AS
        self.addLink(europe, asia,   igp_cost=40)

        # Connecting US to AS
        self.addLink(asia,   ash_1,  igp_cost=50)
        self.addLink(asia,   ash_5,  igp_cost=50)
        
        # Connecting stubs
        self.addLink(chi_1_charter, chi_1)
        self.addLink(ash_1, ash_1_charter)
        self.addLink(ash_1, ash_1_amazon)
        self.addLink(ash_5, ash_5_amazon)

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