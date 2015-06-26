from __future__ import absolute_import, unicode_literals

from collections import defaultdict
import logging
import subprocess

from wheel.install import WheelFile, parse_version

log = logging.getLogger(__name__)


def call_pips(config, pip_args):
    pip_opts = ['-q', 'wheel', '--wheel-dir', str(config.wheelhouse_dpath), '--use-wheel',
                '--find-links', str(config.wheelhouse_dpath)]
    if config.verbose:
        pip_opts.pop(0)

    for pip_bin in config.pip_bins:
        all_args = [pip_bin] + pip_opts + pip_args
        log.info('Call %s', all_args)
        return_code = subprocess.call(all_args)
        if return_code != 0:
            # we had an error, don't try to finish
            return


def build_files(config):
    for req_file in config.requirement_files:
        return_code = call_pips(config, ['-r', str(req_file)])
        if return_code != 0:
            # we had an error, don't try to finish
            return


def build_packages(config, packages):
    packages = config.alias_sub(packages)
    call_pips(config, packages)


def prune_list(config):
    newest = {}
    older = list()
    wheel_files = config.wheelhouse_dpath.glob('*.whl')
    for wheel_fpath in wheel_files:
        wheel_name = wheel_fpath.name
        parts = wheel_name.split('-')
        distname, version = parts[0:2]
        wheel_key = '{}-{}'.format(distname, '-'.join(parts[2:]))
        version = parse_version(version)
        if wheel_key not in newest:
            newest[wheel_key] = (version, wheel_fpath)
        else:
            newest_version, newest_wheel_fpath = newest[wheel_key]
            if version < newest_version:
                older.append(wheel_fpath)
            else:
                older.append(newest_wheel_fpath)
    return older

