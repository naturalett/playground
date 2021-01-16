#!/usr/bin/env python
import os, re, logging
from os.path import dirname


logger = logging.getLogger(__name__)

my_dir = dirname(__file__)

class VersionPattern:
    def __init__(self, path: str):
        self.path = path
        self._field_behaviours: List = []

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
                logger.warning('.git directory not found: Cannot compute the git version')
                return ''
            except git.InvalidGitRepositoryError:
                logger.warning('Invalid .git directory not found: Cannot compute the git version')
                return ''
        except ImportError:
            logger.warning('gitpython not found: Cannot compute the git version.')
            return ''
        if repo:
            tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
            latest_tag = tags[-1]
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

        new_content = re.sub(pattern, r'\1 = "{0}"'.format(new_version), old_content, 1, flags=re.MULTILINE)

        logger.debug(
            f"Writing new version number: path={self.path!r} version={new_version!r}"
        )

        with open(self.path, mode="w") as f:
            f.write(new_content)

    def parse(self):
        """
        Return the versions matching this pattern.
        Because a pattern can match in multiple places, this method returns a
        set of matches.
        """
        latest_tag, latest_tag_commit = self.git_version()
        self._field_behaviours = [
            {'pattern': r'^(__version__) = .*$', 'new_version': latest_tag},
            {'pattern': r'^(__sha__) = .*$', 'new_version': latest_tag_commit}
        ]

        return self._field_behaviours

    def write_version(self):
        """
        Write the Semver version + git hash to file.
        """
        self.parse()
        for behaviour in self._field_behaviours:
            self.replace(behaviour['pattern'], behaviour['new_version'])
            logger.debug(
                f"Writing new version number: path={self.path!r} version={behaviour['new_version']!r}"
            )

        return True

def do_setup() -> None:
    my_dir = dirname(__file__)
    path = os.path.join(*[my_dir, "__init__.py"])

    version = VersionPattern(path)
    version.write_version()

if __name__ == "__main__":
    do_setup()