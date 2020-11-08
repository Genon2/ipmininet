#!/usr/bin/env python3
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE



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
        nwk_1 = self.addRouter("nwk_1", lo_addresses=["2042:8::1/64", "10.8.1.1/24"])
        nwk_5 = self.addRouter("nwk_5", lo_addresses=["2042:9::1/64", "10.9.1.1/24"])
        # Building Bhs routers
        bhs_g1 = self.addRouter("bhs_g1", lo_addresses=["2042:7::1/64", "10.7.1.1/24"])
        bhs_g2 = self.addRouter("bhs_g2", lo_addresses=["2042:10::1/64", "10.10.1.1/24"])
        # Building Chicago routers
        chi_1 = self.addRouter("chi_1", lo_addresses=["2042:5::1/64", "10.5.1.1/24"])
        chi_5 = self.addRouter("chi_5", lo_addresses=["2042:6::1/64", "10.6.1.1/24"])
        # Building Ashburn routers
        ash_1 = self.addRouter("ash_1", lo_addresses=["2042:3::1/64", "10.3.1.1/24"])
        ash_5 = self.addRouter("ash_5", lo_addresses=["2042:4::1/64", "10.4.1.1/24"])
        # Building europe's routers abstractly
        europe = self.addRouter("europe", lo_addresses=["2042:1::1/64", "10.1.1.1/24"])
        # Building asia's routers abstractly
        asia = self.addRouter("asia", lo_addresses=["2042:2::1/64", "10.2.1.1/24"])

        routers = self.routers()
        prefix = {routers[i]: '2001:100:%04x::/48' % i
                  for i in range(len(routers))}
        nwk_1.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[nwk_1],)),))
        nwk_5.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[nwk_5],)),))
        bhs_g1.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[bhs_g1],)),))
        bhs_g2.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[bhs_g2],)),))
        chi_1.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[chi_1],)),))
        chi_5.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[chi_5],)),))
        ash_1.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[ash_1],)),))
        ash_5.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[ash_5],)),))
        europe.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[europe],)),))
        asia.addDaemon(BGP,
                       address_families=(AF_INET6(networks=(prefix[asia],)),))

        # Adding Links  and igp_costs between OVH routers and ip local adress ipv6
        las1 = self.addLink(nwk_1,  nwk_5,  igp_cost=1)
        las1[nwk_1].addParams(ip=("2001:01::1/64",))
        las1[nwk_5].addParams(ip=("2001:06::1/64",))
        las2 = self.addLink(bhs_g1, bhs_g2, igp_cost=1)
        las2[bhs_g1].addParams(ip=("2001:02::1/64",))
        las2[bhs_g2].addParams(ip=("2001:07::1/64",))
        las3 = self.addLink(ash_1,  ash_5,  igp_cost=1)
        las3[ash_1].addParams(ip=("2001:03::1/64",))
        las3[ash_5].addParams(ip=("2001:08::1/64",))
        las4 = self.addLink(chi_1,  chi_5,  igp_cost=1)
        las4[chi_1].addParams(ip=("2001:04::1/64",))
        las4[chi_5].addParams(ip=("2001:09::1/64",))

        las11 = self.addLink(nwk_1,  bhs_g1, igp_cost=1)
        las11[nwk_1].addParams(ip=("2001:01::2/64",))
        las11[bhs_g1].addParams(ip=("2001:02::2/64",))
        las12 = self.addLink(nwk_1,  ash_1,  igp_cost=1)
        las12[nwk_1].addParams(ip=("2001:01::3/64",))
        las12[ash_1].addParams(ip=("2001:03::2/64",))
        las13 = self.addLink(nwk_5,  bhs_g2, igp_cost=1)
        las13[nwk_5].addParams(ip=("2001:06::2/64",))
        las13[bhs_g2].addParams(ip=("2001:07::2/64",))
        las14 = self.addLink(nwk_5,  ash_5,  igp_cost=1)
        las14[nwk_5].addParams(ip=("2001:06::5/64",))
        las14[ash_5].addParams(ip=("2001:08::2/64",))

        las41 = self.addLink(chi_1,  bhs_g1, igp_cost=3)
        las41[chi_1].addParams(ip=("2001:04::2/64",))
        las41[bhs_g1].addParams(ip=("2001:02::3/64",))
        las42 = self.addLink(chi_1,  ash_1,  igp_cost=3)
        las42[chi_1].addParams(ip=("2001:04::3/64",))
        las42[ash_1].addParams(ip=("2001:03::3/64",))
        las43 = self.addLink(chi_5,  bhs_g2, igp_cost=3)
        las43[chi_5].addParams(ip=("2001:09::2/64",))
        las43[bhs_g2].addParams(ip=("2001:07::3/64",))
        las44 = self.addLink(chi_5,  ash_5,  igp_cost=3)
        las44[chi_5].addParams(ip=("2001:09::3/64",))
        las44[ash_5].addParams(ip=("2001:08::3/64",))
        # Connecting US TO EU
        las15 = self.addLink(nwk_1,  europe, igp_cost=30)
        las15[nwk_1].addParams(ip=("2001:01::4/64",))
        las15[europe].addParams(ip=("2001:05::2/64",))
        las16 = self.addLink(nwk_5,  europe, igp_cost=30)
        las16[nwk_5].addParams(ip=("2001:06::3/64",))
        las16[europe].addParams(ip=("2001:05::3/64",))
        # Connection EU to AS
        las5 =  self.addLink(europe, asia,   igp_cost=40)
        las5[europe].addParams(ip=("2001:05::1/64",))
        las5[asia].addParams(ip=("2001:10::1/64",))
        # Connecting US to AS
        las51 = self.addLink(asia,   chi_1,  igp_cost=50)
        las51[chi_1].addParams(ip=("2001:03::4/64",))
        las51[asia].addParams(ip=("2001:10::2/64",))
        las52 = self.addLink(asia,   chi_5,  igp_cost=50)
        las52[chi_5].addParams(ip=("2001:08::3/64",))
        las52[asia].addParams(ip=("2001:10::3/64",))
        las53 = self.addLink(as1_host, nwk_1)  # Host used for tests

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

        # Building AS16509 (AMAZON)
        as16509_ash_1_amazon = self.addHost("amazon_1")
        as16509_ash_5_amazon = self.addHost("amazon_2")
        #Routers + loopback
        as16509_r1 = self.addRouter("as16509_r1", lo_addresses=["2043:1::1/64", "11.1.1.1/24"])
        as16509_r2 = self.addRouter("as16509_r2", lo_addresses=["2043:2::1/64", "11.2.1.1/24"])
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
        lam1 = self.addLink(as16509_r1, ash_1)
        lam1[as16509_r1].addParams(ip=("2001:13::1/64",))
        lam1[ash_1].addParams(ip=("2001:03::7/64",))
        lam2 = self.addLink(as16509_r1, ash_5)
        lam2[as16509_r1].addParams(ip=("2001:14::1/64",))
        lam2[ash_5].addParams(ip=("2001:08::5/64",))
        lam3 = self.addLink(as16509_r2, ash_1)
        lam3[as16509_r2].addParams(ip=("2001:13::2/64",))
        lam3[ash_1].addParams(ip=("2001:03::7/64",))
        lam4 = self.addLink(as16509_r2, ash_5)
        lam4[as16509_r2].addParams(ip=("2001:14::2/64",))
        lam4[ash_5].addParams(ip=("2001:08::6/64",))
        ebgp_session(self, as16509_r1, ash_1, link_type=SHARE)
        #ebgp_session(self, as16509_r1, ash_5, link_type=SHARE)
        ebgp_session(self, as16509_r2, ash_1, link_type=SHARE)
        #ebgp_session(self, as16509_r2, ash_5, link_type=SHARE)


        # Building as7843 (CHARTER) , routers and links
        as7843_chi_1_charter = self.addHost("charter_1")
        as7843_ash_1_charter = self.addHost("charter_2")
        #Routers + loopback
        as7843_r1 = self.addRouter("as7843_r1", lo_addresses=["2044:1::1/64", "12.1.1.1/24"])
        as7843_r2 = self.addRouter("as7843_r2", lo_addresses=["2044:2::1/64", "12.2.1.1/24"])
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
        lach1 = self.addLink(as7843_r1, chi_1)
        lach1[as7843_r1].addParams(ip=("2001:11::1/64",))
        lach1[chi_1].addParams(ip=("2001:04::4/64",))
        lach2 = self.addLink(as7843_r1, ash_1)
        lach2[as7843_r1].addParams(ip=("2001:11::2/64",))
        lach2[ash_1].addParams(ip=("2001:03::5/64",))
        lach3 = self.addLink(as7843_r2, chi_1)
        lach3[as7843_r2].addParams(ip=("2001:12::1/64",))
        lach3[chi_1].addParams(ip=("2001:04::5/64",))
        lach4 = self.addLink(as7843_r2, ash_1)
        lach4[as7843_r2].addParams(ip=("2001:12::2/64",))
        lach4[ash_1].addParams(ip=("2001:03::6/64",))
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
        #Routers + loopback
        as1299_r1 = self.addRouter("as1299_r1", lo_addresses=["2045:1::1/64", "13.1.1.1/24"])
        as1299_r2 = self.addRouter("as1299_r2", lo_addresses=["2045:2::1/64", "13.2.1.1/24"])
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
        #Routers + loopback
        as174_r1 = self.addRouter("as174_r1", lo_addresses=["2046:1::1/64", "14.1.1.1/24"])
        as174_r2 = self.addRouter("as174_r2", lo_addresses=["2046:2::1/64", "14.2.1.1/24"])
        # Added links
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
        #Routers + loopback
        as3356_r1 = self.addRouter("as3356_r1", lo_addresses=["2047:1::1/64", "15.1.1.1/24"])
        as3356_r2 = self.addRouter("as3356_r2", lo_addresses=["2047:2::1/64", "15.2.1.1/24"])
        # Added links
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