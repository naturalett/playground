import setuptools, os
from os.path import dirname, relpath


version = '5.13'
my_dir = dirname(__file__)

with open("packaging_tutorial/README.md", "r") as fh:
    long_description = fh.read()

def local_scheme(version):
    return ""

def git_version(version_: str) -> str:
    """
    Return a version to identify the state of the underlying git repo. The version will
    indicate whether the head of the current git-backed working directory is tied to a
    release tag or not : it will indicate the former with a 'release:{version}' prefix
    and the latter with a 'dev0' prefix. Following the prefix will be a sha of the current
    branch head. Finally, a "dirty" suffix is appended to indicate that uncommitted
    changes are present.
    :param str version_: Semver version
    :return: Found Airflow version in Git repo
    :rtype: str
    """
    try:
        import git

        try:
            repo = git.Repo(os.path.join(*[my_dir, '.git']))
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
        sha = repo.head.commit.hexsha
        print(f"SHA IS: {sha}")
        if repo.is_dirty():
            return f'.dev0+{sha}.dirty'
        # commit is clean
        return f'.release:{version_}+{sha}'
    return 'no_git_version'

def write_version(filename: str = os.path.join(*[my_dir, "git_version"])):
    """
    Write the Semver version + git hash to file, e.g. ".dev0+2f635dc265e78db6708f59f68e8009abb92c1e65".
    :param str filename: Destination file to write
    """
    text = "{}".format(git_version(version))
    print(f"Text is :{text}")
    with open(filename, 'w') as file:
        file.write(text)

def do_setup() -> None:
    write_version()
    print('Step1')
    setuptools.setup(
        name="example-pkg-naturalett", # Replace with your own username
        version=os.environ.get("LIMINAL_BUILD_VERSION", os.environ.get('LIMINAL_VERSION', None)),
        author="Example Author",
        author_email="author@example.com",
        description="A small example package",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/pypa/sampleproject",
        use_scm_version={'local_scheme': local_scheme},
        setup_requires=['setuptools_scm'],
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )

if __name__ == "__main__":
    do_setup()
@staticmethod
def version_scheme(version):
    from setuptools_scm.version import guess_next_dev_version

    version = guess_next_dev_version(version)
    return version.replace("+", ".")


