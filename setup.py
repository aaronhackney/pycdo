import setuptools
import codecs
import os


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="pycdo",
    packages=setuptools.find_packages(),
    version=get_version("pycdo/__init__.py"),
    description="library for accessing Cisco Defense Orchestrator",
    author="Aaron K. Hackney",
    author_email="aaron_309@yahoo.com",
    url="https://github.com/aaronhackney/pycdo",
    keywords=[
        "cdo",
        "cisco",
        "defense",
        "security",
        "orchestrator",
        "cisco defense orchestrator",
    ],
    install_requires=[
        "requests>=2.25.1",
        "pydantic>=1.9.0",
        "pycryptodome>=3.14.1",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    project_urls={
        "Source": "https://github.com/aaronhackney/pycdo",
        "CDO Documentation": "https://edge.us.cdo.cisco.com/content/docs/index.html",
    },
)
