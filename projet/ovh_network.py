#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE, OSPF6, RouterConfig, AccessList, CommunityList


class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        # Building OVH Network
        # test routers used for pingall when checking eBGP
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
                        address_families=(AF_INET6(networks=(prefix[nwk_1],('2001:3c::/64'))),),
                        routerid='1.1.1.1')
        nwk_5.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[nwk_5],)),),
                        routerid='1.1.1.2')
        bhs_g1.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[bhs_g1],)),),
                        routerid='1.1.1.3')
        bhs_g2.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[bhs_g2],)),),
                        routerid='1.1.1.4')
        chi_1.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[chi_1],)),),
                        routerid='1.1.1.5')
        chi_5.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[chi_5],)),),
                        routerid='1.1.1.6')
        ash_1.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[ash_1],)),),
                        routerid='1.1.1.7')
        ash_5.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[ash_5],)),),
                        routerid='1.1.1.8')
        europe.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[europe],('2001:3c::/64'))),),
                        routerid='1.1.2.9')
        asia.addDaemon(BGP,
                        address_families=(AF_INET6(networks=(prefix[asia],('2001:3c::/64'))),),
                        routerid='1.1.3.10')

        # Adding Links  and igp_metrics between OVH routers and ip local adress ipv6
        las1 = self.addLink(nwk_1,  nwk_5)
        las1[nwk_1].addParams(ip4=("192.168.0.0/24"), ip6=("2001:01::1/64",))
        las1[nwk_5].addParams(ip4=("192.168.1.0/24"), ip6=("2001:06::1/64",))
        las2 = self.addLink(bhs_g1, bhs_g2)
        las2[bhs_g1].addParams(ip4=("192.168.2.0/24"), ip6=("2001:02::1/64",))
        las2[bhs_g2].addParams(ip4=("192.168.3.0/24"), ip6=("2001:07::1/64",))
        las3 = self.addLink(ash_1,  ash_5)
        las3[ash_1].addParams(ip4=("192.168.4.0/24"), ip6=("2001:03::1/64",))
        las3[ash_5].addParams(ip4=("192.168.5.0/24"), ip6=("2001:08::1/64",))
        las4 = self.addLink(chi_1,  chi_5)
        las4[chi_1].addParams(ip4=("192.168.6.0/24"), ip6=("2001:04::1/64",))
        las4[chi_5].addParams(ip4=("192.168.7.0/24"), ip6=("2001:09::1/64",))

        las11 = self.addLink(nwk_1,  bhs_g1)
        las11[nwk_1].addParams(ip4=("192.168.0.1/24"), ip6=("2001:01::2/64",))
        las11[bhs_g1].addParams(ip4=("192.168.2.1/24"), ip6=("2001:02::2/64",))
        las12 = self.addLink(nwk_1,  ash_1)
        las12[nwk_1].addParams(ip4=("192.168.0.2/24"), ip6=("2001:01::3/64",))
        las12[ash_1].addParams(ip4=("192.168.4.1/24"), ip6=("2001:03::2/64",))
        las13 = self.addLink(nwk_5,  bhs_g2)
        las13[nwk_5].addParams(ip4=("192.168.1.1/24"), ip6=("2001:06::2/64",))
        las13[bhs_g2].addParams(ip4=("192.168.3.1/24"), ip6=("2001:07::2/64",))
        las14 = self.addLink(nwk_5,  ash_5)
        las14[nwk_5].addParams(ip4=("192.168.1.2/24"), ip6=("2001:06::5/64",))
        las14[ash_5].addParams(ip4=("192.168.5.1/24"), ip6=("2001:08::2/64",))

        las41 = self.addLink(chi_1,  bhs_g1, igp_metric=3)
        las41[chi_1].addParams(ip4=("192.168.6.1/24"), ip6=("2001:04::2/64",))
        las41[bhs_g1].addParams(ip4=("192.168.2.2/24"), ip6=("2001:02::3/64",))
        las42 = self.addLink(chi_1,  ash_1,  igp_metric=3)
        las42[chi_1].addParams(ip4=("192.168.6.2/24"), ip6=("2001:04::3/64",))
        las42[ash_1].addParams(ip4=("192.168.4.2/24"), ip6=("2001:03::3/64",))
        las43 = self.addLink(chi_5,  bhs_g2, igp_metric=3)
        las43[chi_5].addParams(ip4=("192.168.7.1/24"), ip6=("2001:09::2/64",))
        las43[bhs_g2].addParams(ip4=("192.168.3.2/24"), ip6=("2001:07::3/64",))
        las44 = self.addLink(chi_5,  ash_5,  igp_metric=3)
        las44[chi_5].addParams(ip4=("192.168.7.2/24"), ip6=("2001:09::3/64",))
        las44[ash_5].addParams(ip4=("192.168.5.2/24"), ip6=("2001:08::3/64",))
        # Connecting US TO EU
        las15 = self.addLink(nwk_1,  europe, igp_metric=30)  # 30
        las15[nwk_1].addParams(ip4=("192.168.0.3/24"), ip6=("2001:01::4/64",))
        las15[europe].addParams(ip4=("192.168.8.0/24"), ip6=("2001:05::2/64",))
        las16 = self.addLink(nwk_5,  europe, igp_metric=30)  # 30
        las16[nwk_5].addParams(ip4=("192.168.1.3/24"), ip6=("2001:06::3/64",))
        las16[europe].addParams(ip4=("192.168.8.1/24"), ip6=("2001:05::3/64",))
        # Connection EU to AS
        las5 = self.addLink(europe, asia,   igp_metric=40)  # 40
        las5[europe].addParams(ip4=("192.168.8.2/24"), ip6=("2001:05::1/64",))
        las5[asia].addParams(ip4=("192.168.9.0/24"), ip6=("2001:10::1/64",))
        # Connecting US to AS
        las51 = self.addLink(asia,   chi_1,  igp_metric=50)  # 50
        las51[chi_1].addParams(ip4=("192.168.6.3/24"), ip6=("2001:03::4/64",))
        las51[asia].addParams(ip4=("192.168.9.1/24"), ip6=("2001:10::2/64",))
        las52 = self.addLink(asia,   chi_5,  igp_metric=50)  # 50
        las52[chi_5].addParams(ip4=("192.168.7.3/24"), ip6=("2001:09::30/64",))
        las52[asia].addParams(ip4=("192.168.9.2/24"), ip6=("2001:10::3/64",))

        # Adding OVH AS
        as16276_routers = [nwk_1, nwk_5, bhs_g1, bhs_g2,
                           chi_1, chi_5, ash_1, ash_5, europe, asia]

        # Adding OSPF6v3 and BGP to OVH Network
        for r in as16276_routers:
            r.addDaemon(OSPF6)

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
        ma1 = self.addLink(as16509_ash_1_amazon, as16509_r1)
        ma1[as16509_ash_1_amazon].addParams(ip4=("192.168.10.0/24"), ip6=("2001:20::1/64",))
        ma1[as16509_r1].addParams(ip4=("192.168.11.0/24"), ip6=("2001:13::3/64",))
        ma2 = self.addLink(as16509_ash_5_amazon, as16509_r2)
        ma2[as16509_ash_5_amazon].addParams(ip4=("192.168.12.0/24"), ip6=("2001:21::1/64",))
        ma2[as16509_r2].addParams(ip4=("192.168.13.0/24"), ip6=("2001:14::3/64",))
        ma3 = self.addLink(as16509_r1, as16509_r2)
        ma3[as16509_r1].addParams(ip4=("192.168.10.1/24"), ip6=("2001:13::4/64",))
        ma3[as16509_r2].addParams(ip4=("192.168.13.1/24"), ip6=("2001:14::4/64",))



        as16509_routers = [as16509_r1, as16509_r2]
        # Adding OSPF6v3 and BGP to AS174 (Cogent)
        for r in as16509_routers:
            r.addDaemon(OSPF6)

        as16509_r1.addDaemon(BGP,
                        address_families=(AF_INET6(networks=("2001:200:1::/48",)),),
                        routerid='1.2.1.1')
        as16509_r2.addDaemon(BGP,
                        address_families=(AF_INET6(networks=("2001:200:2::/48",)),),
                        routerid='1.2.1.2')
        self.addAS(16509, (as16509_r1, as16509_r2))
        # Building physical links between AS16509 (AMAZON) and OVH
        lam1 = self.addLink(as16509_r1, ash_1)
        lam1[as16509_r1].addParams(ip4=("192.168.10.2/24"), ip6=("2001:13::1/64",))
        lam1[ash_1].addParams(ip4=("192.168.4.3/24"), ip6=("2001:03::9/64",))
        lam2 = self.addLink(as16509_r1, ash_5)
        lam2[as16509_r1].addParams(ip4=("192.168.10.3/24"), ip6=("2001:13::2/64",))
        lam2[ash_5].addParams(ip4=("192.168.5.3/24"), ip6=("2001:08::5/64",))
        lam3 = self.addLink(as16509_r2, ash_1)
        lam3[as16509_r2].addParams(ip4=("192.168.13.2/24"), ip6=("2001:14::1/64",))
        lam3[ash_1].addParams(ip4=("192.168.4.4/24"), ip6=("2001:03::8/64",))
        lam4 = self.addLink(as16509_r2, ash_5)
        lam4[as16509_r2].addParams(ip4=("192.168.13.3/24"), ip6=("2001:14::2/64",))
        lam4[ash_5].addParams(ip4=("192.168.5.4/24"), ip6=("2001:08::6/64",))
        ebgp_session(self, as16509_r1, ash_1, link_type=SHARE)
        ebgp_session(self, as16509_r2, ash_1, link_type=SHARE)


        # Building as7843 (CHARTER) , routers and links
        as7843_chi_1_charter = self.addHost("charter_1")
        as7843_ash_1_charter = self.addHost("charter_2")
        #Routers + loopback
        as7843_r1 = self.addRouter("as7843_r1", lo_addresses=["2044:1::1/64", "12.1.1.1/24"])
        as7843_r2 = self.addRouter("as7843_r2", lo_addresses=["2044:2::1/64", "12.2.1.1/24"])
        # Linking as7843 (CHARTER) to its router
        mo1 = self.addLink(as7843_chi_1_charter, as7843_r1)
        mo1[as7843_chi_1_charter].addParams(ip4=("192.168.14.0/24"), ip6=("2001:22::1/64",))
        mo1[as7843_r1].addParams(ip4=("192.168.15.0/24"), ip6=("2001:11::3/64",))
        mo2 = self.addLink(as7843_ash_1_charter, as7843_r1)
        mo2[as7843_ash_1_charter].addParams(ip4=("192.168.16.0/24"), ip6=("2001:23::1/64",))
        mo2[as7843_r1].addParams(ip4=("192.168.15.1/24"), ip6=("2001:11::4/64",))
        mo3 = self.addLink(as7843_r1, as7843_r2)
        mo3[as7843_r1].addParams(ip4=("192.168.15.2/24"), ip6=("2001:11::5/64",))
        mo3[as7843_r2].addParams(ip4=("192.168.17.0/24"), ip6=("2001:80::1/64",))

        as7843_routers = [as7843_r1, as7843_r2]
        # Adding OSPF6v3 and BGP to AS174 (Cogent)
        for r in as7843_routers:
            r.addDaemon(OSPF6)

        as7843_r1.addDaemon(BGP,
                        address_families=(AF_INET6(networks=("2001:300:1::/48",)),),
                        routerid='1.3.1.1')
        as7843_r2.addDaemon(BGP,
                        address_families=(AF_INET6(networks=("2001:300:2::/48",)),),
                        routerid='1.3.1.2')
        self.addAS(7843, (as7843_r1, as7843_r2))
        # Building physical links between as7843 (CHARTER) and OVH
        lach1 = self.addLink(as7843_r1, chi_1)
        lach1[as7843_r1].addParams(ip4=("192.168.15.3/24"), ip6=("2001:11::1/64",))
        lach1[chi_1].addParams(ip4=("192.168.6.4/24"), ip6=("2001:04::4/64",))
        lach2 = self.addLink(as7843_r1, ash_1)
        lach2[as7843_r1].addParams(ip4=("192.168.15.4/24"), ip6=("2001:11::2/64",))
        lach2[ash_1].addParams(ip4=("192.168.4.5/24"), ip6=("2001:03::5/64",))
        lach3 = self.addLink(as7843_r2, chi_1)
        lach3[as7843_r2].addParams(ip4=("192.168.17.1/24"), ip6=("2001:80::2/64",))
        lach3[chi_1].addParams(ip4=("192.168.6.5/24"), ip6=("2001:04::5/64",))
        lach4 = self.addLink(as7843_r2, ash_1)
        lach4[as7843_r2].addParams(ip4=("192.168.17.2/24"),ip6=("2001:80::3/64",))
        lach4[ash_1].addParams(ip4=("192.168.4.6/24"), ip6=("2001:03::6/64",))
        ebgp_session(self, as7843_r1, chi_1, link_type=SHARE)
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
        ta1 = self.addLink(as1299_nwk_1_telia, as1299_r1)
        ta1[as1299_nwk_1_telia].addParams(ip4=("192.168.18.0/24"), ip6=("2001:24::1/64",))
        ta1[as1299_r1].addParams(ip4=("192.168.19.0/24"), ip6=("2001:70::3/64",))
        ta2 = self.addLink(as1299_nwk_5_telia, as1299_r1)
        ta2[as1299_nwk_5_telia].addParams(ip4=("192.168.20.0/24"), ip6=("2001:25::1/64",))
        ta2[as1299_r1].addParams(ip4=("192.168.19.1/24"), ip6=("2001:70::4/64",))
        ta3 = self.addLink(as1299_chi_5_telia, as1299_r2)
        ta3[as1299_chi_5_telia].addParams(ip4=("192.168.21.0/24"), ip6=("2001:26::1/64",))
        ta3[as1299_r2].addParams(ip4=("192.168.22.0/24"), ip6=("2001:71::3/64",))
        ta4 = self.addLink(as1299_ash_5_telia, as1299_r2)
        ta4[as1299_ash_5_telia].addParams(ip4=("192.168.23.0/24"), ip6=("2001:27::1/64",))
        ta4[as1299_r2].addParams(ip4=("192.168.22.1/24"), ip6=("2001:71::4/64",))
        ta5 = self.addLink(as1299_r1, as1299_r2)
        ta5[as1299_r1].addParams(ip4=("192.168.19.2/24"),ip6=("2001:70::5/64",))
        ta5[as1299_r2].addParams(ip4=("192.168.22.2/24"),ip6=("2001:71::5/64",))

        as1299_routers = [as1299_r1, as1299_r2]
        # Adding OSPF6v3 and BGP to AS174 (Cogent)
        for r in as1299_routers:
            r.addDaemon(OSPF6)
        as1299_r1.addDaemon(BGP,
                        address_families=(AF_INET6(networks=("2001:400:1::/48",)),),
                        routerid='1.4.1.1')
        as1299_r2.addDaemon(BGP,
                        address_families=(AF_INET6(networks=("2001:400:2::/48",)),),
                        routerid='1.4.1.2')
        self.addAS(1299, (as1299_r1, as1299_r2))
        # Building physical links between AS1299 (TElIA) and OVH
        lok1 = self.addLink(as1299_r1, nwk_1)
        lok1[as1299_r1].addParams(ip4=("192.168.19.3/24"), ip6=("2001:70::6/64",))
        lok1[nwk_1].addParams(ip4=("192.168.0.4/24"), ip6=("2001:01::5/64",))
        lok2 = self.addLink(as1299_r1, nwk_5)
        lok2[as1299_r1].addParams(ip4=("192.168.19.4/24"), ip6=("2001:70::7/64",))
        lok2[nwk_5].addParams(ip4=("192.168.1.4/24"), ip6=("2001:06::30/64",))
        lok3 = self.addLink(as1299_r2, chi_5)
        lok3[as1299_r2].addParams(ip4=("192.168.22.3/24"), ip6=("2001:71::6/64",))
        lok3[chi_5].addParams(ip4=("192.168.7.4/24"), ip6=("2001:09::4/64",))
        lok4 = self.addLink(as1299_r2, ash_5)
        lok4[as1299_r2].addParams(ip4=("192.168.22.4/24"), ip6=("2001:71::7/64",))
        lok4[ash_5].addParams(ip4=("192.168.5.5/24"), ip6=("2001:08::7/64",))
        # Remarque : ebgp fonctionne avec 3 n'importe lequels mais
        # dès qu'on actve 4 sessions, problème dans les ping. Aucun échange eBGP.
        # host 1 ne sait pas contacter telia et inversement
        # Je commente un nwk_5 car il y a dejà une session eBGP avec nwk_1
        ebgp_session(self, as1299_r1, nwk_1, link_type=SHARE)
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
        to1 = self.addLink(as174_nwk_1_cogent, as174_r1)
        to1[as174_nwk_1_cogent].addParams(ip4=("192.168.23.1/24"), ip6=("2001:28::1/64",))
        to1[as174_r1].addParams(ip4=("192.168.24.0/24"), ip6=("2001:17::5/64",))
        to2 = self.addLink(as174_nwk_5_cogent, as174_r1)
        to2[as174_nwk_5_cogent].addParams(ip4=("192.168.25.0/24"), ip6=("2001:29::1/64",))
        to2[as174_r1].addParams(ip4=("192.168.24.1/24"), ip6=("2001:17::6/64",))
        to3 = self.addLink(as174_chi_1_cogent, as174_r1)
        to3[as174_chi_1_cogent].addParams(ip4=("192.168.26.0/24"), ip6=("2001:30::1/64",))
        to3[as174_r1].addParams(ip4=("192.168.24.2/24"), ip6=("2001:17::7/64",))
        to4 = self.addLink(as174_chi_5_cogent, as174_r1)
        to4[as174_chi_5_cogent].addParams(ip4=("192.168.27.0/24"), ip6=("2001:31::1/64",))
        to4[as174_r1].addParams(ip4=("192.168.24.3/24"), ip6=("2001:17::8/64",))
        to5 = self.addLink(as174_ash_1_cogent, as174_r2)
        to5[as174_ash_1_cogent].addParams(ip4=("192.168.28.0/24"), ip6=("2001:32::1/64",))
        to5[as174_r2].addParams(ip4=("192.168.29.0/24"), ip6=("2001:18::3/64",))
        to6 = self.addLink(as174_ash_5_cogent, as174_r2)
        to6[as174_ash_5_cogent].addParams(ip4=("192.168.30.0/24"), ip6=("2001:33::1/64",))
        to6[as174_r2].addParams(ip4=("192.168.29.1/24"), ip6=("2001:18::4/64",))
        to7 = self.addLink(as174_r1, as174_r2)
        to7[as174_r1].addParams(ip4=("192.168.24.4/24"), ip6=("2001:17::9/64",))
        to7[as174_r2].addParams(ip4=("192.168.29.2/24"), ip6=("2001:18::5/64",))
        as174_routers = [as174_r1, as174_r2]
        # Adding OSPF6v3 and BGP to AS174 (Cogent)
        for r in as174_routers:
            r.addDaemon(OSPF6)
        as174_r1.addDaemon(BGP,
                    address_families=(AF_INET6(networks=("2001:500:1::/48",)),),
                    routerid='1.5.1.1')
        as174_r2.addDaemon(BGP,
                    address_families=(AF_INET6(networks=("2001:500:2::/48",)),),
                    routerid='1.5.1.2')

        self.addAS(174, (as174_r1, as174_r2))

        lom1 = self.addLink(as174_r1, nwk_1)
        lom1[as174_r1].addParams(ip4=("192.168.24.5/24"), ip6=("2001:17::1/64",))
        lom1[nwk_1].addParams(ip4=("192.168.0.5/24"), ip6=("2001:01::7/64",))
        lom2 = self.addLink(as174_r1, nwk_5)
        lom2[as174_r1].addParams(ip4=("192.168.24.6/24"), ip6=("2001:17::2/64",))
        lom2[nwk_5].addParams(ip4=("192.168.1.5/24"), ip6=("2001:06::7/64",))
        lom3 = self.addLink(as174_r1, chi_1)
        lom3[as174_r1].addParams(ip4=("192.168.24.7/24"), ip6=("2001:17::3/64",))
        lom3[chi_1].addParams(ip4=("192.168.6.6/24"), ip6=("2001:04::7/64",))
        lom4 = self.addLink(as174_r1, chi_5)
        lom4[as174_r1].addParams(ip4=("192.168.24.8/24"), ip6=("2001:17::4/64",))
        lom4[chi_5].addParams(ip4=("192.168.7.5/24"),ip6=("2001:09::6/64",))
        lom5 = self.addLink(as174_r2, ash_1)
        lom5[as174_r2].addParams(ip4=("192.168.29.3/24"), ip6=("2001:18::1/64",))
        lom5[ash_1].addParams(ip4=("192.168.4.7/24"), ip6=("2001:03::7/64",))
        lom6 = self.addLink(as174_r2, ash_5)
        lom6[as174_r2].addParams(ip4=("192.168.29.4/24"), ip6=("2001:18::2/64",))
        lom6[ash_5].addParams(ip4=("192.168.5.6/24"), ip6=("2001:08::8/64",))
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
        ti1 = self.addLink(as3356_nwk_5_level3, as3356_r1)
        ti1[as3356_nwk_5_level3].addParams(ip4=("192.168.31.0/24"), ip6=("2001:34::1/64",))
        ti1[as3356_r1].addParams(ip4=("192.168.32.0/24"), ip6=("2001:15::3/64",))
        ti2 = self.addLink(as3356_nwk_1_level3, as3356_r1)
        ti2[as3356_nwk_1_level3].addParams(ip4=("192.168.33.0/24"), ip6=("2001:35::1/64",))
        ti2[as3356_r1].addParams(ip4=("192.168.32.1/24"), ip6=("2001:15::4/64",))
        ti3 = self.addLink(as3356_chi_1_level3, as3356_r2)
        ti3[as3356_chi_1_level3].addParams(ip4=("192.168.34.0/24"), ip6=("2001:36::1/64",))
        ti3[as3356_r2].addParams(ip4=("192.168.35.0/24"), ip6=("2001:16::3/64",))
        ti4 = self.addLink(as3356_chi_5_level3, as3356_r2)
        ti4[as3356_chi_5_level3].addParams(ip4=("192.168.36.0/24"), ip6=("2001:37::1/64",))
        ti4[as3356_r2].addParams(ip4=("192.168.35.1/24"), ip6=("2001:16::4/64",))
        ti5 = self.addLink(as3356_r1, as3356_r2)
        ti5[as3356_r1].addParams(ip4=("192.168.32.2/24"), ip6=("2001:15::5/64",))
        ti5[as3356_r2].addParams(ip4=("192.168.35.2/24"), ip6=("2001:16::5/64",))

        as3356_routers = [as3356_r1, as3356_r2]
        # Adding OSPFv3 and BGP to AS174 (Cogent)
        for r in as3356_routers:
            r.addDaemon(OSPF6)
        as3356_r1.addDaemon(BGP,
                        address_families=(AF_INET6(networks=("2001:600:1::/48",)),),
                        routerid='1.6.1.1')
        as3356_r2.addDaemon(BGP,
                        address_families=(AF_INET6(networks=("2001:600:2::/48",)),),
                        routerid='1.6.1.2')
        
        
        self.addAS(3356, (as3356_r1, as3356_r2))

        lou1 = self.addLink(as3356_r1, nwk_1)
        lou1[as3356_r1].addParams(ip4=("192.168.32.3/24"), ip6=("2001:15::1/64",))
        lou1[nwk_1].addParams(ip4=("192.168.0.6/24"), ip6=("2001:01::6/64",))
        lou2 = self.addLink(as3356_r1, nwk_5)
        lou2[as3356_r1].addParams(ip4=("192.168.32.4/24"), ip6=("2001:15::2/64",))
        lou2[nwk_5].addParams(ip4=("192.168.1.6/24"), ip6=("2001:06::6/64",))
        lou3 = self.addLink(as3356_r2, chi_1)
        lou3[as3356_r2].addParams(ip4=("192.168.35.3/24"), ip6=("2001:16::1/64",))
        lou3[chi_1].addParams(ip4=("192.168.6.7/24"), ip6=("2001:04::6/64",))
        lou4 = self.addLink(as3356_r2, chi_5)
        lou4[as3356_r2].addParams(ip4=("192.168.35.4/24"), ip6=("2001:16::2/64",))
        lou4[chi_5].addParams(ip4=("192.168.7.6/24"), ip6=("2001:09::5/64",))
        # Added an eBGP session for each datacenter region for redundancy
        ebgp_session(self, as3356_r1, nwk_1, link_type=SHARE)
        ebgp_session(self, as3356_r2, chi_1, link_type=SHARE)
        

        all_al = AccessList('all', ('any',))  # Access list

        # SET MED
        nwk_1.get_config(BGP).set_med(50,  to_peer=as174_r1, matching=(all_al, ))
        chi_5.get_config(BGP).set_med(100, to_peer=as174_r1, matching=(all_al, ))
        chi_1.get_config(BGP).set_med(100, to_peer=as174_r1, matching=(all_al, ))
        
        # SET BGP COMMUNITY
        as16276_routers = [nwk_1, nwk_5, bhs_g1, bhs_g2, chi_1, chi_5, ash_1, ash_5]
        for s in as7843_routers: # charter routers
            europe.get_config(BGP).set_community(4, to_peer=s, matching=(all_al,))
            asia.get_config(BGP).set_community(5, to_peer=s, matching=(all_al,))
            for r in as16276_routers:
                s.get_config(BGP).set_community(21, to_peer=r, matching=(all_al,))
        for s in as16509_routers: # amazon routers
            europe.get_config(BGP).set_community(4, to_peer=s, matching=(all_al,))
            asia.get_config(BGP).set_community(5, to_peer=s, matching=(all_al,))
            for r in as16276_routers:
                s.get_config(BGP).set_community(22, to_peer=r, matching=(all_al,))
       
        for s in as3356_routers: # level3 routers
            europe.get_config(BGP).set_community(4, to_peer=s, matching=(all_al,))
            asia.get_config(BGP).set_community(5, to_peer=s, matching=(all_al,))
            for r in as16276_routers:
                s.get_config(BGP).set_community(11, to_peer=r, matching=(all_al,))
        for s in as174_routers: # cogent routers
            europe.get_config(BGP).set_community(4, to_peer=s, matching=(all_al,))
            asia.get_config(BGP).set_community(5, to_peer=s, matching=(all_al,))
            for r in as16276_routers:
                s.get_config(BGP).set_community(12, to_peer=r, matching=(all_al,))
        for s in as1299_routers: # telia routers
            europe.get_config(BGP).set_community(4, to_peer=s, matching=(all_al,))
            asia.get_config(BGP).set_community(5, to_peer=s, matching=(all_al,))
            for r in as16276_routers:
                s.get_config(BGP).set_community(13, to_peer=r, matching=(all_al,))

        for s in as16276_routers:  # OVH north america routers
            s.get_config(BGP).set_community(3, to_peer=europe, matching=(all_al,))
            s.get_config(BGP).set_community(3, to_peer=asia, matching=(all_al,))
            for r in as16509_routers:# amazon routers
                s.get_config(BGP).set_community(3, to_peer=r, matching=(all_al,))
            for r in as7843_routers:# charter routers
                s.get_config(BGP).set_community(3, to_peer=r, matching=(all_al,))
            for r in as1299_routers:# telia routers
                s.get_config(BGP).set_community(3, to_peer=r, matching=(all_al,))
            for r in as174_routers:# cogent routers
                s.get_config(BGP).set_community(3, to_peer=r, matching=(all_al,))
            for r in as3356_routers:# level3 routers
                s.get_config(BGP).set_community(3, to_peer=r, matching=(all_al,))
            
         # SET CDN
        cdn_europe_host1 = self.addHost("cdn_host1")
        cdn_europe_link1 = self.addLink(cdn_europe_host1, europe)
        cdn_europe_link1[cdn_europe_host1].addParams(ip=("10.0.3.2/24", "2001:3c::2/64"))
        cdn_europe_link1[europe].addParams(ip=("10.0.3.4/24", "2001:3c::4/64"))

        cdn_asia_host1 = self.addHost("cdn_host3")
        cdn_asia_link1 = self.addLink(cdn_asia_host1, asia)
        cdn_asia_link1[cdn_asia_host1].addParams(ip=("10.0.3.2/24", "2001:3c::2/64"))
        cdn_asia_link1[asia].addParams(ip=("10.0.3.3/24", "2001:3c::3/64"))

        cdn_nwk_1_host1 = self.addHost("cdn_host5")
        cdn_nwk_1_link1 = self.addLink(cdn_nwk_1_host1, nwk_1) 
        cdn_nwk_1_link1[cdn_nwk_1_host1].addParams(ip=("10.0.3.2/24", "2001:3c::2/64"))
        cdn_nwk_1_link1[nwk_1].addParams(ip=("10.0.3.1/24", "2001:3c::1/64"))

        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=MyTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

