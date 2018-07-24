#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class for managing monitoring with $PRODUCT
THIS IS A STUB - PLEASE COMPLETE IT

TODO: Copy and rename module (e.g. CheckMkAPIClient.py)
TODO: Replace $PRODUCT with the actual product name (e.g. CheckMkAPIClient)
TODO: Set LOGGER variable to module name (e.g. CheckMkAPIClient)
TODO: Import necessary Python modules (e.g. requests)
TODO: Write code for necessary functions
TODO: Write/adapt code for __calculate_time() function in accordance with
      your monitoring product (e.g. Nagios needs special format)
TODO: If necssary, adapt/remove API request alias functions (see __api_get()
      and __api_post() examples)
TODO: If necessary, set some contants (see HEADERS and SESSION examples)
TODO: Write unit tests!
"""

import logging
from katprep.clients import SessionException, EmptySetException



class MonitoringClient:
    """
    Class for communicating with the $PRODUCT API

.. class:: MonitoringClient
    """
    LOGGER = logging.getLogger('MonitoringClient')
    """
    logging: Logger instance
    """
    HEADERS = {
        'User-Agent': 'katprep (https://github.com/stdevel/katprep)',
        'Accept': 'application/json',
        'Content-Type': "application/json"
    }
    """
    SESSION = None
    """
    session: API session
    """

    def __init__(self, log_level, url,
        username="", password="", verify_ssl=False):
        """
        Constructor, creating the class. It requires specifying a
        URL, an username and password to access the API.

        :param log_level: log level
        :type log_level: logging
        :param url: Icinga URL
        :type url: str
        :param username: API username
        :type username: str
        :param password: corresponding password
        :type password: str
        """
        #set logging
        self.LOGGER.setLevel(log_level)

        #set connection data
	#...

	#connect to interface
        self.__connect()



    def __connect(self):
        """
        This function establishes a connection to the $PRODUCT API.
        """
        #self.SESSION = requests.Session()
        #if self.USERNAME != "":
        #    self.SESSION.auth = HTTPBasicAuth(self.USERNAME, self.PASSWORD)



    def __api_request(self, method, sub_url, payload=""):
        """
	Sends a XYZ request to the $PRODUCT API. This function requires XYZ.
	You cal also specify FOOBAR.
        There are also alias functions available.

        :param method: HTTP request method (GET, POST)
        :type method: str
        :param sub_url: relative path (e.g. /cgi-bin/status.cgi)
        :type sub_url: str
        :param payload: payload for POST requests
        :type payload: str
        """
        #send request to API
        try:
            #...
            self.LOGGER.debug(
                "%s request to %s (payload: %s)",
                method.upper(), sub_url, payload
            )
        except ValueError as err:
            self.LOGGER.error(err)
            raise SessionException(err)

    #Aliases
    def __api_get(self, sub_url):
        """
        Sends a HTTP GET request to the $PRODUCT API.

        :param sub_url: relative path (e.g. /cgi-bin/status.cgi)
        :type sub_url: str
        """
        return self.__api_request("get", sub_url)

    def __api_post(self, sub_url, payload):
        """
        Sends a HTTP POST request to the $PRODUCT API.

        :param sub_url: relative path (e.g. /cgi-bin/status.cgi)
        :type sub_url: str
        :param payload: payload data
        :type payload: str
        """
        return self.__api_request("post", sub_url, payload)



    def __calculate_time(self, hours):
        """
        Calculates the time range for POST requests in the format the
        $PRODUCT API requires. For this, the current time/date
        is chosen and the specified amount of hours is added.

        :param hours: Amount of hours for the time range
        :type hours: int
        """
        current_time = time.strftime("%s")
        end_time = format(
            datetime.now() + timedelta(hours=int(hours)),
            '%s')
        return (current_time, end_time)



    def __manage_downtime(
            self, object_name, object_type, hours, comment, remove_downtime
        ):
        """
        Adds or removes scheduled downtime for a host or hostgroup.
        For this, a object name and type are required.
        You can also specify a comment and downtime period.

        :param object_name: Hostname or hostgroup name
        :type object_name: str
        :param object_type: host or hostgroup
        :type object_type: str
        :param hours: Amount of hours for the downtime
        :type hours: int
        :param comment: Downtime comment
        :type comment: str
        :param remove_downtime: Removes a previously scheduled downtime
        :type remove_downtime: bool
        """
        #calculate timerange
        (current_time, end_time) = self.__calculate_time(hours)

        if object_type.lower() == "hostgroup":
            if remove_downtime:
                #remove hostgroup downtime
                #...
            else:
                #create hostgroup downtime
                #...
        else:
            if remove_downtime:
                #remove host downtime
                #...
            else:
                #create host downtime
                #...
        #send request
        #...

        #return result
        #if xyz:
        #    raise EmptySetException("Host/service not found")
        #else:
        #    return result



    def schedule_downtime(self, object_name, object_type, hours=8, \
        comment="Downtime managed by katprep"):
        """
        Adds scheduled downtime for a host or hostgroup.
        For this, a object name and type are required.
        Optionally, you can specify a customized comment and downtime
        period (the default is 8 hours).

        :param object_name: Hostname or hostgroup name
        :type object_name: str
        :param object_type: host or hostgroup
        :type object_type: str
        :param hours: Amount of hours for the downtime (default: 8 hours)
        :type hours: int
        :param comment: Downtime comment
        :type comment: str
        """
        return self.__manage_downtime(object_name, object_type, hours, \
            comment, remove_downtime=False)



    def remove_downtime(self, object_name, object_type):
        """
        Removes scheduled downtime for a host or hostgroup
        For this, a object name is required.

        :param object_name: Hostname or hostgroup name
        :type object_name: str
        :param object_type: host or hostgroup
        :type object_type: str
        """
        return self.__manage_downtime(object_name, object_type, 8, \
            "Downtime managed by katprep", remove_downtime=True)



    def has_downtime(self, object_name, object_type="host"):
        """
        Returns whether a particular object (host, hostgroup) is currently in
        scheduled downtime. This required specifying an object name and type.

        :param object_name: Hostname or hostgroup name
        :type object_name: str
        :param object_type: Host or hostgroup (default: host)
        :type object_type: str
        """
        #retrieve and load data
        try:
            #execute request
            #...

            #check if downtime
            #...
        except SessionException as err:
            if "404" in err.message:
                raise EmptySetException("Host not found")



    def get_services(self, object_name, only_failed=True):
        """
        Returns all or failed services for a particular host.

        :param object_name:
        :type object_name: str
        :param only_failed: True will only report failed services
        :type only_failed: bool
        """
        #retrieve result
        # results = ...
        services = []
        for result in results:
            #get all the service information
            service = result["display_name"]
            state = result["state"]
            self.LOGGER.debug(
                "Found service '%s' with state '%s'", service, state
            )
            if only_failed == False or float(state) != 0.0:
                #append service if ok or state not ok
                this_service = {"name": service, "state": state}
                services.append(this_service)
        if len(services) == 0:
            #empty set
            raise EmptySetException(
                "No results for host '%s'".format(object_name)
            )
        else:
            return services



    def get_hosts(self, ipv6_only=False):
        """
        Returns hosts by their name and IP.

        :param ipv6_only: use IPv6 addresses only
        :type ipv6_only: bool
        """
        #retrieve result
        #results = ...
        for result in results:
            #get all the host information
            host = result["display_name"]
            if ipv6_only:
                ip = result["address6"]
            else:
                ip = result["address"]
            this_host = {"name": host, "ip": ip}
            hosts.append(this_host)
        return hosts



    def dummy_call(self):
        """
        This function is used for checking whether authorization succeeded.
        It simply retrieves status.cgi
        """
        #retrieve data
        #result = ...
        if result != "":
            return True
        else:
            return False
