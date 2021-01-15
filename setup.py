import setuptools, os

with open("packaging_tutorial/README.md", "r") as fh:
    long_description = fh.read()

def local_scheme(version):
    return ""

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

@staticmethod
def version_scheme(version):
    from setuptools_scm.version import guess_next_dev_version

    version = guess_next_dev_version(version)
    return version.replace("+", ".")


