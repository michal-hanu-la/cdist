#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 2010-2011 Nico Schottelius (nico-cdist at schottelius.org)
#
# This file is part of cdist.
#
# cdist is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cdist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cdist. If not, see <http://www.gnu.org/licenses/>.
#
#

import logging
import os
#import stat
#import shutil
#import sys
#import tempfile
#import time
#
#import cdist.core
#import cdist.exec

class Context:
    """Hold information about current context"""

    def __init__(self, 
        target_host,
        initial_manifest=False,
        base_path=False,
        exec_path=sys.argv[0]):

        self.target_host    = target_host

        # Only required for testing
        self.exec_path      = exec_path

        # Context logging
        self.log = logging.getLogger(__name__)
        self.log.addFilter(self)

        # Base and Temp Base 
        self.base_path = (base_path or
            self.base_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.pardir, os.pardir))

        # Local input
        self.cache_path             = os.path.join(self.base_path, "cache", 
            self.target_host)
        self.conf_path              = os.path.join(self.base_path, "conf")

        self.global_explorer_path   = os.path.join(self.conf_path, "explorer")
        self.manifest_path          = os.path.join(self.conf_path, "manifest")
        self.type_base_path         = os.path.join(self.conf_path, "type")
        self.lib_path               = os.path.join(self.base_path, "lib")

        self.initial_manifest = (initial_manifest or
            os.path.join(self.manifest_path, "init"))

        # Local output
        if '__cdist_out_dir' in os.environ:
            self.out_path = os.environ['__cdist_out_dir']
        else:
            self.out_path = os.path.join(tempfile.mkdtemp(), "out")
        self.bin_path                 = os.path.join(self.out_path, "bin")
        self.global_explorer_out_path = os.path.join(self.out_path, "explorer")
        self.object_base_path         = os.path.join(self.out_path, "object")

        # Remote directory base
        if '__cdist_remote_out_dir' in os.environ:
            self.remote_base_path = os.environ['__cdist_remote_out_dir']
        else:
            self.remote_base_path = "/var/lib/cdist"

        self.remote_conf_path            = os.path.join(self.remote_base_path, "conf")
        self.remote_object_path          = os.path.join(self.remote_base_path, "object")

        self.remote_type_path            = os.path.join(self.remote_conf_path, "type")
        self.remote_global_explorer_path = os.path.join(self.remote_conf_path, "explorer")

    def cleanup(self):
        # Do not use in __del__:
        # http://docs.python.org/reference/datamodel.html#customization
        # "other globals referenced by the __del__() method may already have been deleted 
        # or in the process of being torn down (e.g. the import machinery shutting down)"
        #
        log.debug("Saving " + self.out_path + " to " + self.cache_path)
        # FIXME: raise more beautiful exception / Steven: handle exception
        # Remove previous cache
        if os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path)
        shutil.move(self.out_path, self.cache_path)

    def filter(self, record):
        """Add hostname to logs via logging Filter"""

        record.msg = self.target_host + ": " + record.msg

        return True
