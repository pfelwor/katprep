# unittests-monitoring

This cookbook installs [OMD Labs Edition](https://labs.consol.de/omd/) on a RHEL/CentOS machine. It also configures the following monitoring sites for katprep unit testing:
- Nagios
- Icinga 1.x
- Icinga 2.x
- Naemon

All monitoring sites are configured with two demo hosts and various services used for unit testing.

## Usage
To set-up the instance choose one of the following possibilities.

### Via kitchen
Make sure to have [ChefDK](https://downloads.chef.io/chefdk) installed, before executing the following command within the **unittests-monitoring** directory:

```
$ kitchen verify
...
Profile Summary: 5 successful controls, 0 control failures, 0 controls skipped
Test Summary: 25 successful, 0 failures, 0 skipped
-----> Kitchen is finished.
```

Afterwards, alter the Vagrant instance like this in order to enable port forwarding:
```
$ cd .kitchen/kitchen-vagrant/default-bento-centos-75
$ vi Vagrantfile
Vagrant.configure("2") do |c|
  ...
  c.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  c.vm.network "forwarded_port", guest: 443, host: 8443, host_ip: "127.0.0.1"
  c.vm.network "forwarded_port", guest: 5665, host: 8665, host_ip: "127.0.0.1"
  end
end

ESC ZZ

$ vagrant reload
```

### Via Vagrant-only
If you want to use Vagrant standalone, create a **nodes** directory and use the supplied Vagrantfile from the **test** directory:

```
$ cd ../../
$ mkdir nodes
$ vagrant up --provision
```

On several platforms, including Microsoft Windows, running the command might result in the following error:
```
FATAL: Configuration error NoMethodError: undefined method `<<' for nil:NilClass
FATAL:   /tmp/vagrant-chef/client.rb:22:in `from_string'
FATAL: Aborting due to error in '/tmp/vagrant-chef/client.rb'
```

In this case, [removing the vagrant-ohai plugin](https://github.com/hashicorp/vagrant/issues/9040) might fix it:
```
$ vagrant plugin uninstall vagrant-ohai
```
