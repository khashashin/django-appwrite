from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='django-appwrite',
    version='1.0.1',
    description='Django Middleware to authenticate users with Appwrite',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=("tests",)),
    package_dir={'django_appwrite': 'django_appwrite'},
    install_requires=['appwrite', 'django'],
    license='MIT',
    author='Yusup Khasbulatov',
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
)
