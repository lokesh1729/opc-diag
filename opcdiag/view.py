# -*- coding: utf-8 -*-
#
# view.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Objects that fulfill the view role in opc-diag, interfacing to the console
"""

from __future__ import print_function, unicode_literals

import sys


def _write(text):
    """
    Write *text* to stdout
    """
    print(text, end='', file=sys.stdout)


class OpcView(object):
    """
    Interfaces to the console by formatting command results for proper
    display.
    """

    @staticmethod
    def pkg_item(pkg_item):
        """
        Display the text value of pkg_item, adding a linefeed at the end to
        make the terminal happy.
        """
        text = '%s\n' % pkg_item.text
        _write(text)