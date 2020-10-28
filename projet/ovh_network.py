#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE

HOSTS_PER_ROUTER = 2


class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        # # Adding stubs to AS2 and building AS2 routers
        # as2_chi_1_charter = self.addHost("charter_1")
        # as2_ash_1_charter = self.addHost("charter_2")
        # as2_ash_1_amazon = self.addHost("amazon_1")
        # as2_ash_5_amazon = self.addHost("amazon_2")
        # # Two routers needed to build an AS

        # Building OVH Network
        # test routers used for pingall when checking eBGP
        as1_host = self.addHost("as1_host")
        # Building New York routers
        nwk_1, nwk_5 = self.addRouters("nwk_1", "nwk_5")
        # Building Bhs routers
        bhs_g1, bhs_g2 = self.addRouters("bhs_g1", "bhs_g2")
        # Building Chicago routers
        chi_1, chi_5 = self.addRouters("chi_1", "chi_5")
        # Building Ashburn routers
        ash_1, ash_5 = self.addRouters("ash_1", "ash_5")
        # Building europe's routers abstractly
        europe = self.addRouter("europe")
        # Building asia's routers abstractly
        asia = self.addRouter("asia")

        # Adding Links  and igp_costs between OVH routers
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
        self.addLink(as1_host, nwk_1)  # Host used for tests

        # Adding OVH AS
        as16276_routers = [nwk_1, nwk_5, bhs_g1, bhs_g2,
                           chi_1, chi_5, ash_1, ash_5, europe, asia]

        # Adding OSPFv3 and BGP to OVH Network
        for r in as16276_routers:
            r.addDaemon(OSPF6)
            r.addDaemon(BGP)

        self.addAS(16276, (nwk_1, nwk_5, bhs_g1, bhs_g2,
                           chi_1, chi_5, ash_1, ash_5, europe, asia))
        # Setting up OVH Network Route Reflectors
        set_rr(self, rr=nwk_1, peers=[
               nwk_5, bhs_g1, bhs_g2, chi_1, chi_5, ash_1, ash_5, europe, asia])
        set_rr(self, rr=chi_1, peers=[
               nwk_1, nwk_5, bhs_g1, bhs_g2, chi_5, ash_1, ash_5, europe, asia])


        #############################################################
        #                                                           #
        #              STUB                                         #
        #                                                           #
        #############################################################

        # Building AS16509 (AMAZON) , routers and links
        as16509_ash_1_amazon = self.addHost("amazon_1")
        as16509_ash_5_amazon = self.addHost("amazon_2")
        as16509_r1, as16509_r2 = self.addRouters("as16509_r1", "as16509_r2")
        # Linking AS16509 (AMAZON) to its router
        self.addLink(as16509_ash_1_amazon, as16509_r1)
        self.addLink(as16509_ash_5_amazon, as16509_r1)
        self.addLink(as16509_r1, as16509_r2)
        as16509_r1.addDaemon(OSPF6)
        as16509_r1.addDaemon(BGP)
        as16509_r2.addDaemon(OSPF6)
        as16509_r2.addDaemon(BGP)
        self.addAS(16509, (as16509_r1, as16509_r2))
        # Building physical links between AS16509 (AMAZON) and OVH
        self.addLink(as16509_r1, ash_1)
        self.addLink(as16509_r1, ash_5)
        self.addLink(as16509_r2, ash_1)
        self.addLink(as16509_r2, ash_5)
        ebgp_session(self, as16509_r1, ash_1, link_type=SHARE)
        #ebgp_session(self, as16509_r1, ash_5, link_type=SHARE)
        ebgp_session(self, as16509_r2, ash_1, link_type=SHARE)
        #ebgp_session(self, as16509_r2, ash_5, link_type=SHARE)


        # Building as7843 (CHARTER) , routers and links
        as7843_chi_1_charter = self.addHost("charter_1")
        as7843_ash_1_charter = self.addHost("charter_2")
        as7843_r1, as7843_r2 = self.addRouters("as7843_r1", "as7843_r2")
        # Linking as7843 (CHARTER) to its router
        self.addLink(as7843_chi_1_charter, as7843_r1)
        self.addLink(as7843_ash_1_charter, as7843_r1)
        self.addLink(as7843_r1, as7843_r2)
        as7843_r1.addDaemon(OSPF6)
        as7843_r1.addDaemon(BGP)
        as7843_r2.addDaemon(OSPF6)
        as7843_r2.addDaemon(BGP)
        self.addAS(7843, (as7843_r1, as7843_r2))
        # Building physical links between as7843 (CHARTER) and OVH
        self.addLink(as7843_r1, chi_1)
        self.addLink(as7843_r1, ash_1)
        self.addLink(as7843_r2, chi_1)
        self.addLink(as7843_r2, ash_1)
        ebgp_session(self, as7843_r1, chi_1, link_type=SHARE)
        #ebgp_session(self, as7843_r1, ash_1, link_type=SHARE)
        #ebgp_session(self, as7843_r2, chi_1, link_type=SHARE)
        ebgp_session(self, as7843_r2, ash_1, link_type=SHARE)

        #############################################################
        #                                                           #
        #              TRANSIT                                      #
        #                                                           #
        #############################################################

        # Building AS1299 (TElIA) , routers and links
        as1299_nwk_1_telia = self.addHost("telia_1")
        as1299_nwk_5_telia = self.addHost("telia_2")
        as1299_chi_5_telia = self.addHost("telia_3")
        as1299_ash_5_telia = self.addHost("telia_4")
        as1299_r1, as1299_r2 = self.addRouters("as1299_r1", "as1299_r2")
        # Linking AS1299 (TElIA) to its router
        self.addLink(as1299_nwk_1_telia, as1299_r1)
        self.addLink(as1299_nwk_5_telia, as1299_r1)
        self.addLink(as1299_chi_5_telia, as1299_r2)
        self.addLink(as1299_ash_5_telia, as1299_r2)
        self.addLink(as1299_r1, as1299_r2)
        as1299_r1.addDaemon(OSPF6)
        as1299_r1.addDaemon(BGP)
        as1299_r2.addDaemon(OSPF6)
        as1299_r2.addDaemon(BGP)
        self.addAS(1299, (as1299_r1, as1299_r2))
        # Building physical links between AS1299 (TElIA) and OVH
        self.addLink(as1299_r1, nwk_1)
        self.addLink(as1299_r1, nwk_5)
        self.addLink(as1299_r2, chi_5)
        self.addLink(as1299_r2, ash_5)
        # Remarque : ebgp fonctionne avec 3 n'importe lequels mais
        # dès qu'on actve 4 sessions, problème dans les ping. Aucun échange eBGP.
        # host 1 ne sait pas contacter telia et inversement
        # Je commente un nwk_5 car il y a dejà une session eBGP avec nwk_1
        ebgp_session(self, as1299_r1, nwk_1, link_type=SHARE)
        # ebgp_session(self, as1299_r1, nwk_5, link_type=SHARE)
        ebgp_session(self, as1299_r2, chi_5, link_type=SHARE)
        ebgp_session(self, as1299_r2, ash_5, link_type=SHARE)

        # Building AS174 (Cogent) , routers and links
        as174_nwk_1_cogent = self.addHost("cogent_1")
        as174_nwk_5_cogent = self.addHost("cogent_2")
        as174_chi_1_cogent = self.addHost("cogent_3")
        as174_chi_5_cogent = self.addHost("cogent_4")
        as174_ash_1_cogent = self.addHost("cogent_5")
        as174_ash_5_cogent = self.addHost("cogent_6")
        as174_r1, as174_r2 = self.addRouters("as174_r1", "as174_r2")
        self.addLink(as174_nwk_1_cogent, as174_r1)
        self.addLink(as174_nwk_5_cogent, as174_r1)
        self.addLink(as174_chi_1_cogent, as174_r1)
        self.addLink(as174_chi_5_cogent, as174_r1)
        self.addLink(as174_ash_1_cogent, as174_r2)
        self.addLink(as174_ash_5_cogent, as174_r2)
        self.addLink(as174_r1, as174_r2)
        as174_routers = [as174_r1, as174_r2]
        # Adding OSPFv3 and BGP to AS174 (Cogent)
        for r in as174_routers:
            r.addDaemon(OSPF6)
            r.addDaemon(BGP)

        self.addAS(174, (as174_r1, as174_r2))
        self.addLinks((as174_r1,nwk_1),
                      (as174_r1,nwk_5),
                      (as174_r1,chi_1),
                      (as174_r1,chi_5),
                      (as174_r2,ash_1),
                      (as174_r2,ash_5))
        # Added an eBGP session for each datacenter region for redundancy
        ebgp_session(self, as174_r1, nwk_1, link_type=SHARE)
        ebgp_session(self, as174_r1, chi_1, link_type=SHARE)
        ebgp_session(self, as174_r2, ash_1, link_type=SHARE)

        # Building AS3356 (Level3), routers and links
        as3356_nwk_1_level3 = self.addHost("level3_1")
        as3356_nwk_5_level3 = self.addHost("level3_2")
        as3356_chi_1_level3 = self.addHost("level3_3")
        as3356_chi_5_level3 = self.addHost("level3_4")
        as3356_r1, as3356_r2 = self.addRouters("as3356_r1", "as3356_r2")
        self.addLink(as3356_nwk_5_level3, as3356_r1)
        self.addLink(as3356_nwk_1_level3, as3356_r1)
        self.addLink(as3356_chi_1_level3, as3356_r2)
        self.addLink(as3356_chi_5_level3, as3356_r2)
        self.addLink(as3356_r1, as3356_r2)
        as3356_routers = [as3356_r1, as3356_r2]
        # Adding OSPFv3 and BGP to AS174 (Cogent)
        for r in as3356_routers:
            r.addDaemon(OSPF6)
            r.addDaemon(BGP)
        
        self.addAS(3356, (as3356_r1, as3356_r2))
        self.addLinks((as3356_r1,nwk_1),
                      (as3356_r1,nwk_5),
                      (as3356_r2,chi_1),
                      (as3356_r2,chi_5))
        # Added an eBGP session for each datacenter region for redundancy
        ebgp_session(self, as3356_r1, nwk_1, link_type=SHARE)
        ebgp_session(self, as3356_r2, chi_1, link_type=SHARE)

        # # Linking AS2 stubs to as2 routers
        # self.addLink(as2_r1, as2_r2)
        # self.addLink(as2_ash_1_amazon, as2_r1)
        # self.addLink(as2_chi_1_charter, as2_r1)
        # self.addLink(as2_ash_5_amazon, as2_r1)
        # self.addLink(as2_ash_1_charter, as2_r1)

        

        # # Adding eBGP sessions between AS2 and OVH Network
        # ebgp_session(self, as2_r1, chi_1, link_type=SHARE)
        # ebgp_session(self, as2_r1, nwk_1, link_type=SHARE)


        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=MyTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
