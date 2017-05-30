from __future__ import absolute_import, unicode_literals

import logging
import os
import subprocess

from wheel.install import parse_version

log = logging.getLogger(__name__)


def pip_env(config, no_index=False, pre=False):
    newenv = os.environ.copy()
    newenv['PIP_USE_WHEEL'] = 'true'
    newenv['PIP_FIND_LINKS'] = str(config.wheelhouse_dpath)
    newenv['PIP_WHEEL_DIR'] = str(config.wheelhouse_dpath)
    if no_index:
        newenv['PIP_NO_INDEX'] = 'true'
    if pre:
        newenv['PIP_PRE'] = 'true'
    if config.verbose:
        newenv['PIP_VERBOSE'] = 'true'
    return newenv


def call_pips(config, env, pip_args):
    for pip_bin in config.pip_bins:
        all_args = [pip_bin] + pip_args
        log.info('Call %s', all_args)
        return_code = subprocess.call(all_args, env=env)
        if return_code != 0:
            # we had an error, don't try to finish
            log.info('pip returned non-zero code: %d', return_code)
            return True


def build_files(config):
    log.info('build files')
    for req_file in config.requirement_files:
        log.info('build req file: %s', req_file)
        had_error = call_pips(config, pip_env(config), ['wheel', '-r', str(req_file)])
        if had_error:
            log.error('pip had an error, not processing all requirements files')
            return


def build_packages(config, packages):
    packages = config.alias_sub(packages)
    call_pips(config, pip_env(config), ['wheel'] + packages)


def install(config, pip_args):
    env = pip_env(config, no_index=True, pre=True)
    call_pips(config, env, ['install', '-U'] + pip_args)


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
