#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shared unit test functions
"""

import json
import os
import pytest


def load_config(config_file):
    """
    Loads a configuration file

    :param config_file: filename
    :type config_file: str
    :return: JSON object
    """
    if not os.path.isfile(config_file):
        pytest.skip("Please create configuration file %s!" % config_file)

    try:
        with open(config_file, "r") as json_file:
            return json.load(json_file)
    except IOError as err:
        pytest.skip("Unable to read configuration file: '%s'" % err)
