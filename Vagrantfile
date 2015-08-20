# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.provision 'shell', privileged: true, path: 'vagrant/bootstrap.sh'

  config.vm.network 'forwarded_port', guest: 9200, host: 9200
  config.vm.network 'forwarded_port', guest: 5601, host: 5601
end
