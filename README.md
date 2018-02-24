# MPI-network-simulator
Network is an important component in modern MPI programs running on
clusters. Understanding underlaying network properties is critical to achieve
expected performance from these programs. In this project, my work is focused
on VM based emulation of MPI network. This emulation can be used to change
properties of MPI network like delay, jitter and rate.

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
 1. Linux kernel
 2. python

## How it works
At the core of the framework, we have a MPI network emulation daemon which
when started waits for MPI jobs to run.
1 In order to shape traffic, MPIEM leverages Linux’s builtin Traffic Control
subsystem. Communication with the Traffic Control subsystem is done over the
netlink API and facilitated by pyroute2, a pure python netlink library.
MPIEM will mark all the packets that are coming from MPI jobs. Based
on that mark, a classifier will put the packets in the right ”buckets”, which
then will throttle the bandwidth, add latency, drop packets, corrupt them...
depending on the shaping settings given by user in a JSON file.

## Marking packets
Daemon waits until MPI jobs are up and Packets are marked by using iptable’s
MARK target within the mangle table. Marking is done as the packet traverses
the router on the FORWARD chain.

## Shaping packets
Each marked packet when enters the Linux network stack based on mark is
classified into different queues. Each queue represents a class of service or different
set of network properties. MPIEM creates a different queue for each MPI
process. It uses user given config file to set properties of each queue.
