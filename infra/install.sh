apt-get update
apt-get install -y  mpich
apt-get install -y sshpass

mkdir -p /home/vagrant/.ssh
chmod 700 /home/vagrant/.ssh
chown -R vagrant:vagrant /home/vagrant/.ssh

cat >  ~/.ssh/config  << EOF1
IdentityFile /home/vagrant/files/ssh/`hostname`
EOF1

su vagrant -c "rm /home/vagrant/files/ssh/`hostname`*"
su vagrant -c "ssh-keygen -t rsa -P '' -f /home/vagrant/files/ssh/`hostname`"

cat >  ~/.ssh/config  << EOF1
IdentityFile /home/vagrant/files/ssh/`hostname`
EOF1

#execute this when booted up
#sshpass -p vagrant ssh-copy-id -i /home/vagrant/files/ssh/`hostname` VM2
#sshpass -p vagrant ssh-copy-id -i /home/vagrant/files/ssh/`hostname` VM1

