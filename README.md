# MPI-network-emulation (MPINETEM)
Network is an important component in modern MPI programs running on clusters. Understanding underlaying network properties is critical to achieve expected performance from these programs. In this project, my work is focused on VM based emulation of MPI network properties. This emulation can be used to change properties of MPI network like delay, jitter and packet transfer rate of MPI process running on linux nodes.

## Emulated Network properties
 1. Delay
 2. Jitter
 3. Delay distribution
 4. Packet loss
 5. Packet duplication
 6. Packet corruption
 7. Packet re-ordering
 8. Rate control or Gap

## Requirements
MPINETEM runs on any router or cluster node that runs linux kernel and has python installed.

## How it works
At the core of the framework, we have an MPI network emulation daemon which when started waits for MPI jobs to run. To shape network traffic coming out of MPI process, MPI network emulation (MPINETEM) leverages Linux’s built-in Traffic Control Subsystem. Communication with the traffic control subsystem of linux kernel is done over the Netlink API and facilitated by pyroute2, a pure python Netlink library. MPI network emulation will mark all the packets that are coming from MPI jobs. Based on that mark, a classifier will put the packets in the right ”buckets”, which then will throttle the bandwidth, add latency, drop packets or corrupt them... depending on the shaping settings given by a user in a JSON file.

## Marking packets
Daemon waits until MPI jobs are up and Packets are marked by using iptable’s MARK target within the mangle table. Marking is done as the packet traverses the router on the FORWARD chain.

## Shaping packets
Each marked packet when enters the Linux network stack based on mark is classified into different queues. Each queue represents a class of service or different set of network properties. MPIEM creates a different queue for each MPI
process. It uses user given config file to set properties of each queue.
