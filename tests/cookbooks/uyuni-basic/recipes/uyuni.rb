#
# Cookbook:: uyuni-basic
# Recipe:: uyuni
#
# Copyright:: 2018, Christian Stankowic, All Rights Reserved.

# stage the environment file

template '/root/setup_env.sh' do
  source 'setup_env.sh.erb'
  variables( :uyuni => node['uyuni'])
  owner  'root'
  group  'root'
  mode   '0644'
end

# setup Uyuni database
execute 'uyuni_setup' do
 command '/usr/lib/susemanager/bin/mgr-setup -s'
 creates '/root/.MANAGER_SETUP_COMPLETE'
end

# create initial organization and user
template '/root/uyuni_initial_setup.sh' do
  source 'uyuni_initial_setup.sh.erb'
  variables( :uyuni => node['uyuni'])
  owner  'root'
  group  'root'
  mode   '0700'
  not_if { ::File.exist?('/root/.MANAGER_INITIALIZATION_COMPLETE') }
end
execute 'uyuni_initial_setup' do
  command '/root/uyuni_initial_setup.sh'
  creates '/root/.MANAGER_INITIALIZATION_COMPLETE'
end

# remove script
file '/root/uyuni_initial_setup.sh' do
  action [ :delete ]
end

# TODO: additional customization such as
# activation keys, repositories,...
