#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import subprocess
import shelve

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

packages = sys.argv[1:]
# filter manifest files
packages = [v for v in packages if "Manifest" not in v]
gentoo_repo = '../gentoo/'


def command(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,
                            universal_newlines=True)
    for line in proc.stdout:
        a = line.strip('')
        print(a)

conf_var = "shelve"
d = shelve.open(conf_var)
d["version"] = []

versions = []

for package in packages:
    ebuild_location = gentoo_repo + package
    ebuild_full = 'ROOT=kernel_sources/ /usr/bin/ebuild ' + ebuild_location
    ebuild_manifest = ebuild_full + ' manifest'
    ebuild_merge = ebuild_full + ' merge '

    cmd_emg_manifest = 'echo "' + ebuild_manifest + \
        '" > ebuild_manifest.sh && chmod +x ebuild_manifest.sh'
    command(cmd_emg_manifest)
    cmd_emg_merge = 'echo "' + ebuild_merge + \
        '" > ebuild_merge.sh && chmod +x ebuild_merge.sh'
    command(cmd_emg_merge)
    command('./ebuild_merge.sh')
    command('./ebuild_manifest.sh')
    versions.append(package)

d["version"] = versions
d.close()
