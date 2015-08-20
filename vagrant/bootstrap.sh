#!/bin/bash

# Deps
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -q
sudo apt-get install -q -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" openjdk-7-jre

tempdir=$(mktemp -d)
cd $tempdir

# ES
wget -q https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.1.deb
dpkg -i elasticsearch-1.7.1.deb
update-rc.d elasticsearch defaults
/etc/init.d/elasticsearch start

# Kibana
wget -q https://download.elastic.co/kibana/kibana/kibana-4.0.3-linux-x64.tar.gz
mkdir /usr/local/share/kibana
tar -xzf kibana-4.0.3-linux-x64.tar.gz -C /usr/local/share/kibana --strip-components=1
wget -q https://gist.githubusercontent.com/TronPaul/2d3a238024875efa100a/raw/e841dd37c2b09a5968f5af4c79b4a4005538084f/kibana -O /etc/init.d/kibana
chmod +x /etc/init.d/kibana
update-rc.d kibana defaults
/etc/init.d/kibana start
