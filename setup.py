#!/usr/bin/env python3
import os
import subprocess
from datetime import date

from setuptools import setup, find_packages
local_path = os.path.dirname(__file__)
try:
    with open(os.path.join(local_path, "README.md"), "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = ''


def get_version(app):
    version = date.today().strftime('%Y-%m')
    git_tag = "0.0"
    git_commits = "0"
    suffix = "dev"
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        ).rstrip().decode('utf8')
        git_describe = subprocess.check_output(
            ["git", "describe", "--long"]
        ).rstrip().decode('utf8')
        if not 'fatal' in git_describe:
            git_tag = git_describe.split('-')[0]
            git_commits = git_describe.split('-')[1]
        else:
            git_tag = branch
            git_commits = -1
        if branch == 'main':
            suffix = ''
        else:
            suffix = 'dev'
        print(branch, git_tag, git_commits, suffix)
        if git_commits == -1:
            version = branch
        else:
            version = f'{git_tag}.{git_commits}{suffix}'
    except (subprocess.CalledProcessError, OSError) as e:
        print('git not installed', e)
    try:
        fp = open(os.path.join(local_path, app, 'version.py'), 'w')
        if git_commits == -1:
            fp.write(
                f"api_version = [{branch}]\n")
        else:
            fp.write(
                f"api_version = [{git_tag.replace('.', ', ')}, {git_commits}, \"{suffix}\"]\n")
        fp.close()
    except Exception:
        print(f'ERROR opening {app}/version.py', os.curdir)
    return version


module = 'dynamics_apis'

setup(
    name='dynamics-apis-v3',
    description='API bridge for Kairnial product',
    python_requires='>3.7.0',
    version=get_version(module),
    author='Frédéric MEUROU',
    author_email='frederic.meurou@kairnialgroup.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://apiv3.kairnial.com/',
    install_requires=[
        "Django>=3.10",
        "django-extensions~=3.1.5",
        "djangorestframework~=3.12.0",
        "Markdown~=3.3.0",
        "django-filter~=21.1",
        "drf-spectacular~=0.21.0",
        "django-oauth-toolkit~=1.5.0",
        "python-jose~=3.3.0",
        "python-dotenv~=0.19.0",
        "pytz>=2021.3",
        "djangorestframework-simplejwt~=5.0.0",
        "ariadne_django~=0.2.0",
        "ariadne~=0.14.0"
    ],
    extras_require={
        'prod': ['daphne',],
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Environment :: Web Environment",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
    ],
    py_modules=[
        'dynamics_apis.authentication',
        'dynamics_apis.authorization',
        'dynamics_apis.common',
        'dynamics_apis.controls',
        'dynamics_apis.documents',
        'dynamics_apis.graphql',
        'dynamics_apis.projects',
        'dynamics_apis.users'
    ],
)