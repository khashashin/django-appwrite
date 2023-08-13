import os
from setuptools import setup, find_packages, Command

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


class BuildCommand(Command):
    description = 'Build the package'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('python setup.py sdist')


class PublishCommand(Command):
    description = 'Publish the package to PyPI'
    user_options = [('version=', 'v', 'version number of the package to be uploaded')]
    version = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        if self.version is None:
            raise Exception("Version number is required. Use --version=<version_number>")

    def run(self):
        os.system(f"twine upload ./dist/django-appwrite-{self.version}.tar.gz")


setup(
    name='django-appwrite',
    version='1.5.0',
    description='Django Middleware to authenticate users with Appwrite',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=("tests",)),
    package_dir={'django_appwrite': 'django_appwrite'},
    install_requires=['appwrite', 'django', 'djangorestframework'],
    license='MIT',
    author='Yusuf Khasbulatov',
    readme='README.md',
    keywords="appwrite auth django",
    url='https://github.com/khashashin/django-appwrite',
    project_urls={
        'Documentation': 'https://github.com/khashashin/django-appwrite/blob/main/README.md',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'https://patreon.com/khashashin',
        'Source': 'https://github.com/khashashin/django-appwrite',
        'Tracker': 'https://github.com/khashashin/django-appwrite/issues',
    },
    classifiers=[
        "Framework :: Django",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    cmdclass={
        'build': BuildCommand,
        'publish': PublishCommand,
    },
)
