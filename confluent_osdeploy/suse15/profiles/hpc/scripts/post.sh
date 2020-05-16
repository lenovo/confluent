#!/bin/sh

# This script runs when install is finished, but while the installer
# is still running, with the to-be-booted system mounted in /mnt

# Carry over install-time ssh material into installed system
mkdir -p /mnt/root/.ssh/
chmod 700 /mnt/root/.ssh/
cp /root/.ssh/authorized_keys /mnt/root/.ssh/
chmd 600 /mnt/root/.ssh/authorized_keys
cp /etc/ssh/*key* /mnt/etc/ssh/
for i in /etc/ssh/*-cert.pub; do
    echo HostCertificate $i >> /mnt/etc/ssh/sshd_config
done
for i in /ssh/*.ca; do
    echo '@cert-authority *' $(cat $i) >> /mnt/etc/ssh/ssh_known_hosts
done
# Enable ~/.shosts, for the sake of root user, who is forbidden from using shosts.equiv
echo IgnoreRhosts no >> /mnt/etc/ssh/sshd_config
echo HostbasedAuthentication yes >> /mnt/etc/ssh/sshd_config
echo HostbasedUsesNameFromPacketOnly yes >> /mnt/etc/ssh/sshd_config
echo Host '*' >> /mnt/etc/ssh/ssh_config
echo "    HostbasedAuthentication yes" >> /mnt/etc/ssh/ssh_config
echo "    EnableSSHKeysign yes" >> /mnt/etc/ssh/ssh_config
# Limit the attempts of using host key. This prevents client from using 3 or 4
# authentication attempts through host based attempts
echo "    HostbasedKeyTypes *ed25519*" >> /mnt/etc/ssh/ssh_config

# In SUSE platform, setuid for ssh-keysign is required for host based,
# and also must be opted into.
echo /usr/lib/ssh/ssh-keysign root:root 4711 >> /mnt/etc/permissions.local
chmod 4711 /mnt/usr/lib/ssh/ssh-keysign

# Download list of nodes from confluent, and put it into shosts.equiv (for most users) and .shosts (for root)
nodename=$(grep ^NODENAME /tmp/confluent.info|awk '{print $2}')
curl -f -H "CONFLUENT_NODENAME: $nodename" -H "CONFLUENT_APIKEY: $(cat /tmp/confluent.apikey)" https://$mgr/confluent-api/self/nodelist > /tmp/allnodes
cp /tmp/allnodes /mnt/root/.shosts
cp /tmp/allnodes /mnt/etc/ssh/shosts.equiv

# carry over deployment configuration and api key for OS install action
mkdir -p /mnt/etc/confluent
chmod 700 /mnt/etc/confluent
cp /tmp/confluent.* /mnt/etc/confluent/
cp -a /tls /mnt/etc/confluent/
cp -a /tls/*.0 /mnt/var/lib/ca-certificates/openssl

