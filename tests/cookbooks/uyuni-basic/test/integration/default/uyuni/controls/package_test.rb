# # encoding: utf-8

# Inspec test for recipe uyuni-basic::packages

# The Inspec reference, with examples and extensive documentation, can be
# found at http://inspec.io/docs/reference/resources/

control 'pkg-01' do
  impact 1.0
  title 'System up2date'
  desc 'Ensure that the system is updated'
  describe command('LANG=C zypper lu') do
    its('stdout') { should include "No updates found" }
  end
end

control 'pkg-02' do
  impact 1.0
  title 'Uyuni repository exists'
  desc 'Ensure that the uyuni repository exists'
  describe command('LANG=C zypper lr') do
    its('stdout') { should include('uyuni-server-stable') }
  end
end

control 'pkg-03' do
  impact 1.0
  title 'Uyuni packages installed'
  desc 'Ensure that the Uyuni packages are installed'
  describe package('patterns-uyuni_server') do
    it { should be_installed }
  end
end
