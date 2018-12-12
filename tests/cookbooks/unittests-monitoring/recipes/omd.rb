#
# Cookbook:: unittests-monitoring
# Recipe:: omd
#
# Copyright:: 2018, Christian Stankowic, GPL 3.0.

# OMD sites
omd_sites = ['mon_nagios', 'mon_icinga', 'mon_naemon', 'mon_icinga2']
config_family = {'nagios' => 'nagios', 'icinga' => 'nagios', 'naemon' => 'nagios', 'icinga2' => 'icinga2'}
config_extension = {'nagios' => 'cfg', 'icinga' => 'cfg', 'naemon' => 'cfg', 'icinga2' => 'conf'}
# never _ever_ change order here as really bad things will happen then

# add EPEL repository (for dependencies)
yum_package 'epel-release'

# add Consol Lab repo
yum_repository 'labs_consol_stable' do
  baseurl 'http://labs.consol.de/repo/stable/rhel7/$basearch'
  gpgkey  'http://labs.consol.de/repo/stable/RPM-GPG-KEY'
  action  :create
end

# add OMD packages
yum_package 'omd-labs-edition'

# add OMD sites
omd_sites.each do |site|
  execute "omd-create-#{site}" do
    command "/bin/omd create #{site}"
    # we need to ignore failures as we want to be able to converge multiple times
    ignore_failure true
  end
end

# add OMD site configurations
omd_sites.each do |site|
  template("/opt/omd/sites/#{site}/etc/omd/site.conf") do
    source "site.conf.#{site}"
    owner site
    group site
    mode '0644'
  end
end

# add OMD monitoring configuration
omd_sites.each do |site|
  short_name = site[site.index('_')+1..-1]
  template("/opt/omd/sites/#{site}/etc/#{short_name}/conf.d/katprep_demo.#{config_extension[short_name]}") do
    source "#{config_family[short_name]}_katprep_demo.#{config_extension[short_name]}"
    owner site
    group site
    mode '0644'
  end
end

# yep, we want to have insecure Nagios stuff
file("/opt/omd/sites/mon_nagios/etc/apache/conf.d/disable_nagios.conf") do
  action [:delete]
end

# Icinga2 API user
template("/opt/omd/sites/mon_icinga2/etc/icinga2/conf.d/api-omd.conf") do
  source 'api-omd.conf'
  owner 'mon_icinga2'
  group 'mon_icinga2'
  mode '0644'
end
execute "omd-icinga2-api" do
  user 'root'
  # yep, kinda ugly - but it works
  command 'su - mon_icinga2 -c "icinga2 api setup"'
end

# enable/restart OMD service
service 'omd' do
  action [:enable,:restart]
end
