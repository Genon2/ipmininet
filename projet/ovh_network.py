#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE, OSPF6, RouterConfig, AccessList, CommunityList


class MyTopology(IPTopo):

    def build(self, *args, **kwargs):
#Adressage IP Routeur IPV4

        serveur_ipv4 = "160.72.247."

        nwk_ipv4 = "160.72.241."
        bhs_ipv4 = "160.72.242."
        chi_ipv4 = "160.72.243."
        ash_ipv4 = "160.72.244."


        europe_ipv4 = "160.72.245."
        asia_ipv4 = "160.72.246."

        #Adressage IP Routeur IPV6

        serveur_ipv6 = "2010:1000:0000:0"

        usa_ipv6 = "2010:1100:0000:0"
        europe_ipv6 = "2010:1200:0000:0"
        asia_ipv6 = "2010:1300:0000:0"
        


        # Building OVH Network
        # test routers used for pingall when checking eBGP
        # Building New York routers
        nwk_1 = self.addRouter("nwk_1", lo_addresses=[usa_ipv6 + "000::/64", nwk_ipv4 + "100/24"])
        nwk_5 = self.addRouter("nwk_5", lo_addresses=[usa_ipv6 + "100::/64", nwk_ipv4 + "110/24"])
        # Building Bhs routers
        bhs_g1 = self.addRouter("bhs_g1", lo_addresses=[usa_ipv6 + "200::/64", bhs_ipv4 + "100/24"])
        bhs_g2 = self.addRouter("bhs_g2", lo_addresses=[usa_ipv6 + "300::/64", bhs_ipv4 + "110/24"])
        # Building Chicago routers
        chi_1 = self.addRouter("chi_1", lo_addresses=[usa_ipv6 + "400::/64", chi_ipv4 + "100/24"])
        chi_5 = self.addRouter("chi_5", lo_addresses=[usa_ipv6 + "500::/64", chi_ipv4 + "110/24"])
        # Building Ashburn routers
        ash_1 = self.addRouter("ash_1", lo_addresses=[usa_ipv6 + "600::/64", ash_ipv4 + "100/24"])
        ash_5 = self.addRouter("ash_5", lo_addresses=[usa_ipv6 + "700::/64", ash_ipv4 + "110/24"])
        # Building europe's routers abstractly
        europe = self.addRouter("europe", lo_addresses=[europe_ipv6 + "000::/64", europe_ipv4 + "100/24"])
        # Building asia's routers abstractly
        asia = self.addRouter("asia", lo_addresses=[asia_ipv6 + "000::/64", asia_ipv4 + "100/24"])

        


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
        las1[nwk_1].addParams(ip6=(usa_ipv6 + "000::1/64"), ip4=(nwk_ipv4 + "101/24"))
        las1[nwk_5].addParams(ip6=(usa_ipv6 + "100::1/64"), ip4=(nwk_ipv4 + "111/24"))
        las2 = self.addLink(bhs_g1, bhs_g2)
        las2[bhs_g1].addParams(ip6=(usa_ipv6 + "200::1/64"), ip4=(bhs_ipv4 + "101/24"))
        las2[bhs_g2].addParams(ip6=(usa_ipv6 + "300::1/64"), ip4=(bhs_ipv4 + "111/24"))
        las3 = self.addLink(ash_1,  ash_5)
        las3[ash_1].addParams(ip6=(usa_ipv6 + "600::1/64"), ip4=(ash_ipv4 + "101/24"))
        las3[ash_5].addParams(ip6=(usa_ipv6 + "700::1/64"), ip4=(ash_ipv4 + "111/24"))
        las4 = self.addLink(chi_1,  chi_5)
        las4[chi_1].addParams(ip6=(usa_ipv6 + "400::1/64"), ip4=(chi_ipv4 + "101/24"))
        las4[chi_5].addParams(ip6=(usa_ipv6 + "500::1/64"), ip4=(chi_ipv4 + "111/24"))

        las11 = self.addLink(nwk_1,  bhs_g1)
        las11[nwk_1].addParams(ip6=(usa_ipv6 + "000::2/64"), ip4=(nwk_ipv4 + "102/24"))
        las11[bhs_g1].addParams(ip6=(usa_ipv6 + "200::2/64"), ip4=(bhs_ipv4 + "102/24"))
        las12 = self.addLink(nwk_1,  ash_1)
        las12[nwk_1].addParams(ip6=(usa_ipv6 + "000::3/64"), ip4=(nwk_ipv4 + "103/24"))
        las12[ash_1].addParams(ip6=(usa_ipv6 + "600::2/64"), ip4=(ash_ipv4 + "102/24"))
        las13 = self.addLink(nwk_5,  bhs_g2)
        las13[nwk_5].addParams(ip6=(usa_ipv6 + "100::2/64"), ip4=(nwk_ipv4 + "112/24"))
        las13[bhs_g2].addParams(ip6=(usa_ipv6 + "300::2/64"), ip4=(bhs_ipv4 + "112/24"))
        las14 = self.addLink(nwk_5,  ash_5)
        las14[nwk_5].addParams(ip6=(usa_ipv6 + "100::3/64"), ip4=(nwk_ipv4 + "113/24"))
        las14[ash_5].addParams(ip6=(usa_ipv6 + "700::2/64"), ip4=(ash_ipv4 + "112/24"))

        las41 = self.addLink(chi_1,  bhs_g1, igp_metric=3)
        las41[chi_1].addParams(ip6=(usa_ipv6 + "400::2/64"), ip4=(chi_ipv4 + "102/24"))
        las41[bhs_g1].addParams(ip6=(usa_ipv6 + "200::3/64"), ip4=(bhs_ipv4 + "103/24"))
        las42 = self.addLink(chi_1,  ash_1,  igp_metric=3)
        las42[chi_1].addParams(ip6=(usa_ipv6 + "400::3/64"), ip4=(chi_ipv4 + "103/24"))
        las42[ash_1].addParams(ip6=(usa_ipv6 + "600::3/64"), ip4=(ash_ipv4 + "103/24"))
        las43 = self.addLink(chi_5,  bhs_g2, igp_metric=3)
        las43[chi_5].addParams(ip6=(usa_ipv6 + "500::2/64"), ip4=(chi_ipv4 + "112/24"))
        las43[bhs_g2].addParams(ip6=(usa_ipv6 + "300::3/64"), ip4=(bhs_ipv4 + "113/24"))
        las44 = self.addLink(chi_5,  ash_5,  igp_metric=3)
        las44[chi_5].addParams(ip6=(usa_ipv6 + "500::3/64"), ip4=(chi_ipv4 + "113/24"))
        las44[ash_5].addParams(ip6=(usa_ipv6 + "700::3/64"), ip4=(ash_ipv4 + "113/24"))
        # Connecting US TO EU
        las15 = self.addLink(nwk_1,  europe, igp_metric=30)  # 30
        las15[nwk_1].addParams(ip6=(usa_ipv6 + "000::4/64"), ip4=(nwk_ipv4 + "104/24"))
        las15[europe].addParams(ip6=(europe_ipv6 + "000::1/64"), ip4=(europe_ipv4 + "101/24"))
        las16 = self.addLink(nwk_5,  europe, igp_metric=30)  # 30
        las16[nwk_5].addParams(ip6=(usa_ipv6 + "100::4/64"), ip4=(nwk_ipv4 + "114/24"))
        las16[europe].addParams(ip6=(europe_ipv6 + "000::2/64"), ip4=(europe_ipv4 + "102/24"))
        # Connection EU to AS
        las5 = self.addLink(europe, asia,   igp_metric=40)  # 40
        las5[europe].addParams(ip6=(europe_ipv6 + "000::3/64"), ip4=(europe_ipv4 + "103/24"))
        las5[asia].addParams(ip6=(asia_ipv6 + "000::1/64"), ip4=(asia_ipv4 + "101/24"))
        # Connecting US to AS
        las51 = self.addLink(asia,   chi_1,  igp_metric=50)  # 50
        las51[chi_1].addParams(ip6=(usa_ipv6 + "400::4/64"), ip4=(chi_ipv4 + "104/24"))
        las51[asia].addParams(ip6=(asia_ipv6 + "000::2/64"), ip4=(asia_ipv4 + "102/24"))
        las52 = self.addLink(asia,   chi_5,  igp_metric=50)  # 50
        las52[chi_5].addParams(ip6=(usa_ipv6 + "500::4/64"), ip4=(chi_ipv4 + "114/24"))
        las52[asia].addParams(ip6=(asia_ipv6 + "000::3/64"), ip4=(asia_ipv4 + "103/24"))

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

        #Adressage IPv4

        as16509_ipv4 = "162.61.1."
        as7843_ipv4 = "162.62.1."

        #Adressage IPv6

        as16509_ipv6 = "2010:2100:0000:0"
        as7843_ipv6 = "2010:2200:0000:0"

        # Building AS16509 (AMAZON)
        as16509_ash_1_amazon = self.addHost("amazon_1")
        as16509_ash_5_amazon = self.addHost("amazon_2")
        #Routers + loopback
        as16509_r1 = self.addRouter("as16509_r1", lo_addresses=[as16509_ipv6 + "000::/64", as16509_ipv4 + "100/24"])
        as16509_r2 = self.addRouter("as16509_r2", lo_addresses=[as16509_ipv6 + "100::/64", as16509_ipv4 + "110/24"])
        # Linking AS16509 (AMAZON) to its router
        ma1 = self.addLink(as16509_ash_1_amazon, as16509_r1)
        #as16509_ash_1_amazon et as16509_ash_5_amazon ont des adresses ipv6 et ipv4 proche de ash1 et ash5 par choix
        ma1[as16509_ash_1_amazon].addParams(ip6=(usa_ipv6 + "610::1/64"), ip4=(ash_ipv4 + "150/24"))
        ma1[as16509_r1].addParams(ip6=(as16509_ipv6 + "000::1/64"), ip4=(as16509_ipv4 + "101/24"))
        ma2 = self.addLink(as16509_ash_5_amazon, as16509_r2)
        ma2[as16509_ash_5_amazon].addParams(ip6=(usa_ipv6 + "710::1/64"), ip4=(ash_ipv4 + "160/24"))
        ma2[as16509_r2].addParams(ip6=(as16509_ipv6 + "100::1/64"), ip4=(as16509_ipv4 + "111/24"))
        ma3 = self.addLink(as16509_r1, as16509_r2)
        ma3[as16509_r1].addParams(ip6=(as16509_ipv6 + "000::2/64"), ip4=(as16509_ipv4 + "102/24"))
        ma3[as16509_r2].addParams(ip6=(as16509_ipv6 + "100::2/64"), ip4=(as16509_ipv4 + "112/24"))



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
        lam1[as16509_r1].addParams(ip6=(as16509_ipv6 + "000::3/64"), ip4=(as16509_ipv4 + "103/24"))
        lam1[ash_1].addParams(ip6=(usa_ipv6 + "600::4/64"), ip4=(ash_ipv4 + "104/24"))
        lam2 = self.addLink(as16509_r1, ash_5)
        lam2[as16509_r1].addParams(ip6=(as16509_ipv6 + "000::4/64"), ip4=(as16509_ipv4 + "104/24"))
        lam2[ash_5].addParams(ip6=(usa_ipv6 + "700::4/64"), ip4=(ash_ipv4 + "114/24"))
        lam3 = self.addLink(as16509_r2, ash_1)
        lam3[as16509_r2].addParams(ip6=(as16509_ipv6 + "100::3/64"), ip4=(as16509_ipv4 + "113/24"))
        lam3[ash_1].addParams(ip6=(usa_ipv6 + "600::5/64"), ip4=(ash_ipv4 + "105/24"))
        lam4 = self.addLink(as16509_r2, ash_5)
        lam4[as16509_r2].addParams(ip6=(as16509_ipv6 + "100::4/64"), ip4=(as16509_ipv4 + "114/24"))
        lam4[ash_5].addParams(ip6=(usa_ipv6 + "700::5/64"), ip4=(ash_ipv4 + "115/24"))
        ebgp_session(self, as16509_r1, ash_1, link_type=SHARE)
        ebgp_session(self, as16509_r2, ash_1, link_type=SHARE)


        # Building as7843 (CHARTER) , routers and links
        as7843_chi_1_charter = self.addHost("charter_1")
        as7843_ash_1_charter = self.addHost("charter_2")
        #Routers + loopback
        as7843_r1 = self.addRouter("as7843_r1", lo_addresses=[as7843_ipv6 + "000::/64", as7843_ipv4 + "100/24"])
        as7843_r2 = self.addRouter("as7843_r2", lo_addresses=[as7843_ipv6 + "100::/64", as7843_ipv4 + "110/24"])
        # Linking as7843 (CHARTER) to its router
        mo1 = self.addLink(as7843_chi_1_charter, as7843_r1)
        #as7843_chi_1_charter et as7843_ash_1_charter ont des adresses proches respectivement de chi_1 et de ash_1
        mo1[as7843_chi_1_charter].addParams(ip6=(usa_ipv6 + "410::1/64"), ip4=(chi_ipv4 + "150/24"))
        mo1[as7843_r1].addParams(ip6=(as7843_ipv6 + "000::1/64"), ip4=(as7843_ipv4 + "101/24"))
        mo2 = self.addLink(as7843_ash_1_charter, as7843_r1)
        mo2[as7843_ash_1_charter].addParams(ip6=(usa_ipv6 + "620::/64"), ip4=(ash_ipv4 + "170/24"))
        mo2[as7843_r1].addParams(ip6=(as7843_ipv6 + "000::2/64"), ip4=(as7843_ipv4 + "102/24"))
        mo3 = self.addLink(as7843_r1, as7843_r2)
        mo3[as7843_r1].addParams(ip6=(as7843_ipv6 + "000::3/64"), ip4=(as7843_ipv4 + "103/24"))
        mo3[as7843_r2].addParams(ip6=(as7843_ipv6 + "100::1/64"), ip4=(as7843_ipv4 + "111/24"))

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
        lach1[as7843_r1].addParams(ip6=(as7843_ipv6 + "000::4/64"), ip4=(as7843_ipv4 + "104/24"))
        lach1[chi_1].addParams(ip6=(usa_ipv6 + "400::5/64"), ip4=(chi_ipv4 + "105/24"))
        lach2 = self.addLink(as7843_r1, ash_1)
        lach2[as7843_r1].addParams(ip6=(as7843_ipv6 + "000::5/64"), ip4=(as7843_ipv4 + "105/24"))
        lach2[ash_1].addParams(ip6=(usa_ipv6 + "600::6/64"), ip4=(ash_ipv4 + "106/24"))
        lach3 = self.addLink(as7843_r2, chi_1)
        lach3[as7843_r2].addParams(ip6=(as7843_ipv6 + "100::2/64"), ip4=(as7843_ipv4 + "112/24"))
        lach3[chi_1].addParams(ip6=(usa_ipv6 + "400::6/64"), ip4=(chi_ipv4 + "106/24"))
        lach4 = self.addLink(as7843_r2, ash_1)
        lach4[as7843_r2].addParams(ip6=(as7843_ipv6 + "100::3/64"), ip4=(as7843_ipv4 + "113/24"))
        lach4[ash_1].addParams(ip6=(usa_ipv6 + "600::7/64"), ip4=(ash_ipv4 + "107/24"))
        ebgp_session(self, as7843_r1, chi_1, link_type=SHARE)
        ebgp_session(self, as7843_r2, ash_1, link_type=SHARE)

        #############################################################
        #                                                           #
        #              TRANSIT                                      #
        #                                                           #
        #############################################################

        #Adressage IPv4

        as1299_ipv4 = "162.63.1."
        as174_ipv4 = "162.64.1."
        as3356_ipv4 = "162.65.1."

        #Adressage IPv6

        as1299_ipv6 = "2010:2300:0000:0"
        as174_ipv6 = "2010:2400:0000:0"
        as3356_ipv6 = "2010:2500:0000:0"

        # Building AS1299 (TElIA) , routers and links
        as1299_nwk_1_telia = self.addHost("telia_1")
        as1299_nwk_5_telia = self.addHost("telia_2")
        as1299_chi_5_telia = self.addHost("telia_3")
        as1299_ash_5_telia = self.addHost("telia_4")

        #Routers + loopback
        as1299_r1 = self.addRouter("as1299_r1", lo_addresses=[as1299_ipv6 + "000::/64", as1299_ipv4 + "100/24"])
        as1299_r2 = self.addRouter("as1299_r2", lo_addresses=[as1299_ipv6 + "100::/64", as1299_ipv4 + "110/24"])
        
        # Linking AS1299 (TElIA) to its router
        ta1 = self.addLink(as1299_nwk_1_telia, as1299_r1)
        ta1[as1299_nwk_1_telia].addParams(ip6=(usa_ipv6 + "010::/64"), ip4=(nwk_ipv4 + "150/24"))
        ta1[as1299_r1].addParams(ip6=(as1299_ipv6 + "000::1/64"), ip4=(as1299_ipv4 + "101/24"))
        ta2 = self.addLink(as1299_nwk_5_telia, as1299_r1)
        ta2[as1299_nwk_5_telia].addParams(ip6=(usa_ipv6 + "110::/64"), ip4=(nwk_ipv4 + "160/24"))
        ta2[as1299_r1].addParams(ip6=(as1299_ipv6 + "000::2/64"), ip4=(as1299_ipv4 + "102/24"))
        ta3 = self.addLink(as1299_chi_5_telia, as1299_r2)
        ta3[as1299_chi_5_telia].addParams(ip6=(usa_ipv6 + "510::/64"), ip4=(chi_ipv4 + "160/24"))
        ta3[as1299_r2].addParams(ip6=(as1299_ipv6 + "100::1/64"), ip4=(as1299_ipv4 + "111/24"))
        ta4 = self.addLink(as1299_ash_5_telia, as1299_r2)
        ta4[as1299_ash_5_telia].addParams(ip6=(usa_ipv6 + "720::1/64"), ip4=(ash_ipv4 + "180/24"))
        ta4[as1299_r2].addParams(ip6=(as1299_ipv6 + "100::2/64"), ip4=(as1299_ipv4 + "112/24"))
        ta5 = self.addLink(as1299_r1, as1299_r2)
        ta5[as1299_r1].addParams(ip6=(as1299_ipv6 + "000::3/64"), ip4=(as1299_ipv4 + "103/24"))
        ta5[as1299_r2].addParams(ip6=(as1299_ipv6 + "100::3/64"), ip4=(as1299_ipv4 + "113/24"))

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
        lok1[as1299_r1].addParams(ip6=(as1299_ipv6 + "000::4/64"), ip4=(as1299_ipv4 + "104/24"))
        lok1[nwk_1].addParams(ip6=(usa_ipv6 + "000::5/64"), ip4=(nwk_ipv4 + "105/24"))
        lok2 = self.addLink(as1299_r1, nwk_5)
        lok2[as1299_r1].addParams(ip6=(as1299_ipv6 + "000::5/64"), ip4=(as1299_ipv4 + "105/24"))
        lok2[nwk_5].addParams(ip6=(usa_ipv6 + "100::5/64"), ip4=(nwk_ipv4 + "115/24"))
        lok3 = self.addLink(as1299_r2, chi_5)
        lok3[as1299_r2].addParams(ip6=(as1299_ipv6 + "100::4/64"), ip4=(as1299_ipv4 + "114/24"))
        lok3[chi_5].addParams(ip6=(usa_ipv6 + "500::5/64"), ip4=(chi_ipv4 + "115/24"))
        lok4 = self.addLink(as1299_r2, ash_5)
        lok4[as1299_r2].addParams(ip6=(as1299_ipv6 + "100::5/64"), ip4=(as1299_ipv4 + "115/24"))
        lok4[ash_5].addParams(ip6=(usa_ipv6 + "700::6/64"), ip4=(ash_ipv4 + "116/24"))
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
        as174_r1 = self.addRouter("as174_r1", lo_addresses=[as174_ipv6 + "000::/64", as174_ipv4 + "100/24"])
        as174_r2 = self.addRouter("as174_r2", lo_addresses=[as174_ipv6 + "100::/64", as174_ipv4 + "110/24"])
      
        # Added links
        to1 = self.addLink(as174_nwk_1_cogent, as174_r1)
        to1[as174_nwk_1_cogent].addParams(ip6=(usa_ipv6 + "020::/64"), ip4=(nwk_ipv4 + "170/24"))
        to1[as174_r1].addParams(ip6=(as174_ipv6 + "000::1/64"), ip4=(as174_ipv4 + "101/24"))
        to2 = self.addLink(as174_nwk_5_cogent, as174_r1)
        to2[as174_nwk_5_cogent].addParams(ip6=(usa_ipv6 + "120::/64"), ip4=(nwk_ipv4 + "180/24"))
        to2[as174_r1].addParams(ip6=(as174_ipv6 + "000::2/64"), ip4=(as174_ipv4 + "102/24"))
        to3 = self.addLink(as174_chi_1_cogent, as174_r1)
        to3[as174_chi_1_cogent].addParams(ip6=(usa_ipv6 + "420::1/64"), ip4=(chi_ipv4 + "170/24"))
        to3[as174_r1].addParams(ip6=(as174_ipv6 + "000::3/64"), ip4=(as174_ipv4 + "103/24"))
        to4 = self.addLink(as174_chi_5_cogent, as174_r1)
        to4[as174_chi_5_cogent].addParams(ip6=(usa_ipv6 + "520::/64"), ip4=(chi_ipv4 + "180/24"))
        to4[as174_r1].addParams(ip6=(as174_ipv6 + "000::4/64"), ip4=(as174_ipv4 + "104/24"))
        to5 = self.addLink(as174_ash_1_cogent, as174_r2)
        to5[as174_ash_1_cogent].addParams(ip6=(usa_ipv6 + "630::/64"), ip4=(ash_ipv4 + "190/24"))
        to5[as174_r2].addParams(ip6=(as174_ipv6 + "100::1/64"), ip4=(as174_ipv4 + "111/24"))
        to6 = self.addLink(as174_ash_5_cogent, as174_r2)
        to6[as174_ash_5_cogent].addParams(ip6=(usa_ipv6 + "730::1/64"), ip4=(ash_ipv4 + "200/24"))
        to6[as174_r2].addParams(ip6=(as174_ipv6 + "100::2/64"), ip4=(as174_ipv4 + "112/24"))
        to7 = self.addLink(as174_r1, as174_r2)
        to7[as174_r1].addParams(ip6=(as174_ipv6 + "000::5/64"), ip4=(as174_ipv4 + "105/24"))
        to7[as174_r2].addParams(ip6=(as174_ipv6 + "100::3/64"), ip4=(as174_ipv4 + "113/24"))
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
        lom1[as174_r1].addParams(ip6=(as174_ipv6 + "000::6/64"), ip4=(as174_ipv4 + "106/24"))
        lom1[nwk_1].addParams(ip6=(usa_ipv6 + "000::6/64"), ip4=(nwk_ipv4 + "106/24"))
        lom2 = self.addLink(as174_r1, nwk_5)
        lom2[as174_r1].addParams(ip6=(as174_ipv6 + "000::7/64"), ip4=(as174_ipv4 + "107/24"))
        lom2[nwk_5].addParams(ip6=(usa_ipv6 + "100::6/64"), ip4=(nwk_ipv4 + "116/24"))
        lom3 = self.addLink(as174_r1, chi_1)
        lom3[as174_r1].addParams(ip6=(as174_ipv6 + "000::8/64"), ip4=(as174_ipv4 + "108/24"))
        lom3[chi_1].addParams(ip6=(usa_ipv6 + "400::7/64"), ip4=(chi_ipv4 + "107/24"))
        lom4 = self.addLink(as174_r1, chi_5)
        lom4[as174_r1].addParams(ip6=(as174_ipv6 + "000::9/64"), ip4=(as174_ipv4 + "109/24"))
        lom4[chi_5].addParams(ip6=(usa_ipv6 + "500::6/64"), ip4=(chi_ipv4 + "116/24"))
        lom5 = self.addLink(as174_r2, ash_1)
        lom5[as174_r2].addParams(ip6=(as174_ipv6 + "100::4/64"), ip4=(as174_ipv4 + "114/24"))
        lom5[ash_1].addParams(ip6=(usa_ipv6 + "600::8/64"), ip4=(ash_ipv4 + "108/24"))
        lom6 = self.addLink(as174_r2, ash_5)
        lom6[as174_r2].addParams(ip6=(as174_ipv6 + "100::5/64"), ip4=(as174_ipv4 + "115/24"))
        lom6[ash_5].addParams(ip6=(usa_ipv6 + "700::7/64"), ip4=(ash_ipv4 + "117/24"))
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
        as3356_r1 = self.addRouter("as3356_r1", lo_addresses=[as3356_ipv6 + "000::/64", as3356_ipv4 + "100/24"])
        as3356_r2 = self.addRouter("as3356_r2", lo_addresses=[as3356_ipv6 + "100::/64", as3356_ipv4 + "110/24"])
        
        # Added links
        ti1 = self.addLink(as3356_nwk_5_level3, as3356_r1)
        ti1[as3356_nwk_5_level3].addParams(ip6=(usa_ipv6 + "130::/64"), ip4=(nwk_ipv4 + "190/24"))
        ti1[as3356_r1].addParams(ip6=(as3356_ipv6 + "000::1/64"), ip4=(as3356_ipv4 + "101/24"))
        ti2 = self.addLink(as3356_nwk_1_level3, as3356_r1)
        ti2[as3356_nwk_1_level3].addParams(ip6=(usa_ipv6 + "030::/64"), ip4=(nwk_ipv4 + "200/24"))
        ti2[as3356_r1].addParams(ip6=(as3356_ipv6 + "000::2/64"), ip4=(as3356_ipv4 + "102/24"))
        ti3 = self.addLink(as3356_chi_1_level3, as3356_r2)
        ti3[as3356_chi_1_level3].addParams(ip6=(usa_ipv6 + "430::1/64"), ip4=(chi_ipv4 + "190/24"))
        ti3[as3356_r2].addParams(ip6=(as3356_ipv6 + "100::1/64"), ip4=(as3356_ipv4 + "111/24"))
        ti4 = self.addLink(as3356_chi_5_level3, as3356_r2)
        ti4[as3356_chi_5_level3].addParams(ip6=(usa_ipv6 + "530::/64"), ip4=(chi_ipv4 + "200/24"))
        ti4[as3356_r2].addParams(ip6=(as3356_ipv6 + "100::2/64"), ip4=(as3356_ipv4 + "112/24"))
        ti5 = self.addLink(as3356_r1, as3356_r2)
        ti5[as3356_r1].addParams(ip6=(as3356_ipv6 + "000::3/64"), ip4=(as3356_ipv4 + "103/24"))
        ti5[as3356_r2].addParams(ip6=(as3356_ipv6 + "100::3/64"), ip4=(as3356_ipv4 + "113/24"))

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
        lou1[as3356_r1].addParams(ip6=(as3356_ipv6 + "000::4/64"), ip4=(as3356_ipv4 + "104/24"))
        lou1[nwk_1].addParams(ip6=(usa_ipv6 + "000::7/64"), ip4=(nwk_ipv4 + "107/24"))
        lou2 = self.addLink(as3356_r1, nwk_5)
        lou2[as3356_r1].addParams(ip6=(as3356_ipv6 + "000::5/64"), ip4=(as3356_ipv4 + "105/24"))
        lou2[nwk_5].addParams(ip6=(usa_ipv6 + "100::7/64"), ip4=(nwk_ipv4 + "117/24"))
        lou3 = self.addLink(as3356_r2, chi_1)
        lou3[as3356_r2].addParams(ip6=(as3356_ipv6 + "100::4/64"), ip4=(as3356_ipv4 + "114/24"))
        lou3[chi_1].addParams(ip6=(usa_ipv6 + "400::8/64"), ip4=(chi_ipv4 + "108/24"))
        lou4 = self.addLink(as3356_r2, chi_5)
        lou4[as3356_r2].addParams(ip6=(as3356_ipv6 + "100::5/64"), ip4=(as3356_ipv4 + "115/24"))
        lou4[chi_5].addParams(ip6=(usa_ipv6 + "500::7/64"), ip4=(chi_ipv4 + "117/24"))
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
        cdn_europe_host1 = self.addRouter("cdn_host1", lo_addresses=["10.0.3.2/24", "2001:3c::2/64"])
        cdn_europe_host1.addDaemon(BGP)
        cdn_europe_host1.addDaemon(OSPF6)
        cdn_europe_link1 = self.addLink(cdn_europe_host1, europe)
        cdn_europe_link1[europe].addParams(ip6=("10.0.3.4/24", ") 2ip4=(01:3c::4/64"))

        cdn_asia_host1 = self.addRouter("cdn_host3", lo_addresses=["10.0.3.2/24", "2001:3c::2/64"])
        cdn_asia_host1.addDaemon(BGP)
        cdn_asia_host1.addDaemon(OSPF6)
        cdn_asia_link1 = self.addLink(cdn_asia_host1, asia)
        cdn_asia_link1[asia].addParams(ip6=("10.0.3.3/24", ") 2ip4=(01:3c::3/64"))

        cdn_nwk_1_host1 = self.addRouter("cdn_host5", lo_addresses=["10.0.3.2/24", "2001:3c::2/64"])
        cdn_nwk_1_host1.addDaemon(BGP)
        cdn_nwk_1_host1.addDaemon(OSPF6)
        cdn_nwk_1_link1 = self.addLink(cdn_nwk_1_host1, nwk_1) 
        cdn_nwk_1_link1[nwk_1].addParams(ip6=("10.0.3.1/24", ") 2ip4=(01:3c::1/64"))

        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=MyTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

