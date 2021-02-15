import re
import os
import sys

# This class will bump the version in the setup.py file under the current directory (script will be run from root)
# This class will only promote the patch number (updates of the major and minor versions should be done manually
# when needed)
class Version_Bumper(object):

    SETUP_FILENAME = '__init__.py'
    SNAPSHOT_SUFFIX = '.dev'
    VERSION_SUFFIX = '.ni'
    VERSION = '__version__'
    SHA = '__sha__'
    VERSION_FORMAT = '((\d+\.\d+\.)(\d+)\.?\w*)'

    def __init__(self, is_release, suffix):
        self.__release = is_release
        self.__suffix = suffix

    # in the case we are in a release flow -- the patch will be promoted
    # in the case we are in a snapshot flow -- the patch will be promoted and a .dev suffix will be added
    def bump_version(self):

        tempfile = 'temp_init.py'

        with open(Version_Bumper.SETUP_FILENAME, 'r') as input_file:
            with open(tempfile, 'w') as output_file:
                for line in input_file:
                    if Version_Bumper.VERSION in line:
                        old_version, next_version = self._calc_versions(line)
                        output_file.write(line.replace(old_version, next_version))
                    else:
                        output_file.write(line)

        os.remove(Version_Bumper.SETUP_FILENAME)
        os.rename(tempfile, Version_Bumper.SETUP_FILENAME)
        return next_version
        
    def _calc_versions(self, line):
        # type: (str) -> tuple
        
        match = re.search(Version_Bumper.VERSION_FORMAT, line)
        
        if match is None:
            raise Exception('Version number in {} must follow the convention x.y.z. Version NOT bumped'.format(Version_Bumper.SETUP_FILENAME))
        
        version = match.group(1)
        version_prefix = match.group(2)
        patch_number = int(match.group(3))

        old_version = version
        next_version = version_prefix + self._get_next_version_number(patch_number)

        return old_version, next_version

    def _get_next_version_number(self, patch_number):
        # type: (int) -> str
        
        next_version_number = str(patch_number + 1)

        if not self.__release:
            next_version_number += Version_Bumper.SNAPSHOT_SUFFIX

        if self.__suffix:
            next_version_number += Version_Bumper.VERSION_SUFFIX

        return next_version_number



def main():

    RELEASE_MODE = 'release'
    DEV_MODE = 'dev'
    SUFFIX = 'ni'
    args = sys.argv

    if len(args) > 3:
       raise Exception('Script should be invoked with one command line argument indicating if we are in release mode')
    if args[1] not in [RELEASE_MODE, DEV_MODE]:
        raise Exception('Script should be invoked with either \'release\' or \'dev\'')

    bumper = Version_Bumper(True if args[1] == RELEASE_MODE else False, SUFFIX in args or False)
    return bumper.bump_version()



print(main())