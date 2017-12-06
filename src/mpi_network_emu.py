import subprocess
import sys
import psutil
import iptc
import json
from pyroute2 import IPRoute
from pyroute2.netlink.rtnl import RTM_NEWTCLASS
from pyroute2.netlink.rtnl import RTM_NEWTCLASS
from pyroute2.netlink.rtnl import RTM_DELTCLASS
from pyroute2.netlink.rtnl import RTM_NEWQDISC
from pyroute2.netlink.rtnl import RTM_DELQDISC
from pyroute2.netlink.rtnl import RTM_NEWTFILTER
from pyroute2.netlink.rtnl import RTM_DELTFILTER
from pyroute2.netlink import NetlinkError
from subprocess import check_output

ETH_P_IP = 0x0800
PRIO = 1
HANDLE_MIN = 2
HANDLE_MAX = (2 ** 16) - 1

def get_pid(name):
    return map(int,check_output(["pidof",name]).split())

def tag_packets_with_port(port):
    chain = iptc.Chain(iptc.Table(iptc.Table.MANGLE), "OUTPUT")
    rule = iptc.Rule()
    rule.protocol = "tcp"
    match = iptc.Match(rule, "tcp")
    match.dport = str(port)
    rule.add_match(match)
    rule.out_interface = "eth1"
    target = iptc.Target(rule, "MARK")
    target.set_mark = "0x01"
    rule.target = target
    chain.insert_rule(rule)

def tag_packets(process_name):
    mpi_pids =  get_pid(process_name)
    for pid in mpi_pids :	
       	p = psutil.Process(pid)
        for conn in p.connections() :
         if conn.laddr.ip != '0.0.0.0':
          tag_packets_with_port(conn.laddr.port)

def stop_emu():
     ipr = IPRoute() 
     LINK_ID = ipr.link_lookup(ifname="eth1")[0]
     try:
            ipr.tc(
                RTM_DELTFILTER, 'fw', LINK_ID, 0x01,
                parent = 0x10000, protocol=ETH_P_IP, prio=PRIO
            )
     except NetlinkError as e:
            print "can't delete the filter"+str(e)
     except Exception as e:
            exc_info = sys.exc_info()
            print "can't delete the filter"+str(exc_info)
     
     try:
           ipr.tc(RTM_DELTCLASS, 'htb', LINK_ID, 0x10000 + 0x01)
     except NetlinkError as e:
            print "can't delete the class"+str(e)
     except Exception as e:
            exc_info = sys.exc_info()
            print "cant' delete the class"+str(exc_info)

def netem(  p_rate,
            p_loss_ratio=0,
            p_loss_corr=0,
            p_dup_ratio=0,
            p_delay=0,
            p_delay_corr=0,
            p_jitter=0,
            p_delay_jitter_corr=0,
            p_reorder_ratio=0,
            p_reorder_corr=0,
            p_reorder_gap=0,
            p_corr_ratio=0,
            p_corr_corr=0,
            p_dont_drop_packets = True,
            p_burst_size =0,
          ):
    ipr = IPRoute()
    LINK_ID = ipr.link_lookup(ifname="eth1")[0]
    
    try:
            ipr.tc(
                RTM_NEWTCLASS, 'htb', LINK_ID, 0x10001,
                parent = 0x10000,
                rate="{}kbit".format(p_rate or (2**22 - 1)),
            )
    except NetlinkError as e:
            print "can't create new class"+str(e)
    except Exception as e:
           print "can't create new class"+str(e)
    
    try:
            ipr.tc(
                RTM_NEWQDISC, 'netem',LINK_ID, 0,
                parent= 0x10001,
                loss=p_loss_ratio*100,
                delay=p_delay*1000,
                jitter=p_jitter*1000,
                delay_corr=p_delay_corr,
                loss_corr=p_loss_corr,
                prob_reorder=p_reorder_ratio*100,
                corr_reorder=p_reorder_corr,
                gap=p_reorder_gap,
                prob_corrupt=p_corr_ratio,
                corr_corrupt=p_corr_corr,
              )
    except NetlinkError as e:
            print "can't create new queue des"+str(e)
    except Exception as e:
            exc_info = sys.exc_info()
            print "can't create new queue des"+str(exc_info)
    try:
            extra_args = {}
            if not p_dont_drop_packets:
                extra_args.update({
                    'rate': "{}kbit".format(rate or 2**22 - 1),
                    'burst': p_burst_size,
                    'action': 'drop',
                })
            ipr.tc(RTM_NEWTFILTER, 'fw', LINK_ID,0x01,
                        parent = 0x10000,
                        protocol=ETH_P_IP,
                        prio=PRIO,
                        classid=0x10001,
                        **extra_args
                        )
    except NetlinkError as e:
            print "can't create a new filter"+str(e)
    except Exception as e:
            exc_info = sys.exc_info()
            print "can't create a new filter"+str(exc_info)
      
def read_conf_set_network_emu(conf_file_name):
    stop_emu()
    with open(conf_file_name) as json_file:  
         data = json.load(json_file)
         rate = int(data["mpi_net_conf"]["rate"])
         loss_ratio = float(data["mpi_net_conf"]["loss_ratio"])
         loss_corr = int(data["mpi_net_conf"]["loss_corr"])
         dup_ratio = float(data["mpi_net_conf"]["dup_ratio"])
         delay = int (data["mpi_net_conf"]["delay"])
         delay_corr = int(data["mpi_net_conf"]["delay_corr"])
         jitter = int(data["mpi_net_conf"]["jitter"])
         delay_jitter_corr = int(data["mpi_net_conf"]["delay_jitter_corr"])
         reorder_ratio = float(data["mpi_net_conf"]["reorder_ratio"])
         reorder_corr = int(data["mpi_net_conf"]["reorder_corr"])
         reorder_gap = int(data["mpi_net_conf"]["reorder_gap"])
         corr_ratio = float(data["mpi_net_conf"]["corr_ratio"])
         corr_corr = int(data["mpi_net_conf"]["corr_corr"])
         dont_drop_packets = bool(data["mpi_net_conf"]["dont_drop_packets"])
         burst_size = int(data["mpi_net_conf"]["burst_size"])
    netem(  rate,
            loss_ratio,
            loss_corr,
            dup_ratio,
            delay,
            delay_corr,
            jitter,
            delay_jitter_corr,
            reorder_ratio,
            reorder_corr,
            reorder_gap,
            corr_ratio,
            corr_corr,
            dont_drop_packets,
            burst_size,
          )


tag_packets("mpi")
read_conf_set_network_emu("net_emu_mpi.json")


