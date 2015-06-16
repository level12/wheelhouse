import logging
import subprocess

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

