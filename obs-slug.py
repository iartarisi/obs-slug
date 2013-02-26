#!/usr/bin/env python
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import glob
import os.path
import re
import subprocess
import sys


PROJECT = "Cloud:OpenStack:Master"
SYSTEM = "openSUSE_12.2"
ARCH = "x86_64"
DOWNLOADS = "binaries/"


def zypp_install(package):
    p = subprocess.Popen(["zypper", "--non-interactive", "install", package],
                         stdout=subprocess.PIPE)
    if p.wait() == 0:
        print "Package %s installed." % package
        return

    zypp_output = p.stdout.read()
    print zypp_output
    dependency = re.search("nothing provides (\S+)", zypp_output).group(1)
    osc_getbinaries(dependency)
    zypp_install(package)


def zypp_local(package):
    p = subprocess.Popen(["zypper", "--non-interactive", "install",
                          glob.glob(os.path.join(DOWNLOADS, package)
                                    + "-[0-9]*")[0]],
                         stdout=subprocess.PIPE)

    if p.wait() != 0:
        output = p.stdout.read()
        print output
        print "Couldn't install downloaded package %s." % package
        try:
            dependency = re.search("nothing provides (\S+)",
                                   output).group(1)
        except AttributeError:
            print "Don't know how to deal with this error."

        osc_getbinaries(dependency)
        zypp_local(package)  # call zypp_local again after we have the dep


def osc_getbinaries(package):
    print "Downloading %s with osc getbinaries..." % package
    p = subprocess.Popen(
        ["osc", "getbinaries", PROJECT, package, SYSTEM, ARCH],
        stdout=subprocess.PIPE)
    if p.wait() != 0:
        print "Couldn't download package."

    print p.stdout.read()
    zypp_local(package)


if __name__ == "__main__":
    zypp_install(sys.argv[1])
