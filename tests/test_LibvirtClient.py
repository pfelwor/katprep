#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for Libvirt integration
"""

from __future__ import absolute_import

import logging
import pytest
from katprep.clients import (EmptySetException, InvalidCredentialsException,
                             SessionException)

from .utilities import load_config


@pytest.fixture(scope="session")
def config():
    return load_config("libvirt_config.json")


@pytest.fixture
def client(config):
    LibvirtClient = pytest.importorskip("katprep.clients.LibvirtClient")

    return LibvirtClient.LibvirtClient(
        logging.ERROR,
        config["config"]["uri"],
        config["config"]["api_user"],
        config["config"]["api_pass"]
    )


def test_invalid_login(config):
    """
    Ensure exceptions on invalid logins
    """
    LibvirtClient = pytest.importorskip("katprep.clients.LibvirtClient")

    with pytest.raises(InvalidCredentialsException):
        LibvirtClient.LibvirtClient(
            logging.ERROR,
            config["config"]["uri"],
            "giertz", "paulapinkepank"
        )

        # TODO: make a call?
        # api_dummy.get_vm_ips


@pytest.fixture
def nonexisting_vm():
    return "giertz.pinkepank.loc"


@pytest.fixture
def snapshot_name():
    return "LibvirtClientTest"


def test_create_snapshot_fail(client, nonexisting_vm, snapshot_name):
    """
    Ensure that creating snapshots of non-existing VMs is not possible
    """
    with pytest.raises(SessionException):
        client.create_snapshot(nonexisting_vm, snapshot_name, snapshot_name)


def test_remove_snapshot_fail(client, nonexisting_vm, snapshot_name):
    """
    Ensure that removing snapshots of non-existing VMs is not possible
    """
    with pytest.raises(SessionException):
        client.remove_snapshot(nonexisting_vm, snapshot_name)


def test_has_snapshot_fail(client, nonexisting_vm, snapshot_name):
    """
    Ensure that checking non-existing VMs for snapshots is not possible
    """
    with pytest.raises(EmptySetException):
        client.has_snapshot(nonexisting_vm, snapshot_name)


def test_revert_snapshot_fail(client, nonexisting_vm, snapshot_name):
    """
    Ensure that reverting non-existing snapshots is not possible
    """
    with pytest.raises(SessionException):
        client.revert_snapshot(nonexisting_vm, snapshot_name)


def test_snapshot_handling(client, config, snapshot_name):
    client.create_snapshot(
        config["valid_objects"]["vm"],
        snapshot_name,
        snapshot_name
    )

    try:
        client.revert_snapshot(config["valid_objects"]["vm"], snapshot_name)

        try:
            assert client.has_snapshot(
                config["valid_objects"]["vm"],
                snapshot_name
            )
        except EmptySetException as err:
            print(err)
    finally:
        client.remove_snapshot(config["valid_objects"]["vm"], snapshot_name)
