DISCOVER_NODES ||= 0
PROVISION_MAAS ||= TRUE
SSH_TUNNEL ||= FALSE

vagrant_dir = File.expand_path(File.dirname(__FILE__))
if File.exists?(File.join(vagrant_dir, 'Vagrantfile.custom'))
  eval(IO.read(File.join(vagrant_dir, 'Vagrantfile.custom')), binding)
end


Vagrant.configure("2") do |config|
  config.vm.define :maas do |maas|
    maas.vm.box = "generic/ubuntu1804"
    maas.vm.hostname = "maas-region"
    maas.vm.provider :libvirt do |domain|
      domain.driver = "qemu"
      domain.memory = 2048
      domain.cpus = 2
      domain.nested = true
    end

    maas.vm.network "private_network", libvirt__network_name: "pxe", libvirt__dhcp_enabled: false, ip: "192.168.61.8"

    if SSH_TUNNEL
      maas.vm.network :forwarded_port, guest: 5240, host: 80, host_ip: "0.0.0.0"
    end

    $script = <<-'SCRIPT'
    sudo add-apt-repository ppa:maas/2.8 && apt install maas -y
    maas createadmin --username admin --password admin --email openstack@trendyol.com
    maas apikey --username admin > api_key
    cat api_key
    SCRIPT
    
    if PROVISION_MAAS
      maas.vm.provision "shell", inline: $script
    end

  end

  if DISCOVER_NODES > 0
    (1..self.class.const_get("DISCOVER_NODES")).each do |i|
      config.vm.define "discover-#{i}" do |discover|
        discover.vm.provider :libvirt do |domain|
          domain.memory = 2048
          domain.cpus = 2
          domain.nested = true
          domain.mgmt_attach = false
            boot_network = {'network' => 'pxe'}
            domain.storage :file, :size => '20G', :type => 'qcow2'
            domain.boot boot_network
        end
        discover.vm.network "private_network", libvirt__network_name: "pxe", libvirt__dhcp_enabled: false
      end
    end
  end
end