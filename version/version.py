#!/usr/bin/env python
import os, re, logging, sys
from os.path import dirname

_LOG = logging.getLogger(__name__)

my_dir = dirname(__file__)

class VersionPattern:
    """
    Version pattern class
    """

    def __init__(self, is_release):
        self.path = os.path.join(*[my_dir, "__init__.py"])
        self.__release = is_release
        self.patterns_parser = self._patterns_parser()

    def git_version(self):
        """
        Return a tag of the latest version and its commit hash.
        :return: A latest_tag and latest_tag_commit
        """
        try:
            import git

            try:
                repo = git.Repo(os.path.join(*[my_dir, "../.git"]))
            except git.NoSuchPathError:
                _LOG.warning('.git directory not found: Cannot compute the git version')
                return ''
            except git.InvalidGitRepositoryError:
                _LOG.warning('Invalid .git directory not found: Cannot compute the git version')
                return ''
        except ImportError:
            _LOG.warning('gitpython not found: Cannot compute the git version.')
            return ''
        if repo:
            # tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
            # latest_tag = tags[-1]
            if not self.__release:
                latest_tag_commit = repo.head.commit
                tag = next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)
                print("repo.head.commit: " + str(repo.head.commit))
                print("repo.head.tag: " + str(tag))
                tag_off = os.getenv('GIT_TAG')
                print("repo.head.GIT_TAG : " + str(tag_off))
                print("repo.head.repo repo: " + str(repo))
                tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
                print("tags All dev: " + str(tags))
                print("repo.tags All dev: " + str(repo.tags))
                latest_tag = tags[-1]
                print("latest_tag2 dev: " + str(latest_tag))
                # latest_tag = ""
            else:
                tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
                latest_tag1 = tags[-1]
                latest_tag = tags[0]
                print("latest_tag1: " + str(latest_tag1))
                print("latest_tag2: " + str(latest_tag))
                print("tags All: " + str(tags))
                latest_tag_commit = latest_tag.commit
            return latest_tag, latest_tag_commit

        return 'no_git_version'

    def replace(self, pattern: str, new_version: str):
        """
        Update the versions matching this pattern.
        This method reads the underlying file, replaces each occurrence of the
        matched pattern, then writes the updated file.
        :param new_version: The new version number as a string
        """

        with open(self.path, "r") as f:
            old_content = f.read()

        new_content = re.sub(pattern, r'\1 = "{0}"'.format(new_version), old_content, flags=re.MULTILINE)

        _LOG.debug(
            f"Writing new version number: path={self.path!r} version={new_version!r}"
        )

        with open(self.path, mode="w") as f:
            f.write(new_content)

    def _patterns_parser(self):
        """
        Return the versions matching this pattern.
        Because a pattern can match in multiple places, this method returns a
        set of matches.
        """
        latest_tag, latest_tag_commit = self.git_version()
        patterns_parser = [
            {'pattern': r'^(__sha__) = .*$', 'new_version': latest_tag_commit}
        ]

        # if self.__release:
        if not self.__release:
            patterns_parser += [
                {'pattern': r'^(__version__) = .*$', 'new_version': latest_tag}
            ]

        return patterns_parser

    def write_version(self):
        """
        Write the Semver version + git hash to file.
        """
        for parser in self.patterns_parser:
            self.replace(parser['pattern'], parser['new_version'])
            _LOG.debug(
                f"Writing new version number: path={self.path!r} version={parser['new_version']!r}"
            )

        return True

# def do_setup() -> None:
#     version = VersionPattern()
#     version.write_version()

# if __name__ == "__main__":
#     do_setup()

def main():
    RELEASE_MODE = 'release'
    DEV_MODE = 'dev'
    args = sys.argv

    if len(args) > 2:
        raise Exception('Script should be invoked with one command line argument indicating if we are in release mode or dev mode')
    if args[1] not in [RELEASE_MODE, DEV_MODE]:
        raise Exception('Script should be invoked with either \'release\' or \'dev\'')

    version = VersionPattern(True if args[1] == RELEASE_MODE else False)
    version.write_version()

if __name__ == "__main__":
    main()