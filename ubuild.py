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
    build.executables.run([
        sys.executable, "-m", "rasa_nlu.train",
        "--config" os.path.join(build.root, "config", "config_spacy.yml"),
        "--data", os.path.join(build.root, "data", "training-set.json"),
        "--path", os.path.join(build.root, "projects"),
    ])


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
