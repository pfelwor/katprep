#
# Cookbook:: uyuni-basic
# Recipe:: uyuni
#
# Copyright:: 2018, Christian Stankowic, All Rights Reserved.

# stage the environment file
# TODO: replace values with parameters?
template '/root/setup_env.sh' do
  source 'setup_env.sh.erb'
  owner  'root'
  group  'root'
  mode   '0644'
end

# finally setup Uyuni
# TODO: avoid re-run?
execute 'uyuni_setup' do
  command '/usr/lib/susemanager/bin/mgr-setup -s'
end

# create initial organization and user


# TODO: customization
# Activation keys, repositories, 
