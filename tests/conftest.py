#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shared functions for unit tests
"""

from __future__ import absolute_import

import logging
import pytest

from .utilities import load_config


@pytest.fixture
def nonexisting_vm():
    """
    Return a non-existing VM name.
    :return: non-existing VM name
    """
    return "giertz.pinkepank.loc"


@pytest.fixture
def snapshot_name(virtualisation):
    """
    Return VM snapshot name based on virtualisation client type
    :param virtualisation: virtualisation client type (libvirt, pyvmomi)
    :type virtualisation: str
    :return: VM snapshot name
    """
    if virtualisation == 'libvirt':
        return "LibvirtClientTest"
    elif virtualisation == 'pyvmomi':
        return "PyvmomiClientTest"


@pytest.fixture(params=['libvirt', 'pyvmomi'])
def virtualisation(request):
    """
    Return virtualisation type based on request

    :param request: request type
    :type request: str
    :return: parameter
    """
    return request.param


@pytest.fixture
def virtConfigFile(virtualisation):
    """
    Return virtualisation configuration file name

    :param virtualisation: virtualisation client type
    :type virtualisation: str
    :return: configuration file name
    """
    if virtualisation == 'libvirt':
        return "libvirt_config.json"
    elif virtualisation == 'pyvmomi':
        return "pyvmomi_config.json"


@pytest.fixture
def virtConfig(virtConfigFile):
    """
    Loads configuration file

    :param virtConfigFile: configuration file
    :type virtConfigFile: str
    :return: JSON configuration object
    """
    return load_config(virtConfigFile)


@pytest.fixture
def virtClass(virtualisation):
    """
    Abstracting virtualisation client type

    :param virtualisation: virtualisation client type
    :type virtualisation: str
    :return: virtualisation client object
    """
    if virtualisation == 'libvirt':
        LibvirtClient = pytest.importorskip("katprep.clients.LibvirtClient")
        return LibvirtClient.LibvirtClient
    elif virtualisation == 'pyvmomi':
        PyvmomiClient = pytest.importorskip("katprep.clients.PyvmomiClient")
        return PyvmomiClient.PyvmomiClient


@pytest.fixture
def virtClient(virtualisation, virtConfig, virtClass):
    """

    :param virtualisation: virtualisation client type
    :type virtualisation: str
    :param virtConfig: configuration file
    :type virtConfig: str
    :param virtClass: virtualisation client object
    :return: virtualisation client object
    """
    if virtualisation == 'libvirt':
        address = virtConfig["config"]["uri"],
    elif virtualisation == 'pyvmomi':
        address = virtConfig["config"]["hostname"],

    return virtClass(
        logging.ERROR,
        address,
        virtConfig["config"]["api_user"],
        virtConfig["config"]["api_pass"]
    )
