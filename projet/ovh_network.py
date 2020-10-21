#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE

HOSTS_PER_ROUTER = 2

class MyTopology(IPTopo):
   
    def build(self, *args, **kwargs):
        
        # Adding stubs to AS2 and building AS2 routers
        as2_chi_1_charter = self.addHost("charter1")
        as2_ash_1_charter = self.addHost("charter2")
        as2_ash_1_amazon = self.addHost("amazon1")
        as2_ash_5_amazon = self.addHost("amazon2")
        # Two routers needed to build an AS
        as2_r1 = self.addRouter("as2_r1")
        as2_r2 = self.addRouter("as2_r2")
        

        # Building OVH Network
        as1_host = self.addHost("as1_host") # test routers used for pingall when checking eBGP
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

        # Adding OVH AS
        as16276_routers = [nwk_1,nwk_5,bhs_g1,bhs_g2,chi_1,chi_5,ash_1,ash_5,europe,asia]
        
        # Adding OSPFv3 and BGP to OVH Network
        for r in as16276_routers:
            r.addDaemon(OSPF6)
            r.addDaemon(BGP)

        self.addAS(16276, (nwk_1,nwk_5,bhs_g1,bhs_g2,chi_1,chi_5,ash_1,ash_5,europe,asia))

        # Adding AS2 Daemons
        as2_r1.addDaemon(OSPF6)
        as2_r1.addDaemon(BGP)
        as2_r2.addDaemon(OSPF6)
        as2_r2.addDaemon(BGP)
        self.addAS(2, (as2_r1, as2_r2))
        

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
        
        # Linking router AS2 to OVH routers
        self.addLink(chi_1, as2_r1)
        self.addLink(ash_1, as2_r1)
        self.addLink(ash_5, as2_r1)
        # Linking AS2 stubs to as2 routers
        self.addLink(as2_r1, as2_r2)
        self.addLink(as2_ash_1_amazon, as2_r1)
        self.addLink(as2_chi_1_charter,as2_r1)
        self.addLink(as2_ash_5_amazon, as2_r1)
        self.addLink(as2_ash_1_charter, as2_r1)
        self.addLink(as1_host, nwk_1)

        # Setting up OVH Network Route Reflectors
        set_rr(self, rr=nwk_1, peers=[nwk_5,bhs_g1,bhs_g2,chi_1,chi_5,ash_1,ash_5,europe,asia])
        set_rr(self, rr=chi_1, peers=[nwk_1,nwk_5,bhs_g1,bhs_g2,chi_5,ash_1,ash_5,europe,asia])

        # Adding eBGP sessions between AS2 and OVH Network
        ebgp_session(self, as2_r1, chi_1)
        ebgp_session(self, as2_r1,ash_1)
        ebgp_session(self, as2_r1,ash_5)

        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=MyTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()