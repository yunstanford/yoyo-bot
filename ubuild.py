import os
import sys
import subprocess
from uranium import task_requires


LANGUAGE_MODEL = "en_core_web_md"


def main(build):
    build.packages.install(".", develop=True)
    build.executables.run([
        sys.executable, "-m", "spacy", "download", LANGUAGE_MODEL,
    ])
    build.executables.run([
        sys.executable, "-m", "spacy", "link", LANGUAGE_MODEL,
    ])


def train_model(build):
    pass


def dev(build):
    pass


@task_requires("main")
def test(build):
    build.packages.install("pytest")
    build.packages.install("radon")
    build.packages.install("coverage")
    build.executables.run([
        "coverage", "run", "--append",
        "--source=yoyo_bot",
        "./bin/pytest", "./tests",
    ] + build.options.args)
    build.executables.run([
        "coverage", "report", "-m"
    ])


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload"
    ])
