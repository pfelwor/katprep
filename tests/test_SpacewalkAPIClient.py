#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for Spacewalk API integration
"""

from __future__ import absolute_import

import logging
import ssl
import mock
import pytest
from katprep.clients.SpacewalkAPIClient import SpacewalkAPIClient
from katprep.clients import (APILevelNotSupportedException,
                             InvalidCredentialsException)

from .utilities import load_config


@pytest.fixture(scope='session')
def config():
    """
    Loads the configuration

    :return: JSON object
    """
    return load_config("spw_config.json")


@pytest.fixture
def client(config):
    """
    Instances the Spacewalk API client

    :param config: configuration file
    :type config: JSON object
    :return: Spacewalk API client object
    """
    # TODO: Instance client
    pytest.skip('Diggi, bau mich ein!')


def test_invalid_login(config):
    """
    Ensure exceptions on invalid logins
    """
    with pytest.raises(InvalidCredentialsException):
        SpacewalkAPIClient(
            logging.ERROR,
            config["config"]["hostname"],
            "giertz",
            "paulapinkepank"
        )


def test_deny_legacy(config):
    """
    Ensure that old Spacewalk APIs are refused
    """
    with mock.patch('ssl._create_default_https_context',
                    ssl._create_unverified_context):
        # we really need to skip SSL verification for old versions

        with pytest.raises(APILevelNotSupportedException):
            SpacewalkAPIClient(
                logging.ERROR,
                config["config"]["hostname_legacy"],
                config["config"]["api_user"],
                config["config"]["api_pass"],
            )
