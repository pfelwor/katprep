#
# Cookbook:: uyuni-basic
# Recipe:: packages
#
# Copyright:: 2018, Christian Stankowic, All Rights Reserved.

# ensure we're up2date
execute 'zypper_update' do
  command 'zypper up -y'
end

# Uyuni zypper repository
zypper_repository 'uyuni' do
  baseurl       'https://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Stable/images/repo/Uyuni-Server-4.0-POOL-x86_64-Media1/'
  description   'Uyuni Server Stable'
  gpgkey        'https://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Stable/images/repo/Uyuni-Server-4.0-POOL-x86_64-Media1/media.1/products.key'
  repo_name     'uyuni-server-stable'
end

# Uyuni packages
zypper_package 'uyuni_packages' do
  package_name 'patterns-uyuni_server'
  retries 5
end
