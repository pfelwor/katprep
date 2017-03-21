#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class for sending requests to pyvmomi as libvirt is still
just an endless pain when managing VMware products
"""

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import logging
import ssl
from urlparse import urlparse




class PyvmomiClient:
    """
.. class:: PyvmomiClient
    """
    SESSION = None
    """
    session: pyvmomi session
    """
    LOGGER = logging.getLogger('PyvmomiClient')
    """
    logging: Logger instance
    """

    def __init__(self, hostname, username, password):
        """
        Constructor, creating the class. It requires specifying a URI and
        a username and password for communicating with the hypervisor.
        The constructor will throw an exception if an invalid libvirt URI
        was specified. After initialization, a connection is established
        automatically.

        :param hostname: hostname
        :type hostname: str
        :param username: API username
        :type username: str
        :param password: corresponding password
        :type password: str
        """
        #set logging
        self.LOGGER.setLevel(logging.ERROR)
        #set custom port
        parsed_uri = urlparse(hostname)
        host = '{uri.path}'.format(uri=parsed_uri)
        if ":" in host:
            self.HOSTNAME = host[:host.find(':')]
            self.PORT = host[host.find(':')+1:]
        else:
            self.HOSTNAME = hostname
            self.PORT = 443
        #set connection details and connect
        self.USERNAME = username
        self.PASSWORD = password
        self.__connect()



    def __connect(self):
        """This function establishes a connection to the hypervisor."""
        global SESSION
        context = None
        #skip SSL verification for now
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()
        self.SESSION = SmartConnect(host=self.HOSTNAME,
            user=self.USERNAME, pwd=self.PASSWORD,
            port=self.PORT, sslContext=context
        )



    def __get_obj(self, content, vimtype, name):
        """
        Gets the vSphere object associated with a given text name

        :param content: Session content
        :type content: SI session
        :param vimtype: Internal pyvmomi type
        :type vimtype: pyvmomi type
        :param name: object name
        :type name: str
        """    
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True
        )
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj



    def __manage_snapshot(
            self, vm_name, snapshot_title, snapshot_text, remove_snapshot=False
        ):
        """
        Creates/removes a snapshot for a particular virtual machine.
        This requires specifying a VM, comment title and text.
        There are also two alias functions.

        :param vm_name: Name of a virtual machine
        :type vm_name: str
        :param snapshot_title: Snapshot title
        :type snapshot_title: str
        :param snapshot_text: Snapshot text
        :type snapshot_text: str
        :param remove_snapshot: Removes a snapshot if set to True
        :type remove_snapshot: bool

        """
        #make sure to quiesce and not dump memory
        #TODO: maybe we should supply an option for this?
        dumpMemory = False
        quiesce = True
        try:
            content = self.SESSION.RetrieveContent()
            vm = self.__get_obj(content, [vim.VirtualMachine], vm_name)
            if remove_snapshot:
                #get _all_ the snapshots
                snapshots = self.__get_snapshots(vm_name)
                for snapshot in snapshots:
                    childs = snapshot.childSnapshotList
                    if snapshot.name == snapshot_title:
                        #remove snapshot
                        snapshot.snapshot.RemoveSnapshot_Task(True)
                    if childs:
                        #also iterate through childs
                        for child in childs:
                            if child.name == snapshot_title:
                                child.snapshot.RemoveSnapshot_Task(True)
            else:
                #only create snapshot if not already existing
                if not self.has_snapshot(vm_name, snapshot_title):
                    task = vm.CreateSnapshot(
                        snapshot_title, snapshot_text, dumpMemory, quiesce
                    )
                else:
                    raise ValueError(
                        "Snapshot '{}' for VM '{}' already exists!".format(
                            snapshot_title, vm_name
                        )
                    )
        except ValueError as err:
            self.LOGGER.error("Unable to manage snapshot: '{}'".format(err))



    #Aliases
    def create_snapshot(self, vm_name, snapshot_title, snapshot_text):
        """
        Creates a snapshot for a particular virtual machine.
        This requires specifying a VM, comment title and text.

        :param vm_name: Name of a virtual machine
        :type vm_name: str
        :param snapshot_title: Snapshot title
        :type snapshot_title: str
        :param snapshot_text: Snapshot text
        :type snapshot_text: str
        """
        return self.__manage_snapshot(vm_name, snapshot_title, snapshot_text)

    def remove_snapshot(self, vm_name, snapshot_title):
        """
        Removes a snapshot for a particular virtual machine.
        This requires specifying a VM and a comment title.

        :param vm_name: Name of a virtual machine
        :type vm_name: str
        :param snapshot_title: Snapshot title
        :type snapshot_title: str
        """
        return self.__manage_snapshot(
            vm_name, snapshot_title, "", remove_snapshot=True
        )



    def __get_snapshots(self, vm_name):
        """
        Returns a set of all snapshots for a particular VM.

        :param vm_name: Name of a virtual machine
        :type vm_name: str
        """
        try:
            content = self.SESSION.RetrieveContent()
            container = content.viewManager.CreateContainerView(
                content.rootFolder, [vim.VirtualMachine], True
            )
            for c in container.view:
                if c.name == vm_name:
                    snapshots = c.snapshot.rootSnapshotList
                    return snapshots
        except Exception as err:
            self.LOGGER.error("Unable to get snapshots: '{}'".format(err))



    def has_snapshot(self, vm_name, snapshot_title):
        """
        Returns whether a particular virtual machine is currently protected
        by a snapshot. This requires specifying a VM name.

        :param vm_name: Name of a virtual machine
        :type vm_name: str
        :param snapshot_title: Snapshot title
        :type snapshot_title: str
        """
        content = self.SESSION.RetrieveContent()
        #get _all_ the snapshots
        snapshots = self.__get_snapshots(vm_name)
        for snapshot in snapshots:
            childs = snapshot.childSnapshotList
            if snapshot.name == snapshot_title:
                return True
            #also check childs
            elif childs:
                for child in childs:
                    if child.name == snapshot_title:
                        return True
        return False



    def get_vm_ips(self, hide_empty=True):
        """
        Returns a list of VMs and their IPs available through the current 
        connection.
        """
        try:
            #get _all_ the VMs
            content = self.SESSION.RetrieveContent() 
            result = {}
            #create view cotaining VM objects
            object_view = content.viewManager.CreateContainerView(
                content.rootFolder, [vim.VirtualMachine], True
            )
            for obj in object_view.view:
                if not hide_empty or obj.summary.guest.ipAddress != None:
                    result[obj.config.name] = {
                        "hostname": obj.summary.guest.hostName,
                        "ip": obj.summary.guest.ipAddress
                    }
            return result
        except Exception as err:
            self.LOGGER.error("Unable to get VM IP information: '{}'".format(err))



    def get_vm_hosts(self):
        """
        Returns a list of VMs and their hypervisors available through the
        current connection.
        """
        try:
            #get _all_ the VMs
            content = self.SESSION.RetrieveContent() 
            result = {}
            #create view cotaining VM objects
            object_view = content.viewManager.CreateContainerView(
                content.rootFolder, [vim.VirtualMachine], True
            )
            for obj in object_view.view:
                result[obj.config.name] = {
                    "hypervisor": obj.runtime.host.name
               }
            return result
        except ValueError as err:
            self.LOGGER.error("Unable to get VM hypervisor information: '{}'".format(err))