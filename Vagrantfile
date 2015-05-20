# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 1
      v.name = "Bizness"
  end
  config.ssh.forward_agent = true
  config.vm.provision "ansible" do |ansible|
    ansible.host_key_checking = false
    ansible.extra_vars = { ansible_connection: 'ssh', ansible_ssh_args: '-o ForwardAgent=yes' }
    ansible.raw_ssh_args = ['-o UserKnownHostsFile=/dev/null']
    ansible.playbook = "provision/vagrant.yml"
    ansible.verbose = "vvvv"
  end

  config.vm.network "forwarded_port", guest: 5432, host: 5432
  config.vm.network "forwarded_port", guest: 5000, host: 5000
end
