# # encoding: utf-8

# Inspec test for recipe uyuni-basic::uyuni

# The Inspec reference, with examples and extensive documentation, can be
# found at http://inspec.io/docs/reference/resources/

control 'app-01' do
  impact 1.0
  title 'Web server running'
  desc 'Ensure that the server is listening'
  describe port(80) do
    it { should be_listening }
  end
  describe port(443) do
    it { should be_listening }
  end
end

control 'app-02' do
  impact 1.0
  title 'Jabber running'
  desc 'Ensure that the Jabber server is listening'
  describe port(5222) do
    it { should be_listening }
  end
  describe port(5269) do
    it { should be_listening }
  end
end

control 'app-03' do
  impact 1.0
  title 'Salt running'
  desc 'Ensure that the Salt server is listening'
  describe port(4505) do
    it { should be_listening }
  end
  describe port(4506) do
    it { should be_listening }
  end
end

control 'app-04' do
  impact 1.0
  title 'PostgreSQL running'
  desc 'Ensure that the PostgreSQL server is listening'
  describe port(5432) do
    it { should be_listening }
  end
end

control 'app-05' do
  impact 1.0
  title 'Uyuni database deployed'
  desc 'Ensure that the Uyuni databaase is deployed'
  describe file('/var/lib/pgsql/data/pg_hba.conf') do
    its('content') { should include 'uyuni' }
  end
end

control 'app-06' do
  impact 1.0
  title 'Installation files'
  desc 'Ensure that the installation script was removed'
  describe file ('/root/uyuni_initial_setup.sh') do
    it { should_not exist }
  end
  describe file ('/root/.MANAGER_SETUP_COMPLETE') do
    it { should exist }
  end
  describe file ('/root/.MANAGER_INITIALIZATION_COMPLETE') do
    it { should exist }
  end
end

# TODO: find a way to utilize node attributes?
uyuni_user = attribute('uyuni_username', description: 'Uyuni admin username', default: 'vagrant')
uyuni_pass = attribute('uyuni_password', description: 'Uyuni admin password', default: 'vagrant')
control 'app-07' do
 impact 1.0
 title 'Initial content created'
 desc 'Ensure that the admin user and organization is created'
 describe uyuni('localhost', uyuni_user, uyuni_pass) do
   its('users') { should include 'vagrant' }
   its('orgs') { should include 'Vagrant' }
 end
end
