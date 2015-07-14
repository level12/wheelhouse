try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from pathlib import Path

from .appdirs import AppDirs

appdirs = AppDirs('wheelhouse', appauthor=False, multipath=True)


class Config(object):
    config_fname = 'wheelhouse.ini'

    def __init__(self, verbose):
        self.cp = None
        self.found_fpaths = None
        self.project_root_dpath = None
        self.verbose = verbose
        self.set_project_root()
        self.load_files()

    def search_fpaths(self):
        """
            Return a platform dependent list of file paths which represent locations that a
            wheelhouse.ini file might exist.

            Configs are looked for:

            1) in a user-specific file
            2) a file in the current path and every directory above until we hit the root dir.

            Configs are cumulative with more specific configuration taking precidence over
            earlier configs read.
        """
        dpaths = [Path(appdirs.user_config_dir) / self.config_fname] + self.walk_paths()
        return map(str, dpaths)

    def walk_paths(self):
        walked_paths = []
        config_dpath = Path.cwd()
        path_root = config_dpath.drive + config_dpath.root
        walked_paths.append(config_dpath)
        while True:
            config_dpath = config_dpath.parent
            walked_paths.append(config_dpath)
            if str(config_dpath) == path_root:
                # We've walked all the way up and can't go further.
                break

        return [dpath.joinpath(self.config_fname) for dpath in walked_paths]

    def set_project_root(self):
        for fpath in self.walk_paths():
            if fpath.exists():
                self.project_root_dpath = fpath.resolve().parent
                break

    def load_files(self):
        self.cp = configparser.SafeConfigParser()
        self.set_defaults()
        self.found_fpaths = self.cp.read(self.search_fpaths())

    def set_defaults(self):
        self.cp.add_section('aliases')
        self.cp.add_section('wheelhouse')
        self.cp.set('wheelhouse', 'requirement_files', '')
        self.cp.set('wheelhouse', 'requirements_path', 'requirements')
        self.cp.set('wheelhouse', 'wheelhouse_path', 'requirements/wheelhouse')
        self.cp.set('wheelhouse', 'pip_bins', 'pip')

    @property
    def requirements_dpath(self):
        return self.project_root_dpath / self.cp.get('wheelhouse', 'requirements_path')

    @property
    def wheelhouse_dpath(self):
        return self.project_root_dpath / self.cp.get('wheelhouse', 'wheelhouse_path')

    @property
    def requirement_files(self):
        retval = []
        for fname in self.cp.get('wheelhouse', 'requirement_files').strip().splitlines():
            retval.append(self.requirements_dpath / fname)
        return retval

    @property
    def pip_bins(self):
        return map(lambda x: x.strip(), self.cp.get('wheelhouse', 'pip_bins').strip().split(','))

    def alias_sub(self, package_names):
        retval = []
        for name in package_names:
            try:
                retval.append(self.cp.get('aliases', name))
            except configparser.NoOptionError:
                retval.append(name)
        return retval
