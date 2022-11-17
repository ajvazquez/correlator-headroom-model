from setuptools import setup, find_packages
import os
from distutils import sysconfig

site_packages_path = sysconfig.get_python_lib()

VERSION = "version.txt"
REQUIREMENTS_V = [
    "requirements.txt",
    "requirements.dashboard.txt"
]


def get_path(fi):
    return os.path.join(os.path.dirname(__file__), fi)

reqs = []
for req in REQUIREMENTS_V:
    with open(get_path(req)) as f:
        reqs.extend([line.strip() for line in f if "==" in line and not line.strip().startswith("#")])

with open(get_path(VERSION)) as f:
    version = [x.strip() for x in f][0]

exclude = [
]
setup(
    name="correlator-headroom-model",
    version=version,
    description="Headroom Performance Model for Radio Interferometry Software Correlators",
    author="AJ",
    author_email="ajvazquez.teleco@gmail.com",
    # url
    install_requires=reqs,
    packages=[x for x in find_packages(exclude=exclude)],
)