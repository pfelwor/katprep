name 'uyuni-basic'
maintainer 'Christian Stankowic'
maintainer_email 'info@cstan.io'
license 'GPL-3.0'
description 'Installs/Configures Uyuni'
long_description 'Installs and configures Uyuni on openSUSE'
recipe 'uyuni-basic::packages', 'Installs Uyuni packages'
recipe 'uyuni-basic::uyuni', 'Deploys Uyuni'
supports 'opensuse'
version '0.1.0'
chef_version '>= 12.14' if respond_to?(:chef_version)

# The `issues_url` points to the location where issues for this cookbook are
# tracked.  A `View Issues` link will be displayed on this cookbook's page when
# uploaded to a Supermarket.
#
# issues_url 'https://github.com/<insert_org_here>/uyuni-basic/issues'

# The `source_url` points to the development repository for this cookbook.  A
# `View Source` link will be displayed on this cookbook's page when uploaded to
# a Supermarket.
#
# source_url 'https://github.com/<insert_org_here>/uyuni-basic'
