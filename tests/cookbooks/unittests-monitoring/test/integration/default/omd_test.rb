# # encoding: utf-8

# Inspec test for recipe unittests-monitoring::omd

# OMD sites
omd_sites = ['mon_nagios', 'mon_icinga', 'mon_naemon', 'mon_icinga2']
config_extension = {'nagios' => 'cfg', 'icinga' => 'cfg', 'naemon' => 'cfg', 'icinga2' => 'conf'}
url = {'nagios' => 'nagios', 'icinga' => 'icinga', 'naemon' => 'thruk', 'icinga2' => 'thruk'}
omd_username = 'omdadmin'
omd_password = 'omd'

# YUM repository
control 'katprep-unittests-mon-01' do
  impact 1.0
  title  'Consol Labs repository'
  desc   'Ensure that Consol Labs YUM repository exists'
  describe yum.repo('labs_consol_stable') do
    it { should exist }
    it { should be_enabled }
    its('baseurl') { should include 'http://labs.consol.de/repo/stable/rhel7/' }
  end
end

# ensure that the OMD packages are installed
control 'katprep-unittests-mon-02' do
  impact 1.0
  title  'OMD package installed'
  desc   'Ensure that OMD labs edition package is installed'
  describe package('omd-labs-edition') do
    it { should be_installed }
  end
end

# ensure that OMD sites are created
control 'katprep-unittests-mon-03' do
  impact 1.0
  title  'OMD sites created'
  desc   'Ensure that OMD sites are created'
  omd_sites.each do |site|
    describe command("omd sites -b") do
      its("stdout.strip") { should include site }
    end
  end
end

# ensure that OMD sites are healthy
control 'katprep-unittests-mon-04' do
  impact 1.0
  title  'OMD sites healthy'
  desc   'Ensure that OMD sites are healthy'
  describe command("omd status -b | grep OVERALL | sort -u") do
    its("stdout.strip") { should eq "OVERALL 0" }
  end
end

# ensure that OMD site configuration files are created
control 'katprep-unittests-mon-04' do
  impact 1.0
  title  'OMD sites healthy'
  desc   'Ensure that OMD sites are healthy'
  omd_sites.each do |site|
    short_name = site[site.index('_')+1..-1]
    describe file("/opt/omd/sites/#{site}/etc/#{short_name}/conf.d/katprep_demo.#{config_extension[short_name]}") do
      its('size') { should > 100 }
      its('owner') { should eq site }
      its('group') { should eq site }
      its('mode') { should cmp '0644' }
    end
    describe file("/opt/omd/sites/mon_nagios/etc/apache/conf.d/disable_nagios.conf") do
      it { should_not exist }
    end
  end
end

# ensure that http port is open
control 'katprep-unittests-mon-06' do
  impact 1.0
  title  'Web server accessable'
  desc   'Ensure that web server is listening for requests'
  describe port(80) do
    it { should be_listening }
  end
end

# ensure that http sites are accessible via HTTP Basic
control 'katprep-unittests-mon-07' do
  impact 1.0
  title  'Site login possible'
  desc   'Ensure that site logins are possible'
  omd_sites.each do |site|
    short_name = site[site.index('_')+1..-1]
    describe http("https://localhost/#{site}/#{url[short_name]}/", auth: {user: omd_username, pass: omd_password}, ssl_verify: false) do
      its('status') { should eq 200 }
    end
  end
end
