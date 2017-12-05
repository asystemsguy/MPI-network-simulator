apt-get update
apt-get install -y  mpich
mkdir -p /home/vagrant/.ssh
chmod 700 /home/vagrant/.ssh
chown -R vagrant:vagrant /home/vagrant/.ssh
su vagrant -c "ssh-keygen -t rsa -P '' -f /home/vagrant/.ssh/id_rsa"

mkdir -p /vagrant/files/ssh
cp /home/vagrant/.ssh/id_rsa.pub /vagrant/files/ssh/`hostname`.pub

