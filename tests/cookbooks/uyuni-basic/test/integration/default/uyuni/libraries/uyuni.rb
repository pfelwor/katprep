# encoding: utf-8
# copyright: 2019, Christian Stankowic

class Uyuni < Inspec.resource(1)
  name 'uyuni'

  def initialize(hostname, username, password)
    # set-up global parameters
    @hostname = hostname
    @username = username
    @password = password
  end

  def users
    # retrieve users
    inspec.command("spacecmd -q -u #{@username} -p #{@password} user_list").stdout.strip.split("\n")
  end

  def orgs
    # retrieve organizations
    inspec.command("spacecmd -q -u #{@username} -p #{@password} org_list").stdout.strip.split("\n")
  end
end
