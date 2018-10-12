#
# Cookbook:: unittests-monitoring
# Recipe:: omd
#
# Copyright:: 2018, Christian Stankowic, GPL 3.0.

# OMD sites
omd_sites = ['mon_nagios', 'mon_icinga', 'mon_icinga2', 'mon_naemon']

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
['mon_nagios', 'mon_icinga', 'mon_naemon'].each do |site|
  short_name = site[site.index('_')+1..-1]
  template("/opt/omd/sites/#{site}/etc/#{short_name}/conf.d/katprep_demo.cfg") do
    source 'nagios_katprep_demo.cfg'
    owner site
    group site
    mode '0644'
  end
end
#Icinga2
template("/opt/omd/sites/mon_icinga2/etc/icinga2/conf.d/katprep_demo.conf") do
  source 'icinga2_katprep_demo.conf'
  owner 'mon_icinga2'
  group 'mon_icinga2'
  mode '0644'
end

# enable/restart OMD service
service 'omd' do
  action [:enable,:restart]
end
