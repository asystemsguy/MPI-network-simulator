pids=$(pgrep mpi)
echo $pids
lsof -Pan -p $pids -i
sudo iptables -t mangle -A OUTPUT -m owner --pid-owner $pids -j MARK --set-mark 0x1
sudo iptables -S
